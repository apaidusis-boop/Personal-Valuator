import { NextResponse } from "next/server";
import { getTickerSnapshot } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Bundled snapshot for the ticker side-sheet drawer.
// Returns 404 only when the ticker exists in neither DB.
export async function GET(
  _req: Request,
  { params }: { params: Promise<{ ticker: string }> }
) {
  const { ticker } = await params;
  try {
    const snap = getTickerSnapshot(ticker);
    if (!snap) {
      return NextResponse.json(
        { error: `ticker ${ticker.toUpperCase()} not found` },
        { status: 404 }
      );
    }
    return NextResponse.json(snap);
  } catch (e: any) {
    return NextResponse.json(
      { error: String(e?.message || e) },
      { status: 500 }
    );
  }
}
