// ── /desk page data composer ────────────────────────────────────────
//
// Server-side build for the 4-pane Bloomberg-style /desk view.
// Top:    big chart (focus ticker, fetched client-side via /api/prices)
// Middle: positions blotter (compact)
// Right:  next dividends + next filings (rolling 14-30 day window)

import {
  getHomeMarketSnapshot,
  upcomingDividends,
  upcomingFilings,
  type DividendEvent,
  type UpcomingFiling,
} from "@/lib/db";
import type { HomePosition } from "@/components/home-view";

export type DeskPosition = HomePosition & {
  market: "br" | "us";
  weight_pct: number;
  day_pct: number | null;
};

export type DeskData = {
  positions: DeskPosition[];
  br_nav: number;
  us_nav: number;
  next_dividends: DividendEvent[];   // already sorted by ex_date
  next_filings: UpcomingFiling[];    // already sorted by earnings_date
  initial_focus_ticker: string;
  initial_focus_market: "br" | "us";
};

export function buildDeskData(): DeskData {
  const br = getHomeMarketSnapshot("br");
  const us = getHomeMarketSnapshot("us");

  const allPositions: DeskPosition[] = [
    ...br.positions.map((p) => ({
      ...p,
      market: "br" as const,
      weight_pct: br.account_value > 0 ? (p.current_value / br.account_value) * 100 : 0,
      day_pct: null, // wired via /api/prices client-side or in a follow-up
    })),
    ...us.positions.map((p) => ({
      ...p,
      market: "us" as const,
      weight_pct: us.account_value > 0 ? (p.current_value / us.account_value) * 100 : 0,
      day_pct: null,
    })),
  ];

  // Sort by weight descending — biggest positions first in the blotter
  allPositions.sort((a, b) => b.weight_pct - a.weight_pct);

  // Default focus = top US holding (most users have biggest concentration there;
  // can be overridden by clicking a row in the blotter)
  const focus = allPositions[0] || null;

  return {
    positions: allPositions,
    br_nav: br.account_value,
    us_nav: us.account_value,
    next_dividends: upcomingDividends(30).slice(0, 12),
    next_filings: upcomingFilings(30).slice(0, 12),
    initial_focus_ticker: focus?.ticker || "AAPL",
    initial_focus_market: focus?.market || "us",
  };
}
