"use client";

import { useEffect, useMemo, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

// ─── Period selector ──────────────────────────────────────────────────

type PeriodKey = "1M" | "3M" | "6M" | "YTD" | "1Y" | "3Y" | "ALL";

const PERIOD_DAYS: Record<PeriodKey, number | "ytd" | "all"> = {
  "1M": 30,
  "3M": 90,
  "6M": 180,
  "YTD": "ytd",
  "1Y": 365,
  "3Y": 365 * 3,
  "ALL": "all",
};

function PeriodTabs({
  options,
  value,
  onChange,
}: {
  options: PeriodKey[];
  value: PeriodKey;
  onChange: (k: PeriodKey) => void;
}) {
  return (
    <div className="flex items-center gap-px">
      {options.map((p) => {
        const active = p === value;
        return (
          <button
            key={p}
            type="button"
            onClick={() => onChange(p)}
            className="text-[11px] tracking-wider px-2.5 py-1 transition-colors"
            style={{
              color: active ? "var(--accent-glow)" : "var(--text-tertiary)",
              borderBottom: active
                ? "1px solid var(--accent-glow)"
                : "1px solid transparent",
              background: "transparent",
              fontFamily: "var(--font-sans)",
              fontWeight: active ? 600 : 500,
            }}
          >
            {p}
          </button>
        );
      })}
    </div>
  );
}

// ─── Slicing helpers ──────────────────────────────────────────────────

function sliceByPeriod<T extends { date: string }>(
  rows: T[],
  period: PeriodKey
): T[] {
  if (rows.length === 0) return rows;
  const setting = PERIOD_DAYS[period];
  if (setting === "all") return rows;
  if (setting === "ytd") {
    const yyyy = new Date().getFullYear();
    return rows.filter((r) => r.date >= `${yyyy}-01-01`);
  }
  const cutoff = new Date(Date.now() - setting * 86400000)
    .toISOString()
    .slice(0, 10);
  return rows.filter((r) => r.date >= cutoff);
}

// ─── X-axis tick formatting ───────────────────────────────────────────

const PT_MONTHS = [
  "jan", "fev", "mar", "abr", "mai", "jun",
  "jul", "ago", "set", "out", "nov", "dez",
];

function formatXTick(iso: string, span: PeriodKey): string {
  const d = new Date(iso + "T00:00:00");
  const day = d.getDate();
  const m = PT_MONTHS[d.getMonth()];
  const yy = String(d.getFullYear()).slice(-2);
  if (span === "1M") return `${day} ${m}`;
  if (span === "3M" || span === "6M") return `${day} ${m}`;
  if (span === "YTD" || span === "1Y") return m;
  return `${m} ${yy}`;
}

function formatYTick(v: number): string {
  const abs = Math.abs(v);
  if (abs >= 1_000_000) return `${(v / 1_000_000).toFixed(1)}M`;
  if (abs >= 1_000) return `${(v / 1_000).toFixed(0)}k`;
  return v.toFixed(0);
}

// ─── Stamp (date label) ────────────────────────────────────────────────

function formatStamp(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso + (iso.length <= 10 ? "T00:00:00" : ""));
  if (isNaN(d.getTime())) return iso;
  const dd = String(d.getDate()).padStart(2, "0");
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const yy = String(d.getFullYear()).slice(-2);
  return `${dd}/${mm}/${yy}`;
}

function formatCurrencyValue(
  v: number,
  currency: "BRL" | "USD",
  digits = 2
): string {
  const sym = currency === "BRL" ? "R$" : "$";
  return `${sym}${v.toLocaleString(currency === "BRL" ? "pt-BR" : "en-US", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  })}`;
}

// ─── Editorial chart shell ────────────────────────────────────────────
// Single shared chart aesthetic — WSJ/Bloomberg discipline.
// Thin line · right Y-axis · sparse X ticks · zero grid · faint reference

type Point = { date: string; value: number; ref?: number; index?: number };

