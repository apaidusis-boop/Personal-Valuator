"use client";

// ── WORKBENCH · COMPARE TAB ──────────────────────────────────────────
//
// Up to 4 tickers, normalized-to-100 price series, period switcher.
// Side panel shows fundamentals row-by-row so the user can eyeball
// who's "more expensive vs growth" without a screener detour.
//
// REAL DATA: fetches from /api/compare-series which reads the local
// `prices` SQLite (BR + US) and returns per-ticker normalized series
// aligned to a common calendar. Tickers without DB coverage render as
// "no data" (grey) instead of inventing values.

import { useState, useMemo, useEffect } from "react";
import { X, Plus } from "lucide-react";
import { useFocusTicker } from "@/lib/focus-ticker";
import { TickerLogo } from "../../jpm-atoms";
import { NormalizedLineChart } from "@/components/charts/normalized-line-chart";

type Period = "3M" | "1Y" | "5Y" | "MAX";

export type CompareTickerFundamentals = {
  ticker: string;
  name: string;
  sector: string;
  pe: number | null;
  pb: number | null;
  dy: number | null;
  roe: number | null;
  vitality: number | null;   // 0-100 composite
  fv_gap_pct: number | null; // (price/fair − 1) × 100
};

export type CompareTabProps = {
  default_tickers: string[]; // pre-loaded from spotlight + benchmark
  benchmark: string;          // SPY or BOVA11
  available_tickers: string[]; // for autocomplete
  fundamentals_by_ticker: Record<string, CompareTickerFundamentals>;
};

// Five plot colors — JPM blue + warm contrast
const COLORS = ["#0F62D1", "#C77700", "#15A861", "#7E22CE", "#5A6577"];

// API response shape (matches /api/compare-series GET payload)
type ApiTickerSeries = {
  ticker: string;
  market: "br" | "us" | null;
  name: string | null;
  has_data: boolean;
  start_price: number | null;
  end_price: number | null;
  pct_change: number | null;
  values: number[];
};

function formatDateShort(iso: string): string {
  // yyyy-mm-dd → mm/dd
  if (!iso || iso.length < 10) return iso;
  return `${iso.slice(5, 7)}/${iso.slice(8, 10)}`;
}

