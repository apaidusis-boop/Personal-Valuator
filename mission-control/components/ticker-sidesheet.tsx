"use client";

// JPM-style ticker side-sheet drawer.
// - Slides in from the right when openTickerSheet(ticker) is called.
// - Listens for the custom event AND for URL hash changes (#sheet=TKR).
// - ESC key, click overlay, or close button dismisses.
// - Click "Open full ticker page" → navigates to /ticker/[ticker].
//
// Renders header price + period chart + Statistics / Fundamentals /
// Ownership tabs + Council strip + recent filings + analyst highlights.

import { useEffect, useRef, useState, useMemo } from "react";
import Link from "next/link";
import { X, Bell, ExternalLink, ArrowRight, Plus } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

import {
  TICKER_SHEET_EVENT,
  closeTickerSheet,
  readTickerFromHash,
} from "@/lib/ticker-sheet";
import { TickerLogo, PercentDelta } from "./jpm-atoms";
import { formatCurrency, formatDate, formatPercent } from "@/lib/format";

// ─── Types ────────────────────────────────────────────────────────────

type Snap = {
  ticker: string;
  market: "br" | "us";
  name: string | null;
  sector: string | null;
  is_holding: boolean;
  price: number | null;
  price_date: string | null;
  prev_close: number | null;
  day_change_abs: number | null;
  day_change_pct: number | null;
  position: {
    quantity: number;
    entry_price: number;
    entry_date: string;
    cost: number;
    market_value: number | null;
    pnl_abs: number | null;
    pnl_pct: number | null;
    yoc_pct: number | null;
  } | null;
  fundamentals: {
    pe: number | null;
    pb: number | null;
    dy: number | null;
    roe: number | null;
    eps: number | null;
    bvps: number | null;
    market_cap: number | null;
    period_end: string | null;
  } | null;
  forward_dividend_amount: number | null;
  next_ex_date: string | null;
  council: {
    stance: string;
    confidence: number | null;
    date: string;
    dissent_count: number;
    flag_count: number;
  } | null;
  strategies: { engine: string; verdict: string; score: number; run_date: string }[];
  events: { date: string; kind: string; summary: string | null; url: string | null }[];
  divs_12m: number | null;
  fair_value: { method: string; fair_price: number; upside_pct: number; computed_at: string } | null;
};

type PriceRow = { date: string; close: number };

const PERIODS = [
  { key: "1M", days: 30, label: "1M" },
  { key: "3M", days: 90, label: "3M" },
  { key: "6M", days: 180, label: "6M" },
  { key: "1Y", days: 365, label: "1Y" },
  { key: "3Y", days: 365 * 3, label: "3Y" },
  { key: "5Y", days: 365 * 5, label: "5Y" },
  { key: "MAX", days: 365 * 20, label: "Max" },
] as const;

type PeriodKey = typeof PERIODS[number]["key"];

// ─── Component ────────────────────────────────────────────────────────

