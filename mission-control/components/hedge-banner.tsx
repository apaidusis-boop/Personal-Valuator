import { loadLatestAllocation } from "@/lib/vault";

export default function HedgeBanner() {
  const us = loadLatestAllocation("us");
  const br = loadLatestAllocation("br");
  const banners: Array<{ market: string; hedge: any }> = [];
  for (const data of [us, br]) {
    if (data?.hedge_overlay?.active) {
      banners.push({ market: data.market, hedge: data.hedge_overlay });
    }
  }
  if (!banners.length) return null;
  return (
    <div className="border-b border-red-800/40 bg-red-900/20 px-6 py-2">
      {banners.map((b) => (
        <div
          key={b.market}
          className="flex items-center gap-3 text-xs font-mono"
        >
          <span className="text-red-300 font-bold">[!]</span>
          <span className="text-red-200">
            HEDGE ON · {b.market.toUpperCase()}
          </span>
          <span className="text-zinc-400">
            regime={b.hedge.regime} · size=
            {(b.hedge.hedge_size_pct * 100).toFixed(0)}%
          </span>
          <span className="text-yellow-300">
            via {(b.hedge.instruments || []).join(", ")}
          </span>
        </div>
      ))}
    </div>
  );
}
