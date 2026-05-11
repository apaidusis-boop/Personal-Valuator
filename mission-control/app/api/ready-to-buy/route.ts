import { NextRequest, NextResponse } from "next/server";
import { listReadyToBuy } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Phase LL Sprint 3.1 — Ready-to-Buy data endpoint.
 *
 * Returns top tickers with action ∈ {BUY, STRONG_BUY} AND confidence !=
 * disputed. Sorted by our_upside_pct desc.
 *
 * Query params:
 *   market: 'br' | 'us' (optional — both if omitted)
 *   limit: integer (default 6)
 */
export async function GET(req: NextRequest) {
  const market = req.nextUrl.searchParams.get("market") as "br" | "us" | null;
  const limit = parseInt(req.nextUrl.searchParams.get("limit") || "6", 10);
  const rows = listReadyToBuy(
    market === "br" || market === "us" ? market : undefined,
    Math.max(1, Math.min(50, limit))
  );
  return NextResponse.json({ rows, n: rows.length });
}
