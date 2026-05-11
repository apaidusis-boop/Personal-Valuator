import { NextRequest, NextResponse } from "next/server";
import {
  listAlerts,
  createAlert,
  updateAlertStatus,
  deleteAlert,
  type AlertDirection,
  type AlertKind,
} from "@/lib/alerts";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// GET /api/alerts?status=active
export async function GET(req: NextRequest) {
  const status = req.nextUrl.searchParams.get("status") as
    | "active"
    | "triggered"
    | "dismissed"
    | null;
  return NextResponse.json({
    alerts: listAlerts(status || undefined),
  });
}

// POST /api/alerts  { ticker, market, kind, direction, threshold, source?, note? }
export async function POST(req: NextRequest) {
  let body: any;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "invalid json" }, { status: 400 });
  }
  const ticker = String(body.ticker || "").trim().toUpperCase();
  const market = body.market === "us" ? "us" : "br";
  const kind: AlertKind =
    body.kind === "fair_value_entry" || body.kind === "manual"
      ? body.kind
      : "price";
  const direction: AlertDirection = body.direction === "above" ? "above" : "below";
  const threshold = Number(body.threshold);

  if (!ticker || isNaN(threshold) || threshold <= 0) {
    return NextResponse.json(
      { error: "ticker, threshold (>0) required" },
      { status: 400 }
    );
  }

  const alert = createAlert({
    ticker,
    market,
    kind,
    direction,
    threshold,
    current_price: typeof body.current_price === "number" ? body.current_price : null,
    source: typeof body.source === "string" ? body.source : "manual",
    note: typeof body.note === "string" ? body.note : null,
  });
  return NextResponse.json({ alert });
}
