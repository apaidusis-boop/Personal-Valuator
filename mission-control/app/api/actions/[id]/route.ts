import { NextRequest, NextResponse } from "next/server";
import Database from "better-sqlite3";
import { DB_BR, DB_US } from "@/lib/paths";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function PATCH(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const aid = parseInt(id, 10);
  if (Number.isNaN(aid)) {
    return NextResponse.json({ error: "invalid id" }, { status: 400 });
  }
  let body: { status?: string; market?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "invalid json" }, { status: 400 });
  }
  const status = (body.status || "").toLowerCase();
  if (!["resolved", "ignored"].includes(status)) {
    return NextResponse.json(
      { error: "status must be resolved | ignored" },
      { status: 400 }
    );
  }

  const now = new Date().toISOString().slice(0, 19) + "+00:00";
  const targets =
    body.market === "br"
      ? [DB_BR]
      : body.market === "us"
      ? [DB_US]
      : [DB_BR, DB_US];

  for (const file of targets) {
    try {
      const db = new Database(file);
      const r = db
        .prepare(
          `UPDATE watchlist_actions SET status=?, resolved_at=? WHERE id=? AND status='open'`
        )
        .run(status, now, aid);
      db.close();
      if (r.changes > 0) {
        return NextResponse.json({ ok: true, id: aid, status, file });
      }
    } catch (e: unknown) {
      const err = e instanceof Error ? e.message : String(e);
      return NextResponse.json({ error: err }, { status: 500 });
    }
  }
  return NextResponse.json({ error: "action not found" }, { status: 404 });
}
