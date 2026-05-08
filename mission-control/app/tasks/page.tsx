import type { Metadata } from "next";
import Link from "next/link";

import { listOpenActions } from "@/lib/db";
import { formatDate } from "@/lib/format";
import { Pill } from "@/components/ui";
import TaskRowActions from "./row-actions";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Tasks · Mission Control" };

export default function TasksPage() {
  const actions = listOpenActions(120);
  const byKind = new Map<string, typeof actions>();
  for (const a of actions) {
    const k = a.kind || "misc";
    if (!byKind.has(k)) byKind.set(k, []);
    byKind.get(k)!.push(a);
  }

  const latestTs = actions.reduce<string>((acc, a) => {
    return (a.created_at || "") > acc ? a.created_at : acc;
  }, "");

  return (
    <div className="p-5 space-y-5">
      {/* Header --------------------------------------------- */}
      <div>
        <h1
          className="font-display text-xl font-bold"
          style={{ color: "var(--text-primary)" }}
        >
          Tasks
        </h1>
        <p
          className="text-xs mt-0.5"
          style={{ color: "var(--text-tertiary)" }}
        >
          {actions.length > 0
            ? `${actions.length} watchlist actions abertas · último ${formatDate(latestTs, "relative")}`
            : "watchlist actions"}
        </p>
      </div>

      {actions.length === 0 ? (
        <div
          className="p-12 rounded text-center space-y-2"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <p
            className="text-sm"
            style={{ color: "var(--text-secondary)" }}
          >
            Nenhuma action aberta
          </p>
          <p
            className="text-xs italic"
            style={{ color: "var(--text-tertiary)" }}
          >
            Quando os perpetuums ou triggers detectarem um sinal vão aparecer aqui.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
          {[...byKind.entries()]
            .sort((a, b) => b[1].length - a[1].length)
            .map(([kind, items]) => (
              <section
                key={kind}
                className="rounded overflow-hidden"
                style={{
                  background: "var(--bg-elevated)",
                  border: "1px solid var(--border-subtle)",
                }}
              >
                <div
                  className="px-4 py-3 flex items-center justify-between"
                  style={{
                    borderBottom: "1px solid var(--border-subtle)",
                  }}
                >
                  <h2
                    className="text-sm font-semibold"
                    style={{ color: "var(--text-primary)" }}
                  >
                    {kind}
                  </h2>
                  <span
                    className="text-[10px] font-data px-1.5 py-0.5 rounded"
                    style={{
                      background: "var(--bg-overlay)",
                      color: "var(--text-tertiary)",
                    }}
                  >
                    {items.length}
                  </span>
                </div>
                <div className="p-3 space-y-2 max-h-[28rem] overflow-y-auto">
                  {items.map((a) => (
                    <article
                      key={`${a.market}-${a.id}`}
                      className="pl-3 py-2 rounded transition-colors"
                      style={{
                        borderLeft: "2px solid var(--border-strong)",
                      }}
                    >
                      <header className="flex items-center gap-2 mb-1">
                        <Pill
                          variant={a.market === "br" ? "mkt-br" : "mkt-us"}
                        >
                          {a.market.toUpperCase()}
                        </Pill>
                        <Link
                          href={`/ticker/${a.ticker}`}
                          className="text-sm font-data font-bold hover:underline"
                          style={{ color: "var(--text-primary)" }}
                        >
                          {a.ticker}
                        </Link>
                        <span
                          className="text-[10px] font-data ml-auto"
                          style={{ color: "var(--text-disabled)" }}
                        >
                          #{a.id}
                        </span>
                      </header>
                      <p
                        className="text-xs leading-snug mb-2 line-clamp-3"
                        style={{ color: "var(--text-secondary)" }}
                      >
                        {a.description}
                      </p>
                      <footer className="flex items-center justify-between gap-2">
                        <span
                          className="text-[10px]"
                          style={{ color: "var(--text-tertiary)" }}
                        >
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
              </section>
            ))}
        </div>
      )}
    </div>
  );
}
