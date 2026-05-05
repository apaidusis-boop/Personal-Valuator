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
    <div
      className="border-b border-t-2 px-6 py-2 flex flex-wrap gap-x-6 gap-y-1"
      style={{
        background: "var(--bg-overlay)",
        borderTopColor: "var(--verdict-avoid)",
        borderBottomColor: "var(--border-subtle)",
      }}
    >
      {banners.map((b) => (
        <div
          key={b.market}
          className="flex items-center gap-3 type-mono-sm"
        >
          <span
            className="pill pill-avoid"
            title={`Tactical hedge active in ${b.market.toUpperCase()}`}
          >
            hedge on · {b.market.toUpperCase()}
          </span>
          <span className="text-[var(--text-secondary)]">
            regime <span className="text-[var(--text-primary)]">{b.hedge.regime}</span>
          </span>
          <span className="text-[var(--text-secondary)]">
            size{" "}
            <span className="text-[var(--verdict-avoid)]">
              {(b.hedge.hedge_size_pct * 100).toFixed(0)}%
            </span>
          </span>
          <span className="text-[var(--text-secondary)]">
            via{" "}
            <span className="text-[var(--verdict-hold)]">
              {(b.hedge.instruments || []).join(", ")}
            </span>
          </span>
        </div>
      ))}
    </div>
  );
}
