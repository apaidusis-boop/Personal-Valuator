import { NextResponse } from "next/server";
import Database from "better-sqlite3";
import { DB_BR, DB_US } from "@/lib/paths";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

type Point = { date: string; mv: number; cost: number; index?: number };

// Aggregate per-day MV from portfolio_snapshots (per-ticker rows → SUM by date),
// then extend forward up to today using current positions × latest close.
// `cost` is constant = SUM(quantity × entry_price) from portfolio_positions.
function buildSeries(file: string, indexSymbol?: string | null): Point[] {
  const db = new Database(file, { readonly: true, fileMustExist: true });
  try {
    // Cost basis (constant horizontal line)
    const cost = (
      db
        .prepare(
          "SELECT COALESCE(SUM(quantity * entry_price), 0) AS c FROM portfolio_positions WHERE active=1"
        )
        .get() as { c: number }
    ).c;

    // Aggregated daily MV from per-ticker snapshots
    const snap = db
      .prepare(
        "SELECT date, SUM(mv_native) AS mv FROM portfolio_snapshots GROUP BY date ORDER BY date ASC"
      )
      .all() as { date: string; mv: number }[];

    const series: Point[] = snap.map((r) => ({
      date: r.date,
      mv: Math.round(r.mv * 100) / 100,
      cost: Math.round(cost * 100) / 100,
    }));

    // Extend forward: for each date between (last snapshot + 1) and today,
    // use latest close × current quantity for each active position.
    const lastDate = snap.length ? snap[snap.length - 1].date : null;
    const today = new Date().toISOString().slice(0, 10);
    if (lastDate && lastDate < today) {
      const positions = db
        .prepare(
          "SELECT ticker, quantity FROM portfolio_positions WHERE active=1"
        )
        .all() as { ticker: string; quantity: number }[];

      // Pull recent prices once; map ticker → date → close
      const priceRows = db
        .prepare(
          "SELECT ticker, date, close FROM prices WHERE date > ? ORDER BY ticker, date"
        )
        .all(lastDate) as { ticker: string; date: string; close: number }[];

      const byDate = new Map<string, Map<string, number>>(); // date → ticker → close
      for (const r of priceRows) {
        if (!byDate.has(r.date)) byDate.set(r.date, new Map());
        byDate.get(r.date)!.set(r.ticker, r.close);
      }

      // Carry forward last known price per ticker so partial trading days still work
      const lastKnown = new Map<string, number>();
      // Seed from final snapshot row (per ticker)
      const lastSnapPerTicker = db
        .prepare(
          `SELECT ticker, price_close FROM portfolio_snapshots
           WHERE date = (SELECT MAX(date) FROM portfolio_snapshots)`
        )
        .all() as { ticker: string; price_close: number }[];
      for (const r of lastSnapPerTicker) lastKnown.set(r.ticker, r.price_close);

      const sortedDates = [...byDate.keys()].sort();
      for (const d of sortedDates) {
        const closes = byDate.get(d)!;
        for (const [tk, px] of closes) lastKnown.set(tk, px);
        let mv = 0;
        for (const p of positions) {
          const px = lastKnown.get(p.ticker);
          if (px !== undefined) mv += p.quantity * px;
        }
        if (mv > 0) {
          series.push({
            date: d,
            mv: Math.round(mv * 100) / 100,
            cost: Math.round(cost * 100) / 100,
          });
        }
      }
    }

    // Optional: rebase index to first MV value so % moves overlay nicely
    if (indexSymbol && series.length > 0) {
      const idxRows = db
        .prepare(
          "SELECT date, close FROM prices WHERE ticker = ? AND date >= ? AND date <= ? ORDER BY date"
        )
        .all(indexSymbol, series[0].date, series[series.length - 1].date) as {
        date: string;
        close: number;
      }[];
      if (idxRows.length > 1) {
        const idxByDate = new Map(idxRows.map((r) => [r.date, r.close]));
        const baseMv = series[0].mv;
        let baseIdx: number | null = null;
        for (const p of series) {
          const idxClose = idxByDate.get(p.date);
          if (idxClose !== undefined) {
            if (baseIdx === null) baseIdx = idxClose;
            p.index = (idxClose / baseIdx) * baseMv;
          }
        }
      }
    }

    return series;
  } finally {
    db.close();
  }
}

export async function GET(req: Request) {
  const url = new URL(req.url);
  const indexBR = url.searchParams.get("index_br"); // e.g. BOVA11
  const indexUS = url.searchParams.get("index_us"); // e.g. SPY

  const out: { br: Point[]; us: Point[]; source: string } = {
    br: [],
    us: [],
    source: "snapshots+forward",
  };

  try {
    out.br = buildSeries(DB_BR, indexBR);
  } catch {
    /* skip */
  }
  try {
    out.us = buildSeries(DB_US, indexUS);
  } catch {
    /* skip */
  }

  return NextResponse.json(out);
}
