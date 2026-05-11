"use client";

/**
 * FairTrajectoryChart — Phase LL Sprint 3.3.
 *
 * 5-year sparkline of our_fair (filings-grounded conservative target) +
 * fair_price (Buffett/Graham consensus ceiling) + current_price (yfinance/B3).
 *
 * Reads /api/fair-trajectory/[ticker] which serves the append-only history
 * from fair_value table (Phase KK timestamp keys). Powers the user's
 * "5 years ago ITSA4 was R$10, now R$15" use case for compounding insight.
 */

import { useEffect, useMemo, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

type TrajectoryPoint = {
  date: string;
  computed_at: string;
  method: string;
  fair_price: number | null;
  our_fair: number | null;
  current_price: number | null;
  action: string | null;
  confidence: string | null;
  trigger: string | null;
};

type ApiResponse = {
  ticker: string;
  market: "br" | "us";
  name: string | null;
  sector: string | null;
  n_trajectory: number;
  latest: TrajectoryPoint | null;
  trajectory: TrajectoryPoint[];
  prices: { date: string; close: number }[];
};

type PeriodKey = "1Y" | "3Y" | "5Y" | "ALL";

const PT_MONTHS = [
  "jan", "fev", "mar", "abr", "mai", "jun",
  "jul", "ago", "set", "out", "nov", "dez",
];

function formatStamp(iso: string): string {
  const d = new Date(iso + (iso.length <= 10 ? "T00:00:00" : ""));
  if (isNaN(d.getTime())) return iso;
  const dd = String(d.getDate()).padStart(2, "0");
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const yy = String(d.getFullYear()).slice(-2);
  return `${dd}/${mm}/${yy}`;
}

function formatXTick(iso: string, period: PeriodKey): string {
  const d = new Date(iso + "T00:00:00");
  if (isNaN(d.getTime())) return iso;
  const m = PT_MONTHS[d.getMonth()];
  const yy = String(d.getFullYear()).slice(-2);
  if (period === "1Y") return m;
  return `${m} ${yy}`;
}

function formatCurrencyValue(v: number, cur: "BRL" | "USD"): string {
  const sym = cur === "BRL" ? "R$" : "$";
  return `${sym}${v.toLocaleString(cur === "BRL" ? "pt-BR" : "en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

const PERIOD_DAYS: Record<PeriodKey, number | "all"> = {
  "1Y": 365,
  "3Y": 365 * 3,
  "5Y": 365 * 5,
  "ALL": "all",
};

export function FairTrajectoryChart({
  ticker,
  height = 240,
}: {
  ticker: string;
  height?: number;
}) {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);
  const [period, setPeriod] = useState<PeriodKey>("5Y");

  useEffect(() => {
    let alive = true;
    setLoading(true);
    fetch(`/api/fair-trajectory/${ticker}?days=1825&include_price=true`)
      .then((r) => r.json())
      .then((j) => {
        if (!alive) return;
        if (j.error) setErr(j.error);
        else setData(j);
      })
      .catch((e) => alive && setErr(String(e)))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [ticker]);

  // Merge trajectory + price series by date for overlay charting. The
  // trajectory is sparse (one row per fair_value compute, e.g. daily);
  // prices are dense (every trading day). Build a map keyed by date so
  // the line interpolates naturally.
  const merged = useMemo(() => {
    if (!data) return [] as Array<{
      date: string;
      our_fair: number | null;
      fair_price: number | null;
      price: number | null;
    }>;
    const setting = PERIOD_DAYS[period];
    const cutoff =
      setting === "all"
        ? "0000-01-01"
        : new Date(Date.now() - setting * 86400000).toISOString().slice(0, 10);

    // Index trajectory by date (last write wins for same-date)
    const trajByDate = new Map<string, TrajectoryPoint>();
    for (const t of data.trajectory) {
      if (t.date >= cutoff) trajByDate.set(t.date, t);
    }
    const priceByDate = new Map<string, number>();
    for (const p of data.prices) {
      if (p.date >= cutoff) priceByDate.set(p.date, p.close);
    }

    // Union of dates, sorted
    const allDates = Array.from(
      new Set([...trajByDate.keys(), ...priceByDate.keys()])
    ).sort();

    // Forward-fill our_fair and fair_price (sparse) so the line is continuous
    let lastOur: number | null = null;
    let lastFair: number | null = null;
    return allDates.map((d) => {
      const t = trajByDate.get(d);
      if (t) {
        if (t.our_fair != null) lastOur = t.our_fair;
        if (t.fair_price != null) lastFair = t.fair_price;
      }
      return {
        date: d,
        our_fair: lastOur,
        fair_price: lastFair,
        price: priceByDate.get(d) ?? null,
      };
    });
  }, [data, period]);

  if (loading) {
    return (
      <div
        className="grid place-items-center text-xs"
        style={{ height, color: "var(--text-tertiary)" }}
      >
        loading trajectory…
      </div>
    );
  }
  if (err) {
    return (
      <div className="text-xs italic" style={{ color: "var(--verdict-avoid)" }}>
        {err}
      </div>
    );
  }
  if (!data || data.n_trajectory === 0) {
    return (
      <div
        className="text-xs italic p-3"
        style={{ color: "var(--text-tertiary)" }}
      >
        sem trajectória de fair value — primeiros pontos aparecem após Phase
        KK ({formatStamp(new Date().toISOString().slice(0, 10))} em diante).
      </div>
    );
  }

  const currency: "BRL" | "USD" = data.market === "br" ? "BRL" : "USD";
  const accentOur = "var(--accent-glow)";   // our_fair: solid accent
  const accentFair = "var(--text-tertiary)"; // consensus: muted
  const accentPrice =
    data.market === "br" ? "var(--mkt-br)" : "var(--mkt-us)"; // price

  const latest = data.latest;
  const firstPrice = merged.find((m) => m.price != null)?.price ?? null;
  const lastPrice =
    [...merged].reverse().find((m) => m.price != null)?.price ?? null;
  const priceChangePct =
    firstPrice && lastPrice ? (lastPrice / firstPrice - 1) * 100 : null;

  const firstOur = merged.find((m) => m.our_fair != null)?.our_fair ?? null;
  const lastOur =
    [...merged].reverse().find((m) => m.our_fair != null)?.our_fair ?? null;
  const ourChangePct =
    firstOur && lastOur ? (lastOur / firstOur - 1) * 100 : null;

  return (
    <div className="space-y-3">
      {/* Header — KPI strip + period tabs */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <p
            className="text-[10px] uppercase tracking-wider mb-1"
            style={{ color: "var(--text-tertiary)" }}
          >
            fair value · trajectória {period}
          </p>
          {latest && (
            <div className="flex items-baseline gap-3 flex-wrap">
              <span
                className="font-display font-bold tabular"
                style={{ fontSize: 22, color: "var(--text-primary)" }}
              >
                {latest.our_fair != null
                  ? formatCurrencyValue(latest.our_fair, currency)
                  : "—"}
              </span>
              <span
                className="text-[10px] uppercase tracking-wider"
                style={{ color: "var(--text-tertiary)" }}
              >
                our_fair
              </span>
              <span
                className="text-[11px] font-data"
                style={{ color: "var(--text-secondary)" }}
              >
                consensus{" "}
                {latest.fair_price != null
                  ? formatCurrencyValue(latest.fair_price, currency)
                  : "—"}
              </span>
              {latest.action && (
                <span
                  className="text-[10px] font-semibold px-1.5 py-0.5 rounded uppercase tracking-wider"
                  style={{
                    background:
                      latest.action === "STRONG_BUY"
                        ? "var(--action-gold)"
                        : latest.action === "BUY"
                          ? "var(--action-gold-soft)"
                          : "var(--bg-overlay)",
                    color:
                      latest.action === "STRONG_BUY"
                        ? "white"
                        : latest.action === "BUY"
                          ? "var(--action-gold-ink)"
                          : latest.action === "SELL"
                            ? "var(--loss)"
                            : "var(--text-secondary)",
                  }}
                >
                  {latest.action}
                </span>
              )}
              {latest.confidence && (
                <span
                  className="text-[10px] font-data"
                  style={{ color: "var(--text-tertiary)" }}
                >
                  [{latest.confidence}]
                </span>
              )}
            </div>
          )}
          {ourChangePct != null && (
            <p
              className="text-[11px] mt-1 font-data"
              style={{
                color: ourChangePct >= 0 ? "var(--gain)" : "var(--loss)",
              }}
            >
              {ourChangePct >= 0 ? "▲" : "▼"} our_fair{" "}
              {ourChangePct >= 0 ? "+" : ""}
              {ourChangePct.toFixed(1)}%
              {priceChangePct != null && (
                <span
                  className="ml-2"
                  style={{
                    color: priceChangePct >= 0 ? "var(--gain)" : "var(--loss)",
                  }}
                >
                  · price{" "}
                  {priceChangePct >= 0 ? "+" : ""}
                  {priceChangePct.toFixed(1)}%
                </span>
              )}
              <span
                className="ml-2"
                style={{ color: "var(--text-tertiary)" }}
              >
                {period}
              </span>
            </p>
          )}
        </div>

        {/* Period tabs */}
        <div className="flex items-center gap-px">
          {(["1Y", "3Y", "5Y", "ALL"] as PeriodKey[]).map((p) => {
            const active = p === period;
            return (
              <button
                key={p}
                type="button"
                onClick={() => setPeriod(p)}
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
      </div>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={merged} margin={{ top: 4, right: 8, left: 4, bottom: 4 }}>
          <XAxis
            dataKey="date"
            axisLine={{ stroke: "var(--border-subtle)" }}
            tickLine={false}
            tick={{
              fontSize: 10,
              fill: "var(--text-tertiary)",
              fontFamily: "var(--font-mono)",
            }}
            tickFormatter={(v: string) => formatXTick(v, period)}
            minTickGap={42}
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
            tickFormatter={(v: number) => v.toFixed(0)}
            width={48}
          />
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
            itemStyle={{ padding: 0 }}
            labelFormatter={(label) => formatStamp(String(label))}
            formatter={(value, name) => {
              const num = typeof value === "number" ? value : Number(value);
              if (!isFinite(num)) return ["—", String(name)];
              return [formatCurrencyValue(num, currency), String(name)];
            }}
            separator=" "
          />
          <Legend
            verticalAlign="top"
            height={20}
            wrapperStyle={{
              fontSize: 10,
              fontFamily: "var(--font-sans)",
              color: "var(--text-tertiary)",
              textTransform: "uppercase",
              letterSpacing: "0.05em",
            }}
          />
          {/* Order matters: price drawn on top so it doesn't get covered */}
          <Line
            type="monotone"
            dataKey="fair_price"
            name="consensus"
            stroke={accentFair}
            strokeWidth={1}
            strokeDasharray="3 3"
            dot={false}
            isAnimationActive={false}
            connectNulls
          />
          <Line
            type="monotone"
            dataKey="our_fair"
            name="our_fair"
            stroke={accentOur}
            strokeWidth={1.75}
            dot={false}
            isAnimationActive={false}
            connectNulls
          />
          <Line
            type="monotone"
            dataKey="price"
            name="price"
            stroke={accentPrice}
            strokeWidth={1.5}
            dot={false}
            activeDot={{
              r: 3,
              fill: accentPrice,
              stroke: "var(--bg-canvas)",
              strokeWidth: 1.5,
            }}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>

      {/* Footer: trajectory provenance */}
      <div
        className="flex items-center gap-6 flex-wrap text-[11px] pt-2"
        style={{
          color: "var(--text-tertiary)",
          borderTop: "1px solid var(--border-subtle)",
        }}
      >
        <span>
          n{" "}
          <span
            className="font-data"
            style={{ color: "var(--text-secondary)" }}
          >
            {data.n_trajectory}
          </span>{" "}
          fv computes
        </span>
        {latest?.method && (
          <span>
            método{" "}
            <span
              className="font-data"
              style={{ color: "var(--text-secondary)" }}
            >
              {latest.method}
            </span>
          </span>
        )}
        {latest?.trigger && (
          <span>
            últ. trigger{" "}
            <span
              className="font-data"
              style={{ color: "var(--text-secondary)" }}
            >
              {latest.trigger}
            </span>
          </span>
        )}
      </div>
    </div>
  );
}
