"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";

type Props = {
  label: string;
  busyLabel?: string;
  doneLabel?: string;
  tone?: "ok" | "danger" | "primary" | "ghost";
  size?: "xs" | "sm";
  onClick: () => Promise<{ ok: boolean; message?: string }>;
  /** if true, the page will be re-fetched after a successful click */
  refreshAfter?: boolean;
};

export default function ActionButton({
  label,
  busyLabel = "…",
  doneLabel,
  tone = "primary",
  size = "sm",
  onClick,
  refreshAfter = true,
}: Props) {
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState<{ ok: boolean; message?: string } | null>(null);
  const [, startTransition] = useTransition();
  const router = useRouter();

  async function handle() {
    if (busy) return;
    setBusy(true);
    setDone(null);
    try {
      const r = await onClick();
      setDone(r);
      if (r.ok && refreshAfter) {
        startTransition(() => router.refresh());
      }
    } catch (e: unknown) {
      const err = e instanceof Error ? e.message : String(e);
      setDone({ ok: false, message: err });
    } finally {
      setBusy(false);
      setTimeout(() => setDone(null), 5000);
    }
  }

  const sz = size === "xs"
    ? "px-2 py-0.5 text-[10px]"
    : "px-3 py-1 text-xs";

  const toneCls = {
    primary: "border-purple-700/50 bg-purple-900/30 hover:bg-purple-900/50 text-purple-200",
    ok:      "border-green-700/50 bg-green-900/30 hover:bg-green-900/50 text-green-200",
    danger:  "border-red-700/50 bg-red-900/30 hover:bg-red-900/50 text-red-200",
    ghost:   "border-zinc-700 bg-zinc-900/40 hover:bg-zinc-900/70 text-zinc-300",
  }[tone];

  return (
    <button
      onClick={handle}
      disabled={busy}
      className={`font-mono rounded border ${sz} ${toneCls} disabled:opacity-50`}
      title={done?.message}
    >
      {busy ? busyLabel : done?.ok ? (doneLabel || "✓") : done && !done.ok ? "✗" : label}
    </button>
  );
}

// ─── Helpers usable from server-rendered pages ─────────────────────────────

export async function patchAction(id: number, status: "resolved" | "ignored", market?: string) {
  const res = await fetch(`/api/actions/${id}`, {
    method: "PATCH",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ status, market }),
  });
  const data = await res.json();
  return { ok: res.ok, message: data.error || data.status || "" };
}

export async function runScript(script: string, qs: Record<string, string> = {}) {
  const url = `/api/run/${script}?${new URLSearchParams(qs).toString()}`;
  const res = await fetch(url, { method: "POST" });
  const data = await res.json();
  return {
    ok: res.ok,
    message:
      (data.stdout ? data.stdout.slice(-300) : "") +
      (data.error ? " · " + data.error : ""),
  };
}
