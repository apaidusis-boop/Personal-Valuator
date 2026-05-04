import { NextRequest, NextResponse } from "next/server";
import Database from "better-sqlite3";
import { DB_BR, DB_US } from "@/lib/paths";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ ticker: string }> }
) {
  const { ticker } = await params;
  const tk = ticker.toUpperCase().replace(/\.SA$/, "");
  const days = parseInt(req.nextUrl.searchParams.get("days") || "365", 10);
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
      const rows = db
        .prepare(
          `SELECT date, close FROM prices
           WHERE ticker=? AND date >= ?
           ORDER BY date ASC`
        )
        .all(tk, cutoff) as { date: string; close: number }[];
      const meta = db
        .prepare("SELECT name, sector FROM companies WHERE ticker=?")
        .get(tk) as { name: string; sector: string } | undefined;
      db.close();
      return NextResponse.json({
        ticker: tk,
        market,
        name: meta?.name,
        sector: meta?.sector,
        n_points: rows.length,
        series: rows,
      });
    } catch {
      /* skip */
    }
  }
  return NextResponse.json({ error: `ticker ${tk} not found` }, { status: 404 });
}
