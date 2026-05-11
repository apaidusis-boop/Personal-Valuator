import { NextRequest, NextResponse } from "next/server";
import Database from "better-sqlite3";
import { DB_BR, DB_US } from "@/lib/paths";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// ── /api/compare-series?tickers=SPY,AAPL,BOVA11&period=1Y ─────────────
//
// Reads `prices` from BR + US DBs for each ticker, aligns to a common
// trading-day calendar, normalizes each series to 100 at the first
// available date, returns one JSON payload the Compare chart can plot.
//
// Periods: 3M, 1Y, 5Y, MAX.
// Stride: daily for 3M/1Y, weekly sample for 5Y/MAX (perf + clarity).
//
// If a ticker has no prices in either DB, it's returned with empty
// `values` and `has_data: false` so the UI can render a "no data" hint
// instead of inventing numbers.

type Period = "3M" | "1Y" | "5Y" | "MAX";

const PERIOD_DAYS: Record<Period, number> = {
  "3M": 90,
  "1Y": 365,
  "5Y": 365 * 5,
  "MAX": 365 * 20, // cap, real horizon depends on prices coverage
};

type PriceRow = { date: string; close: number };

type TickerSeries = {
  ticker: string;
  market: "br" | "us" | null;
  name: string | null;
  has_data: boolean;
  start_price: number | null;
  end_price: number | null;
  pct_change: number | null;
  // Aligned: same length as `dates`, normalized to 100 at start.
  values: number[];
};

type Payload = {
  period: Period;
  dates: string[];     // common calendar (ISO yyyy-mm-dd)
  series: TickerSeries[];
};

function readPrices(ticker: string, cutoff: string): { rows: PriceRow[]; market: "br" | "us"; name: string | null } | null {
  const tk = ticker.toUpperCase().replace(/\.SA$/, "");
  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = new Database(file, { readonly: true, fileMustExist: true });
      const meta = db
        .prepare("SELECT name FROM companies WHERE ticker=?")
        .get(tk) as { name: string | null } | undefined;
      if (!meta) {
        db.close();
        continue;
      }
      const rows = db
        .prepare(
          `SELECT date, close FROM prices
           WHERE ticker=? AND date >= ?
           ORDER BY date ASC`,
        )
        .all(tk, cutoff) as PriceRow[];
      db.close();
      if (rows.length === 0) {
        // Company exists but no prices in window — try other market
        continue;
      }
      return { rows, market, name: meta.name };
    } catch {
      /* skip market */
    }
  }
  return null;
}

function sampleWeekly(rows: PriceRow[]): PriceRow[] {
  if (rows.length === 0) return rows;
  // Pick last close per ISO week
  const out: PriceRow[] = [];
  let lastWeek = "";
  for (const r of rows) {
    const d = new Date(r.date);
    // ISO week-ish key: year + week number (Sunday-anchored is fine for sampling)
    const wk = `${d.getFullYear()}-W${Math.floor((d.getTime() / 86400000 + 4) / 7)}`;
    if (wk !== lastWeek) {
      out.push(r);
      lastWeek = wk;
    } else {
      out[out.length - 1] = r; // keep last close of the week
    }
  }
  return out;
}

export async function GET(req: NextRequest) {
  const tickersRaw = req.nextUrl.searchParams.get("tickers") || "";
  const periodRaw = (req.nextUrl.searchParams.get("period") || "1Y") as Period;
  const period: Period = ["3M", "1Y", "5Y", "MAX"].includes(periodRaw) ? periodRaw : "1Y";

  const tickers = tickersRaw
    .split(",")
    .map((t) => t.trim().toUpperCase())
    .filter(Boolean)
    .slice(0, 6);

  if (tickers.length === 0) {
    return NextResponse.json({ error: "no tickers" }, { status: 400 });
  }

  const cutoff = new Date(Date.now() - PERIOD_DAYS[period] * 86400000)
    .toISOString()
    .slice(0, 10);
  const useWeekly = period === "5Y" || period === "MAX";

  // Read each ticker's series
  const raw: Array<{ ticker: string; rows: PriceRow[]; market: "br" | "us" | null; name: string | null }> = [];
  for (const t of tickers) {
    const r = readPrices(t, cutoff);
    if (!r) {
      raw.push({ ticker: t, rows: [], market: null, name: null });
    } else {
      raw.push({ ticker: t, rows: useWeekly ? sampleWeekly(r.rows) : r.rows, market: r.market, name: r.name });
    }
  }

  // Build a *common* calendar — union of all dates across tickers, sorted
  const dateSet = new Set<string>();
  for (const r of raw) {
    for (const p of r.rows) dateSet.add(p.date);
  }
  const dates = Array.from(dateSet).sort();

  // Align each ticker to the common calendar. If a date is missing for a
  // ticker, forward-fill from its previous known close (typical when a
  // foreign exchange is closed but another isn't — public holidays etc).
  const series: TickerSeries[] = raw.map((r) => {
    if (r.rows.length === 0) {
      return {
        ticker: r.ticker,
        market: null,
        name: null,
        has_data: false,
        start_price: null,
        end_price: null,
        pct_change: null,
        values: [],
      };
    }
    const map = new Map<string, number>();
    for (const p of r.rows) map.set(p.date, p.close);
    const aligned: number[] = [];
    let last: number | null = null;
    for (const d of dates) {
      const v = map.get(d);
      if (v !== undefined) {
        last = v;
        aligned.push(v);
      } else if (last !== null) {
        aligned.push(last);
      } else {
        // No prior data yet — leave NaN; will be filtered to first non-null
        aligned.push(NaN);
      }
    }
    // Find first valid (non-NaN) and use as base for normalization
    const firstIdx = aligned.findIndex((v) => isFinite(v));
    if (firstIdx === -1) {
      return {
        ticker: r.ticker,
        market: r.market,
        name: r.name,
        has_data: false,
        start_price: null,
        end_price: null,
        pct_change: null,
        values: [],
      };
    }
    const base = aligned[firstIdx];
    // Replace pre-firstIdx NaNs with base (so the line starts at 100)
    const normalized: number[] = aligned.map((v, i) => {
      if (i < firstIdx) return 100;
      if (!isFinite(v)) return 100;
      return Number(((v / base) * 100).toFixed(2));
    });
    const last_v = aligned[aligned.length - 1];
    const start_p = base;
    const end_p = isFinite(last_v) ? last_v : null;
    const pct = end_p !== null ? Number((((end_p / start_p) - 1) * 100).toFixed(2)) : null;
    return {
      ticker: r.ticker,
      market: r.market,
      name: r.name,
      has_data: true,
      start_price: Number(start_p.toFixed(2)),
      end_price: end_p !== null ? Number(end_p.toFixed(2)) : null,
      pct_change: pct,
      values: normalized,
    };
  });

  const payload: Payload = { period, dates, series };
  return NextResponse.json(payload);
}
