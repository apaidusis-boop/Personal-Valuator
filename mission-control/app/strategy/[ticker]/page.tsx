import Link from "next/link";
import { listStrategyRuns } from "@/lib/db";

export const dynamic = "force-dynamic";

const VERDICT_COLOR: Record<string, string> = {
  BUY: "text-emerald-400 border-emerald-700/40 bg-emerald-900/20",
  HOLD: "text-yellow-400 border-yellow-700/40 bg-yellow-900/20",
  AVOID: "text-red-400 border-red-700/40 bg-red-900/20",
  "N/A": "text-zinc-500 border-zinc-700/40 bg-zinc-900/20",
};

const ENGINE_BLURB: Record<string, string> = {
  graham: "Deep value (Graham number, low PE/PB, ROE 15%, debt < 3x EBITDA)",
  buffett: "Quality compounding (PE ≤ 20, PB ≤ 3, ROE 15%, ROIC 15%, Aristocrat)",
  drip: "Dividend safety (SAFE/WATCH/RISK) + yield floor (US 2.5%, BR 6%)",
  macro: "Top-down sector tilt — multiplier from regime + sector",
  hedge: "Tactical defensive overlay — quiet in expansion, on in late_cycle/recession",
};

function pct(n: number, digits = 1) {
  if (n == null || isNaN(n)) return "—";
  return `${(n * 100).toFixed(digits)}%`;
}

export default async function StrategyTickerPage({
  params,
  searchParams,
}: {
  params: Promise<{ ticker: string }>;
  searchParams: Promise<{ market?: string }>;
}) {
  const { ticker } = await params;
  const { market } = await searchParams;
  const tk = ticker.toUpperCase();
  const m = (market === "br" || market === "us") ? market : null;
  const runs = listStrategyRuns(tk, m, 50);

  if (!runs.length) {
    return (
      <div className="p-8 max-w-4xl">
        <Link href="/allocation" className="text-zinc-500 text-sm hover:text-zinc-300">
          ← back to allocation
        </Link>
        <h1 className="text-3xl font-bold mt-4 text-purple-200">
          {tk}
        </h1>
        <p className="mt-4 text-zinc-400">
          No strategy runs found for this ticker.
        </p>
        <p className="text-xs text-zinc-500 font-mono mt-2">
          Run <code>ii overnight</code> or <code>ii strategy all {tk}</code> to populate.
        </p>
      </div>
    );
  }

  // Group by market (in case ticker exists in both — unlikely)
  const byMarket = runs.reduce<Record<string, typeof runs>>((acc, r) => {
    (acc[r.market] = acc[r.market] || []).push(r);
    return acc;
  }, {});

  return (
    <div className="p-8 max-w-5xl">
      <Link href="/allocation" className="text-zinc-500 text-sm hover:text-zinc-300">
        ← back to allocation
      </Link>
      <h1 className="text-3xl font-bold mt-4 mb-1 text-purple-200">{tk}</h1>
      <p className="text-sm text-zinc-400 mb-6">
        Last strategy outputs across all engines. Click each engine for rationale.
      </p>

      {Object.entries(byMarket).map(([mkt, rs]) => (
        <section key={mkt} className="mb-8">
          <h2 className="text-sm font-mono text-purple-300 uppercase tracking-wider mb-3">
            {mkt} — last run {rs[0]?.run_ts.slice(0, 10)}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {rs.map((r) => (
              <details
                key={r.engine}
                className={`rounded-lg border ${
                  VERDICT_COLOR[r.verdict] || "border-zinc-800 bg-zinc-900/30"
                } p-4 group`}
              >
                <summary className="cursor-pointer flex items-baseline justify-between gap-3">
                  <div>
                    <span className="text-lg font-semibold capitalize">
                      {r.engine}
                    </span>
                    <span className="ml-3 text-xs font-mono opacity-60">
                      {ENGINE_BLURB[r.engine] || ""}
                    </span>
                  </div>
                  <div className="text-right shrink-0">
                    <div className="font-mono text-sm">
                      {pct(r.score, 0)}
                    </div>
                    <div className="text-xs">{r.verdict}</div>
                  </div>
                </summary>
                <pre className="mt-3 text-xs text-zinc-300 overflow-x-auto whitespace-pre-wrap">
                  {JSON.stringify(r.rationale, null, 2)}
                </pre>
              </details>
            ))}
          </div>
        </section>
      ))}

      <footer className="mt-8 pt-4 border-t border-zinc-800 text-xs text-zinc-500">
        <Link href={`/ticker/${tk}`} className="hover:text-cyan-300">
          → open price/fundamentals view
        </Link>
      </footer>
    </div>
  );
}
