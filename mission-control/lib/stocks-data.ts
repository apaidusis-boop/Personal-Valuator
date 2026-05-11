// ── /stocks page data composer ───────────────────────────────────────
//
// Now covers the FULL universe — holdings (active positions) + watchlist
// (companies not held, but tracked) + Kings/Aristocrats. NN.3 expansion.
//
// Holdings get fully populated rows (qty, cost, value, P&L, weight).
// Watchlist gets last_price + fundamentals + verdict, but position-only
// fields are null. The UI shows them differently.

import { getHomeMarketSnapshot, listAllCompanies, batchFundamentals } from "@/lib/db";
import { getCompareFundamentals } from "@/lib/home-data";
import { buildHomeMockBundle } from "@/lib/home-mock";
import type { CompareTickerFundamentals } from "@/components/home/workbench/compare-tab";
import type { DeepReviewTickerData } from "@/components/home/deep-review";

export type StockKind = "holding" | "watchlist";

export type StockRow = {
  ticker: string;
  name: string;
  sector: string;
  market: "br" | "us";
  kind: StockKind;
  is_holding: boolean;        // backwards-compat with existing UIs
  strategy_tag: string | null; // useful filter on watchlist (Buffett/Value/DRIP)
  // Position numbers (only filled when is_holding)
  quantity: number | null;
  cost_basis: number | null;
  current_value: number | null;
  pnl_pct: number | null;
  // Live data
  last_price: number | null;
  // Fundamentals (P/E, P/B, DY, ROE, fv_gap)
  pe: number | null;
  pb: number | null;
  dy: number | null;
  roe: number | null;
  fv_gap_pct: number | null;
  // Deep review summary
  verdict: "BUY" | "HOLD" | "AVOID" | "N/A";
  one_line_stance: string;
  // Weight relative to its market's NAV (null for non-holdings)
  weight_pct: number | null;
};

export type StocksData = {
  rows: StockRow[];
  br_nav: number;
  us_nav: number;
  // Counts surfaced to the UI for filter chips / header
  n_holdings: number;
  n_watchlist: number;
  // Per-ticker dossier — for tearsheet (read mode). Populated for holdings;
  // watchlist tickers may have a stub or no entry (UI handles missing).
  deep_review_by_ticker: Record<string, DeepReviewTickerData>;
  fundamentals_by_ticker: Record<string, CompareTickerFundamentals>;
};

export function buildStocksData(): StocksData {
  const br = getHomeMarketSnapshot("br");
  const us = getHomeMarketSnapshot("us");

  // Deep review map (covers holdings — built by home-mock)
  const home = buildHomeMockBundle(br, us, 0, null, "");
  const fundisByTicker = home.compare.fundamentals_by_ticker;
  const deepByTicker = home.deep_review.by_ticker;

  // Quick lookup for active position numbers
  const positionByTicker = new Map<string, { quantity: number | null; cost_basis: number; current_value: number; pnl_pct: number | null; current_unit: number | null }>();
  for (const p of br.positions) positionByTicker.set(`br:${p.ticker}`, {
    quantity: p.quantity, cost_basis: p.cost_basis, current_value: p.current_value, pnl_pct: p.pnl_pct, current_unit: p.current_unit,
  });
  for (const p of us.positions) positionByTicker.set(`us:${p.ticker}`, {
    quantity: p.quantity, cost_basis: p.cost_basis, current_value: p.current_value, pnl_pct: p.pnl_pct, current_unit: p.current_unit,
  });

  // Pull the entire universe from companies table
  const universe = listAllCompanies();

  // Enrich watchlist tickers with fundamentals (holdings already covered
  // by the home bundle's fundamentals_by_ticker).
  const watchlistTickers = universe.filter((c) => !c.is_holding).map((c) => c.ticker);
  const missingFromMap = watchlistTickers.filter((t) => !fundisByTicker[t]);
  if (missingFromMap.length > 0) {
    const extra = getCompareFundamentals(missingFromMap);
    for (const t of Object.keys(extra)) fundisByTicker[t] = extra[t];
  }

  // Also need last_price for non-holdings (positions cover holdings).
  // batchFundamentals already returns last_price; pull it if not in our
  // current map.
  const fundisLive = batchFundamentals(watchlistTickers);

  const rows: StockRow[] = universe.map((c) => {
    const pos = positionByTicker.get(`${c.market}:${c.ticker}`);
    const f = fundisByTicker[c.ticker];
    const live = fundisLive[c.ticker];
    const d = deepByTicker[c.ticker];
    const nav = c.market === "br" ? br.account_value : us.account_value;
    const last_price = pos?.current_unit ?? live?.last_price ?? null;
    const sector = c.sector || f?.sector || "—";
    const name = c.name || c.ticker;

    if (c.is_holding && pos) {
      return {
        ticker: c.ticker,
        name,
        sector,
        market: c.market,
        kind: "holding",
        is_holding: true,
        strategy_tag: c.strategy_tag,
        quantity: pos.quantity,
        cost_basis: pos.cost_basis,
        current_value: pos.current_value,
        pnl_pct: pos.pnl_pct,
        last_price,
        pe: f?.pe ?? null,
        pb: f?.pb ?? null,
        dy: f?.dy ?? null,
        roe: f?.roe ?? null,
        fv_gap_pct: f?.fv_gap_pct ?? null,
        verdict: d?.verdict ?? "N/A",
        one_line_stance: d?.one_line_stance ?? "—",
        weight_pct: nav > 0 ? (pos.current_value / nav) * 100 : null,
      };
    }
    // Watchlist row — no position fields
    return {
      ticker: c.ticker,
      name,
      sector,
      market: c.market,
      kind: "watchlist",
      is_holding: false,
      strategy_tag: c.strategy_tag,
      quantity: null,
      cost_basis: null,
      current_value: null,
      pnl_pct: null,
      last_price,
      pe: f?.pe ?? null,
      pb: f?.pb ?? null,
      dy: f?.dy ?? null,
      roe: f?.roe ?? null,
      fv_gap_pct: f?.fv_gap_pct ?? null,
      verdict: d?.verdict ?? "N/A",
      one_line_stance: d?.one_line_stance ?? "—",
      weight_pct: null,
    };
  });

  // Default sort: holdings first (by weight desc), then watchlist (by FV
  // gap ascending — the cheapest first). The Read/Operate modes can
  // override via their own sort controls.
  rows.sort((a, b) => {
    if (a.kind !== b.kind) return a.kind === "holding" ? -1 : 1;
    if (a.kind === "holding") return (b.weight_pct ?? 0) - (a.weight_pct ?? 0);
    // watchlist: cheapest by FV gap (negative = under fair value)
    return (a.fv_gap_pct ?? 999) - (b.fv_gap_pct ?? 999);
  });

  const n_holdings = rows.filter((r) => r.kind === "holding").length;
  const n_watchlist = rows.filter((r) => r.kind === "watchlist").length;

  return {
    rows,
    br_nav: br.account_value,
    us_nav: us.account_value,
    n_holdings,
    n_watchlist,
    deep_review_by_ticker: deepByTicker,
    fundamentals_by_ticker: fundisByTicker,
  };
}
