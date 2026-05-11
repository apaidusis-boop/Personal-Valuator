"use client";

// JPM-style design atoms: TickerLogo, PercentDelta, MarketToggle.
// Pure presentation, no data fetching. Reused across home / portfolio /
// ticker side-sheet so the visual language stays consistent.

import { ReactNode } from "react";

// ─── TickerLogo ───────────────────────────────────────────────────────
// Circular avatar with ticker initials. Color is derived from ticker
// hash so each company keeps a stable identity (no design assets needed).
//
// Mirrors JPM's small colored circle next to each holding name (the J&J
// red, JPM black, BLK yellow, etc. logos in the screenshot).

const PALETTE = [
  "#0F62D1", // JPM blue
  "#15A861", // green
  "#C77700", // amber
  "#9333EA", // violet
  "#0891B2", // teal
  "#D6206E", // rose
  "#1B4DB5", // deep blue
  "#0F766E", // forest
  "#A16207", // ochre
  "#7E22CE", // purple
];

function colorFor(ticker: string): string {
  let h = 0;
  for (let i = 0; i < ticker.length; i++) {
    h = (h * 31 + ticker.charCodeAt(i)) | 0;
  }
  return PALETTE[Math.abs(h) % PALETTE.length];
}

export function TickerLogo({
  ticker,
  size = "md",
}: {
  ticker: string;
  size?: "sm" | "md";
}) {
  const initials = ticker.slice(0, 4);
  const cls = size === "sm" ? "ticker-logo ticker-logo-sm" : "ticker-logo";
  return (
    <span
      className={cls}
      style={{ background: colorFor(ticker) }}
      aria-label={ticker}
    >
      {initials}
    </span>
  );
}

// ─── PercentDelta ─────────────────────────────────────────────────────
// "+1.24%" green / "-2.31%" red, optionally with the absolute amount and
// a triangle glyph. Mirrors JPM's "Loss of -30.58 (-1.24%)" formatting.

export function PercentDelta({
  pct,
  abs,
  currency,
  withTriangle = false,
  inline = false,
}: {
  pct: number | null;
  abs?: number | null;
  currency?: "BRL" | "USD";
  withTriangle?: boolean;
  inline?: boolean;
}) {
  if (pct === null || !isFinite(pct)) {
    return <span className="delta-flat">—</span>;
  }
  const cls = pct > 0 ? "delta-pos" : pct < 0 ? "delta-neg" : "delta-flat";
  const tri = pct > 0 ? "▲" : pct < 0 ? "▼" : "·";
  const sign = pct > 0 ? "+" : "";
  return (
    <span className={cls} style={{ display: inline ? "inline" : "inline-block" }}>
      {withTriangle && <span aria-hidden style={{ marginRight: 4 }}>{tri}</span>}
      {abs != null && currency
        ? `${sign}${formatAbs(abs, currency)} `
        : null}
      {abs != null && <span style={{ opacity: 0.85 }}>(</span>}
      {sign}
      {pct.toFixed(2)}%
      {abs != null && <span style={{ opacity: 0.85 }}>)</span>}
    </span>
  );
}

function formatAbs(n: number, currency: "BRL" | "USD"): string {
  const sym = currency === "BRL" ? "R$" : "$";
  return `${sym}${Math.abs(n).toLocaleString(currency === "BRL" ? "pt-BR" : "en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

// ─── MarketToggle ─────────────────────────────────────────────────────
// Segmented control switching the home hero between Brasil (R$) and
// United States ($). Each option accepts a label override so callers can
// add live indicators (e.g. small dot for "is_open").

export function MarketToggle({
  value,
  onChange,
  brLabel = "Brasil",
  usLabel = "EUA",
}: {
  value: "br" | "us";
  onChange: (m: "br" | "us") => void;
  brLabel?: ReactNode;
  usLabel?: ReactNode;
}) {
  return (
    <div className="segmented" role="tablist" aria-label="Mercado">
      <button
        type="button"
        role="tab"
        data-active={value === "br"}
        aria-selected={value === "br"}
        onClick={() => onChange("br")}
      >
        {brLabel}
      </button>
      <button
        type="button"
        role="tab"
        data-active={value === "us"}
        aria-selected={value === "us"}
        onClick={() => onChange("us")}
      >
        {usLabel}
      </button>
    </div>
  );
}
