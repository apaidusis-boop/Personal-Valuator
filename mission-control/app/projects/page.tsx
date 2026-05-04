import { listPhases, readConstitution } from "@/lib/vault";

export const dynamic = "force-dynamic";

function statusTone(status: string): string {
  if (status.includes("SHIPPED") || status.includes("DONE") || status.includes("COMPLETE"))
    return "border-green-700/40 bg-green-900/10 text-green-300";
  if (status.includes("IN PROGRESS"))
    return "border-cyan-700/40 bg-cyan-900/10 text-cyan-300";
  if (status.includes("PROPOSED") || status.includes("PLANNED"))
    return "border-purple-700/40 bg-purple-900/10 text-purple-300";
  if (status.includes("DEFERRED"))
    return "border-zinc-700 bg-zinc-900/40 text-zinc-400";
  return "border-zinc-700 bg-zinc-900/40 text-zinc-400";
}

export default function ProjectsPage() {
  const phases = listPhases();
  const constitution = readConstitution();
  const constitutionExcerpt =
    constitution
      ?.split("\n")
      .filter((l) => l.startsWith("# ") || l.startsWith("## "))
      .slice(0, 30)
      .join("\n") || "";

  return (
    <div className="p-8 space-y-6">
      <header className="border-b border-[#1f1f3d] pb-4">
        <h1 className="text-3xl font-light text-zinc-100">
          <span className="text-purple-400">❑</span> Projects
        </h1>
        <p className="text-xs font-mono text-zinc-500 mt-1">
          Phase tracker do CONSTITUTION.md — cada Phase é um projecto.
        </p>
      </header>

      <section>
        <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300 mb-3">
          Phases ({phases.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {phases.map((p, i) => (
            <div
              key={`${p.id}-${i}`}
              className={`p-4 rounded-lg border ${statusTone(p.status)}`}
            >
              <div className="flex items-center gap-2 mb-2">
                <span className="font-mono text-xs tracking-wider">{p.id}</span>
                <span className="ml-auto text-[9px] font-mono uppercase tracking-wider opacity-80">
                  {p.status}
                </span>
              </div>
              <div className="text-sm text-zinc-200">{p.title}</div>
              {p.date && (
                <div className="text-[10px] font-mono text-zinc-500 mt-1">{p.date}</div>
              )}
            </div>
          ))}
          {phases.length === 0 && (
            <div className="col-span-full card p-12 rounded-lg text-center text-zinc-500">
              Nenhuma Phase encontrada em CONSTITUTION.md.
            </div>
          )}
        </div>
      </section>

      <section className="card-purple p-5 rounded-lg">
        <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300 mb-3">
          Constitution outline
        </h2>
        <pre className="text-xs text-zinc-300 font-mono whitespace-pre-wrap leading-relaxed max-h-96 overflow-y-auto">
          {constitutionExcerpt || "(constitution não encontrada)"}
        </pre>
      </section>
    </div>
  );
}
