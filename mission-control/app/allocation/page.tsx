import Link from "next/link";
import { loadLatestAllocation } from "@/lib/vault";

export const dynamic = "force-dynamic";

const VERDICT_COLOR: Record<string, string> = {
  BUY: "text-emerald-400",
  HOLD: "text-yellow-400",
  AVOID: "text-red-400",
  "N/A": "text-zinc-500",
};

function pct(n: number) {
  return `${(n * 100).toFixed(1)}%`;
}

export default function AllocationPage() {
  const us = loadLatestAllocation("us");
  const br = loadLatestAllocation("br");

  return (
    <div className="p-8 max-w-6xl">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2 text-purple-200">Allocation Proposal</h1>
        <p className="text-sm text-zinc-400">
          Output do <code className="text-cyan-300">portfolio_engine</code>: 5
          strategy engines combinados via bucket weights, com macro overlay
          e hedge tactical separados.
        </p>
      </header>

      {[us, br].map((data, i) => (
        <Section key={i} data={data} />
      ))}

      {!us && !br && (
        <div className="bg-zinc-900/50 border border-zinc-800 rounded-lg p-8 text-center">
          <p className="text-zinc-400 mb-2">
            No allocation files found in vault.
          </p>
          <p className="text-xs text-zinc-500 font-mono">
            Run: <code>ii overnight</code> to generate.
          </p>
        </div>
      )}
    </div>
  );
}

function Section({ data }: { data: ReturnType<typeof loadLatestAllocation> }) {
  if (!data) return null;
  const sorted = Object.entries(data.target_weights).sort(
    (a, b) => b[1] - a[1]
  );
  const hedge = data.hedge_overlay;
  const macro = data.macro_overlay;
  return (
    <section className="mb-12 bg-zinc-900/30 border border-[#1f1f3d] rounded-lg p-6">
      <header className="flex items-baseline justify-between mb-4 pb-3 border-b border-[#1f1f3d]">
        <h2 className="text-xl font-semibold">
          {data.market.toUpperCase()} —{" "}
          <span className="text-zinc-400 text-base">{data.date}</span>
        </h2>
        <span className="text-xs font-mono text-purple-300">
          {sorted.length} candidates
        </span>
      </header>

      {/* Bucket weights pill */}
      <div className="mb-4 flex flex-wrap gap-2 text-xs font-mono">
        {Object.entries(data.bucket_weights).map(([k, v]) => (
          <span
            key={k}
            className="px-2 py-1 rounded bg-purple-900/30 border border-purple-800/40 text-purple-200"
          >
            {k}: {pct(v as number)}
          </span>
        ))}
      </div>

      {/* Macro */}
      <div className="mb-4 text-sm">
        <span className="text-zinc-500">Macro regime: </span>
        <span className="text-cyan-300 font-mono">{macro.regime || "?"}</span>
        <span className="text-zinc-500"> · confidence: </span>
        <span className="text-cyan-300 font-mono">{macro.confidence || "?"}</span>
        {macro.tilt_up?.length > 0 && (
          <div className="mt-1 text-xs text-zinc-500">
            Tilt up: {macro.tilt_up.join(" · ")} | Tilt down:{" "}
            {(macro.tilt_down || []).join(" · ") || "—"}
          </div>
        )}
      </div>

      {/* Hedge */}
      {hedge.active && (
        <div className="mb-4 px-3 py-2 rounded bg-red-900/20 border border-red-800/40 text-sm">
          <span className="text-red-300 font-mono">HEDGE ON</span>
          <span className="text-zinc-300"> · {pct(hedge.hedge_size_pct)} via </span>
          <span className="font-mono text-yellow-300">
            {(hedge.instruments || []).join(", ")}
          </span>
        </div>
      )}

      {/* Top weights table */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <h3 className="text-sm font-semibold text-zinc-300 mb-2">
            Target weights
          </h3>
          <table className="w-full text-sm font-mono">
            <tbody>
              {sorted.slice(0, 15).map(([t, w]) => (
                <tr key={t} className="hover:bg-zinc-900/40">
                  <td className="py-1">
                    <Link
                      href={`/strategy/${t}?market=${data.market}`}
                      className="text-cyan-300 hover:text-cyan-200"
                    >
                      {t}
                    </Link>
                  </td>
                  <td className="text-right text-zinc-300">{pct(w)}</td>
                  <td className="pl-3 w-32">
                    <div
                      className="h-2 rounded bg-purple-700/60"
                      style={{ width: `${Math.min(w * 400, 100)}%` }}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-zinc-300 mb-2">
            Conflicts ({data.conflicts.length})
          </h3>
          <p className="text-xs text-zinc-500 mb-3">
            Tickers onde os engines discordam (BUY+AVOID na mesma linha).
          </p>
          <div className="space-y-2">
            {data.conflicts.slice(0, 10).map((c) => (
              <div
                key={c.ticker}
                className="text-xs font-mono px-2 py-1 rounded bg-zinc-900/50 border border-zinc-800"
              >
                <Link
                  href={`/strategy/${c.ticker}?market=${data.market}`}
                  className="text-cyan-300 hover:text-cyan-200"
                >
                  {c.ticker}
                </Link>
                <div className="mt-0.5 flex gap-2">
                  {Object.entries(c.verdicts).map(([eng, v]) => (
                    <span
                      key={eng}
                      className={VERDICT_COLOR[v as string] || "text-zinc-500"}
                    >
                      {eng}={v}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {data.notes.length > 0 && (
        <div className="mt-4 pt-3 border-t border-zinc-800 text-xs text-zinc-500 font-mono">
          {data.notes.map((n, i) => (
            <div key={i}>· {n}</div>
          ))}
        </div>
      )}
    </section>
  );
}
