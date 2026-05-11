import { NextRequest, NextResponse } from "next/server";
import Database from "better-sqlite3";
import { DB_BR, DB_US } from "@/lib/paths";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Phase LL.4 Sprint 3.3 — fair value trajectory over time.
 *
 * Returns the historical sequence of (computed_at, fair_price, our_fair,
 * current_price, action, confidence_label) for a ticker, plus the price
 * series joined for overlay visualization.
 *
 * The fair_value table has been append-only with timestamp keys since
 * Phase KK; this endpoint surfaces that depth for the dashboard sparkline
 * (5-year compounding view the user described — "ITSA4 was R$10 5y ago,
 * now R$15 — confidence to add more given my R$8 entry").
 *
 * Query params:
 *   days (default 1825 = 5y) — window backwards from today
 *   include_price (default true) — join prices.close at computed_at
 */
export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ ticker: string }> }
) {
  const { ticker } = await params;
  const tk = ticker.toUpperCase().replace(/\.SA$/, "");
  const days = parseInt(req.nextUrl.searchParams.get("days") || "1825", 10);
  const includePrice = req.nextUrl.searchParams.get("include_price") !== "false";
  const cutoff = new Date(Date.now() - days * 86400000)
    .toISOString()
    .slice(0, 10);

  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = new Database(file, { readonly: true, fileMustExist: true });
      const exists = db
        .prepare("SELECT 1 FROM companies WHERE ticker=?")
        .get(tk);
      if (!exists) {
        db.close();
        continue;
      }

      // Trajectory rows from fair_value (append-only since Phase KK)
      // computed_at column may be either ISO timestamp (post-KK) or date
      // (pre-KK). >= cutoff comparison works on both.
      let trajectory: any[] = [];
      try {
        trajectory = db
          .prepare(
            `SELECT computed_at, method, fair_price, our_fair,
                    current_price, action, confidence_label, trigger
             FROM fair_value
             WHERE ticker = ? AND computed_at >= ?
             ORDER BY computed_at ASC`
          )
          .all(tk, cutoff) as any[];
      } catch {
        // older schema may not have all columns — fall back
        trajectory = db
          .prepare(
            `SELECT computed_at, method, fair_price, current_price
             FROM fair_value
             WHERE ticker = ? AND computed_at >= ?
             ORDER BY computed_at ASC`
          )
          .all(tk, cutoff) as any[];
      }

      // Optional: join price series at the same dates for overlay
      let prices: { date: string; close: number }[] = [];
      if (includePrice) {
        prices = db
          .prepare(
            `SELECT date, close FROM prices
             WHERE ticker = ? AND date >= ?
             ORDER BY date ASC`
          )
          .all(tk, cutoff) as { date: string; close: number }[];
      }

      const meta = db
        .prepare("SELECT name, sector FROM companies WHERE ticker=?")
        .get(tk) as { name: string; sector: string } | undefined;

      // Latest fair_value snapshot (header band) — normalize same way as trajectory
      const latestRaw = trajectory.length > 0 ? trajectory[trajectory.length - 1] : null;
      const latest = latestRaw
        ? {
            date:
              typeof latestRaw.computed_at === "string"
                ? latestRaw.computed_at.slice(0, 10)
                : latestRaw.computed_at,
            computed_at: latestRaw.computed_at,
            method: latestRaw.method,
            fair_price: latestRaw.fair_price,
            our_fair: latestRaw.our_fair ?? null,
            current_price: latestRaw.current_price ?? null,
            action: latestRaw.action ?? null,
            confidence: latestRaw.confidence_label ?? null,
            trigger: latestRaw.trigger ?? null,
          }
        : null;

      db.close();
      return NextResponse.json({
        ticker: tk,
        market,
        name: meta?.name,
        sector: meta?.sector,
        n_trajectory: trajectory.length,
        n_prices: prices.length,
        latest,
        trajectory: trajectory.map((r) => ({
          // Normalize date prefix from ISO timestamps for charting
          date: typeof r.computed_at === "string" ? r.computed_at.slice(0, 10) : r.computed_at,
          computed_at: r.computed_at,
          method: r.method,
          fair_price: r.fair_price,
          our_fair: r.our_fair ?? null,
          current_price: r.current_price ?? null,
          action: r.action ?? null,
          confidence: r.confidence_label ?? null,
          trigger: r.trigger ?? null,
        })),
        prices,
      });
    } catch {
      /* skip — table or DB missing */
    }
  }
  return NextResponse.json({ error: `ticker ${tk} not found` }, { status: 404 });
}
