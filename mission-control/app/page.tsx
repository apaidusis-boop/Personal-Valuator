import { getHomeMarketSnapshot } from "@/lib/db";
import { listCouncilOutputs, summariseCouncil, readBriefingMeta } from "@/lib/vault";
import { formatDate } from "@/lib/format";
import { buildHomeMockBundle } from "@/lib/home-mock";
import { HomeView } from "@/components/home-view";
import type { Metadata } from "next";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Mission Control" };

export default function Home() {
  const br = getHomeMarketSnapshot("br");
  const us = getHomeMarketSnapshot("us");

  const councilAll = listCouncilOutputs(500);
  const councilSummary = summariseCouncil(councilAll);
  const { mtime: briefingMtime } = readBriefingMeta();
  const briefing_relative = briefingMtime ? `briefing ${formatDate(briefingMtime, "relative")}` : "";
  const council_date = councilSummary.total > 0 ? formatDate(councilSummary.date, "short") : null;

  const bundle = buildHomeMockBundle(
    br,
    us,
    councilSummary.total,
    council_date,
    briefing_relative,
  );

  return (
    <HomeView
      spotlight={bundle.spotlight}
      lead={bundle.lead}
      workbench={{
        compare: bundle.compare,
        drip: bundle.drip,
        positions: { br_positions: br.positions, us_positions: us.positions },
        dividends: bundle.dividends,
      }}
      deep_review={bundle.deep_review}
    />
  );
}
