import Link from "next/link";
import { listCouncilOutputs, summariseCouncil, type CouncilEntry, type CouncilStance } from "@/lib/vault";
import StancePill from "@/components/stance-pill";

export const dynamic = "force-dynamic";

const STANCE_ORDER: CouncilStance[] = ["BUY", "HOLD", "AVOID", "NEEDS_DATA", "UNKNOWN"];
const STANCE_LABEL: Record<CouncilStance, string> = {
  BUY: "🟢 BUY",
  HOLD: "🟡 HOLD",
  AVOID: "🔴 AVOID",
  NEEDS_DATA: "⚪ NEEDS DATA",
  UNKNOWN: "· uncategorised",
};

export default function CouncilIndexPage() {
  const all = listCouncilOutputs(500);
  const summary = summariseCouncil(all);
  const latest = all.filter((e) => e.date === summary.date);
  const previous = all.filter((e) => e.date && e.date !== summary.date);

  const grouped: Record<CouncilStance, CouncilEntry[]> = {
    BUY: [],
    HOLD: [],
    AVOID: [],
    NEEDS_DATA: [],
    UNKNOWN: [],
  };
  for (const e of latest) grouped[e.stance].push(e);

  return (
    <div className="p-8 space-y-6">
      <header className="border-b border-[#1f1f3d] pb-4">
        <h1 className="text-3xl font-light text-zinc-100">
          <span className="text-purple-400">⚖</span> Council
        </h1>
        <p className="text-xs font-mono text-zinc-500 mt-1">
          Night Shift outputs · STORYT_3.0 · {latest.length} dossiers · {summary.date}
        </p>
      </header>

      <section className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <SummaryStat label="total" value={summary.total} tone="zinc" />
        <SummaryStat label="BUY" value={summary.buy} tone="green" />
        <SummaryStat label="HOLD" value={summary.hold} tone="yellow" />
        <SummaryStat label="AVOID" value={summary.avoid} tone="red" />
        <SummaryStat label="needs data" value={summary.needs_data} tone="zinc" />
      </section>

      {STANCE_ORDER.map((st) => {
        const items = grouped[st];
        if (items.length === 0) return null;
        return (
          <section key={st}>
            <h2 className="text-sm font-mono uppercase tracking-wider mb-3 text-zinc-400">
              {STANCE_LABEL[st]} <span className="text-purple-400">({items.length})</span>
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {items
                .sort((a, b) => a.ticker.localeCompare(b.ticker))
                .map((e) => (
                  <CouncilCard key={e.ticker} e={e} />
                ))}
            </div>
          </section>
        );
      })}

      {previous.length > 0 && (
        <section>
          <h2 className="text-sm font-mono uppercase tracking-wider mb-3 text-zinc-500">
            Earlier runs <span className="text-zinc-600">({previous.length})</span>
          </h2>
          <div className="card p-3 rounded-lg max-h-72 overflow-y-auto">
            <table className="w-full text-xs font-mono">
              <thead>
                <tr className="text-zinc-500 text-left">
                  <th className="py-1">Date</th>
                  <th className="py-1">Ticker</th>
                  <th className="py-1">Stance</th>
                  <th className="py-1">Conf</th>
                  <th className="py-1">Sector</th>
                </tr>
              </thead>
              <tbody>
                {previous.slice(0, 100).map((e) => (
                  <tr key={`${e.ticker}-${e.date}`} className="border-t border-[#1f1f3d]">
                    <td className="py-1.5 text-zinc-500">{e.date}</td>
                    <td className="py-1.5">
                      <Link href={`/council/${e.ticker}`} className="text-cyan-300 hover:underline">
                        {e.ticker}
                      </Link>
                    </td>
                    <td className="py-1.5 text-zinc-300">{e.stance}</td>
                    <td className="py-1.5 text-zinc-500">{e.confidence}</td>
                    <td className="py-1.5 text-zinc-600">{e.sector || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}

      {latest.length === 0 && (
        <div className="card p-12 rounded-lg text-center text-zinc-500">
          Sem outputs do Council ainda. Corre <code>python -m agents.council.story &lt;TK&gt;</code>.
        </div>
      )}
    </div>
  );
}

function SummaryStat({
  label,
  value,
  tone,
}: {
  label: string;
  value: number;
  tone: "green" | "yellow" | "red" | "zinc";
}) {
  const valueColor =
    tone === "green"
      ? "text-green-300"
      : tone === "yellow"
        ? "text-yellow-300"
        : tone === "red"
          ? "text-red-300"
          : "text-zinc-200";
  return (
    <div className="card p-3 rounded-lg">
      <div className="text-[10px] font-mono uppercase tracking-wider text-zinc-500">{label}</div>
      <div className={`text-2xl font-light tabular ${valueColor} mt-1`}>{value}</div>
    </div>
  );
}

function CouncilCard({ e }: { e: CouncilEntry }) {
  const mosPct =
    e.margin_of_safety && e.margin_of_safety !== 0
      ? `${(e.margin_of_safety * 100).toFixed(1)}% MoS`
      : null;
  return (
    <Link
      href={`/council/${e.ticker}`}
      className="card p-4 rounded-lg hover:border-cyan-500/50 transition-colors block"
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-mono text-cyan-300 text-base">{e.ticker}</h3>
        <StancePill stance={e.stance} confidence={e.confidence} />
      </div>
      <div className="text-[10px] font-mono text-zinc-500 mb-2">
        {e.market.toUpperCase()} · {e.modo ? `Modo ${e.modo}` : "—"}
        {e.is_holding && <span className="text-purple-300 ml-1">· holding</span>}
      </div>
      {(e.dissent_count > 0 || e.flag_count > 0) && (
        <div className="flex gap-2 text-[10px] font-mono">
          {e.dissent_count > 0 && (
            <span className="text-orange-300">
              ◇ {e.dissent_count} dissent
            </span>
          )}
          {e.flag_count > 0 && (
            <span className="text-red-300">
              ⚑ {e.flag_count} pre-pub
            </span>
          )}
        </div>
      )}
      {e.seats.length > 0 && (
        <div className="text-[10px] text-zinc-600 mt-2 truncate">
          {e.seats.slice(0, 4).join(" · ")}
          {e.seats.length > 4 && ` +${e.seats.length - 4}`}
        </div>
      )}
      {mosPct && (
        <div className="text-[10px] font-mono text-zinc-500 mt-1">{mosPct}</div>
      )}
    </Link>
  );
}
