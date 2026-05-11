import { NextRequest, NextResponse } from "next/server";
import { updateAlertStatus, deleteAlert } from "@/lib/alerts";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// PATCH /api/alerts/[id]  { status: 'active'|'triggered'|'dismissed' }
export async function PATCH(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  let body: any;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "invalid json" }, { status: 400 });
  }
  const status = body.status;
  if (status !== "active" && status !== "triggered" && status !== "dismissed") {
    return NextResponse.json(
      { error: "status must be active|triggered|dismissed" },
      { status: 400 }
    );
  }
  const updated = updateAlertStatus(id, status);
  if (!updated) return NextResponse.json({ error: "not found" }, { status: 404 });
  return NextResponse.json({ alert: updated });
}

// DELETE /api/alerts/[id]
export async function DELETE(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const ok = deleteAlert(id);
  if (!ok) return NextResponse.json({ error: "not found" }, { status: 404 });
  return NextResponse.json({ deleted: true });
}
