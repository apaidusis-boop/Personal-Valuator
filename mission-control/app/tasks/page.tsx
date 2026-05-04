import Link from "next/link";

import { listOpenActions } from "@/lib/db";
import { formatDate } from "@/lib/format";
import { PageHeader, Section, Pill, EmptyState } from "@/components/ui";
import TaskRowActions from "./row-actions";

export const dynamic = "force-dynamic";

export default function TasksPage() {
  const actions = listOpenActions(120);
  const byKind = new Map<string, typeof actions>();
  for (const a of actions) {
    const k = a.kind || "misc";
    if (!byKind.has(k)) byKind.set(k, []);
    byKind.get(k)!.push(a);
  }

  // Latest creation timestamp for freshness pill
  const latestTs = actions.reduce<string>((acc, a) => {
    return (a.created_at || "") > acc ? a.created_at : acc;
  }, "");

  return (
    <div className="p-8 space-y-8 max-w-[1400px]">
      <PageHeader
        title="Tasks"
        subtitle="Watchlist actions abertas — clica APROVAR ou IGNORAR para resolver"
        crumbs={[{ label: "Home", href: "/" }, { label: "Tasks" }]}
        freshness={latestTs || null}
        freshnessLabel={
          actions.length > 0
            ? `${actions.length} open · last ${formatDate(latestTs, "relative")}`
            : undefined
        }
      />

      {actions.length === 0 ? (
        <EmptyState
          icon="◯"
          title="Nenhuma action aberta"
          description="Quando os perpetuums ou triggers detectarem um sinal, vão aparecer aqui."
        />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {[...byKind.entries()]
            .sort((a, b) => b[1].length - a[1].length)
            .map(([kind, items]) => (
              <Section
                key={kind}
                label={kind}
                meta={`${items.length}`}
              >
                <div className="card p-4 space-y-2 max-h-[28rem] overflow-y-auto">
                  {items.map((a) => (
                    <article
                      key={`${a.market}-${a.id}`}
                      className="border-l-2 border-[var(--border-strong)] pl-3 py-2 hover:bg-[var(--bg-overlay)] rounded-r transition-colors"
                    >
                      <header className="flex items-center gap-2 mb-1">
                        <Pill variant={a.market === "br" ? "mkt-br" : "mkt-us"}>
                          {a.market.toUpperCase()}
                        </Pill>
                        <Link
                          href={`/ticker/${a.ticker}`}
                          className="type-mono text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors font-medium"
                        >
                          {a.ticker}
                        </Link>
                        <span className="type-mono-sm text-[var(--text-disabled)] ml-auto">
                          #{a.id}
                        </span>
                      </header>
                      <p className="type-body-sm text-[var(--text-secondary)] mb-2 line-clamp-3">
                        {a.description}
                      </p>
                      <footer className="flex items-center justify-between gap-2">
                        <span className="type-mono-sm text-[var(--text-tertiary)]">
                          {formatDate(a.created_at, "relative")}
                        </span>
                        <TaskRowActions
                          id={a.id}
                          market={a.market}
                          ticker={a.ticker}
                        />
                      </footer>
                    </article>
                  ))}
                </div>
              </Section>
            ))}
        </div>
      )}
    </div>
  );
}
