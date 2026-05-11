// ── Home page real-data layer ────────────────────────────────────────
//
// Phase MM Layer 1 wires (W1–W8). Each function here replaces a piece
// of `home-mock.ts` with a real DB/vault query. Anything that cannot
// be resolved (table missing, no rows) returns null and the caller
// falls back to the mock.
//
// Convention: pure read-only queries, fast (<50ms), no LLM calls. The
// mock layer is allowed to keep deterministic placeholders for things
// that genuinely need offline derivation (review prose templates).

import type { HomeMarketSnapshot } from "@/lib/db";
import {
  listRecentEvents,
  upcomingDividends,
  pastDividends,
  batchFundamentals,
  listFairValue,
  type FilingEvent,
} from "@/lib/db";
import type { LeadHeadline, LeadDividendDay } from "@/components/home/lead";
import type { DividendsTabDay } from "@/components/home/workbench/dividends-tab";
import type { CompareTickerFundamentals } from "@/components/home/workbench/compare-tab";

// ── W1 · Real headline + spotlight ──────────────────────────────────
//
// Story-of-the-day picker. Heuristic: severity × is_holding × recency.
// Severity is keyed off filing kind:
//   8-K, fato_relevante, dividend     → 3 (material)
//   10-K, ITR, 20-F                   → 2 (periodic)
//   anything else                     → 1
//
// Returns null when nothing material crossed the desk in the last 48h
// — caller uses the "Quiet tape" fallback.

export type RealHeadline = {
  headline: LeadHeadline;
  spotlight: { ticker: string; market: "br" | "us" };
};

const MATERIAL_KINDS = new Set([
  "8-K", "8-k",
  "fato_relevante", "fato relevante",
  "dividend", "dividend_declaration",
]);
const PERIODIC_KINDS = new Set([
  "10-K", "10-k", "10-Q", "10-q",
  "ITR", "DFP",
  "20-F", "20-f",
]);

function severity(kind: string): number {
  const k = kind.toLowerCase();
  if (MATERIAL_KINDS.has(k)) return 3;
  if (PERIODIC_KINDS.has(k)) return 2;
  return 1;
}

function ageHours(iso: string): number {
  const t = Date.parse(iso);
  if (!isFinite(t)) return Infinity;
  return (Date.now() - t) / 3600_000;
}

export function getRealHeadline(
  br: HomeMarketSnapshot,
  us: HomeMarketSnapshot,
): RealHeadline | null {
  const holdingTickers = new Set([
    ...br.positions.map((p) => p.ticker),
    ...us.positions.map((p) => p.ticker),
  ]);
  if (holdingTickers.size === 0) return null;

  // Pull a wider event window so we can rank.
  const events = listRecentEvents(60);
  const ranked = events
    .map((e) => ({
      e,
      score:
        severity(e.kind) *
        (holdingTickers.has(e.ticker) ? 3 : 1) *
        Math.max(0.1, 1 - Math.min(1, ageHours(e.event_date) / 72)),
    }))
    .filter((x) => x.score > 0.5 && holdingTickers.has(x.e.ticker))
    .sort((a, b) => b.score - a.score);

  const top = ranked[0];
  if (!top) return null;
  // Only use as headline if event is < 48h old (otherwise stale)
  if (ageHours(top.e.event_date) > 48) return null;

  return { headline: buildHeadlineFromEvent(top.e), spotlight: { ticker: top.e.ticker, market: top.e.market } };
}

function buildHeadlineFromEvent(e: FilingEvent): LeadHeadline {
  const kicker = kickerFor(e);
  const summary = e.summary?.trim();
  // Hero title — short, declarative. If summary is long, take first sentence.
  const title = titleFor(e, summary);
  const dek = dekFor(e, summary);
  return {
    kicker,
    title,
    dek,
    ticker: e.ticker,
    market: e.market,
    href: e.url || `/ticker/${e.ticker}`,
  };
}

function kickerFor(e: FilingEvent): string {
  const kindLabel = e.kind.toUpperCase().replace(/_/g, " ");
  const sourceLabel = e.source.toUpperCase();
  return `Filings · ${sourceLabel} · ${kindLabel}`;
}

function titleFor(e: FilingEvent, summary?: string): string {
  if (summary && summary.length > 0) {
    // First sentence, cap at ~12 words / 90 chars
    const firstSentence = summary.split(/(?<=[.!?])\s+/)[0] || summary;
    if (firstSentence.length <= 110) return `${e.ticker}: ${firstSentence}`;
    const words = firstSentence.split(/\s+/).slice(0, 14).join(" ");
    return `${e.ticker}: ${words}…`;
  }
  // Fallback by kind
  const k = e.kind.toLowerCase();
  if (k.includes("8-k") || k.includes("fato")) return `${e.ticker} files a material disclosure.`;
  if (k.includes("10-k") || k.includes("dfp")) return `${e.ticker} closes the year — annual report on file.`;
  if (k.includes("10-q") || k.includes("itr")) return `${e.ticker} prints a quarter — interim numbers in.`;
  if (k.includes("dividend")) return `${e.ticker} declares a dividend.`;
  return `${e.ticker} updates the record on a ${e.kind} filing.`;
}

