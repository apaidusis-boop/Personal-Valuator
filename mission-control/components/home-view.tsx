"use client";

// JPM-style home dashboard. Receives both BR and US data from the server
// component and renders the active market based on a client-side toggle.
// The toggle defaults to BR (most assets live there) and persists via URL
// `?market=br|us` so a copy/paste link reopens the same view.

import { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { TickerLogo, PercentDelta, MarketToggle } from "./jpm-atoms";
import { AccountValueChart } from "./charts";
import { formatCurrency, formatDate } from "@/lib/format";
import { openTickerSheet } from "@/lib/ticker-sheet";
import AlertsRibbon from "./alerts-ribbon";
import CalendarCard from "./calendar-card";

// ── Public types ────────────────────────────────────────────────────

export type HomePosition = {
  ticker: string;
  name: string;
  sector: string | null;
  group_label: string;
  quantity: number | null;
  current_unit: number | null;
  current_value: number;
  cost_basis: number;
  pnl_pct: number | null;
};

export type HomeWatchlistItem = {
  ticker: string;
  name: string;
  last: number | null;
  pct_chg: number | null;
};

export type HomeIndex = {
  symbol: string;
  label: string;
  value: number | null;
  delta_abs: number | null;
  delta_pct: number | null;
};

export type HomeMarketData = {
  market: "br" | "us";
  account_value: number;     // MV of equities (+ RF for BR)
  total_cost: number;
  day_gain_abs: number | null;
  day_gain_pct: number | null;
  total_gain_abs: number;
  total_gain_pct: number;
  estimated_annual_income: number | null;
  cash_sweep: number | null;
  positions: HomePosition[];
  watchlist: HomeWatchlistItem[];
  indices: HomeIndex[];
  asset_classes: { name: string; allocation: number; value: number; color: string }[];
};

export type HomeViewProps = {
  br: HomeMarketData;
  us: HomeMarketData;
  council_summary: string;     // e.g. "Council 7 May · 33 subjects"
  briefing_relative: string;   // e.g. "briefing há 2h"
};

// ── Helpers ─────────────────────────────────────────────────────────

function readInitialMarket(): "br" | "us" {
  if (typeof window === "undefined") return "br";
  const url = new URL(window.location.href);
  const m = url.searchParams.get("market");
  if (m === "us" || m === "br") return m;
  return "br";
}

// ── HomeView ────────────────────────────────────────────────────────

export function HomeView({ br, us, council_summary, briefing_relative }: HomeViewProps) {
  const [market, setMarket] = useState<"br" | "us">("br");
  const [hydrated, setHydrated] = useState(false);

  // Hydrate from URL on mount (avoids SSR/CSR mismatch).
  useEffect(() => {
    setMarket(readInitialMarket());
    setHydrated(true);
  }, []);

  // Persist to URL without reload.
  useEffect(() => {
    if (!hydrated) return;
    const url = new URL(window.location.href);
    url.searchParams.set("market", market);
    window.history.replaceState({}, "", url.toString());
  }, [market, hydrated]);

  const data = market === "br" ? br : us;
  const currency = market === "br" ? "BRL" : "USD";
  const accountLabel = market === "br" ? "Carteira Brasil (XP)" : "Carteira EUA (JPM)";

  return (
    <div className="px-6 py-5 max-w-[1440px] mx-auto">
      {/* ── Page header: account label + freshness + market toggle ── */}
      <header className="flex items-end justify-between flex-wrap gap-3 mb-5">
        <div>
          <h1
            className="font-display"
            style={{ fontSize: 18, fontWeight: 600, color: "var(--text-primary)" }}
          >
            {accountLabel}
          </h1>
          <p className="type-byline" style={{ marginTop: 2 }}>
            {council_summary}
            {briefing_relative ? ` · ${briefing_relative}` : ""}
          </p>
        </div>
        <MarketToggle
          value={market}
          onChange={setMarket}
          brLabel={<>Brasil <span className="font-data" style={{ marginLeft: 4, color: "var(--text-tertiary)", fontSize: 11 }}>BRL</span></>}
          usLabel={<>EUA <span className="font-data" style={{ marginLeft: 4, color: "var(--text-tertiary)", fontSize: 11 }}>USD</span></>}
        />
      </header>

      {/* ── Alerts ribbon: divs / earnings / filings ─────────────── */}
      <div className="mb-5">
        <AlertsRibbon />
      </div>

      {/* ── 12-col grid: hero + chart (8) | side rail (4) ─────────── */}
      <div className="grid grid-cols-12 gap-5">
        {/* ── Account value hero ───────────────────────────────── */}
        <section
          className="col-span-12 lg:col-span-8 card p-5"
          aria-label="Account value summary"
        >
          <div className="flex items-start justify-between mb-3">
            <h2 className="type-h3">Account value</h2>
            <Link
              href="/portfolio"
              className="text-[12px] flex items-center gap-1 hover:underline"
              style={{ color: "var(--accent-primary)", fontWeight: 500 }}
            >
              See all balances <ArrowRight size={12} />
            </Link>
          </div>

          <div className="type-display tabular" style={{ marginBottom: 10 }}>
            {formatCurrency(data.account_value, currency, 2)}
          </div>

          {/* 4-stat row: Day / Total / Income / Cash & sweep */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <Stat
              label="Day's gain/loss"
              primary={
                data.day_gain_abs !== null && data.day_gain_pct !== null ? (
                  <PercentDelta
                    pct={data.day_gain_pct}
                    abs={data.day_gain_abs}
                    currency={currency}
                  />
                ) : (
                  <span className="delta-flat">—</span>
                )
              }
            />
            <Stat
              label="Total gain/loss"
              primary={
                <PercentDelta
                  pct={data.total_gain_pct}
                  abs={data.total_gain_abs}
                  currency={currency}
                />
              }
            />
            <Stat
              label="Estimated annual income"
              primary={
                data.estimated_annual_income !== null ? (
                  <span className="font-data" style={{ color: "var(--text-primary)" }}>
                    {formatCurrency(data.estimated_annual_income, currency, 2)}
                  </span>
                ) : (
                  <span className="delta-flat">—</span>
                )
              }
            />
            <Stat
              label="Cash & sweep funds"
              primary={
                data.cash_sweep !== null ? (
                  <span className="font-data" style={{ color: "var(--text-primary)" }}>
                    {formatCurrency(data.cash_sweep, currency, 2)}
                  </span>
                ) : (
                  <span className="delta-flat">—</span>
                )
              }
            />
          </div>

          {/* Chart */}
          <div style={{ marginTop: 8 }}>
            <AccountValueChart market={market} height={260} />
          </div>
        </section>

        {/* ── Right rail: Markets / Calendar / Watchlist ──────── */}
        <aside className="col-span-12 lg:col-span-4 space-y-5">
          <MarketsCard indices={data.indices} marketLabel={market === "br" ? "Brasil" : "EUA"} />
          <CalendarCard />
          <WatchlistCard items={data.watchlist} market={market} />
        </aside>
      </div>

      {/* ── Positions table (full width) ──────────────────────── */}
      <section className="mt-5 card p-5">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h2 className="type-h3">Top positions</h2>
            <p className="type-byline" style={{ marginTop: 2 }}>
              Top {Math.min(data.positions.length, 5)} of {data.positions.length} securities · ordered by value
            </p>
          </div>
          <Link
            href="/portfolio"
            className="text-[12px] flex items-center gap-1 hover:underline"
            style={{ color: "var(--accent-primary)", fontWeight: 500 }}
          >
            See all positions <ArrowRight size={12} />
          </Link>
        </div>

        <PositionsTable rows={data.positions.slice(0, 5)} currency={currency} />
      </section>

      {/* ── Asset allocation ──────────────────────────────────── */}
      <section className="mt-5 card p-5">
        <h2 className="type-h3 mb-4">Asset allocation</h2>
        <AssetAllocation rows={data.asset_classes} currency={currency} total={data.account_value} />
      </section>
    </div>
  );
}

// ── Sub-components ─────────────────────────────────────────────────

function Stat({ label, primary }: { label: string; primary: React.ReactNode }) {
  return (
    <div>
      <p className="type-caption" style={{ marginBottom: 4 }}>
        {label}
      </p>
      <div style={{ fontSize: 14, fontWeight: 500 }}>{primary}</div>
    </div>
  );
}

function MarketsCard({
  indices,
  marketLabel,
}: {
  indices: HomeIndex[];
  marketLabel: string;
}) {
  return (
    <div className="card p-4">
      <div className="flex items-center justify-between mb-1">
        <h2 className="type-h3">Markets · {marketLabel}</h2>
        <Link
          href="/research"
          className="text-[11px] flex items-center gap-1 hover:underline"
          style={{ color: "var(--accent-primary)", fontWeight: 500 }}
        >
          See market details <ArrowRight size={11} />
        </Link>
      </div>
      <p className="type-byline" style={{ marginBottom: 12 }}>
        {indices[0] && indices[0].value !== null
          ? `Last close · ${formatDate(new Date().toISOString().slice(0, 10), "short")}`
          : "sem dados"}
      </p>
      <div className="grid grid-cols-3 gap-3">
        {indices.map((idx) => (
          <div key={idx.symbol}>
            <p
              className="type-caption"
              style={{ color: "var(--text-secondary)", fontWeight: 600, marginBottom: 4 }}
            >
              {idx.label}
            </p>
            <p
              className="font-data"
              style={{ color: "var(--text-primary)", fontSize: 13, fontWeight: 600 }}
            >
              {idx.value !== null
                ? idx.value.toLocaleString("en-US", { maximumFractionDigits: 2 })
                : "—"}
            </p>
            <p style={{ fontSize: 11, marginTop: 2 }}>
              <PercentDelta
                pct={idx.delta_pct}
                abs={idx.delta_abs}
                currency={"USD"}
                inline
              />
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

function WatchlistCard({
  items,
  market,
}: {
  items: HomeWatchlistItem[];
  market: "br" | "us";
}) {
  return (
    <div className="card p-4">
      <div className="flex items-center justify-between mb-1">
        <h2 className="type-h3">Watchlist</h2>
        <Link
          href="/research"
          className="text-[11px] flex items-center gap-1 hover:underline"
          style={{ color: "var(--accent-primary)", fontWeight: 500 }}
        >
          See full watchlist <ArrowRight size={11} />
        </Link>
      </div>
      <p className="type-byline" style={{ marginBottom: 12 }}>
        {market === "br" ? "B3 · seguidos" : "NYSE/NASDAQ · seguidos"}
      </p>
      {items.length === 0 ? (
        <p className="type-caption" style={{ fontStyle: "italic" }}>
          Sem watchlist activa para este mercado.
        </p>
      ) : (
        <ul style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {items.slice(0, 5).map((it) => (
            <li
              key={it.ticker}
              className="flex items-center gap-3"
              style={{ minHeight: 32, cursor: "pointer" }}
              onClick={() => openTickerSheet(it.ticker)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  openTickerSheet(it.ticker);
                }
              }}
            >
              <TickerLogo ticker={it.ticker} size="sm" />
              <div style={{ flex: 1, minWidth: 0 }}>
                <p
                  className="font-data"
                  style={{ color: "var(--text-primary)", fontSize: 12, fontWeight: 600 }}
                >
                  {it.ticker}
                </p>
                <p
                  className="type-caption"
                  style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}
                >
                  {it.name}
                </p>
              </div>
              <div style={{ textAlign: "right" }}>
                <p
                  className="font-data"
                  style={{ color: "var(--text-primary)", fontSize: 12, fontWeight: 600 }}
                >
                  {it.last !== null
                    ? it.last.toLocaleString(market === "br" ? "pt-BR" : "en-US", {
                        maximumFractionDigits: 2,
                        minimumFractionDigits: 2,
                      })
                    : "—"}
                </p>
                <p style={{ fontSize: 10 }}>
                  <PercentDelta pct={it.pct_chg} inline />
                </p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function InsightsCard() {
  return (
    <div className="card p-4">
      <div className="flex items-center justify-between mb-1">
        <h2 className="type-h3">Investing insights</h2>
        <Link
          href="/research"
          className="text-[11px] flex items-center gap-1 hover:underline"
          style={{ color: "var(--accent-primary)", fontWeight: 500 }}
        >
          See more articles <ArrowRight size={11} />
        </Link>
      </div>
      <p className="type-byline" style={{ marginBottom: 12 }}>
        Da nossa pesquisa · vault + cliques
      </p>
      <Link
        href="/research"
        className="block"
        style={{
          background: "var(--bg-overlay)",
          borderRadius: "var(--radius)",
          padding: 12,
          textDecoration: "none",
        }}
      >
        <p
          className="font-display"
          style={{
            fontSize: 14,
            fontWeight: 600,
            color: "var(--text-primary)",
            lineHeight: 1.3,
            marginBottom: 4,
          }}
        >
          Como o regime macro actual afecta a tese DRIP
        </p>
        <p className="type-byline">Pesquisa interna · Aurora</p>
      </Link>
    </div>
  );
}

function PositionsTable({
  rows,
  currency,
}: {
  rows: HomePosition[];
  currency: "BRL" | "USD";
}) {
  if (rows.length === 0) {
    return (
      <p className="type-caption" style={{ fontStyle: "italic" }}>
        Sem posições neste mercado.
      </p>
    );
  }
  const totalValue = rows.reduce((s, r) => s + r.current_value, 0);
  return (
    <table className="data-table">
      <thead>
        <tr>
          <th>Security</th>
          <th>Description</th>
          <th className="num">Value</th>
          <th className="num">Total gain/loss</th>
          <th className="num">Weight</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((p) => {
          const weight = totalValue ? (p.current_value / totalValue) * 100 : 0;
          const totalAbs = p.current_value - p.cost_basis;
          return (
            <tr
              key={p.ticker}
              onClick={() => openTickerSheet(p.ticker)}
            >
              <td>
                <div className="flex items-center gap-3">
                  <TickerLogo ticker={p.ticker} size="sm" />
                  <span
                    className="font-data"
                    style={{ fontWeight: 600, color: "var(--text-primary)", fontSize: 13 }}
                  >
                    {p.ticker}
                  </span>
                </div>
              </td>
              <td style={{ color: "var(--text-secondary)", fontSize: 13 }}>
                {(p.name || "—").toUpperCase()}
              </td>
              <td className="num" style={{ color: "var(--text-primary)", fontWeight: 500 }}>
                {formatCurrency(p.current_value, currency, 2)}
              </td>
              <td className="num">
                <PercentDelta pct={p.pnl_pct} abs={totalAbs} currency={currency} />
              </td>
              <td className="num" style={{ color: "var(--text-primary)" }}>
                {weight.toFixed(2)}%
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

function AssetAllocation({
  rows,
  currency,
  total,
}: {
  rows: { name: string; allocation: number; value: number; color: string }[];
  currency: "BRL" | "USD";
  total: number;
}) {
  if (rows.length === 0) {
    return (
      <p className="type-caption" style={{ fontStyle: "italic" }}>
        Sem dados de alocação.
      </p>
    );
  }
  // Simple SVG donut — JPM-style
  const SIZE = 180;
  const CX = SIZE / 2;
  const STROKE = 28;
  const RADIUS = (SIZE - STROKE) / 2;
  const CIRC = 2 * Math.PI * RADIUS;
  let acc = 0;
  return (
    <div className="grid grid-cols-12 gap-6 items-center">
      <div className="col-span-12 md:col-span-3 flex flex-col items-center">
        <svg width={SIZE} height={SIZE} viewBox={`0 0 ${SIZE} ${SIZE}`}>
          <circle
            cx={CX}
            cy={CX}
            r={RADIUS}
            fill="none"
            stroke="var(--bg-overlay)"
            strokeWidth={STROKE}
          />
          {rows.map((r) => {
            const dash = (r.allocation / 100) * CIRC;
            const dashArray = `${dash} ${CIRC - dash}`;
            const offset = -acc;
            acc += dash;
            return (
              <circle
                key={r.name}
                cx={CX}
                cy={CX}
                r={RADIUS}
                fill="none"
                stroke={r.color}
                strokeWidth={STROKE}
                strokeDasharray={dashArray}
                strokeDashoffset={offset}
                transform={`rotate(-90 ${CX} ${CX})`}
              />
            );
          })}
          <text
            x={CX}
            y={CX - 6}
            textAnchor="middle"
            style={{ fontSize: 10, fill: "var(--text-tertiary)", fontFamily: "var(--font-sans)" }}
          >
            Total
          </text>
          <text
            x={CX}
            y={CX + 14}
            textAnchor="middle"
            style={{
              fontSize: 14,
              fontWeight: 600,
              fill: "var(--text-primary)",
              fontFamily: "var(--font-mono)",
            }}
          >
            {formatCurrency(total, currency, 0)}
          </text>
        </svg>
      </div>
      <div className="col-span-12 md:col-span-9">
        <table className="data-table">
          <thead>
            <tr>
              <th>Asset class</th>
              <th className="num">Allocation</th>
              <th className="num">Value</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.name} style={{ cursor: "default" }}>
                <td>
                  <span
                    style={{
                      display: "inline-block",
                      width: 8,
                      height: 8,
                      borderRadius: 999,
                      background: r.color,
                      marginRight: 10,
                    }}
                    aria-hidden
                  />
                  <span style={{ color: "var(--accent-primary)", fontWeight: 500 }}>
                    {r.name}
                  </span>
                </td>
                <td className="num">{r.allocation.toFixed(2)}%</td>
                <td className="num">{formatCurrency(r.value, currency, 2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
