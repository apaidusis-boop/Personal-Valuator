import { getHomeMarketSnapshot } from "@/lib/db";
import { listCouncilOutputs, summariseCouncil, readBriefingMeta } from "@/lib/vault";
import { formatDate } from "@/lib/format";
import { HomeView, HomeMarketData } from "@/components/home-view";
import type { Metadata } from "next";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Mission Control" };

function snapshotToViewData(snap: ReturnType<typeof getHomeMarketSnapshot>): HomeMarketData {
  return {
    market: snap.market,
    account_value: snap.account_value,
    total_cost: snap.total_cost,
    day_gain_abs: snap.day_gain_abs,
    day_gain_pct: snap.day_gain_pct,
    total_gain_abs: snap.total_gain_abs,
    total_gain_pct: snap.total_gain_pct,
    estimated_annual_income: snap.estimated_annual_income,
    cash_sweep: snap.cash_sweep,
    positions: snap.positions,
    watchlist: snap.watchlist,
    indices: snap.indices,
    asset_classes: snap.asset_classes,
  };
}

export default function Home() {
  const br = snapshotToViewData(getHomeMarketSnapshot("br"));
  const us = snapshotToViewData(getHomeMarketSnapshot("us"));

  // Council & briefing freshness — small subline under the page header.
  const councilAll = listCouncilOutputs(500);
  const councilSummary = summariseCouncil(councilAll);
  const { mtime: briefingMtime } = readBriefingMeta();

  const council_summary = councilSummary.total > 0
    ? `Council ${formatDate(councilSummary.date, "short")} · ${councilSummary.total} subjects`
    : "Council sem run";
  const briefing_relative = briefingMtime
    ? `briefing ${formatDate(briefingMtime, "relative")}`
    : "";

  return (
    <HomeView
      br={br}
      us={us}
      council_summary={council_summary}
      briefing_relative={briefing_relative}
    />
  );
}