function dekFor(e: FilingEvent, summary?: string): string {
  const dateLabel = formatDateShort(e.event_date);
  if (summary && summary.length > 110) {
    const rest = summary.split(/(?<=[.!?])\s+/).slice(1, 3).join(" ");
    if (rest && rest.length > 0) {
      return `${dateLabel}. ${rest.length > 280 ? rest.slice(0, 277) + "…" : rest}`;
    }
  }
  return `Disclosure de ${dateLabel}. Workbench pré-carregado com ${e.ticker}; Deep Review abaixo cobre o contexto, peers e o que o council disse.`;
}

function formatDateShort(iso: string): string {
  // Best-effort dd/mm/yyyy in pt-BR-ish
  const t = Date.parse(iso);
  if (!isFinite(t)) return iso;
  const d = new Date(t);
  return `${String(d.getDate()).padStart(2, "0")}/${String(d.getMonth() + 1).padStart(2, "0")}/${d.getFullYear()}`;
}

// ── W5 · DRIP assumptions from real data ────────────────────────────
//
// For each holding ticker:
//   - start_price ← last close
//   - start_dy_pct ← last reported DY (or computed from div_12m / price)
//   - growth scenarios (low/mid/high) ← dividend CAGR over 1Y / 3Y / 5Y
//
// CAGR uses sum of dividends per ticker per calendar year. If a window
// is missing data, the scenario falls back to a market-typical default
// (3 / 6 / 9 %).

import type { DripCalcTabProps } from "@/components/home/workbench/drip-calc-tab";

const DEFAULT_GROWTH = { low: 3, mid: 6, high: 9 };

export function getDripAssumptions(
  br_tickers: string[],
  us_tickers: string[],
): DripCalcTabProps["ticker_assumptions"] {
  const all = [...br_tickers, ...us_tickers];
  if (all.length === 0) return {};

  const fundis = batchFundamentals(all);
  const sixYrAgoIso = new Date(Date.now() - 6 * 365 * 86400000).toISOString().slice(0, 10);
  const todayIso = new Date().toISOString().slice(0, 10);
  const allDivs = pastDividends(sixYrAgoIso, todayIso);

  // Group dividends by ticker → year → sum
  const byTickerYear: Record<string, Record<number, number>> = {};
  for (const d of allDivs) {
    const yr = Number(d.ex_date.slice(0, 4));
    if (!byTickerYear[d.ticker]) byTickerYear[d.ticker] = {};
    byTickerYear[d.ticker][yr] = (byTickerYear[d.ticker][yr] || 0) + d.amount;
  }

  const out: DripCalcTabProps["ticker_assumptions"] = {};
  const usSet = new Set(us_tickers);
  for (const t of all) {
    const f = fundis[t];
    const currency: "BRL" | "USD" = usSet.has(t) ? "USD" : "BRL";
    const start_price = f?.last_price ?? 100;

    // DY: prefer fundamentals.dy; else computed from trailing 12mo divs / price
    let start_dy_pct: number;
    if (f?.dy !== null && f?.dy !== undefined) {
      start_dy_pct = f.dy > 1 ? f.dy : f.dy * 100;
    } else {
      const ttm = (allDivs.filter((d) => d.ticker === t && d.ex_date >= isoDaysAgo(365))
        .reduce((s, d) => s + d.amount, 0));
      start_dy_pct = start_price > 0 ? (ttm / start_price) * 100 : 3;
    }

    const growth = computeDivGrowth(byTickerYear[t] || {});
    out[t] = {
      name: f?.name || t,
      start_price,
      start_dy_pct: Math.max(0.1, start_dy_pct),
      growth_low: growth.low,
      growth_mid: growth.mid,
      growth_high: growth.high,
      currency,
    };
  }
  return out;
}

function isoDaysAgo(days: number): string {
  return new Date(Date.now() - days * 86400000).toISOString().slice(0, 10);
}

