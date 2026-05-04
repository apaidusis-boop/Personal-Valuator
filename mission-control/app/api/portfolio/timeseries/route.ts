import { NextResponse } from "next/server";
import Database from "better-sqlite3";
import { DB_BR, DB_US } from "@/lib/paths";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Best-effort portfolio P&L over time. Tries portfolio_snapshots first
// (Phase R), then falls back to reconstructing from prices × current quantities.
export async function GET() {
  const out: { br: { date: string; mv: number; cost: number }[];
               us: { date: string; mv: number; cost: number }[];
               source: string } = { br: [], us: [], source: "fallback" };

  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = new Database(file, { readonly: true, fileMustExist: true });
      // Try snapshot table first
      try {
        const rows = db
          .prepare(
            `SELECT date, total_market_value AS mv, total_cost AS cost
             FROM portfolio_snapshots
             ORDER BY date ASC LIMIT 365`
          )
          .all() as { date: string; mv: number; cost: number }[];
        if (rows.length > 0) {
          out[market] = rows;
          out.source = "portfolio_snapshots";
          db.close();
          continue;
        }
      } catch {
        /* table may not exist */
      }

      // Fallback: per-day MV from prices × current positions
      const positions = db
        .prepare(
          "SELECT ticker, quantity, entry_price FROM portfolio_positions WHERE active=1"
        )
        .all() as { ticker: string; quantity: number; entry_price: number }[];

      const totalCost = positions.reduce(
        (n, p) => n + p.quantity * p.entry_price,
        0
      );

      // Build a cross-ticker time series — common dates across all positions
      const series = new Map<string, number>();
      for (const p of positions) {
        const rows = db
          .prepare(
            `SELECT date, close FROM prices WHERE ticker=?
             AND date >= date('now', '-365 day') ORDER BY date ASC`
          )
          .all(p.ticker) as { date: string; close: number }[];
        for (const r of rows) {
          series.set(r.date, (series.get(r.date) || 0) + p.quantity * r.close);
        }
      }
      out[market] = [...series.entries()]
        .sort((a, b) => a[0].localeCompare(b[0]))
        .map(([date, mv]) => ({ date, mv, cost: totalCost }));
      db.close();
    } catch {
      /* skip */
    }
  }

  return NextResponse.json(out);
}
