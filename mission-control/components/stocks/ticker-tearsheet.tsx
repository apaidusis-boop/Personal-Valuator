"use client";

// ── /stocks · Single-ticker tearsheet (Read mode right pane) ──────────
//
// Editorial single-page view for ONE ticker. Composition:
//   1. Hero band — ticker, name, sector, verdict pill, key stats strip
//      (last, day delta, qty, P&L%, fair value gap, DY, weight)
//   2. Compact price line (placeholder mini-chart — wires to /api/prices)
//   3. Stance sentence (one-line from deep review)
//   4. Embedded DeepReview (already exists, focus-driven)

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { StocksData } from "@/lib/stocks-data";
import { useFocusTicker } from "@/lib/focus-ticker";
import { TickerLogo, PercentDelta } from "../jpm-atoms";
import { DeepReview } from "../home/deep-review";
import { formatCurrency } from "@/lib/format";
import { PriceLineChart, type PriceLinePoint } from "@/components/charts/price-line-chart";

export function TickerTearsheet({ data }: { data: StocksData }) {
  const { focus } = useFocusTicker();
  const row = data.rows.find((r) => r.ticker === focus.ticker);

  if (!row) {
    return (
      <div
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
          borderRadius: "var(--radius)",
          padding: 32,
          textAlign: "center",
          color: "var(--text-tertiary)",
        }}
      >
        <p className="type-h3" style={{ marginBottom: 6 }}>Tearsheet</p>
        <p className="type-byline">
          Selecciona um ticker no rail à esquerda para abrir o dossier.
        </p>
      </div>
    );
  }

  const currency: "BRL" | "USD" = row.market === "br" ? "BRL" : "USD";

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
      {/* ── Hero ─────────────────────────────────────── */}
      <Hero row={row} currency={currency} />

      {/* ── Mini price line (placeholder chart) ──────── */}
      <PriceLine row={row} />

      {/* ── Deep review (focus-driven, already wired) ── */}
      <DeepReview by_ticker={data.deep_review_by_ticker} />
    </div>
  );
}

// ── Hero ─────────────────────────────────────────────────────────────

function Hero({ row, currency }: { row: any; currency: "BRL" | "USD" }) {
  const verdictClass =
    row.verdict === "BUY" ? "pill-buy"
      : row.verdict === "HOLD" ? "pill-hold"
      : row.verdict === "AVOID" ? "pill-avoid" : "pill-na";

  return (
    <section
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderRadius: "var(--radius)",
        boxShadow: "var(--shadow-sm)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "20px 24px",
          borderBottom: "1px solid var(--border-subtle)",
          display: "flex",
          alignItems: "center",
          gap: 16,
          flexWrap: "wrap",
        }}
      >
        <TickerLogo ticker={row.ticker} size="md" />
        <div style={{ flex: 1, minWidth: 0 }}>
          <p
            className="type-h3"
            style={{ color: row.market === "br" ? "var(--mkt-br)" : "var(--mkt-us)", marginBottom: 2 }}
          >
            {row.sector} · {row.market.toUpperCase()}
          </p>
          <h2
            style={{
              fontFamily: "var(--font-display)",
              fontSize: 26,
              lineHeight: 1.15,
              fontWeight: 700,
              letterSpacing: "-0.015em",
              color: "var(--text-primary)",
              marginBottom: 4,
            }}
          >
            {row.ticker} · {row.name}
          </h2>
          <p
            style={{
              fontFamily: "var(--font-display)",
              fontSize: 14,
              color: "var(--text-secondary)",
              fontStyle: "italic",
            }}
          >
            {row.one_line_stance}
          </p>
        </div>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 6 }}>
          <span className={`pill pill-solid ${verdictClass}`} style={{ fontSize: 12 }}>
            {row.verdict}
          </span>
          <Link
            href={`/ticker/${row.ticker}`}
            style={{
              fontSize: 11, color: "var(--accent-primary)", fontWeight: 500,
              display: "inline-flex", alignItems: "center", gap: 2, textDecoration: "none",
            }}
          >
            Full dossier <ArrowRight size={11} />
          </Link>
        </div>
      </div>

      {/* ── Stats strip ─────────────────────────────── */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(7, 1fr)",
          borderTop: "1px solid var(--border-subtle)",
        }}
      >
        <Cell label="Last" value={row.last_price !== null ? formatCurrency(row.last_price, currency, 2) : "—"} />
        <Cell label="Position">
          <span className="font-data" style={{ fontSize: 13, fontWeight: 600 }}>
            {row.quantity !== null ? row.quantity.toFixed(0) : "—"}
            <span style={{ color: "var(--text-tertiary)", fontSize: 10, marginLeft: 4 }}>shares</span>
          </span>
        </Cell>
        <Cell label="Value" value={row.current_value !== null ? formatCurrency(row.current_value, currency, 0) : "—"} />
        <Cell label="P&L">
          <PercentDelta pct={row.pnl_pct} inline />
        </Cell>
        <Cell label="DY" value={row.dy !== null ? `${row.dy.toFixed(1)}%` : "—"} />
        <Cell label="P/E" value={row.pe !== null ? row.pe.toFixed(1) : "—"} />
        <Cell label="Weight" value={row.weight_pct !== null ? `${row.weight_pct.toFixed(1)}%` : "—"} last />
      </div>
    </section>
  );
}

function Cell({
  label,
  value,
  children,
  last,
}: {
  label: string;
  value?: string;
  children?: React.ReactNode;
  last?: boolean;
}) {
  return (
    <div
      style={{
        padding: "12px 14px",
        borderRight: last ? "none" : "1px solid var(--border-subtle)",
      }}
    >
      <p
        style={{
          fontSize: 9, letterSpacing: "0.08em", textTransform: "uppercase",
          color: "var(--text-tertiary)", fontWeight: 600, marginBottom: 4, fontFamily: "var(--font-sans)",
        }}
      >
        {label}
      </p>
      <div style={{ fontSize: 13, fontWeight: 600 }}>
        {children ?? <span className="font-data">{value}</span>}
      </div>
    </div>
  );
}

// ── Mini price line — real prices from /api/prices/[ticker] ─────────

function PriceLine({ row }: { row: any }) {
  const [series, setSeries] = useState<PriceLinePoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setErr(null);
    fetch(`/api/prices/${encodeURIComponent(row.ticker)}?days=180`)
      .then((r) => r.ok ? r.json() : Promise.reject(`HTTP ${r.status}`))
      .then((d: { series: PriceLinePoint[] }) => {
        if (!cancelled) { setSeries(d.series || []); setLoading(false); }
      })
      .catch((e) => { if (!cancelled) { setErr(String(e)); setLoading(false); } });
    return () => { cancelled = true; };
  }, [row.ticker]);

  const currency: "BRL" | "USD" = row.market === "br" ? "BRL" : "USD";

  return (
    <section
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderRadius: "var(--radius)",
        padding: "12px 16px",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 6 }}>
        <p className="type-h3">Price · 180 dias</p>
        <p className="type-byline">
          {loading ? "loading…" : err ? `erro: ${err}` : series.length < 2 ? "sem prices na DB" : "fonte: prices DB local · hover para inspecionar"}
        </p>
      </div>
      <PriceLineChart series={series} currency={currency} height={120} showGrid={false} />
    </section>
  );
}

// Old synthetic-data SVG mini-chart removed in NN.1.