function EditorialLineChart({
  data,
  accent,
  height,
  showReference,
  span,
  currency,
  showIndex,
  indexLabel,
}: {
  data: Point[];
  accent: string;
  height: number;
  showReference: boolean;
  span: PeriodKey;
  currency: "BRL" | "USD";
  showIndex?: boolean;
  indexLabel?: string;
}) {
  // Recharts ResponsiveContainer relies on DOM measurement; render only after mount
  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <div style={{ height }} aria-hidden />;
  }

  if (data.length < 2) {
    return (
      <div
        className="grid place-items-center text-xs italic"
        style={{
          height,
          color: "var(--text-tertiary)",
        }}
      >
        sem série temporal
      </div>
    );
  }

  // Build domain padding so the line never touches the borders
  const values = data.map((d) => d.value);
  if (showReference) {
    for (const d of data) if (d.ref !== undefined) values.push(d.ref);
  }
  if (showIndex) {
    for (const d of data) if (d.index !== undefined) values.push(d.index);
  }
  const lo = Math.min(...values);
  const hi = Math.max(...values);
  const pad = (hi - lo) * 0.08 || hi * 0.05;
  const domain: [number, number] = [Math.max(0, lo - pad), hi + pad];

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 4, right: 8, left: 4, bottom: 4 }}>
        <XAxis
          dataKey="date"
          axisLine={{ stroke: "var(--border-subtle)" }}
          tickLine={false}
          tick={{
            fontSize: 10,
            fill: "var(--text-tertiary)",
            fontFamily: "var(--font-mono)",
          }}
          tickFormatter={(v: string) => formatXTick(v, span)}
          minTickGap={36}
          interval="preserveStartEnd"
        />
        <YAxis
          orientation="right"
          axisLine={false}
          tickLine={false}
          tick={{
            fontSize: 10,
            fill: "var(--text-tertiary)",
            fontFamily: "var(--font-mono)",
          }}
          tickFormatter={formatYTick}
          domain={domain}
          width={48}
        />
        {showReference && data[data.length - 1]?.ref !== undefined && (
          <ReferenceLine
            y={data[data.length - 1].ref!}
            stroke="var(--text-disabled)"
            strokeDasharray="2 4"
            ifOverflow="extendDomain"
          />
        )}
        <Tooltip
          cursor={{
            stroke: "var(--border-strong)",
            strokeDasharray: "2 2",
          }}
          contentStyle={{
            background: "var(--bg-canvas)",
            border: "1px solid var(--border-strong)",
            borderRadius: 2,
            fontSize: 11,
            padding: "6px 10px",
            fontFamily: "var(--font-mono)",
          }}
          labelStyle={{
            color: "var(--text-tertiary)",
            fontSize: 10,
            marginBottom: 4,
            fontFamily: "var(--font-sans)",
            textTransform: "uppercase",
            letterSpacing: "0.05em",
          }}
          itemStyle={{ color: "var(--text-primary)", padding: 0 }}
          labelFormatter={(label) => formatStamp(String(label))}
          formatter={(value, name) => {
            const num = typeof value === "number" ? value : Number(value);
            const v = isFinite(num)
              ? formatCurrencyValue(num, currency, 0)
              : String(value);
            const label = name === "value" ? "mv" : String(name ?? "");
            return [v, label];
          }}
          separator=" "
        />
        {showReference && (
          <Line
            type="monotone"
            dataKey="ref"
            name="cost"
            stroke="var(--text-disabled)"
            strokeWidth={1}
            strokeDasharray="3 3"
            dot={false}
            isAnimationActive={false}
          />
        )}
        {showIndex && (
          <Line
            type="monotone"
            dataKey="index"
            name={indexLabel || "index"}
            stroke="var(--val-gold, #ca8a04)"
            strokeWidth={1.25}
            strokeDasharray="4 2"
            dot={false}
            isAnimationActive={false}
          />
        )}
        <Line
          type="monotone"
          dataKey="value"
          name="value"
          stroke={accent}
          strokeWidth={1.5}
          dot={false}
          activeDot={{ r: 3, fill: accent, stroke: "var(--bg-canvas)", strokeWidth: 1.5 }}
          isAnimationActive={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

// ─── Per-ticker price chart (WSJ-style) ────────────────────────────────

export function PriceChart({
  ticker,
  days = 365,
  height = 240,
}: {
  ticker: string;
  days?: number;
  height?: number;
}) {
  const [series, setSeries] = useState<{ date: string; close: number }[]>([]);
  const [meta, setMeta] = useState<{ name?: string; market?: string }>({});
  const [period, setPeriod] = useState<PeriodKey>("YTD");
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    fetch(`/api/prices/${ticker}?days=${Math.max(days, 365 * 3)}`)
      .then((r) => r.json())
      .then((j) => {
        if (!alive) return;
        if (j.error) setErr(j.error);
        else {
          setSeries(j.series || []);
          setMeta({ name: j.name, market: j.market });
        }
      })
      .catch((e) => alive && setErr(String(e)))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [ticker, days]);

  const sliced = useMemo(
    () => sliceByPeriod(series, period),
    [series, period]
  );

  const points: Point[] = useMemo(
    () => sliced.map((r) => ({ date: r.date, value: r.close })),
    [sliced]
  );

  if (loading) {
    return (
      <div
        className="grid place-items-center text-xs"
        style={{ height, color: "var(--text-tertiary)" }}
      >
        loading {ticker}…
      </div>
    );
  }
  if (err) {
    return (
      <div
        className="text-xs italic"
        style={{ color: "var(--verdict-avoid)" }}
      >
        {err}
      </div>
    );
  }
  if (series.length === 0) {
    return (
      <div
        className="text-xs italic"
        style={{ color: "var(--text-tertiary)" }}
      >
        sem dados de preço
      </div>
    );
  }

  const currency = meta.market === "br" ? "BRL" : "USD";
  const first = sliced[0]?.close ?? 0;
  const last = sliced[sliced.length - 1]?.close ?? 0;
  const pct = first ? ((last / first - 1) * 100) : 0;
  const positive = pct >= 0;
  const accent =
    meta.market === "br" ? "var(--mkt-br)" : "var(--mkt-us)";
  const lastDate = sliced[sliced.length - 1]?.date;

  // Compute period high/low for "52w range"-style line
  const hi = sliced.reduce((m, r) => (r.close > m ? r.close : m), -Infinity);
  const lo = sliced.reduce((m, r) => (r.close < m ? r.close : m), Infinity);

  return (
    <div className="space-y-3">
      {/* Header: KPI left + period tabs right ----------------------- */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <p
            className="text-[10px] uppercase tracking-wider mb-1"
            style={{ color: "var(--text-tertiary)" }}
          >
            últ. cotação · {formatStamp(lastDate)}
          </p>
          <div className="flex items-baseline gap-3 flex-wrap">
            <span
              className="font-display font-bold tabular"
              style={{ fontSize: 26, color: "var(--text-primary)" }}
            >
              {formatCurrencyValue(last, currency, 2)}
            </span>
            <span
              className="text-xs font-data"
              style={{ color: "var(--text-tertiary)" }}
            >
              {currency}
            </span>
          </div>
          <div
            className="flex items-center gap-1 mt-1 text-xs font-data"
            style={{ color: positive ? "var(--gain)" : "var(--loss)" }}
          >
            <span aria-hidden>{positive ? "▲" : "▼"}</span>
            <span>
              {positive ? "+" : ""}
              {(last - first).toFixed(2)}
            </span>
            <span>·</span>
            <span>
              {positive ? "+" : ""}
              {pct.toFixed(2)}%
            </span>
            <span style={{ color: "var(--text-tertiary)" }} className="ml-1">
              {period}
            </span>
          </div>
        </div>
        <PeriodTabs
          options={["1M", "3M", "6M", "YTD", "1Y", "3Y"]}
          value={period}
          onChange={setPeriod}
        />
      </div>

      {/* Chart -------------------------------------------------- */}
      <EditorialLineChart
        data={points}
        accent={accent}
        height={height}
        showReference={false}
        span={period}
        currency={currency as "BRL" | "USD"}
      />

      {/* Footer KPI row — period range, like WSJ "52 Week Range" */}
      <div
        className="flex items-center gap-6 flex-wrap text-[11px] pt-2"
        style={{
          color: "var(--text-tertiary)",
          borderTop: "1px solid var(--border-subtle)",
        }}
      >
        <span>
          range {period}{" "}
          <span
            className="font-data"
            style={{ color: "var(--text-secondary)" }}
          >
            {formatCurrencyValue(lo, currency, 2)} —{" "}
            {formatCurrencyValue(hi, currency, 2)}
          </span>
        </span>
        {meta.name && (
          <span>
            ticker{" "}
            <span style={{ color: "var(--text-secondary)" }}>
              {meta.name}
            </span>
          </span>
        )}
      </div>
    </div>
  );
}

// ─── Portfolio P&L chart (WSJ-style stacked BR + US) ──────────────────

// Single-market account value chart — JPM-style, used by the home hero.
// Caller passes `market` and we render only that market's series with a
// period selector. Pure client-side fetch from /api/portfolio/timeseries.
export function AccountValueChart({
  market,
  height = 240,
}: {
  market: "br" | "us";
  height?: number;
}) {
  const [data, setData] = useState<{
    br: { date: string; mv: number; cost: number; index?: number }[];
    us: { date: string; mv: number; cost: number; index?: number }[];
  }>({ br: [], us: [] });
  const [loading, setLoading] = useState(true);
  const [showIndex, setShowIndex] = useState(false);

  const indexSymbolBR = "BOVA11";
  const indexSymbolUS = "SPY";

  useEffect(() => {
    let alive = true;
    setLoading(true);
    const qs = showIndex
      ? `?index_br=${indexSymbolBR}&index_us=${indexSymbolUS}`
      : "";
    fetch(`/api/portfolio/timeseries${qs}`)
      .then((r) => r.json())
      .then((j) => alive && setData(j))
      .catch(() => {})
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [showIndex]);

  if (loading) {
    return (
      <div
        className="grid place-items-center text-xs"
        style={{ height, color: "var(--text-tertiary)" }}
      >
        loading…
      </div>
    );
  }

  const rows = market === "br" ? data.br : data.us;
  const currency = market === "br" ? "BRL" : "USD";
  const accent = market === "br" ? "var(--mkt-br)" : "var(--mkt-us)";
  const label = market === "br" ? "Brasil · BRL" : "EUA · USD";
  const indexSymbol = market === "br" ? indexSymbolBR : indexSymbolUS;

  if (rows.length < 2) {
    return (
      <div
        className="text-xs italic"
        style={{ color: "var(--text-tertiary)" }}
      >
        sem timeseries — corre <code className="font-data">ii snapshot --backfill 90</code>
      </div>
    );
  }

  return (
    <PortfolioMarketBlock
      label={label}
      rows={rows}
      accent={accent}
      currency={currency}
      height={height}
      indexSymbol={indexSymbol}
      showIndex={showIndex}
      onToggleIndex={() => setShowIndex((v) => !v)}
    />
  );
}

export function PortfolioChart({ height = 200 }: { height?: number }) {
  const [data, setData] = useState<{
    br: { date: string; mv: number; cost: number }[];
    us: { date: string; mv: number; cost: number }[];
    source?: string;
  }>({ br: [], us: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    fetch("/api/portfolio/timeseries")
      .then((r) => r.json())
      .then((j) => alive && setData(j))
      .catch(() => {})
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, []);

  if (loading) {
    return (
      <div
        className="grid place-items-center text-xs"
        style={{ height, color: "var(--text-tertiary)" }}
      >
        loading portfolio…
      </div>
    );
  }

  const hasBR = data.br.length > 1;
  const hasUS = data.us.length > 1;
  if (!hasBR && !hasUS) {
    return (
      <div
        className="text-xs italic"
        style={{ color: "var(--text-tertiary)" }}
      >
        sem timeseries — corre <code className="font-data">ii snapshot --backfill 90</code>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {hasBR && (
        <PortfolioMarketBlock
          label="Brasil · BRL"
          rows={data.br}
          accent="var(--mkt-br)"
          currency="BRL"
          height={height}
        />
      )}
      {hasBR && hasUS && (
        <div
          aria-hidden
          style={{
            height: 1,
            background: "var(--border-subtle)",
          }}
        />
      )}
      {hasUS && (
        <PortfolioMarketBlock
          label="EUA · USD"
          rows={data.us}
          accent="var(--mkt-us)"
          currency="USD"
          height={height}
        />
      )}
      {data.source && (
        <p
          className="text-[10px]"
          style={{ color: "var(--text-disabled)" }}
        >
          source: {data.source}
        </p>
      )}
    </div>
  );
}

function PortfolioMarketBlock({
  label,
  rows,
  accent,
  currency,
  height,
  indexSymbol,
  showIndex,
  onToggleIndex,
}: {
  label: string;
  rows: { date: string; mv: number; cost: number; index?: number }[];
  accent: string;
  currency: "BRL" | "USD";
  height: number;
  indexSymbol?: string;
  showIndex?: boolean;
  onToggleIndex?: () => void;
}) {
  const [period, setPeriod] = useState<PeriodKey>("ALL");

  const sliced = useMemo(() => sliceByPeriod(rows, period), [rows, period]);

  // Re-rebase the index to first visible MV so the overlay aligns to the slice
  const points = useMemo(() => {
    if (!showIndex) {
      return sliced.map((r) => ({ date: r.date, value: r.mv, ref: r.cost }));
    }
    const firstWithIndex = sliced.find((r) => r.index !== undefined);
    if (!firstWithIndex) {
      return sliced.map((r) => ({ date: r.date, value: r.mv, ref: r.cost }));
    }
    const baseMv = firstWithIndex.mv;
    const baseIdx = firstWithIndex.index!;
    return sliced.map((r) => {
      const rebased =
        r.index !== undefined ? (r.index / baseIdx) * baseMv : undefined;
      return {
        date: r.date,
        value: r.mv,
        ref: r.cost,
        index: rebased,
      } as Point & { index?: number };
    });
  }, [sliced, showIndex]);

  if (sliced.length < 2) {
    return (
      <div className="space-y-2">
        <Header
          label={label}
          last={null}
          first={null}
          currency={currency}
          period={period}
          setPeriod={setPeriod}
        />
        <p
          className="text-xs italic"
          style={{ color: "var(--text-tertiary)" }}
        >
          janela curta — escolhe outro período
        </p>
      </div>
    );
  }

  const last = sliced[sliced.length - 1];
  const first = sliced[0];

  return (
    <div className="space-y-3">
      <Header
        label={label}
        last={last}
        first={first}
        currency={currency}
        period={period}
        setPeriod={setPeriod}
      />
      {indexSymbol && onToggleIndex && (
        <div className="flex items-center justify-end gap-2 -mt-2 mb-1">
          <button
            type="button"
            onClick={onToggleIndex}
            className="text-[10px] px-2 py-0.5 rounded transition-colors uppercase tracking-wider"
            style={{
              background: showIndex ? "var(--accent-primary)" : "transparent",
              color: showIndex ? "white" : "var(--text-tertiary)",
              border: `1px solid ${showIndex ? "var(--accent-primary)" : "var(--border-subtle)"}`,
              fontFamily: "var(--font-sans)",
              fontWeight: 600,
            }}
          >
            vs {indexSymbol}
          </button>
        </div>
      )}
      <EditorialLineChart
        data={points}
        accent={accent}
        height={height}
        showReference={true}
        span={period}
        currency={currency}
        showIndex={showIndex}
        indexLabel={indexSymbol}
      />
      {/* Footer: cost + period high/low */}
      <PortfolioFooter rows={sliced} currency={currency} period={period} />
    </div>
  );
}

function Header({
  label,
  last,
  first,
  currency,
  period,
  setPeriod,
}: {
  label: string;
  last: { date: string; mv: number; cost: number } | null;
  first: { date: string; mv: number; cost: number } | null;
  currency: "BRL" | "USD";
  period: PeriodKey;
  setPeriod: (p: PeriodKey) => void;
}) {
  const periodPnl =
    first && last && first.mv ? ((last.mv / first.mv - 1) * 100) : null;
  const totalPnlPct =
    last && last.cost ? ((last.mv / last.cost - 1) * 100) : null;
  const positive = (periodPnl ?? totalPnlPct ?? 0) >= 0;
  return (
    <div className="flex items-start justify-between gap-4 flex-wrap">
      <div>
        <p
          className="text-[10px] uppercase tracking-wider mb-1"
          style={{ color: "var(--text-tertiary)" }}
        >
          {label} · att. {last ? formatStamp(last.date) : "—"}
        </p>
        <div className="flex items-baseline gap-3 flex-wrap">
          <span
            className="font-display font-bold tabular"
            style={{ fontSize: 24, color: "var(--text-primary)" }}
          >
            {last ? formatCurrencyValue(last.mv, currency, 0) : "—"}
          </span>
        </div>
        {last && (
          <div className="flex items-center gap-2 mt-1 text-xs font-data flex-wrap">
            {periodPnl !== null && (
              <span
                style={{ color: positive ? "var(--gain)" : "var(--loss)" }}
              >
                <span aria-hidden>{positive ? "▲" : "▼"}</span>{" "}
                {positive ? "+" : ""}
                {periodPnl.toFixed(2)}%{" "}
                <span style={{ color: "var(--text-tertiary)" }}>{period}</span>
              </span>
            )}
            {totalPnlPct !== null && (
              <span style={{ color: "var(--text-tertiary)" }}>
                ·{" "}
                <span
                  style={{
                    color:
                      totalPnlPct >= 0
                        ? "var(--gain)"
                        : "var(--loss)",
                  }}
                >
                  {totalPnlPct >= 0 ? "+" : ""}
                  {totalPnlPct.toFixed(1)}%
                </span>{" "}
                vs custo
              </span>
            )}
          </div>
        )}
      </div>
      <PeriodTabs
        options={["1M", "3M", "6M", "YTD", "1Y", "ALL"]}
        value={period}
        onChange={setPeriod}
      />
    </div>
  );
}

function PortfolioFooter({
  rows,
  currency,
  period,
}: {
  rows: { date: string; mv: number; cost: number }[];
  currency: "BRL" | "USD";
  period: PeriodKey;
}) {
  if (rows.length === 0) return null;
  const hi = rows.reduce((m, r) => (r.mv > m ? r.mv : m), -Infinity);
  const lo = rows.reduce((m, r) => (r.mv < m ? r.mv : m), Infinity);
  const last = rows[rows.length - 1];
  return (
    <div
      className="flex items-center gap-6 flex-wrap text-[11px] pt-2"
      style={{
        color: "var(--text-tertiary)",
        borderTop: "1px solid var(--border-subtle)",
      }}
    >
      <span>
        custo{" "}
        <span
          className="font-data"
          style={{ color: "var(--text-secondary)" }}
        >
          {formatCurrencyValue(last.cost, currency, 0)}
        </span>
      </span>
      <span>
        range {period}{" "}
        <span
          className="font-data"
          style={{ color: "var(--text-secondary)" }}
        >
          {formatCurrencyValue(lo, currency, 0)} —{" "}
          {formatCurrencyValue(hi, currency, 0)}
        </span>
      </span>
      <span>
        n{" "}
        <span
          className="font-data"
          style={{ color: "var(--text-secondary)" }}
        >
          {rows.length}
        </span>{" "}
        pontos
      </span>
    </div>
  );
}