function computeDivGrowth(
  yearSum: Record<number, number>,
): { low: number; mid: number; high: number } {
  const years = Object.keys(yearSum).map(Number).sort();
  if (years.length < 2) return DEFAULT_GROWTH;

  // Drop the current calendar year (incomplete) if today is < Dec 31
  const now = new Date();
  const isFullYearDone = now.getMonth() === 11 && now.getDate() === 31;
  const lastFullYear = isFullYearDone ? now.getFullYear() : now.getFullYear() - 1;

  function cagr(yr_a: number, yr_b: number): number | null {
    const a = yearSum[yr_a];
    const b = yearSum[yr_b];
    if (!a || !b || a <= 0 || b <= 0) return null;
    const n = yr_b - yr_a;
    if (n <= 0) return null;
    return (Math.pow(b / a, 1 / n) - 1) * 100;
  }

  // 1Y CAGR (last full year vs prior)
  const c1 = cagr(lastFullYear - 1, lastFullYear);
  // 3Y CAGR
  const c3 = cagr(lastFullYear - 3, lastFullYear);
  // 5Y CAGR
  const c5 = cagr(lastFullYear - 5, lastFullYear);

  const candidates = [c1, c3, c5].filter((x): x is number => x !== null);
  if (candidates.length === 0) return DEFAULT_GROWTH;

  const minG = Math.max(0, Math.min(...candidates));
  const maxG = Math.max(...candidates);
  const midG = candidates.reduce((s, x) => s + x, 0) / candidates.length;

  // Cap to sane band so a one-off 200% jump doesn't blow up the projection
  const cap = (v: number) => Math.max(0, Math.min(20, v));
  return {
    low: Number(cap(minG).toFixed(1)),
    mid: Number(cap(midG).toFixed(1)),
    high: Number(cap(maxG).toFixed(1)),
  };
}

// ── W4 · Real fundamentals for Compare tab ──────────────────────────
//
// Joins `batchFundamentals` (P/E, P/B, DY, ROE) with `listFairValue`
// (fair_price upside %). Tickers without coverage just appear with
// nulls — the Compare panel renders "—".

export function getCompareFundamentals(tickers: string[]): Record<string, CompareTickerFundamentals> {
  const fundis = batchFundamentals(tickers);
  // Build fair-value lookup from both markets
  const fvMap: Record<string, number> = {};
  for (const m of ["br", "us"] as const) {
    for (const r of listFairValue(m)) {
      // upside = (fair / current) - 1 → we want (current / fair) - 1 (gap_pct)
      // listFairValue already returns upside_pct; we just invert sign so
      // positive = expensive vs fair.
      fvMap[r.ticker] = -1 * r.upside_pct;
    }
  }

  const out: Record<string, CompareTickerFundamentals> = {};
  for (const t of tickers) {
    const f = fundis[t];
    out[t] = {
      ticker: t,
      name: f?.name || t,
      sector: f?.sector || "—",
      pe: f?.pe ?? null,
      pb: f?.pb ?? null,
      dy: f?.dy !== null && f?.dy !== undefined
        ? (f.dy > 1 ? f.dy : f.dy * 100)  // normalize to percentage
        : null,
      roe: f?.roe !== null && f?.roe !== undefined
        ? (f.roe > 1 ? f.roe : f.roe * 100)
        : null,
      vitality: null,            // wired in a later sprint (analytics.vitality)
      fv_gap_pct: fvMap[t] ?? null,
    };
  }
  return out;
}

// ── W3 · Forward annual income y/y (from dividends history) ─────────
//
// "Y/y" defined as: trailing 12 months received vs the 12 months
// immediately before that. We weight by *current* shares held so the
// number reflects "what would last year have paid me at today's
// position size" — the relevant comparison for a DRIP investor.
//
// Returns null if either window has insufficient coverage; caller
// falls back to placeholder.

export type ForwardIncomeYoy = {
  br_annual: number;
  us_annual: number;
  br_yoy_pct: number | null;
  us_yoy_pct: number | null;
};

export function getForwardIncomeYoy(
  br: HomeMarketSnapshot,
  us: HomeMarketSnapshot,
): ForwardIncomeYoy {
  return {
    br_annual: br.estimated_annual_income ?? 0,
    us_annual: us.estimated_annual_income ?? 0,
    br_yoy_pct: computeYoy(br),
    us_yoy_pct: computeYoy(us),
  };
}

