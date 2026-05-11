"use client";

// ── HOME VIEW · 3-band layout ────────────────────────────────────────
//
// This file used to be a single-pane JPM-style dashboard. Phase MM
// rebuilds it as a 3-band hybrid (FT Lead · Bloomberg Workbench · FT
// Deep Review) so the page does three jobs cleanly instead of one job
// poorly. The legacy types (HomePosition, HomeMarketData) are retained
// because lib/db.ts and other consumers still depend on them.
//
// Band 1 (Lead) — editorial story-of-the-day above the fold
// Band 2 (Workbench) — Compare · DRIP Calc · Positions · Dividends tabs
// Band 3 (Deep Review) — long-form per-ticker section, synced to focus
//
// Cross-band sync via FocusTickerProvider: Lead picks the headline
// ticker, Workbench can change focus, Deep Review re-renders on focus
// change. Lead headline itself stays anchored to the story of the day.

import { Lead, type LeadProps } from "./home/lead";
import { Workbench, type WorkbenchProps } from "./home/workbench";
import { DeepReview, type DeepReviewProps } from "./home/deep-review";
import { FocusTickerProvider } from "@/lib/focus-ticker";

// ── Public types kept for back-compat with lib/db.ts ────────────────

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
  account_value: number;
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

// ── New props for the 3-band layout ─────────────────────────────────

export type HomeViewProps = {
  spotlight: { ticker: string; market: "br" | "us" };
  lead: LeadProps;
  workbench: WorkbenchProps;
  deep_review: DeepReviewProps;
};

export function HomeView({ spotlight, lead, workbench, deep_review }: HomeViewProps) {
  return (
    <FocusTickerProvider initialTicker={spotlight.ticker} initialMarket={spotlight.market}>
      <div
        className="px-6 py-5 max-w-[1440px] mx-auto"
        style={{ display: "flex", flexDirection: "column", gap: 24 }}
      >
        <Lead {...lead} />
        <Workbench {...workbench} />
        <DeepReview {...deep_review} />
      </div>
    </FocusTickerProvider>
  );
}
