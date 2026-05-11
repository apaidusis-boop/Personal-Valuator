"use client";

// ── Normalized line chart (Recharts v2) ──────────────────────────────
//
// Reusable chart for the home Compare tab and the /desk BigChart. Uses
// Recharts under the hood — gives us:
//   • True responsive width via <ResponsiveContainer>
//   • Vertical crosshair on hover (cursor stroke)
//   • Floating tooltip with all series values at the hovered x
//   • Active dots on each line at the hovered point
//   • Auto Y-axis with tick interval that doesn't overlap
//
// Series shape: { ticker, values[], pct_change, has_data, end_price }
// + a parallel `dates: string[]` array (same length as values).
// Series with has_data=false are skipped (no fake lines).

import { useMemo } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  CartesianGrid,
} from "recharts";

// SVG text props (what Recharts wants for `tick={...}`) — typed loosely
// because Recharts 3.x types CSSProperties as too narrow for fontFamily.
const tickStyle = {
  fill: "var(--text-tertiary)",
  fontSize: 10,
  fontFamily: "var(--font-mono)",
} as const;

export type ChartSeries = {
  ticker: string;
  values: number[];
  has_data: boolean;
  pct_change: number | null;
  end_price: number | null;
};

export function NormalizedLineChart({
  series,
  dates,
  colors,
  height = 320,
  showBaseline = true,
  yLabelFormat = (v) => v.toFixed(0),
  tooltipValueFormat = (v) => v.toFixed(1),
  isPriceChart = false, // when true, tooltip shows actual prices not normalized index
}: {
  series: ChartSeries[];
  dates: string[];
  colors: string[];
  height?: number;
  showBaseline?: boolean;
  yLabelFormat?: (v: number) => string;
  tooltipValueFormat?: (v: number) => string;
  isPriceChart?: boolean;
}) {
  // Recharts wants row-shaped data: one object per x point with all
  // series values keyed by ticker. We zip series + dates here.
  const chartData = useMemo(() => {
    const out: Record<string, string | number | null>[] = [];
    const N = dates.length;
    for (let i = 0; i < N; i++) {
      const row: Record<string, string | number | null> = { date: dates[i] };
      for (const s of series) {
        if (s.has_data && s.values[i] !== undefined) {
          row[s.ticker] = s.values[i];
        }
      }
      out.push(row);
    }
    return out;
  }, [series, dates]);

  const plotted = series.filter((s) => s.has_data && s.values.length > 0);
  if (plotted.length === 0) {
    return (
      <div
        style={{
          height,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "var(--text-tertiary)",
          fontSize: 13,
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
          borderRadius: "var(--radius-sm)",
        }}
      >
        Sem séries com dados.
      </div>
    );
  }

  // Reasonable Y bounds: include 100 baseline if showBaseline
  const allY = plotted.flatMap((s) => s.values);
  const minY = Math.min(...allY, showBaseline ? 100 : Infinity);
  const maxY = Math.max(...allY, showBaseline ? 100 : -Infinity);
  const padY = (maxY - minY) * 0.05 || 1;

  return (
    <div style={{ width: "100%", height, position: "relative" }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={chartData}
          margin={{ top: 12, right: 64, left: 8, bottom: 4 }}
        >
          <CartesianGrid stroke="var(--jpm-grid)" strokeDasharray="2 3" vertical={false} />

          <XAxis
            dataKey="date"
            tick={tickStyle}
            axisLine={{ stroke: "var(--border-subtle)" }}
            tickLine={false}
            minTickGap={48}
            tickFormatter={formatDateTick}
          />
          <YAxis
            tick={tickStyle}
            axisLine={false}
            tickLine={false}
            domain={[minY - padY, maxY + padY]}
            width={48}
            tickFormatter={yLabelFormat}
          />

          {showBaseline ? (
            <ReferenceLine
              y={100}
              stroke="var(--text-tertiary)"
              strokeWidth={1}
              strokeDasharray="0"
              ifOverflow="extendDomain"
            />
          ) : null}

          <Tooltip
            cursor={{ stroke: "var(--accent-primary)", strokeWidth: 1, strokeDasharray: "0" }}
            content={((props: any) => (
              <ChartTooltip
                active={props.active}
                payload={props.payload}
                label={props.label}
                series={plotted}
                colors={colors}
                tickerToColor={makeColorMap(series, colors)}
                isPriceChart={isPriceChart}
                valueFormat={tooltipValueFormat}
              />
            )) as any}
            wrapperStyle={{ outline: "none" }}
          />

          {series.map((s, idx) => {
            if (!s.has_data) return null;
            return (
              <Line
                key={s.ticker}
                type="monotone"
                dataKey={s.ticker}
                stroke={colors[idx]}
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
                dot={false}
                activeDot={{ r: 4, strokeWidth: 0, fill: colors[idx] }}
                isAnimationActive={false}
                connectNulls={false}
              />
            );
          })}
        </LineChart>
      </ResponsiveContainer>

      {/* Last-value labels overlay (right-side, shows pct change like the old SVG) */}
      <LastValueLabels series={series} colors={colors} />
    </div>
  );
}

// ── Tooltip ─────────────────────────────────────────────────────────

type RechartsTooltipPayload = {
  payload: Record<string, string | number | null>;
  dataKey: string;
  value: number | null;
  color: string;
};

function ChartTooltip({
  active,
  payload,
  label,
  series,
  colors,
  tickerToColor,
  isPriceChart,
  valueFormat,
}: {
  active?: boolean;
  payload?: RechartsTooltipPayload[];
  label?: string;
  series: ChartSeries[];
  colors: string[];
  tickerToColor: Record<string, string>;
  isPriceChart: boolean;
  valueFormat: (v: number) => string;
}) {
  if (!active || !payload || payload.length === 0) return null;
  return (
    <div
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-strong)",
        borderRadius: "var(--radius-sm)",
        padding: "10px 12px",
        boxShadow: "var(--shadow-lg)",
        minWidth: 180,
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
          marginBottom: 6,
        }}
      >
        {formatDateLong(String(label || ""))}
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
        {payload.map((p) => {
          const ticker = String(p.dataKey);
          const color = tickerToColor[ticker] || p.color;
          const v = typeof p.value === "number" ? p.value : null;
          // For normalized chart: also surface the pct-since-start (v − 100)
          const pctSinceStart = !isPriceChart && v !== null ? v - 100 : null;
          return (
            <div key={ticker} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12 }}>
              <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
                <span style={{ width: 8, height: 8, borderRadius: 999, background: color }} />
                <span
                  className="font-data"
                  style={{ fontSize: 12, fontWeight: 700, color: "var(--text-primary)" }}
                >
                  {ticker}
                </span>
              </span>
              <span style={{ display: "inline-flex", alignItems: "baseline", gap: 6 }}>
                <span className="font-data" style={{ fontSize: 12, color: "var(--text-primary)", fontWeight: 600 }}>
                  {v !== null ? valueFormat(v) : "—"}
                </span>
                {pctSinceStart !== null ? (
                  <span
                    className="font-data"
                    style={{
                      fontSize: 10,
                      color: pctSinceStart >= 0 ? "var(--gain)" : "var(--loss)",
                      fontWeight: 600,
                    }}
                  >
                    {pctSinceStart >= 0 ? "+" : ""}{pctSinceStart.toFixed(1)}%
                  </span>
                ) : null}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── Last-value labels (right rail) ──────────────────────────────────
//
// Recharts doesn't have a clean built-in for "label at last data point";
// we overlay our own absolute-positioned labels. Computed once per render.

function LastValueLabels({ series, colors }: { series: ChartSeries[]; colors: string[] }) {
  return (
    <div
      aria-hidden
      style={{
        position: "absolute",
        top: 12,
        right: 4,
        bottom: 28,
        width: 60,
        pointerEvents: "none",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-around",
      }}
    >
      {series.map((s, idx) => {
        if (!s.has_data || s.pct_change === null) return null;
        const sign = s.pct_change >= 0 ? "+" : "";
        return (
          <div
            key={s.ticker}
            style={{
              fontSize: 10,
              fontFamily: "var(--font-mono)",
              color: colors[idx],
              fontWeight: 700,
              textAlign: "right",
              lineHeight: 1.2,
              whiteSpace: "nowrap",
            }}
          >
            <div>{s.ticker}</div>
            <div>{sign}{s.pct_change.toFixed(1)}%</div>
          </div>
        );
      })}
    </div>
  );
}

// ── Helpers ─────────────────────────────────────────────────────────

function makeColorMap(series: ChartSeries[], colors: string[]): Record<string, string> {
  const out: Record<string, string> = {};
  series.forEach((s, i) => { out[s.ticker] = colors[i]; });
  return out;
}

function formatDateTick(iso: string): string {
  if (!iso || iso.length < 10) return iso;
  return `${iso.slice(5, 7)}/${iso.slice(8, 10)}`;
}

function formatDateLong(iso: string): string {
  if (!iso || iso.length < 10) return iso;
  // dd/mm/yyyy for tooltip header
  return `${iso.slice(8, 10)}/${iso.slice(5, 7)}/${iso.slice(0, 4)}`;
}