function computeYoy(snap: HomeMarketSnapshot): number | null {
  const todayIso = new Date().toISOString().slice(0, 10);
  const oneYrAgoIso = new Date(Date.now() - 365 * 86400000).toISOString().slice(0, 10);
  const twoYrAgoIso = new Date(Date.now() - 730 * 86400000).toISOString().slice(0, 10);

  // Pull the last 24 months of dividends for current holdings (BR or US,
  // not both). Use pastDividends — but that helper queries both DBs;
  // we filter by snap.market via the position list.
  const tickers = new Set(snap.positions.map((p) => p.ticker));
  if (tickers.size === 0) return null;

  const all = pastDividends(twoYrAgoIso, todayIso);
  const inMarket = all.filter((d) => d.market === snap.market && tickers.has(d.ticker));
  if (inMarket.length === 0) return null;

  // Map ticker → quantity for weighting
  const qty: Record<string, number> = {};
  for (const p of snap.positions) qty[p.ticker] = p.quantity ?? 0;

  let curWindow = 0;
  let prevWindow = 0;
  for (const d of inMarket) {
    const q = qty[d.ticker] || 0;
    const contribution = q * d.amount;
    if (d.ex_date >= oneYrAgoIso) curWindow += contribution;
    else prevWindow += contribution;
  }

  if (prevWindow <= 0) return null;
  return ((curWindow - prevWindow) / prevWindow) * 100;
}

// ── W2 · Real dividend strip 14d/90d ────────────────────────────────
//
// 14-day strip = 7 past + today + 6 future (anchored on today).
// 90-day strip = 30 past + today + 59 future. (Wider window for tab.)
//
// Past payments come from `dividends` (ex_date <= today). Future from
// `upcomingDividends`. Both DBs queried, market tagged. Currency
// inferred from market unless explicit on the row.

export type DividendStripRow = {
  iso_date: string;
  ticker: string;
  amount: number;
  currency: "BRL" | "USD";
  is_past: boolean;
};

export function getDividendStrip(
  daysPast: number,
  daysFuture: number,
): DividendStripRow[] {
  const todayIso = new Date().toISOString().slice(0, 10);
  const today = Date.parse(todayIso);
  const startIso = new Date(today - daysPast * 86400000).toISOString().slice(0, 10);

  const out: DividendStripRow[] = [];

  // Future from upcomingDividends (already a wired helper)
  for (const d of upcomingDividends(daysFuture + 5)) {
    if (d.ex_date < todayIso) continue;
    out.push({
      iso_date: d.ex_date,
      ticker: d.ticker,
      amount: d.amount,
      currency: (d.currency === "BRL" || d.currency === "USD")
        ? d.currency
        : (d.market === "br" ? "BRL" : "USD"),
      is_past: false,
    });
  }

  // Past from dividends (already-paid window)
  for (const d of pastDividends(startIso, todayIso)) {
    if (d.ex_date >= todayIso) continue; // dedup with future bucket
    out.push({
      iso_date: d.ex_date,
      ticker: d.ticker,
      amount: d.amount,
      currency: (d.currency === "BRL" || d.currency === "USD")
        ? d.currency
        : (d.market === "br" ? "BRL" : "USD"),
      is_past: true,
    });
  }

  return out;
}

// Materialize into the Lead-strip shape (anchored on today).
export function buildLeadDividendDays(strip: DividendStripRow[], anchor: Date, daysPast: number, daysFuture: number): LeadDividendDay[] {
  const total = daysPast + 1 + daysFuture;
  const startOffset = -daysPast;
  const out: LeadDividendDay[] = [];
  const todayIso = anchor.toISOString().slice(0, 10);
  for (let i = 0; i < total; i++) {
    const d = new Date(anchor);
    d.setDate(d.getDate() + startOffset + i);
    const iso = d.toISOString().slice(0, 10);
    const wd = d.getDay();
    const weekday = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][wd];
    const is_weekend = wd === 0 || wd === 6;
    const payments = strip
      .filter((r) => r.iso_date === iso)
      .map((r) => ({ ticker: r.ticker, amount: r.amount, currency: r.currency }));
    out.push({
      iso_date: iso,
      weekday,
      day_num: d.getDate(),
      is_today: iso === todayIso,
      is_weekend,
      payments,
    });
  }
  return out;
}

export function buildDividendsTabDays(strip: DividendStripRow[], anchor: Date, daysPast: number, daysFuture: number): DividendsTabDay[] {
  const total = daysPast + 1 + daysFuture;
  const startOffset = -daysPast;
  const out: DividendsTabDay[] = [];
  const todayIso = anchor.toISOString().slice(0, 10);
  for (let i = 0; i < total; i++) {
    const d = new Date(anchor);
    d.setDate(d.getDate() + startOffset + i);
    const iso = d.toISOString().slice(0, 10);
    const wd = d.getDay();
    const weekday = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][wd];
    const payments = strip
      .filter((r) => r.iso_date === iso)
      .map((r) => ({
        ticker: r.ticker,
        amount: r.amount,
        currency: r.currency,
        status: (r.is_past ? "paid" : "scheduled") as "paid" | "scheduled" | "ex",
      }));
    out.push({
      iso_date: iso,
      weekday,
      day_num: d.getDate(),
      is_today: iso === todayIso,
      is_past: iso < todayIso,
      payments,
    });
  }
  return out;
}
