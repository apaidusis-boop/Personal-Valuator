"use client";

// ── Single-ticker price line chart (Recharts) ────────────────────────
//
// For /desk BigChart, ticker tearsheet mini-chart, etc. Hover crosshair
// + tooltip with the actual price + date. Gradient fill matches gain/loss
// direction.

import { useMemo } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

export type PriceLinePoint = { date: string; close: number };

export function PriceLineChart({
  series,
  height = 280,
  currency = "USD",
  showGrid = true,
}: {
  series: PriceLinePoint[];
  height?: number;
  currency?: "BRL" | "USD";
  showGrid?: boolean;
}) {
  const stats = useMemo(() => {
    if (series.length < 2) return null;
    const start = series[0].close;
    const end = series[series.length - 1].close;
    const min = Math.min(...series.map((p) => p.close));
    const max = Math.max(...series.map((p) => p.close));
    const pct = ((end / start) - 1) * 100;
    return { start, end, min, max, pct };
  }, [series]);

  if (series.length < 2 || !stats) {
    return (
      <div
        style={{
          height,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "var(--text-tertiary)",
          fontSize: 13,
        }}
      >
        Sem prices suficientes na DB.
      </div>
    );
  }

  const isPos = stats.pct >= 0;
  const lineColor = isPos ? "var(--gain)" : "var(--loss)";
  const fillId = `pricefill-${isPos ? "pos" : "neg"}`;

  // Y bounds with 5% padding so the line doesn't kiss the edges
  const padY = (stats.max - stats.min) * 0.05 || 1;
  const minY = stats.min - padY;
  const maxY = stats.max + padY;

  return (
    <div style={{ width: "100%", height }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={series} margin={{ top: 8, right: 12, left: 8, bottom: 4 }}>
          <defs>
            <linearGradient id={fillId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={lineColor} stopOpacity={0.22} />
              <stop offset="100%" stopColor={lineColor} stopOpacity={0.02} />
            </linearGradient>
          </defs>

          {showGrid ? (
            <CartesianGrid stroke="var(--jpm-grid)" strokeDasharray="2 3" vertical={false} />
          ) : null}

          <XAxis
            dataKey="date"
            tick={{ fill: "var(--text-tertiary)", fontSize: 10, fontFamily: "var(--font-mono)" }}
            axisLine={{ stroke: "var(--border-subtle)" }}
            tickLine={false}
            minTickGap={56}
            tickFormatter={formatDateTick}
          />
          <YAxis
            tick={{ fill: "var(--text-tertiary)", fontSize: 10, fontFamily: "var(--font-mono)" }}
            axisLine={false}
            tickLine={false}
            domain={[minY, maxY]}
            width={52}
            tickFormatter={(v) => formatCompactCurrency(v, currency)}
          />

          <Tooltip
            cursor={{ stroke: "var(--accent-primary)", strokeWidth: 1 }}
            content={((props: any) => (
              <PriceTooltip
                active={props.active}
                payload={props.payload}
                label={props.label}
                currency={currency}
                startPrice={stats.start}
              />
            )) as any}
            wrapperStyle={{ outline: "none" }}
          />

          <Area
            type="monotone"
            dataKey="close"
            stroke={lineColor}
            strokeWidth={1.8}
            fill={`url(#${fillId})`}
            isAnimationActive={false}
            activeDot={{ r: 4, strokeWidth: 0, fill: lineColor }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

// ── Tooltip ────────────────────────────────────────────────────────

function PriceTooltip({
  active,
  payload,
  label,
  currency,
  startPrice,
}: {
  active?: boolean;
  payload?: Array<{ value?: number | string }>;
  label?: string | number;
  currency: "BRL" | "USD";
  startPrice: number;
}) {
  if (!active || !payload || payload.length === 0) return null;
  const value = typeof payload[0].value === "number" ? payload[0].value : null;
  if (value === null) return null;
  const pctSinceStart = ((value / startPrice) - 1) * 100;
  const sym = currency === "BRL" ? "R$" : "$";
  return (
    <div
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-strong)",
        borderRadius: "var(--radius-sm)",
        padding: "8px 12px",
        boxShadow: "var(--shadow-lg)",
        minWidth: 140,
        fontFamily: "var(--font-sans)",
      }}
    >
      <p
        style={{
          fontSize: 10,
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          fontWeight: 600,
          color: "var(--text-tertiary)",
          marginBottom: 4,
        }}
      >
        {formatDateLong(String(label || ""))}
      </p>
      <p className="font-data" style={{ fontSize: 14, fontWeight: 700, color: "var(--text-primary)", marginBottom: 2 }}>
        {sym}{value.toFixed(2)}
      </p>
      <p
        className="font-data"
        style={{
          fontSize: 11,
          fontWeight: 600,
          color: pctSinceStart >= 0 ? "var(--gain)" : "var(--loss)",
        }}
      >
        {pctSinceStart >= 0 ? "+" : ""}{pctSinceStart.toFixed(2)}% desde início
      </p>
    </div>
  );
}

// ── Helpers ───────────────────────────────────────────────────────

function formatDateTick(iso: string): string {
  if (!iso || iso.length < 10) return iso;
  return `${iso.slice(5, 7)}/${iso.slice(8, 10)}`;
}

function formatDateLong(iso: string): string {
  if (!iso || iso.length < 10) return iso;
  return `${iso.slice(8, 10)}/${iso.slice(5, 7)}/${iso.slice(0, 4)}`;
}

function formatCompactCurrency(v: number, currency: "BRL" | "USD"): string {
  const sym = currency === "BRL" ? "R$" : "$";
  if (Math.abs(v) >= 1000) return `${sym}${v.toFixed(0)}`;
  return `${sym}${v.toFixed(2)}`;
}
