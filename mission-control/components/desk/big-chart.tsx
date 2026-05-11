"use client";

// ── Desk · Big Chart ──────────────────────────────────────────────────
//
// Single-ticker price chart synced to focus-ticker. Uses /api/prices/
// [ticker]?days=N. Period switcher mutates `days`. Real data only —
// no synthetic fallback.

import { useState, useEffect, useMemo } from "react";
import { useFocusTicker } from "@/lib/focus-ticker";
import { TickerLogo, PercentDelta } from "../jpm-atoms";
import { formatCurrency } from "@/lib/format";
import type { DeskPosition } from "@/lib/desk-data";
import { PriceLineChart } from "@/components/charts/price-line-chart";

type Period = "1M" | "3M" | "1Y" | "5Y" | "MAX";
const PERIOD_DAYS: Record<Period, number> = {
  "1M": 30,
  "3M": 90,
  "1Y": 365,
  "5Y": 365 * 5,
  "MAX": 365 * 20,
};

type PricePoint = { date: string; close: number };
type PriceResp = {
  ticker: string;
  market: "br" | "us";
  name?: string;
  sector?: string;
  n_points: number;
  series: PricePoint[];
};

export function BigChart({ positions }: { positions: DeskPosition[] }) {
  const { focus } = useFocusTicker();
  const [period, setPeriod] = useState<Period>("1Y");
  const [data, setData] = useState<PriceResp | null>(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setErr(null);
    fetch(`/api/prices/${encodeURIComponent(focus.ticker)}?days=${PERIOD_DAYS[period]}`)
      .then((r) => r.ok ? r.json() : Promise.reject(`HTTP ${r.status}`))
      .then((d: PriceResp) => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch((e) => { if (!cancelled) { setErr(String(e)); setLoading(false); setData(null); } });
    return () => { cancelled = true; };
  }, [focus.ticker, period]);

  const series = data?.series || [];
  const pos = positions.find((p) => p.ticker === focus.ticker);
  const currency: "BRL" | "USD" = focus.market === "br" ? "BRL" : "USD";

  // Derived stats
  const stats = useMemo(() => {
    if (series.length < 2) return null;
    const start = series[0].close;
    const end = series[series.length - 1].close;
    const min = Math.min(...series.map((p) => p.close));
    const max = Math.max(...series.map((p) => p.close));
    const pct = ((end / start) - 1) * 100;
    return { start, end, min, max, pct };
  }, [series]);

  return (
    <section
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderRadius: "var(--radius)",
        boxShadow: "var(--shadow-sm)",
        padding: "14px 18px",
        display: "flex",
        flexDirection: "column",
        height: "100%",
        minHeight: 320,
      }}
    >
      {/* Header strip */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 10, marginBottom: 12 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <TickerLogo ticker={focus.ticker} size="md" />
          <div>
            <p
              className="type-h3"
              style={{ color: focus.market === "br" ? "var(--mkt-br)" : "var(--mkt-us)", marginBottom: 2 }}
            >
              {data?.sector || "—"} · {focus.market.toUpperCase()}
            </p>
            <h2
              style={{
                fontFamily: "var(--font-display)",
                fontSize: 20,
                lineHeight: 1.1,
                fontWeight: 700,
                letterSpacing: "-0.01em",
                color: "var(--text-primary)",
              }}
            >
              {focus.ticker} · {data?.name || focus.ticker}
            </h2>
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
          {stats ? (
            <>
              <Stat label="Last">
                <span className="font-data" style={{ fontSize: 16, fontWeight: 700 }}>
                  {formatCurrency(stats.end, currency, 2)}
                </span>
              </Stat>
              <Stat label={`${period}`}>
                <span style={{ fontSize: 14, fontWeight: 600 }}>
                  <PercentDelta pct={stats.pct} inline />
                </span>
              </Stat>
              {pos ? (
                <Stat label="Position">
                  <span className="font-data" style={{ fontSize: 13, color: "var(--text-secondary)" }}>
                    {pos.quantity?.toFixed(0) || "—"} sh · {formatCurrency(pos.current_value, currency, 0)}
                  </span>
                </Stat>
              ) : null}
            </>
          ) : null}
          <div className="period-chips" role="tablist" aria-label="Período">
            {(["1M", "3M", "1Y", "5Y", "MAX"] as Period[]).map((p) => (
              <button key={p} data-active={p === period} onClick={() => setPeriod(p)}>
                {p}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Chart body */}
      <div style={{ flex: 1, minHeight: 220, position: "relative" }}>
        {loading ? (
          <Centered>A carregar série…</Centered>
        ) : err ? (
          <Centered>Erro: {err}</Centered>
        ) : series.length < 2 ? (
          <Centered>
            Sem prices na DB para <span className="font-data" style={{ fontWeight: 700 }}>{focus.ticker}</span>.
            Corre o fetcher para popular.
          </Centered>
        ) : (
          <PriceLineChart series={series} currency={currency} height={260} showGrid />
        )}
      </div>
    </section>
  );
}

function Stat({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start", lineHeight: 1.1 }}>
      <span
        style={{
          fontSize: 9, fontWeight: 600, letterSpacing: "0.08em",
          textTransform: "uppercase", color: "var(--text-tertiary)", marginBottom: 2,
        }}
      >
        {label}
      </span>
      {children}
    </div>
  );
}

function Centered({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", color: "var(--text-tertiary)", fontSize: 12 }}>
      {children}
    </div>
  );
}

// Old SVG PriceChart removed — replaced by <PriceLineChart> from
// components/charts/price-line-chart.tsx (NN.1 Chart system v2).
