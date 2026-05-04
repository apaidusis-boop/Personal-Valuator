import Link from "next/link";

import { listOpenActions, listPortfolio, upcomingDividends, listChatIds } from "@/lib/db";
import { loadAgentStatus } from "@/lib/agents";
import {
  listDossiers,
  readBriefingMeta,
  listCouncilOutputs,
  summariseCouncil,
} from "@/lib/vault";
import { formatCurrency, formatDate, formatNumber, formatPercent } from "@/lib/format";

import HomeToolbar from "@/components/toolbar";
import { PortfolioChart } from "@/components/charts";
import StancePill from "@/components/stance-pill";
import TaskRowActions from "./tasks/row-actions";

import { PageHeader, Section, Stat, Pill } from "@/components/ui";

export const dynamic = "force-dynamic";

export default function Home() {
  const portfolio = listPortfolio();
  const actions = listOpenActions(20);
  const dividends = upcomingDividends(30);
  const status = loadAgentStatus();
  const chats = listChatIds();
  const dossiers = listDossiers(5);
  const { content: briefingRaw, mtime: briefingMtime } = readBriefingMeta();
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

  const okAgents = Object.values(status).filter((s) => s.last_status === "ok").length;
  const failedAgents = Object.values(status).filter((s) => s.last_status === "failed").length;
  const totalAgents = Object.keys(status).length;

  // Briefing preview — strip front matter + first heading line, keep paragraph
  const briefingPreview = briefingRaw
    ? briefingRaw
        .split("\n")
        .filter((l) => !l.startsWith("---"))
        .slice(0, 14)
        .join("\n")
        .trim()
    : null;

  return (
    <div className="p-8 space-y-8 max-w-[1400px]">
      <PageHeader
        title="Home"
        subtitle={`${okAgents}/${totalAgents} agents online · ${chats.length} active chats`}
        freshness={briefingMtime}
        freshnessLabel={briefingMtime ? `briefing ${formatDate(briefingMtime, "relative")}` : undefined}
        actions={
          failedAgents > 0 ? (
            <Pill variant="avoid">⚑ {failedAgents} failed</Pill>
          ) : null
        }
      />

      <HomeToolbar />

      {/* Stats — 4 quadrants */}
      <section className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Stat
          label="Portfolio BR"
          value={formatCurrency(totalsBR.mv, "BRL", 0)}
          delta={{ value: pnlPctBR, format: "percent" }}
          caption="vs cost"
          icon="◇"
        />
        <Stat
          label="Portfolio US"
          value={formatCurrency(totalsUS.mv, "USD", 0)}
          delta={{ value: pnlPctUS, format: "percent" }}
          caption="vs cost"
          icon="◇"
        />
        <Stat
          label="Open Actions"
          value={formatNumber(actions.length)}
          caption="watchlist triggers"
          icon="▤"
        />
        <Stat
          label="Council Today"
          value={formatNumber(councilSummary.total)}
          caption={
            councilSummary.total > 0
              ? `${councilSummary.avoid} AVOID · ${councilSummary.hold} HOLD · ${councilSummary.buy} BUY`
              : "no run yet"
          }
          icon="⚖"
        />
      </section>

      {/* Portfolio chart */}
      <Section
        label="Portfolio P&L"
        meta="all positions · BRL+USD aggregated"
      >
        <div className="card p-5">
          <PortfolioChart />
        </div>
      </Section>

      {/* Briefing + Actions row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Section
          label="Briefing matinal"
          meta={briefingMtime ? formatDate(briefingMtime, "relative") : "n/a"}
        >
          <div className="card-purple p-5">
            {briefingPreview ? (
              <pre className="type-body-sm text-[var(--text-primary)] whitespace-pre-wrap font-sans leading-relaxed max-h-72 overflow-y-auto">
                {briefingPreview}
              </pre>
            ) : (
              <p className="type-body-sm text-[var(--text-tertiary)] italic">
                Sem briefing matinal disponível. Aurora gera às 07:00 (BRT).
              </p>
            )}
          </div>
        </Section>

        <Section
          label="Actions priority"
          meta={`${actions.length} open`}
          action={
            <Link
              href="/tasks"
              className="type-mono-sm text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors"
            >
              view all →
            </Link>
          }
        >
          <div className="card p-4 space-y-2 max-h-72 overflow-y-auto">
            {actions.slice(0, 5).map((a) => (
              <ActionItem key={`${a.market}-${a.id}`} action={a} />
            ))}
            {actions.length === 0 && (
              <p className="type-body-sm text-[var(--text-tertiary)] italic px-2 py-3">
                Nenhum trigger aberto.
              </p>
            )}
          </div>
        </Section>

        <Section
          label="Council snapshot"
          meta={
            councilSummary.total > 0
              ? formatDate(councilSummary.date, "relative")
              : "n/a"
          }
          action={
            <Link
              href="/council"
              className="type-mono-sm text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors"
            >
              full council →
            </Link>
          }
        >
          <div className="card-cyan p-5">
            {councilSummary.total > 0 ? (
              <CouncilCard
                avoid={councilAvoid}
                flagged={councilFlagged}
                buy={councilSummary.buy}
                hold={councilSummary.hold}
                avoidCount={councilSummary.avoid}
                needs={councilSummary.needs_data}
              />
            ) : (
              <div>
                <p className="type-body-sm text-[var(--text-tertiary)] italic mb-3">
                  Nenhum output do Council ainda.
                </p>
                {dossiers.length > 0 && (
                  <ul className="space-y-1">
                    {dossiers.map((d) => (
                      <li
                        key={d.path}
                        className="type-mono-sm text-[var(--text-tertiary)]"
                      >
                        {d.title}{" "}
                        <span className="text-[var(--text-disabled)]">
                          · {formatDate(d.modified, "relative")}
                        </span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        </Section>
      </div>

      {/* Dividends + Agents row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Section
          label="Próximos dividendos"
          meta="next 30 days"
        >
          <div className="card p-4 max-h-80 overflow-y-auto">
            {dividends.length > 0 ? (
              <table className="w-full">
                <thead className="type-mono-sm text-[var(--text-tertiary)]">
                  <tr>
                    <th className="text-left pb-2">ticker</th>
                    <th className="text-left pb-2">ex-date</th>
                    <th className="text-right pb-2">amount</th>
                  </tr>
                </thead>
                <tbody className="type-mono">
                  {dividends.slice(0, 16).map((d, i) => (
                    <tr
                      key={`${d.market}-${d.ticker}-${d.ex_date}-${i}`}
                      className="border-t border-[var(--border-subtle)]"
                    >
                      <td className="py-1.5">
                        <Link
                          href={`/ticker/${d.ticker}`}
                          className="text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors"
                        >
                          {d.ticker}
                        </Link>
                        <Pill
                          variant={d.market === "br" ? "mkt-br" : "mkt-us"}
                          className="ml-2"
                        >
                          {d.market.toUpperCase()}
                        </Pill>
                      </td>
                      <td className="py-1.5 text-[var(--text-secondary)]">
                        {formatDate(d.ex_date, "short")}
                      </td>
                      <td className="py-1.5 text-right text-[var(--text-primary)]">
                        {d.market === "br" ? "R$" : "$"}
                        {d.amount.toFixed(d.market === "br" ? 4 : 3)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="type-body-sm text-[var(--text-tertiary)] italic px-2 py-4">
                Nenhum próximo dividendo em 30 dias.
              </p>
            )}
          </div>
        </Section>

        <Section
          label="Agents"
          meta={`${okAgents}/${totalAgents} ok`}
          action={
            <Link
              href="/team"
              className="type-mono-sm text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors"
            >
              org chart →
            </Link>
          }
        >
          <div className="card p-4 max-h-80 overflow-y-auto">
            <ul className="space-y-1.5">
              {Object.values(status)
                .sort((a, b) => (b.last_run || "").localeCompare(a.last_run || ""))
                .slice(0, 14)
                .map((s) => (
                  <li
                    key={s.name}
                    className="flex items-center justify-between type-mono-sm"
                  >
                    <span className="flex items-center gap-2 truncate min-w-0">
                      <StatusDot status={s.last_status} />
                      <span className="text-[var(--text-primary)] truncate">
                        {s.name}
                      </span>
                    </span>
                    <span className="text-[var(--text-tertiary)] shrink-0 ml-2">
                      {s.last_run
                        ? formatDate(s.last_run, "relative")
                        : "—"}
                    </span>
                  </li>
                ))}
            </ul>
          </div>
        </Section>
      </div>
    </div>
  );
}

function StatusDot({ status }: { status: string | null | undefined }) {
  const cls =
    status === "ok"
      ? "bg-[var(--verdict-buy)] dot-live"
      : status === "no_action"
      ? "bg-[var(--text-tertiary)]"
      : status === "failed"
      ? "bg-[var(--verdict-avoid)] dot-fail"
      : "bg-[var(--text-disabled)]";
  return <span className={`w-1.5 h-1.5 rounded-full inline-block shrink-0 ${cls}`} aria-hidden />;
}

function ActionItem({ action }: { action: { id: number; market: "br" | "us"; ticker: string; kind: string; description: string; created_at: string } }) {
  return (
    <div className="border-l-2 border-[var(--border-strong)] pl-3 py-2 hover:bg-[var(--bg-overlay)] rounded-r transition-colors">
      <div className="flex items-center gap-2 mb-1">
        <Link
          href={`/ticker/${action.ticker}`}
          className="type-mono text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors"
        >
          {action.ticker}
        </Link>
        <Pill variant={action.market === "br" ? "mkt-br" : "mkt-us"}>
          {action.market.toUpperCase()}
        </Pill>
        <Pill variant="purple">{action.kind}</Pill>
        <span className="type-mono-sm text-[var(--text-tertiary)] ml-auto">
          {formatDate(action.created_at, "relative")}
        </span>
      </div>
      <p className="type-body-sm text-[var(--text-secondary)] line-clamp-2 mb-2">
        {action.description}
      </p>
      <TaskRowActions
        id={action.id}
        market={action.market}
        ticker={action.ticker}
      />
    </div>
  );
}

function CouncilCard({
  avoid,
  flagged,
  buy,
  hold,
  avoidCount,
  needs,
}: {
  avoid: any[];
  flagged: any[];
  buy: number;
  hold: number;
  avoidCount: number;
  needs: number;
}) {
  return (
    <div className="space-y-4">
      {/* counts row */}
      <div className="grid grid-cols-4 gap-2 text-center">
        <CountBox label="BUY" n={buy} variant="buy" />
        <CountBox label="HOLD" n={hold} variant="hold" />
        <CountBox label="AVOID" n={avoidCount} variant="avoid" />
        <CountBox label="N/A" n={needs} variant="na" />
      </div>

      {avoid.length > 0 && (
        <div>
          <h4 className="type-h3 mb-1.5">avoid</h4>
          <ul className="space-y-1">
            {avoid.slice(0, 5).map((e) => (
              <li key={e.ticker}>
                <Link
                  href={`/council/${e.ticker}`}
                  className="flex items-center justify-between text-sm hover:bg-[var(--bg-overlay)] px-2 py-1 rounded transition-colors"
                >
                  <span className="type-mono text-[var(--verdict-avoid)]">
                    {e.ticker}
                  </span>
                  <span className="type-mono-sm text-[var(--text-tertiary)]">
                    {e.dissent_count}d · {e.flag_count}⚑
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}

      {flagged.length > 0 && (
        <div>
          <h4 className="type-h3 mb-1.5">flagged (3+)</h4>
          <ul className="space-y-1">
            {flagged.slice(0, 4).map((e) => (
              <li key={e.ticker}>
                <Link
                  href={`/council/${e.ticker}`}
                  className="flex items-center justify-between text-sm hover:bg-[var(--bg-overlay)] px-2 py-1 rounded transition-colors"
                >
                  <span className="flex items-center gap-2">
                    <span className="type-mono text-[var(--text-primary)]">
                      {e.ticker}
                    </span>
                    <StancePill stance={e.stance} />
                  </span>
                  <span className="type-mono-sm text-[var(--text-tertiary)]">
                    {e.dissent_count}d · {e.flag_count}⚑
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function CountBox({
  label,
  n,
  variant,
}: {
  label: string;
  n: number;
  variant: "buy" | "hold" | "avoid" | "na";
}) {
  const cls =
    variant === "buy"
      ? "border-[rgba(34,197,94,0.3)] text-[var(--verdict-buy)]"
      : variant === "hold"
      ? "border-[rgba(245,158,11,0.3)] text-[var(--verdict-hold)]"
      : variant === "avoid"
      ? "border-[rgba(239,68,68,0.3)] text-[var(--verdict-avoid)]"
      : "border-[var(--border-subtle)] text-[var(--text-tertiary)]";
  return (
    <div className={`px-2 py-2 rounded border ${cls}`}>
      <div className="type-mono-sm opacity-70">{label}</div>
      <div className="type-h2 tabular">{n}</div>
    </div>
  );
}