export function CompareTab({
  default_tickers,
  benchmark,
  available_tickers,
  fundamentals_by_ticker,
}: CompareTabProps) {
  const { focus } = useFocusTicker();
  const initial = useMemo(() => {
    const seed = [focus.ticker, benchmark, ...default_tickers].filter((t, i, a) => a.indexOf(t) === i);
    return seed.slice(0, 4);
  }, [focus.ticker, benchmark, default_tickers]);

  const [tickers, setTickers] = useState<string[]>(initial);
  const [period, setPeriod] = useState<Period>("1Y");

  // Real-data state — fetched from /api/compare-series
  const [apiSeries, setApiSeries] = useState<ApiTickerSeries[]>([]);
  const [apiDates, setApiDates] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  function add(t: string) {
    if (tickers.length >= 4) return;
    if (tickers.includes(t)) return;
    setTickers([...tickers, t]);
  }
  function remove(t: string) {
    setTickers(tickers.filter((x) => x !== t));
  }

  // Fetch on tickers/period change
  useEffect(() => {
    if (tickers.length === 0) return;
    let cancelled = false;
    setLoading(true);
    setErrorMsg(null);
    const url = `/api/compare-series?tickers=${tickers.join(",")}&period=${period}`;
    fetch(url)
      .then((r) => r.ok ? r.json() : Promise.reject(`HTTP ${r.status}`))
      .then((d: { period: Period; dates: string[]; series: ApiTickerSeries[] }) => {
        if (cancelled) return;
        setApiSeries(d.series || []);
        setApiDates(d.dates || []);
        setLoading(false);
      })
      .catch((e) => {
        if (cancelled) return;
        setErrorMsg(String(e));
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [tickers, period]);

  // Derive plotting series in the chart's expected shape
  const series = useMemo<Series[]>(() => {
    return apiSeries.map((s) => ({
      ticker: s.ticker,
      values: s.values,
      labels: apiDates.map(formatDateShort),
      has_data: s.has_data,
      pct_change: s.pct_change,
      end_price: s.end_price,
    }));
  }, [apiSeries, apiDates]);

  return (
    <div style={{ padding: "16px 20px 20px" }}>
      {/* ── Toolbar ─────────────────────────────────────── */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: 16,
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          {tickers.map((t, i) => (
            <TickerChip
              key={t}
              ticker={t}
              color={COLORS[i]}
              onRemove={tickers.length > 1 ? () => remove(t) : undefined}
            />
          ))}
          {tickers.length < 4 ? (
            <AddTickerChip available={available_tickers.filter((t) => !tickers.includes(t))} onAdd={add} />
          ) : null}
        </div>
        <div className="period-chips" role="tablist" aria-label="Período">
          {(["3M", "1Y", "5Y", "MAX"] as Period[]).map((p) => (
            <button key={p} data-active={p === period} onClick={() => setPeriod(p)}>
              {p}
            </button>
          ))}
        </div>
      </div>

      {/* ── Chart + side panel ──────────────────────────── */}
      <div className="grid grid-cols-12 gap-5">
        <div className="col-span-12 lg:col-span-8">
          <NormalizedLineChart
            series={series}
            dates={apiDates}
            colors={COLORS}
            height={340}
            showBaseline
          />
          <p className="type-byline" style={{ marginTop: 8 }}>
            {loading ? "A carregar séries reais…"
              : errorMsg ? `Erro: ${errorMsg}`
              : `Normalized to 100 at start of period · ${apiDates.length} pontos · fonte: prices DB local`}
          </p>
          {/* Per-ticker no-data warnings */}
          {series.filter((s) => !s.has_data).length > 0 ? (
            <p className="type-byline" style={{ marginTop: 4, color: "var(--verdict-hold)" }}>
              ⚠️ Sem prices na DB para: {series.filter((s) => !s.has_data).map((s) => s.ticker).join(", ")}
              {" "}— corre o fetcher para ver a linha. Por enquanto tratado como ausente, não inventado.
            </p>
          ) : null}
        </div>
        <div className="col-span-12 lg:col-span-4">
          <FundamentalsPanel tickers={tickers} fundamentals={fundamentals_by_ticker} colors={COLORS} />
        </div>
      </div>
    </div>
  );
}

// ── Toolbar pieces ──────────────────────────────────────────────────

function TickerChip({
  ticker,
  color,
  onRemove,
}: {
  ticker: string;
  color: string;
  onRemove?: () => void;
}) {
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 8,
        padding: "6px 10px",
        background: "var(--bg-elevated)",
        border: `1px solid var(--border-subtle)`,
        borderLeft: `3px solid ${color}`,
        borderRadius: "var(--radius-sm)",
        fontFamily: "var(--font-mono)",
        fontSize: 12,
        fontWeight: 600,
        color: "var(--text-primary)",
      }}
    >
      <span style={{ width: 8, height: 8, background: color, borderRadius: 999 }} aria-hidden />
      {ticker}
      {onRemove ? (
        <button
          onClick={onRemove}
          aria-label={`Remove ${ticker}`}
          style={{
            background: "transparent",
            border: 0,
            cursor: "pointer",
            padding: 0,
            color: "var(--text-tertiary)",
            display: "inline-flex",
          }}
        >
          <X size={12} />
        </button>
      ) : null}
    </span>
  );
}

function AddTickerChip({ available, onAdd }: { available: string[]; onAdd: (t: string) => void }) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const filtered = available.filter((t) => t.toLowerCase().includes(query.toLowerCase())).slice(0, 8);
  return (
    <span style={{ position: "relative" }}>
      <button
        onClick={() => setOpen(!open)}
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 6,
          padding: "6px 10px",
          background: "transparent",
          border: "1px dashed var(--border-strong)",
          borderRadius: "var(--radius-sm)",
          color: "var(--text-tertiary)",
          fontSize: 12,
          fontWeight: 500,
          cursor: "pointer",
        }}
      >
        <Plus size={12} /> Add ticker
      </button>
      {open ? (
        <div
          style={{
            position: "absolute",
            top: "calc(100% + 6px)",
            left: 0,
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
            borderRadius: "var(--radius-sm)",
            boxShadow: "var(--shadow-lg)",
            zIndex: 20,
            minWidth: 200,
            padding: 6,
          }}
        >
          <input
            autoFocus
            placeholder="ticker..."
            value={query}
            onChange={(e) => setQuery(e.target.value.toUpperCase())}
            style={{
              width: "100%",
              padding: "6px 8px",
              border: "1px solid var(--border-subtle)",
              borderRadius: 4,
              fontSize: 12,
              fontFamily: "var(--font-mono)",
              marginBottom: 6,
              background: "var(--bg-overlay)",
              color: "var(--text-primary)",
            }}
          />
          <div style={{ maxHeight: 200, overflowY: "auto", display: "flex", flexDirection: "column", gap: 2 }}>
            {filtered.length === 0 ? (
              <p className="type-byline" style={{ padding: 8 }}>Sem resultados</p>
            ) : filtered.map((t) => (
              <button
                key={t}
                onClick={() => { onAdd(t); setOpen(false); setQuery(""); }}
                style={{
                  background: "transparent",
                  border: 0,
                  textAlign: "left",
                  padding: "6px 8px",
                  borderRadius: 4,
                  cursor: "pointer",
                  fontFamily: "var(--font-mono)",
                  fontSize: 12,
                  color: "var(--text-primary)",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = "var(--bg-overlay)")}
                onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
              >
                {t}
              </button>
            ))}
          </div>
        </div>
      ) : null}
    </span>
  );
}

