import { listOpenActions, listPortfolio, upcomingDividends, listChatIds } from "@/lib/db";
import { loadAgentStatus, listDepartments } from "@/lib/agents";
import {
  listResearchDigests,
  listDossiers,
  readBriefing,
  listCouncilOutputs,
  summariseCouncil,
} from "@/lib/vault";
import HomeToolbar from "@/components/toolbar";
import { PortfolioChart } from "@/components/charts";
import StancePill from "@/components/stance-pill";
import Link from "next/link";

export const dynamic = "force-dynamic";

function statusDot(status: string | null | undefined) {
  if (status === "ok") return "bg-green-400 dot-live";
  if (status === "no_action") return "bg-zinc-500";
  if (status === "failed") return "bg-red-400 dot-fail";
  return "bg-zinc-700";
}

function fmt(n: number | null | undefined, d = 0) {
  if (n == null) return "—";
  return Number(n).toLocaleString("pt-BR", { maximumFractionDigits: d });
}

export default function Home() {
  const portfolio = listPortfolio();
  const actions = listOpenActions(20);
  const dividends = upcomingDividends(30);
  const status = loadAgentStatus();
  const chats = listChatIds();
  const dossiers = listDossiers(5);
  const briefingRaw = readBriefing();
  const councilAll = listCouncilOutputs(500);
  const councilSummary = summariseCouncil(councilAll);
  const councilLatest = councilAll.filter((e) => e.date === councilSummary.date);
  const councilAvoid = councilLatest.filter((e) => e.stance === "AVOID");
  const councilFlagged = councilLatest
    .filter((e) => e.flag_count >= 3 || e.dissent_count >= 3)
    .filter((e) => e.stance !== "AVOID")
    .slice(0, 4);

  const totalsBR = portfolio
    .filter((p) => p.market === "br")
    .reduce(
      (acc, p) => ({
        cost: acc.cost + p.cost,
        mv: acc.mv + (p.market_value || 0),
      }),
      { cost: 0, mv: 0 }
    );
  const totalsUS = portfolio
    .filter((p) => p.market === "us")
    .reduce(
      (acc, p) => ({
        cost: acc.cost + p.cost,
        mv: acc.mv + (p.market_value || 0),
      }),
      { cost: 0, mv: 0 }
    );
  const pnlPctBR = totalsBR.cost ? ((totalsBR.mv - totalsBR.cost) / totalsBR.cost) * 100 : 0;
  const pnlPctUS = totalsUS.cost ? ((totalsUS.mv - totalsUS.cost) / totalsUS.cost) * 100 : 0;

  const departments = listDepartments();
  const totalAgents = departments.reduce((n, d) => n + d.members.length, 0);
  const okAgents = Object.values(status).filter((s) => s.last_status === "ok").length;
  const failedAgents = Object.values(status).filter((s) => s.last_status === "failed").length;

  const lastBriefingPreview = briefingRaw
    ? briefingRaw
        .split("\n")
        .slice(0, 12)
        .filter((l) => !l.startsWith("---"))
        .join("\n")
    : "(sem briefing — corre `python scripts/morning_briefing.py`)";

  return (
    <div className="p-8 space-y-6">
      <header className="flex items-end justify-between border-b border-[#1f1f3d] pb-4">
        <div>
          <h1 className="text-3xl font-light tracking-wide text-zinc-100">
            <span className="text-purple-400">◇</span> Home
          </h1>
          <p className="text-xs font-mono text-zinc-500 mt-1">
            LocalClaw · Phase EE shipped {new Date().toISOString().slice(0, 10)}
          </p>
        </div>
        <div className="text-right">
          <div className="text-xs font-mono uppercase tracking-wider text-cyan-300">
            {okAgents}/{totalAgents} agents ok
          </div>
          {failedAgents > 0 && (
            <div className="text-xs font-mono text-red-400">{failedAgents} failed</div>
          )}
        </div>
      </header>

      <HomeToolbar />

      <section className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          label="Portfolio BR"
          value={`R$ ${fmt(totalsBR.mv, 0)}`}
          sub={`${pnlPctBR >= 0 ? "+" : ""}${fmt(pnlPctBR, 2)}% vs cost`}
          tone={pnlPctBR >= 0 ? "ok" : "down"}
        />
        <StatCard
          label="Portfolio US"
          value={`US$ ${fmt(totalsUS.mv, 0)}`}
          sub={`${pnlPctUS >= 0 ? "+" : ""}${fmt(pnlPctUS, 2)}% vs cost`}
          tone={pnlPctUS >= 0 ? "ok" : "down"}
        />
        <StatCard
          label="Open Actions"
          value={String(actions.length)}
          sub="watchlist triggers"
          tone="purple"
        />
        <StatCard
          label="Antonio Carlos"
          value={`${chats.length} chats`}
          sub={`${chats.reduce((n, c) => n + c.n_messages, 0)} msgs`}
          tone="cyan"
        />
      </section>

      <section className="card p-5 rounded-lg">
        <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300 mb-3">
          📈 Portfolio P&amp;L over time
        </h2>
        <PortfolioChart />
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="card-purple p-5 lg:col-span-2 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300">
              ☀ Briefing matinal
            </h2>
            <span className="tag text-zinc-400">vault/dashboards</span>
          </div>
          <pre className="text-xs text-zinc-300 whitespace-pre-wrap font-mono leading-relaxed max-h-64 overflow-y-auto">
            {lastBriefingPreview}
          </pre>
        </div>

        <div className="card p-5 rounded-lg">
          <h2 className="text-sm font-mono uppercase tracking-wider text-zinc-400 mb-3">
            ◉ Agents
          </h2>
          <div className="space-y-1.5 max-h-64 overflow-y-auto">
            {Object.values(status)
              .sort((a, b) => (b.last_run || "").localeCompare(a.last_run || ""))
              .slice(0, 12)
              .map((s) => (
                <div
                  key={s.name}
                  className="flex items-center justify-between text-xs font-mono"
                >
                  <span className="flex items-center gap-2 truncate">
                    <span
                      className={`w-2 h-2 rounded-full inline-block ${statusDot(
                        s.last_status
                      )}`}
                    ></span>
                    <span className="text-zinc-300 truncate">{s.name}</span>
                  </span>
                  <span className="text-zinc-500 text-[10px]">
                    {(s.last_run || "").slice(0, 16)}
                  </span>
                </div>
              ))}
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="card p-5 rounded-lg">
          <h2 className="text-sm font-mono uppercase tracking-wider text-zinc-400 mb-3">
            ▤ Open actions <span className="text-purple-400">({actions.length})</span>
          </h2>
          <div className="space-y-2 max-h-72 overflow-y-auto">
            {actions.slice(0, 10).map((a) => (
              <Link
                key={`${a.market}-${a.id}`}
                href={`/ticker/${a.ticker}`}
                className="block border-l-2 border-purple-700/50 pl-3 py-1 hover:bg-purple-900/10"
              >
                <div className="flex items-center gap-2 text-xs">
                  <span className="font-mono text-cyan-300">{a.ticker}</span>
                  <span className="tag text-purple-300">{a.kind}</span>
                </div>
                <div className="text-xs text-zinc-400 truncate">{a.description}</div>
              </Link>
            ))}
            {actions.length === 0 && (
              <div className="text-xs text-zinc-500 italic">Sem triggers abertos.</div>
            )}
          </div>
        </div>

        <div className="card p-5 rounded-lg">
          <h2 className="text-sm font-mono uppercase tracking-wider text-zinc-400 mb-3">
            💸 Próximos dividendos (30d)
          </h2>
          <div className="space-y-1.5 max-h-72 overflow-y-auto">
            {dividends.slice(0, 12).map((d, i) => (
              <div
                key={`${d.market}-${d.ticker}-${d.ex_date}-${i}`}
                className="flex items-center justify-between text-xs font-mono"
              >
                <span className="text-zinc-300">
                  <span className="text-purple-300">{d.ticker}</span>
                </span>
                <span className="text-zinc-400">{d.ex_date.slice(5)}</span>
                <span className="text-cyan-300 tabular">
                  {d.market === "br" ? "R$" : "$"}
                  {fmt(d.amount, 4)}
                </span>
              </div>
            ))}
            {dividends.length === 0 && (
              <div className="text-xs text-zinc-500 italic">Nenhum próximo.</div>
            )}
          </div>
        </div>

        <div className="card-cyan p-5 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-mono uppercase tracking-wider text-cyan-300">
              ⚖ Council · Night Shift
            </h2>
            <Link
              href="/council"
              className="text-[10px] font-mono text-zinc-500 hover:text-cyan-300"
            >
              all {councilSummary.total} →
            </Link>
          </div>
          {councilSummary.total > 0 ? (
            <>
              <div className="text-[10px] font-mono text-zinc-500 mb-3">
                run {councilSummary.date}
              </div>
              <div className="grid grid-cols-4 gap-1.5 mb-4">
                <CountChip label="BUY" n={councilSummary.buy} tone="green" />
                <CountChip label="HOLD" n={councilSummary.hold} tone="yellow" />
                <CountChip label="AVOID" n={councilSummary.avoid} tone="red" />
                <CountChip label="?" n={councilSummary.needs_data} tone="zinc" />
              </div>

              {councilAvoid.length > 0 && (
                <div className="mb-3">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-red-300 mb-1">
                    AVOID
                  </div>
                  <div className="space-y-1">
                    {councilAvoid.map((e) => (
                      <Link
                        key={e.ticker}
                        href={`/council/${e.ticker}`}
                        className="flex items-center justify-between text-xs hover:bg-red-900/10 px-1.5 py-0.5 rounded"
                      >
                        <span className="font-mono text-red-300">{e.ticker}</span>
                        <span className="text-[10px] text-zinc-500">
                          {e.dissent_count}d · {e.flag_count}⚑
                        </span>
                      </Link>
                    ))}
                  </div>
                </div>
              )}

              {councilFlagged.length > 0 && (
                <div>
                  <div className="text-[10px] font-mono uppercase tracking-wider text-orange-300 mb-1">
                    Flagged (3+)
                  </div>
                  <div className="space-y-1">
                    {councilFlagged.map((e) => (
                      <Link
                        key={e.ticker}
                        href={`/council/${e.ticker}`}
                        className="flex items-center justify-between text-xs hover:bg-orange-900/10 px-1.5 py-0.5 rounded"
                      >
                        <span className="flex items-center gap-2">
                          <span className="font-mono text-orange-300">{e.ticker}</span>
                          <StancePill stance={e.stance} />
                        </span>
                        <span className="text-[10px] text-zinc-500">
                          {e.dissent_count}d · {e.flag_count}⚑
                        </span>
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="text-xs text-zinc-500 italic">
              Sem outputs do Council — corre <code>python -m agents.council.story &lt;TK&gt;</code>.
            </div>
          )}
          {dossiers.length > 0 && councilSummary.total === 0 && (
            <div className="mt-2 space-y-1">
              {dossiers.map((d) => (
                <div key={d.path} className="text-[10px] font-mono text-zinc-500">
                  {d.title} · {new Date(d.modified).toISOString().slice(0, 10)}
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

function CountChip({
  label,
  n,
  tone,
}: {
  label: string;
  n: number;
  tone: "green" | "yellow" | "red" | "zinc";
}) {
  const c =
    tone === "green"
      ? "border-green-700/50 text-green-300 bg-green-900/20"
      : tone === "yellow"
        ? "border-yellow-700/50 text-yellow-300 bg-yellow-900/20"
        : tone === "red"
          ? "border-red-700/50 text-red-300 bg-red-900/20"
          : "border-zinc-700/50 text-zinc-400 bg-zinc-900/40";
  return (
    <div className={`text-center px-1 py-1.5 rounded border ${c}`}>
      <div className="text-[9px] font-mono uppercase tracking-wider opacity-80">{label}</div>
      <div className="text-base font-light tabular">{n}</div>
    </div>
  );
}

function StatCard({
  label,
  value,
  sub,
  tone,
}: {
  label: string;
  value: string;
  sub: string;
  tone: "ok" | "down" | "purple" | "cyan";
}) {
  const valueColor =
    tone === "ok"
      ? "text-green-400"
      : tone === "down"
      ? "text-red-400"
      : tone === "cyan"
      ? "text-cyan-300"
      : "text-purple-300";
  return (
    <div className="card p-4 rounded-lg">
      <div className="text-[10px] font-mono uppercase tracking-wider text-zinc-500">
        {label}
      </div>
      <div className={`text-2xl font-light ${valueColor} mt-1 tabular`}>{value}</div>
      <div className="text-xs text-zinc-400 mt-1">{sub}</div>
    </div>
  );
}
