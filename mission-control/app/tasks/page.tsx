import { listOpenActions } from "@/lib/db";
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

  return (
    <div className="p-8 space-y-6">
      <header className="flex items-end justify-between border-b border-[#1f1f3d] pb-4">
        <div>
          <h1 className="text-3xl font-light text-zinc-100">
            <span className="text-purple-400">▤</span> Tasks
          </h1>
          <p className="text-xs font-mono text-zinc-500 mt-1">
            Open watchlist actions — clica APROVAR ou IGNORAR para resolver
          </p>
        </div>
        <div className="text-xs font-mono text-cyan-300 uppercase tracking-wider">
          {actions.length} open
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[...byKind.entries()].map(([kind, items]) => (
          <div key={kind} className="card p-4 rounded-lg">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300">
                {kind}
              </h2>
              <span className="tag text-zinc-400">{items.length}</span>
            </div>
            <div className="space-y-2 max-h-[28rem] overflow-y-auto">
              {items.map((a) => (
                <div
                  key={`${a.market}-${a.id}`}
                  className="border-l-2 border-purple-700/40 pl-3 py-2 hover:bg-purple-900/10 rounded-r"
                >
                  <div className="flex items-center gap-2 text-xs">
                    <span
                      className={`px-1.5 py-0.5 rounded text-[9px] font-mono ${
                        a.market === "br"
                          ? "bg-green-900/30 text-green-400"
                          : "bg-blue-900/30 text-blue-300"
                      }`}
                    >
                      {a.market.toUpperCase()}
                    </span>
                    <span className="font-mono text-cyan-300 font-medium">{a.ticker}</span>
                    <span className="text-[9px] text-zinc-500 ml-auto font-mono">
                      #{a.id}
                    </span>
                  </div>
                  <div className="text-xs text-zinc-300 mt-1">{a.description}</div>
                  <div className="flex items-center justify-between mt-2">
                    <div className="text-[10px] text-zinc-500 font-mono">
                      {(a.created_at || "").slice(0, 16)}
                    </div>
                    <TaskRowActions id={a.id} market={a.market} ticker={a.ticker} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
        {actions.length === 0 && (
          <div className="card p-12 rounded-lg col-span-full text-center text-zinc-500">
            <div className="text-4xl mb-2">▤</div>
            <p>Sem actions abertas. Os perpetuums e triggers vão criar quando houver sinal.</p>
          </div>
        )}
      </div>
    </div>
  );
}
