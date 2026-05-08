import { NextResponse } from "next/server";
import Database from "better-sqlite3";
import { DB_BR, DB_US } from "@/lib/paths";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Mojibake guard for BR rows that were stored as latin-1 → mis-decoded as UTF-8.
function fix(s: string | null | undefined): string {
  if (!s) return "";
  // Common mojibake markers
  if (!/[À-ÿ�]/.test(s)) return s;
  try {
    return new TextDecoder("utf-8").decode(
      new Uint8Array([...s].map((c) => c.charCodeAt(0)))
    );
  } catch {
    return s;
  }
}

type DivItem = {
  ticker: string;
  market: "br" | "us";
  ex_date: string;
  pay_date: string | null;
  amount: number;
  currency: string;
  shares: number | null;
  payout: number | null; // shares × amount
  is_holding: boolean;
};

type EarnItem = {
  ticker: string;
  market: "br" | "us";
  earnings_date: string;
  period_type: string | null;
  estimate_eps: number | null;
  is_holding: boolean;
};

type FilingItem = {
  ticker: string;
  market: "br" | "us";
  event_date: string;
  source: string; // cvm | sec
  kind: string;
  summary: string;
  url: string | null;
  is_holding: boolean;
};

export async function GET(req: Request) {
  const url = new URL(req.url);
  const daysAhead = parseInt(url.searchParams.get("days") || "60");
  const daysBack = parseInt(url.searchParams.get("filings_days") || "10");
  const holdingsOnly = url.searchParams.get("holdings_only") === "1";

  const dividends: DivItem[] = [];
  const earnings: EarnItem[] = [];
  const filings: FilingItem[] = [];

  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = new Database(file, { readonly: true, fileMustExist: true });

      // Map of holdings → quantity
      const positions = new Map<string, number>();
      const isHolding = new Set<string>();
      try {
        const rows = db
          .prepare(
            "SELECT ticker, quantity FROM portfolio_positions WHERE active=1"
          )
          .all() as { ticker: string; quantity: number }[];
        for (const r of rows) {
          positions.set(r.ticker.toUpperCase(), r.quantity);
          isHolding.add(r.ticker.toUpperCase());
        }
      } catch {
        /* skip */
      }

      // Forward dividends
      try {
        const filter = holdingsOnly
          ? "AND UPPER(ticker) IN (SELECT UPPER(ticker) FROM portfolio_positions WHERE active=1)"
          : "";
        const rows = db
          .prepare(
            `SELECT ticker, ex_date, pay_date, amount, currency
             FROM dividends
             WHERE ex_date >= date('now') AND ex_date <= date('now', '+' || ? || ' day')
             ${filter}
             ORDER BY ex_date`
          )
          .all(daysAhead) as any[];
        for (const r of rows) {
          const tk = String(r.ticker).toUpperCase();
          const shares = positions.get(tk) ?? null;
          const payout =
            shares !== null && r.amount !== null
              ? Math.round(shares * r.amount * 100) / 100
              : null;
          dividends.push({
            ticker: tk,
            market,
            ex_date: r.ex_date,
            pay_date: r.pay_date,
            amount: r.amount,
            currency: r.currency || (market === "br" ? "BRL" : "USD"),
            shares,
            payout,
            is_holding: isHolding.has(tk),
          });
        }
      } catch {
        /* skip */
      }

      // Earnings calendar
      try {
        const filter = holdingsOnly
          ? "AND UPPER(ticker) IN (SELECT UPPER(ticker) FROM portfolio_positions WHERE active=1)"
          : "";
        const rows = db
          .prepare(
            `SELECT ticker, earnings_date, period_type, estimate_eps
             FROM earnings_calendar
             WHERE earnings_date >= date('now') AND earnings_date <= date('now', '+' || ? || ' day')
             ${filter}
             ORDER BY earnings_date`
          )
          .all(daysAhead) as any[];
        for (const r of rows) {
          const tk = String(r.ticker).toUpperCase();
          earnings.push({
            ticker: tk,
            market,
            earnings_date: r.earnings_date,
            period_type: r.period_type,
            estimate_eps: r.estimate_eps,
            is_holding: isHolding.has(tk),
          });
        }
      } catch {
        /* skip */
      }

      // Recent filings (back-window only)
      try {
        const filter = holdingsOnly
          ? "AND UPPER(ticker) IN (SELECT UPPER(ticker) FROM portfolio_positions WHERE active=1)"
          : "";
        const rows = db
          .prepare(
            `SELECT ticker, event_date, source, kind, summary, url
             FROM events
             WHERE event_date >= date('now', '-' || ? || ' day')
             ${filter}
             ORDER BY event_date DESC, id DESC
             LIMIT 200`
          )
          .all(daysBack) as any[];
        for (const r of rows) {
          const tk = String(r.ticker).toUpperCase();
          filings.push({
            ticker: tk,
            market,
            event_date: r.event_date,
            source: r.source,
            kind: r.kind,
            summary: fix(r.summary),
            url: r.url,
            is_holding: isHolding.has(tk),
          });
        }
      } catch {
        /* skip */
      }

      db.close();
    } catch {
      /* skip whole DB */
    }
  }

  // Final cross-market sort
  dividends.sort((a, b) => a.ex_date.localeCompare(b.ex_date));
  earnings.sort((a, b) => a.earnings_date.localeCompare(b.earnings_date));
  filings.sort((a, b) => b.event_date.localeCompare(a.event_date));

  // Aggregates for header ribbon
  const next7 = (d: string) =>
    d >= new Date().toISOString().slice(0, 10) &&
    d <=
      new Date(Date.now() + 7 * 86400000).toISOString().slice(0, 10);

  const summary = {
    div_next7: dividends.filter((d) => next7(d.ex_date) && d.is_holding).length,
    div_next30: dividends.filter((d) => d.is_holding).length,
    earn_next7: earnings.filter(
      (e) => next7(e.earnings_date) && e.is_holding
    ).length,
    earn_next30: earnings.filter((e) => e.is_holding).length,
    filings_recent: filings.filter((f) => f.is_holding).length,
    expected_payout_next30: dividends
      .filter((d) => d.is_holding && d.payout !== null)
      .reduce(
        (acc, d) => {
          const k = d.currency || (d.market === "br" ? "BRL" : "USD");
          acc[k] = (acc[k] || 0) + (d.payout || 0);
          return acc;
        },
        {} as Record<string, number>
      ),
  };

  return NextResponse.json({
    dividends,
    earnings,
    filings,
    summary,
  });
}
