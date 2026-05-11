import { NextResponse } from "next/server";
import Database from "better-sqlite3";
import { DB_BR, DB_US } from "@/lib/paths";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

type Hit = {
  ticker: string;
  name: string | null;
  sector: string | null;
  market: "br" | "us";
  is_holding: 0 | 1;
};

// Global search across companies (BR + US). Used by the top-bar search box.
// Returns up to `limit` hits ranked: holdings first, exact-prefix > substring,
// then by name.
export async function GET(req: Request) {
  const url = new URL(req.url);
  const q = (url.searchParams.get("q") || "").trim().toUpperCase();
  const limit = Math.min(parseInt(url.searchParams.get("limit") || "12"), 50);
  if (!q) return NextResponse.json({ hits: [] });

  const hits: Hit[] = [];
  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = new Database(file, { readonly: true, fileMustExist: true });
      const rows = db
        .prepare(
          `SELECT ticker, name, sector, COALESCE(is_holding,0) AS is_holding
           FROM companies
           WHERE UPPER(ticker) LIKE ? OR UPPER(name) LIKE ?
           ORDER BY is_holding DESC,
                    (UPPER(ticker) = ?) DESC,
                    (UPPER(ticker) LIKE ?) DESC,
                    name
           LIMIT ?`
        )
        .all(`%${q}%`, `%${q}%`, q, `${q}%`, limit) as any[];
      for (const r of rows) {
        hits.push({
          ticker: r.ticker,
          name: r.name,
          sector: r.sector,
          market,
          is_holding: r.is_holding ? 1 : 0,
        });
      }
      db.close();
    } catch {
      /* skip */
    }
  }

  hits.sort((a, b) => {
    if (b.is_holding !== a.is_holding) return b.is_holding - a.is_holding;
    const aExact = a.ticker.toUpperCase() === q ? 1 : 0;
    const bExact = b.ticker.toUpperCase() === q ? 1 : 0;
    if (bExact !== aExact) return bExact - aExact;
    const aPref = a.ticker.toUpperCase().startsWith(q) ? 1 : 0;
    const bPref = b.ticker.toUpperCase().startsWith(q) ? 1 : 0;
    if (bPref !== aPref) return bPref - aPref;
    return (a.name || "").localeCompare(b.name || "");
  });

  return NextResponse.json({ hits: hits.slice(0, limit) });
}