// Old SVG NormalizedChart removed — replaced by Recharts wrapper in
// components/charts/normalized-line-chart.tsx (NN.1 Chart system v2).
// Local Series type kept (matches ChartSeries structurally) for the
// useMemo<Series[]> in the parent.

type Series = {
  ticker: string;
  values: number[];
  labels: string[];          // unused by Recharts wrapper but kept for compat
  has_data: boolean;
  pct_change: number | null;
  end_price: number | null;
};

// ── Fundamentals panel ──────────────────────────────────────────────

function FundamentalsPanel({
  tickers,
  fundamentals,
  colors,
}: {
  tickers: string[];
  fundamentals: Record<string, CompareTickerFundamentals>;
  colors: string[];
}) {
  return (
    <div
      style={{
        background: "var(--bg-overlay)",
        border: "1px solid var(--border-subtle)",
        borderRadius: "var(--radius-sm)",
        padding: 12,
      }}
    >
      <p className="type-h3" style={{ marginBottom: 10 }}>
        Fundamentals · snapshot
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        {tickers.map((t, idx) => {
          const f = fundamentals[t];
          return (
            <div
              key={t}
              style={{
                background: "var(--bg-elevated)",
                border: `1px solid var(--border-subtle)`,
                borderLeft: `3px solid ${colors[idx]}`,
                borderRadius: 4,
                padding: 10,
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                <TickerLogo ticker={t} size="sm" />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <p
                    className="font-data"
                    style={{ fontWeight: 700, fontSize: 12, color: "var(--text-primary)" }}
                  >
                    {t}
                  </p>
                  <p
                    className="type-byline"
                    style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}
                  >
                    {f?.name || "—"}
                  </p>
                </div>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 6, fontSize: 11 }}>
                <Cell label="P/E" value={f?.pe} />
                <Cell label="P/B" value={f?.pb} />
                <Cell label="DY" value={f?.dy} suffix="%" />
                <Cell label="ROE" value={f?.roe} suffix="%" />
                <Cell label="Vital" value={f?.vitality} />
                <Cell label="FV gap" value={f?.fv_gap_pct} suffix="%" colorize />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function Cell({
  label,
  value,
  suffix,
  colorize,
}: {
  label: string;
  value: number | null | undefined;
  suffix?: string;
  colorize?: boolean;
}) {
  const display = value === null || value === undefined ? "—"
    : `${value.toFixed(value > 100 ? 0 : 1)}${suffix || ""}`;
  let color = "var(--text-primary)";
  if (colorize && typeof value === "number") {
    color = value > 0 ? "var(--gain)" : value < 0 ? "var(--loss)" : "var(--text-tertiary)";
  }
  return (
    <div>
      <p style={{ fontSize: 9, letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--text-tertiary)", fontWeight: 600, marginBottom: 1 }}>
        {label}
      </p>
      <p className="font-data" style={{ fontSize: 12, fontWeight: 600, color }}>
        {display}
      </p>
    </div>
  );
}

// Mock series generator removed — chart now uses /api/compare-series.
