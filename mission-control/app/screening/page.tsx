import type { Metadata } from "next";
import { listCouncilOutputs, summariseCouncil } from "@/lib/vault";
import { listAllPositions } from "@/lib/db";
import { formatDate } from "@/lib/format";
import {
  ScreeningTable,
  type ScreeningRow,
} from "@/components/screening/screening-table";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Buscar Ativos · Mission Control" };

export default function ScreeningPage() {
  const all = listCouncilOutputs(500);
  const summary = summariseCouncil(all);
  const latest = all.filter((e) => e.date === summary.date);
  const positions = listAllPositions();
  const holdings = new Set(
    positions.map((p) => (p.ticker || "").toUpperCase())
  );

  // Sort: BUY first (low dissent), then HOLD, then NEEDS_DATA, AVOID last
  const STANCE_ORDER = ["BUY", "HOLD", "NEEDS_DATA", "AVOID", "UNKNOWN"];
  const sorted = [...latest].sort(
    (a, b) =>
      STANCE_ORDER.indexOf(a.stance) - STANCE_ORDER.indexOf(b.stance) ||
      a.dissent_count - b.dissent_count ||
      a.ticker.localeCompare(b.ticker)
  );

  const rows: ScreeningRow[] = sorted.map((e) => ({
    ticker: e.ticker,
    market: e.market,
    sector: e.sector,
    stance: e.stance,
    confidence: e.confidence,
    flag_count: e.flag_count,
    philosophy_primary: e.philosophy_primary,
    is_holding: holdings.has(e.ticker.toUpperCase()),
  }));

  const buys = rows.filter((r) => r.stance === "BUY").length;
  const holds = rows.filter((r) => r.stance === "HOLD").length;
  const avoids = rows.filter((r) => r.stance === "AVOID").length;
  const needs = rows.filter((r) => r.stance === "NEEDS_DATA").length;

  return (
    <div className="p-5 space-y-5">
      <div>
        <h1
          className="font-display text-xl font-bold"
          style={{ color: "var(--text-primary)" }}
        >
          Buscar Ativos
        </h1>
        <p
          className="text-xs mt-0.5"
          style={{ color: "var(--text-tertiary)" }}
        >
          {rows.length} subjects no Council ·{" "}
          {summary.date !== "—" ? formatDate(summary.date, "medium") : "sem run"}
        </p>
      </div>

      {/* Stance counts -------------------------------------------- */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <CountBlock label="BUY" value={buys} variant="buy" />
        <CountBlock label="HOLD" value={holds} variant="hold" />
        <CountBlock label="AVOID" value={avoids} variant="avoid" />
        <CountBlock label="NEEDS DATA" value={needs} variant="na" />
      </div>

      <ScreeningTable rows={rows} />
    </div>
  );
}

function CountBlock({
  label,
  value,
  variant,
}: {
  label: string;
  value: number;
  variant: "buy" | "hold" | "avoid" | "na";
}) {
  const color =
    variant === "buy"
      ? "var(--verdict-buy)"
      : variant === "hold"
      ? "var(--verdict-hold)"
      : variant === "avoid"
      ? "var(--verdict-avoid)"
      : "var(--verdict-na)";
  return (
    <div
      className="p-4 rounded"
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
      }}
    >
      <p
        className="text-[10px] font-semibold tracking-wider uppercase mb-1.5"
        style={{ color: "var(--text-label)" }}
      >
        {label}
      </p>
      <p className="text-2xl font-display font-bold" style={{ color }}>
        {value}
      </p>
    </div>
  );
}