export default function TickerSideSheet() {
  const [ticker, setTicker] = useState<string | null>(null);
  const [snap, setSnap] = useState<Snap | null>(null);
  const [series, setSeries] = useState<PriceRow[]>([]);
  const [period, setPeriod] = useState<PeriodKey>("1Y");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [tab, setTab] = useState<"statistics" | "fundamentals" | "ownership">(
    "statistics"
  );
  const sheetRef = useRef<HTMLElement | null>(null);

  // ── Listen for opens (event + initial hash) ────────────────────────
  useEffect(() => {
    const fromHash = readTickerFromHash();
    if (fromHash) setTicker(fromHash);

    function onEvent(e: Event) {
      const detail = (e as CustomEvent).detail;
      setTicker(detail?.ticker ?? null);
    }
    function onHashChange() {
      setTicker(readTickerFromHash());
    }
    window.addEventListener(TICKER_SHEET_EVENT, onEvent);
    window.addEventListener("hashchange", onHashChange);
    return () => {
      window.removeEventListener(TICKER_SHEET_EVENT, onEvent);
      window.removeEventListener("hashchange", onHashChange);
    };
  }, []);

  // ── Lock body scroll when open ─────────────────────────────────────
  useEffect(() => {
    if (!ticker) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = prev; };
  }, [ticker]);

  // ── ESC key closes ─────────────────────────────────────────────────
  useEffect(() => {
    if (!ticker) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") closeTickerSheet();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [ticker]);

  // ── Fetch snapshot whenever ticker changes ─────────────────────────
  useEffect(() => {
    if (!ticker) {
      setSnap(null);
      setSeries([]);
      setErr(null);
      return;
    }
    let alive = true;
    setLoading(true);
    setErr(null);
    setTab("statistics");

    Promise.all([
      fetch(`/api/ticker/${ticker}`).then((r) => r.json()),
      fetch(`/api/prices/${ticker}?days=${365 * 20}`).then((r) => r.json()),
    ])
      .then(([snapJson, pricesJson]) => {
        if (!alive) return;
        if (snapJson.error) {
          setErr(snapJson.error);
          setSnap(null);
        } else {
          setSnap(snapJson);
        }
        if (Array.isArray(pricesJson?.series)) setSeries(pricesJson.series);
      })
      .catch((e) => alive && setErr(String(e)))
      .finally(() => alive && setLoading(false));

    return () => { alive = false; };
  }, [ticker]);

  // ── Period slice for chart ─────────────────────────────────────────
  const sliced = useMemo(() => {
    if (series.length === 0) return [];
    const conf = PERIODS.find((p) => p.key === period)!;
    const cutoff = new Date(Date.now() - conf.days * 86400000)
      .toISOString()
      .slice(0, 10);
    return series.filter((r) => r.date >= cutoff);
  }, [series, period]);

  if (!ticker) return null;

  const cur = snap?.market === "br" ? "BRL" : "USD";

  return (
    <>
      <div
        className="sidesheet-overlay"
        onClick={() => closeTickerSheet()}
        aria-hidden
      />
      <aside
        ref={sheetRef}
        className="sidesheet"
        role="dialog"
        aria-label={`Detalhes de ${ticker}`}
        aria-modal="true"
      >
        {/* ── Sticky header with close + actions ────────────────── */}
        <header
          className="sticky top-0 z-10 px-6 py-4"
          style={{
            background: "var(--bg-elevated)",
            borderBottom: "1px solid var(--border-subtle)",
          }}
        >
          <div className="flex items-center gap-3 mb-3">
            <button
              type="button"
              onClick={() => closeTickerSheet()}
              aria-label="Fechar"
              className="p-1.5 rounded-md transition-colors"
              style={{ color: "var(--text-tertiary)" }}
            >
              <X size={18} />
            </button>
            <Link
              href={ticker ? `/ticker/${ticker}` : "/"}
              className="text-[12px] flex items-center gap-1 hover:underline ml-auto"
              style={{ color: "var(--accent-primary)", fontWeight: 500 }}
              onClick={() => closeTickerSheet()}
            >
              Open full page <ArrowRight size={12} />
            </Link>
          </div>

          {snap ? (
            <div className="flex items-start justify-between gap-3 flex-wrap">
              <div className="flex items-center gap-3">
                <TickerLogo ticker={snap.ticker} />
                <div>
                  <h2
                    className="font-display"
                    style={{ fontSize: 22, fontWeight: 600, lineHeight: 1.15 }}
                  >
                    {snap.ticker}
                  </h2>
                  <p
                    className="type-byline"
                    style={{ marginTop: 2, color: "var(--text-tertiary)" }}
                  >
                    {(snap.name || "—")}
                    {snap.sector ? ` · ${snap.sector}` : ""}
                    {" · "}
                    <span style={{ color: snap.market === "br" ? "var(--mkt-br)" : "var(--mkt-us)" }}>
                      {snap.market.toUpperCase()}
                    </span>
                    {snap.is_holding && (
                      <span style={{ color: "var(--accent-primary)", marginLeft: 8 }}>· HOLDING</span>
                    )}
                  </p>
                </div>
              </div>
              {snap.price !== null && (
                <div className="text-right">
                  <div
                    className="font-data tabular"
                    style={{ fontSize: 26, fontWeight: 600, color: "var(--text-primary)", lineHeight: 1.1 }}
                  >
                    {formatCurrency(snap.price, cur as any, 2)}
                  </div>
                  {snap.day_change_pct !== null && (
                    <div style={{ marginTop: 4, fontSize: 12 }}>
                      <PercentDelta
                        pct={snap.day_change_pct}
                        abs={snap.day_change_abs}
                        currency={cur as any}
                        withTriangle
                      />
                    </div>
                  )}
                  {snap.price_date && (
                    <p className="type-byline" style={{ marginTop: 2, color: "var(--text-tertiary)" }}>
                      cotação {formatDate(snap.price_date, "relative")}
                    </p>
                  )}
                </div>
              )}
            </div>
          ) : loading ? (
            <p className="type-body-sm" style={{ color: "var(--text-tertiary)" }}>
              loading {ticker}…
            </p>
          ) : err ? (
            <p className="type-body-sm" style={{ color: "var(--verdict-avoid)" }}>{err}</p>
          ) : null}

          {/* ── Action row ──────────────────────────────────────── */}
          {snap && (
            <div className="flex items-center gap-2 mt-3 flex-wrap">
              <button
                type="button"
                className="flex items-center gap-1.5 text-[12px] font-medium px-3 py-1.5 rounded-md transition-colors"
                style={{
                  background: "var(--accent-primary)",
                  color: "white",
                  border: 0,
                }}
                onClick={() => suggestAlert(snap)}
              >
                <Bell size={13} /> Set price alert
              </button>
              <Link
                href={`/council/${snap.ticker}`}
                className="flex items-center gap-1.5 text-[12px] font-medium px-3 py-1.5 rounded-md transition-colors"
                style={{
                  background: "var(--bg-overlay)",
                  color: "var(--text-secondary)",
                  border: "1px solid var(--border-subtle)",
                }}
                onClick={() => closeTickerSheet()}
              >
                ⚖ Council
              </Link>
              {!snap.is_holding && (
                <button
                  type="button"
                  className="flex items-center gap-1.5 text-[12px] font-medium px-3 py-1.5 rounded-md transition-colors"
                  style={{
                    background: "var(--bg-overlay)",
                    color: "var(--text-secondary)",
                    border: "1px solid var(--border-subtle)",
                  }}
                  onClick={() => alert("TODO: add to watchlist via /api/actions")}
                >
                  <Plus size={13} /> Add to watchlist
                </button>
              )}
            </div>
          )}
        </header>

        {/* ── Body ──────────────────────────────────────────────── */}
        {!snap && !loading && !err && (
          <div className="px-6 py-12 text-center">
            <p className="type-body-sm" style={{ color: "var(--text-tertiary)" }}>
              Sem dados.
            </p>
          </div>
        )}

        {snap && (
          <div className="px-6 py-5 space-y-5">
            {/* ── Council strip (highlighted) ─────────────────── */}
            {snap.council && (
              <Link
                href={`/council/${snap.ticker}`}
                onClick={() => closeTickerSheet()}
                className="block card p-4"
                style={{ borderTop: "2px solid var(--accent-primary)" }}
              >
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <div className="flex items-center gap-2">
                    <span className="type-h3">⚖ Council</span>
                    <span
                      className="pill pill-solid"
                      style={{
                        background: stanceBg(snap.council.stance),
                        color: stanceFg(snap.council.stance),
                      }}
                    >
                      {snap.council.stance}
                    </span>
                    {snap.council.confidence !== null && (
                      <span className="type-byline">conf {Math.round(snap.council.confidence * 100)}</span>
                    )}
                    <span className="type-byline">{formatDate(snap.council.date, "relative")}</span>
                    {snap.council.dissent_count > 0 && (
                      <span className="pill pill-hold">{snap.council.dissent_count} dissent</span>
                    )}
                    {snap.council.flag_count > 0 && (
                      <span className="pill pill-avoid">⚑ {snap.council.flag_count}</span>
                    )}
                  </div>
                  <span style={{ fontSize: 12, color: "var(--accent-primary)", fontWeight: 500 }}>
                    open dossier →
                  </span>
                </div>
              </Link>
            )}

            {/* ── Period chips + chart ────────────────────────── */}
            <section className="card p-5">
              <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
                <h3 className="type-h3">Price history</h3>
                <div className="period-chips" role="tablist">
                  {PERIODS.map((p) => (
                    <button
                      key={p.key}
                      type="button"
                      data-active={period === p.key}
                      onClick={() => setPeriod(p.key)}
                    >
                      {p.label}
                    </button>
                  ))}
                </div>
              </div>
              <SheetChart series={sliced} market={snap.market} />
            </section>

            {/* ── Tabs: Statistics / Fundamentals / Ownership ── */}
            <section className="card p-5">
              <div className="flex border-b" style={{ borderColor: "var(--border-subtle)" }}>
                {(["statistics", "fundamentals", "ownership"] as const).map((t) => (
                  <button
                    key={t}
                    type="button"
                    onClick={() => setTab(t)}
                    className="px-4 py-2 text-[13px] font-medium transition-colors capitalize"
                    style={{
                      color: tab === t ? "var(--text-primary)" : "var(--text-tertiary)",
                      borderBottom: tab === t ? "2px solid var(--accent-primary)" : "2px solid transparent",
                      background: "transparent",
                      marginBottom: "-1px",
                    }}
                  >
                    {t}
                  </button>
                ))}
              </div>
              <div className="pt-4">
                {tab === "statistics" && <StatisticsTab snap={snap} cur={cur as "BRL" | "USD"} />}
                {tab === "fundamentals" && <FundamentalsTab snap={snap} cur={cur as "BRL" | "USD"} />}
                {tab === "ownership" && <OwnershipTab snap={snap} cur={cur as "BRL" | "USD"} />}
              </div>
            </section>

            {/* ── Strategy verdicts ribbon ────────────────────── */}
            {snap.strategies.length > 0 && (
              <section className="card p-5">
                <h3 className="type-h3 mb-3">Strategy engines</h3>
                <div className="flex flex-wrap gap-2">
                  {snap.strategies.map((s) => (
                    <span
                      key={s.engine}
                      className="flex items-center gap-2 text-[12px] font-data px-3 py-1.5 rounded-md"
                      style={{
                        background: "var(--bg-overlay)",
                        border: "1px solid var(--border-subtle)",
                      }}
                    >
                      <span style={{ color: "var(--text-tertiary)", textTransform: "capitalize" }}>
                        {s.engine}
                      </span>
                      <span style={{ color: "var(--text-primary)", fontWeight: 600 }}>
                        {(s.score * 100).toFixed(0)}
                      </span>
                      <span
                        className="pill pill-solid"
                        style={{
                          background: stanceBg(s.verdict),
                          color: stanceFg(s.verdict),
                        }}
                      >
                        {s.verdict}
                      </span>
                    </span>
                  ))}
                </div>
              </section>
            )}

            {/* ── Recent filings ──────────────────────────────── */}
            {snap.events.length > 0 && (
              <section className="card p-5">
                <h3 className="type-h3 mb-3">Recent filings</h3>
                <ul className="space-y-3">
                  {snap.events.map((ev, i) => (
                    <li
                      key={i}
                      className="flex items-start gap-3 pb-3"
                      style={{
                        borderBottom: i === snap.events.length - 1
                          ? "0"
                          : "1px solid var(--border-subtle)",
                      }}
                    >
                      <span
                        className="font-data tabular"
                        style={{
                          color: "var(--text-tertiary)",
                          fontSize: 12,
                          minWidth: 70,
                          paddingTop: 2,
                        }}
                      >
                        {formatDate(ev.date, "short")}
                      </span>
                      <span
                        className="pill"
                        style={{
                          color: "var(--text-secondary)",
                          padding: "2px 8px",
                          fontSize: 10,
                          flexShrink: 0,
                          marginTop: 1,
                        }}
                      >
                        {ev.kind}
                      </span>
                      <p
                        className="type-body-sm"
                        style={{
                          flex: 1,
                          color: "var(--text-secondary)",
                          margin: 0,
                          lineHeight: 1.5,
                        }}
                      >
                        {ev.summary || "—"}
                        {ev.url && (
                          <a
                            href={ev.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="ml-2 inline-flex items-center gap-1 hover:underline"
                            style={{ color: "var(--accent-primary)", fontSize: 11 }}
                          >
                            <ExternalLink size={11} />
                          </a>
                        )}
                      </p>
                    </li>
                  ))}
                </ul>
              </section>
            )}

            <div style={{ height: 24 }} aria-hidden />
          </div>
        )}
      </aside>
    </>
  );
}

// ─── Sub-components ───────────────────────────────────────────────────

function SheetChart({
  series,
  market,
}: {
  series: PriceRow[];
  market: "br" | "us";
}) {
  if (series.length === 0) {
    return (
      <div
        className="grid place-items-center text-xs"
        style={{ height: 220, color: "var(--text-tertiary)" }}
      >
        sem dados de preço
      </div>
    );
  }
  const accent = market === "br" ? "var(--mkt-br)" : "var(--mkt-us)";
  const first = series[0]?.close ?? 0;
  const last = series[series.length - 1]?.close ?? 0;
  const pct = first ? ((last / first - 1) * 100) : 0;
  const positive = pct >= 0;
  const color = positive ? "var(--gain)" : "var(--loss)";

  return (
    <div>
      <p className="type-byline" style={{ marginBottom: 8, color: "var(--text-tertiary)" }}>
        period change · <span style={{ color }}>{pct >= 0 ? "+" : ""}{pct.toFixed(2)}%</span>
      </p>
      <div style={{ width: "100%", height: 220 }}>
        <ResponsiveContainer>
          <LineChart data={series} margin={{ top: 4, right: 8, left: 0, bottom: 4 }}>
            <XAxis
              dataKey="date"
              tick={{ fontSize: 10, fill: "var(--text-tertiary)" }}
              axisLine={{ stroke: "var(--border-subtle)" }}
              tickLine={false}
              minTickGap={48}
            />
            <YAxis
              domain={["auto", "auto"]}
              tick={{ fontSize: 10, fill: "var(--text-tertiary)" }}
              axisLine={false}
              tickLine={false}
              width={50}
              tickFormatter={(v) =>
                v.toLocaleString("en-US", { maximumFractionDigits: 2 })
              }
            />
            <Tooltip
              contentStyle={{
                background: "var(--bg-elevated)",
                border: "1px solid var(--border-subtle)",
                borderRadius: 6,
                fontSize: 11,
              }}
              labelStyle={{ color: "var(--text-tertiary)" }}
              itemStyle={{ color: "var(--text-primary)" }}
              formatter={(v: any) =>
                Number(v).toLocaleString(market === "br" ? "pt-BR" : "en-US", {
                  maximumFractionDigits: 2,
                  minimumFractionDigits: 2,
                })
              }
            />
            <ReferenceLine y={first} stroke="var(--border-subtle)" strokeDasharray="3 3" />
            <Line
              type="monotone"
              dataKey="close"
              stroke={accent}
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function StatisticsTab({ snap, cur }: { snap: Snap; cur: "BRL" | "USD" }) {
  const items: { label: string; value: React.ReactNode }[] = [
    {
      label: "Previous close",
      value: snap.prev_close !== null ? formatCurrency(snap.prev_close, cur, 2) : "—",
    },
    {
      label: "Day's range",
      value: snap.price !== null && snap.prev_close !== null
        ? `${formatCurrency(Math.min(snap.price, snap.prev_close), cur, 2)} – ${formatCurrency(Math.max(snap.price, snap.prev_close), cur, 2)}`
        : "—",
    },
    {
      label: "Forward dividend",
      value: snap.forward_dividend_amount !== null
        ? `${formatCurrency(snap.forward_dividend_amount, cur, 2)}${snap.next_ex_date ? ` · ex ${formatDate(snap.next_ex_date, "short")}` : ""}`
        : "—",
    },
    {
      label: "Trailing 12m dividends",
      value: snap.divs_12m !== null && snap.divs_12m > 0
        ? formatCurrency(snap.divs_12m, cur, 2)
        : "—",
    },
    {
      label: "Market cap",
      value: snap.fundamentals?.market_cap
        ? compactCurrency(snap.fundamentals.market_cap, cur)
        : "—",
    },
    {
      label: "Sector",
      value: snap.sector || "—",
    },
  ];
  return (
    <dl className="grid grid-cols-2 gap-x-6 gap-y-3">
      {items.map((it) => (
        <div key={it.label}>
          <dt className="type-caption" style={{ marginBottom: 2 }}>{it.label}</dt>
          <dd
            className="font-data tabular"
            style={{ color: "var(--text-primary)", fontSize: 13, fontWeight: 500 }}
          >
            {it.value}
          </dd>
        </div>
      ))}
      {snap.fair_value && (
        <div className="col-span-2 mt-2 pt-3" style={{ borderTop: "1px solid var(--border-subtle)" }}>
          <dt className="type-caption" style={{ marginBottom: 4 }}>
            Fair value · {snap.fair_value.method}
          </dt>
          <dd className="flex items-baseline gap-3 flex-wrap">
            <span
              className="font-data tabular"
              style={{ color: "var(--text-primary)", fontSize: 16, fontWeight: 600 }}
            >
              {formatCurrency(snap.fair_value.fair_price, cur, 2)}
            </span>
            <span
              className="font-data"
              style={{
                color: snap.fair_value.upside_pct >= 0 ? "var(--gain)" : "var(--loss)",
                fontSize: 13,
                fontWeight: 500,
              }}
            >
              {snap.fair_value.upside_pct >= 0 ? "+" : ""}
              {snap.fair_value.upside_pct.toFixed(1)}% upside
            </span>
            <span className="type-byline" style={{ color: "var(--text-tertiary)" }}>
              {formatDate(snap.fair_value.computed_at, "relative")}
            </span>
          </dd>
        </div>
      )}
    </dl>
  );
}

function FundamentalsTab({ snap, cur }: { snap: Snap; cur: "BRL" | "USD" }) {
  if (!snap.fundamentals) {
    return (
      <p className="type-body-sm italic" style={{ color: "var(--text-tertiary)" }}>
        Sem dados de fundamentals.
      </p>
    );
  }
  const f = snap.fundamentals;
  const items: { label: string; value: React.ReactNode }[] = [
    { label: "P/E", value: numFmt(f.pe) },
    { label: "P/B", value: numFmt(f.pb) },
    { label: "Dividend yield", value: f.dy !== null ? `${(f.dy * 100).toFixed(2)}%` : "—" },
    { label: "ROE", value: f.roe !== null ? `${(f.roe * 100).toFixed(2)}%` : "—" },
    { label: "EPS", value: f.eps !== null ? formatCurrency(f.eps, cur, 2) : "—" },
    { label: "BVPS", value: f.bvps !== null ? formatCurrency(f.bvps, cur, 2) : "—" },
  ];
  return (
    <>
      <dl className="grid grid-cols-2 gap-x-6 gap-y-3">
        {items.map((it) => (
          <div key={it.label}>
            <dt className="type-caption" style={{ marginBottom: 2 }}>{it.label}</dt>
            <dd
              className="font-data tabular"
              style={{ color: "var(--text-primary)", fontSize: 13, fontWeight: 500 }}
            >
              {it.value}
            </dd>
          </div>
        ))}
      </dl>
      <p
        className="type-byline mt-4"
        style={{ color: "var(--text-tertiary)" }}
      >
        period {f.period_end || "—"}
      </p>
    </>
  );
}

function OwnershipTab({ snap, cur }: { snap: Snap; cur: "BRL" | "USD" }) {
  if (!snap.position) {
    return (
      <div className="space-y-3">
        <p className="type-body-sm italic" style={{ color: "var(--text-tertiary)" }}>
          Não tens posição activa em {snap.ticker}.
        </p>
        {!snap.is_holding && (
          <p className="type-byline" style={{ color: "var(--text-tertiary)" }}>
            Em watchlist? Adiciona com o botão "Add to watchlist" acima.
          </p>
        )}
      </div>
    );
  }
  const p = snap.position;
  const items: { label: string; value: React.ReactNode; tone?: "gain" | "loss" }[] = [
    { label: "Shares held", value: p.quantity.toLocaleString() },
    { label: "Average cost", value: formatCurrency(p.entry_price, cur, 2) },
    { label: "Cost basis", value: formatCurrency(p.cost, cur, 2) },
    { label: "Market value", value: p.market_value !== null ? formatCurrency(p.market_value, cur, 2) : "—" },
    {
      label: "Total gain/loss",
      value: p.pnl_abs !== null && p.pnl_pct !== null
        ? `${formatCurrency(p.pnl_abs, cur, 2)} (${formatPercent(p.pnl_pct, 1, { signed: true })})`
        : "—",
      tone: (p.pnl_abs ?? 0) >= 0 ? "gain" : "loss",
    },
    {
      label: "Yield on cost",
      value: p.yoc_pct !== null ? formatPercent(p.yoc_pct, 2) : "—",
    },
    {
      label: "Acquired",
      value: formatDate(p.entry_date, "medium"),
    },
  ];
  return (
    <dl className="grid grid-cols-2 gap-x-6 gap-y-3">
      {items.map((it) => (
        <div key={it.label}>
          <dt className="type-caption" style={{ marginBottom: 2 }}>{it.label}</dt>
          <dd
            className="font-data tabular"
            style={{
              fontSize: 13,
              fontWeight: 500,
              color: it.tone === "gain"
                ? "var(--gain)"
                : it.tone === "loss"
                ? "var(--loss)"
                : "var(--text-primary)",
            }}
          >
            {it.value}
          </dd>
        </div>
      ))}
    </dl>
  );
}

// ─── Helpers ──────────────────────────────────────────────────────────

function numFmt(n: number | null | undefined): string {
  if (n === null || n === undefined) return "—";
  if (Math.abs(n) < 1) return n.toFixed(3);
  return n.toFixed(2);
}

function compactCurrency(n: number, cur: "BRL" | "USD"): string {
  const sym = cur === "BRL" ? "R$" : "$";
  const abs = Math.abs(n);
  if (abs >= 1e12) return `${sym}${(n / 1e12).toFixed(2)}T`;
  if (abs >= 1e9) return `${sym}${(n / 1e9).toFixed(2)}B`;
  if (abs >= 1e6) return `${sym}${(n / 1e6).toFixed(2)}M`;
  if (abs >= 1e3) return `${sym}${(n / 1e3).toFixed(2)}k`;
  return formatCurrency(n, cur, 0);
}

function stanceBg(stance: string): string {
  const s = stance.toUpperCase();
  if (s.includes("BUY") || s === "ACCUMULATE") return "var(--jpm-gain-soft)";
  if (s.includes("SELL") || s === "AVOID" || s === "REDUCE") return "var(--jpm-loss-soft)";
  if (s === "HOLD" || s === "NEUTRAL") return "var(--jpm-amber-soft)";
  return "var(--bg-overlay)";
}

function stanceFg(stance: string): string {
  const s = stance.toUpperCase();
  if (s.includes("BUY") || s === "ACCUMULATE") return "var(--verdict-buy)";
  if (s.includes("SELL") || s === "AVOID" || s === "REDUCE") return "var(--verdict-avoid)";
  if (s === "HOLD" || s === "NEUTRAL") return "var(--verdict-hold)";
  return "var(--text-tertiary)";
}

function suggestAlert(snap: Snap) {
  // Lightweight prompt-based flow until /alerts route ships.
  if (snap.price === null) return;
  const direction = window.prompt(
    `Set alert for ${snap.ticker} — type "below X" or "above X"\nCurrent: ${snap.price.toFixed(2)}`,
    `below ${(snap.price * 0.95).toFixed(2)}`
  );
  if (!direction) return;
  const m = direction.match(/^(above|below)\s+([\d.]+)/i);
  if (!m) {
    alert("Formato inválido. Usa: \"below 100\" ou \"above 120\".");
    return;
  }
  fetch(`/api/alerts`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      ticker: snap.ticker,
      market: snap.market,
      kind: "price",
      direction: m[1].toLowerCase(),
      threshold: parseFloat(m[2]),
      current_price: snap.price,
      source: "manual",
    }),
  })
    .then((r) => r.json())
    .then((j) => {
      if (j?.error) alert(`Falhou: ${j.error}`);
      else alert(`Alerta gravado para ${snap.ticker}: ${m[1]} ${m[2]}`);
    })
    .catch((e) => alert(`Erro: ${e}`));
}
