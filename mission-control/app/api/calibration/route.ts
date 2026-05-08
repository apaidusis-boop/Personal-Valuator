import { NextRequest, NextResponse } from "next/server";
import { getCalibrationData } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// GET /api/calibration?market=us  (default: both)
export async function GET(req: NextRequest) {
  const m = req.nextUrl.searchParams.get("market");
  if (m === "us" || m === "br") {
    return NextResponse.json({ [m]: getCalibrationData(m) });
  }
  return NextResponse.json({
    us: getCalibrationData("us"),
    br: getCalibrationData("br"),
  });
}
