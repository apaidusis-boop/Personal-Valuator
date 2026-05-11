"use client";

// ── Desk header — masthead-light, no editorial register ──────────────

import { useFocusTicker } from "@/lib/focus-ticker";

export function DeskHeader({
  br_nav,
  us_nav,
  n_positions,
}: {
  br_nav: number;
  us_nav: number;
  n_positions: number;
}) {
  const { focus, resetToHeadline } = useFocusTicker();
  return (
    <header
      style={{
        background: "var(--jpm-ink)",
        color: "#F4F6F8",
        padding: "8px 16px",
        borderRadius: "var(--radius-sm)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexWrap: "wrap",
        gap: 12,
        fontFamily: "var(--font-sans)",
        fontSize: 11,
        letterSpacing: "0.06em",
        textTransform: "uppercase",
        fontWeight: 600,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
        <span>The Desk</span>
        <span style={{ color: "rgba(244,246,248,0.4)" }}>·</span>
        <span style={{ color: "rgba(244,246,248,0.7)", fontWeight: 500 }}>
          {n_positions} positions
        </span>
        <span style={{ color: "rgba(244,246,248,0.4)" }}>·</span>
        <span style={{ color: "rgba(244,246,248,0.7)", fontWeight: 500 }}>
          BR R${formatCompact(br_nav)} · US ${formatCompact(us_nav)}
        </span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <span style={{ color: "rgba(244,246,248,0.5)" }}>focus</span>
        <span
          className="font-data"
          style={{
            background: "var(--action-gold)",
            color: "var(--jpm-ink)",
            padding: "2px 8px",
            borderRadius: 3,
            letterSpacing: "0.04em",
            fontWeight: 700,
          }}
        >
          {focus.ticker} · {focus.market.toUpperCase()}
        </span>
      </div>
    </header>
  );
}

function formatCompact(v: number): string {
  if (v >= 1_000_000) return (v / 1_000_000).toFixed(2) + "M";
  if (v >= 1_000) return (v / 1_000).toFixed(0) + "k";
  return v.toFixed(0);
}
