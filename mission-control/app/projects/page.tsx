import { listPhases, readConstitution } from "@/lib/vault";
import { formatDate } from "@/lib/format";
import { PageHeader, EmptyState } from "@/components/ui";

export const dynamic = "force-dynamic";

function statusTone(status: string): string {
  if (status.includes("SHIPPED") || status.includes("DONE") || status.includes("COMPLETE"))
    return "border-[rgba(34,197,94,0.3)] bg-[rgba(34,197,94,0.04)] text-[var(--verdict-buy)]";
  if (status.includes("IN PROGRESS"))
    return "border-[rgba(6,182,212,0.3)] bg-[rgba(6,182,212,0.04)] text-[var(--accent-glow)]";
  if (status.includes("PROPOSED") || status.includes("PLANNED"))
    return "border-[rgba(139,92,246,0.3)] bg-[rgba(139,92,246,0.04)] text-[var(--accent-primary)]";
  if (status.includes("DEFERRED"))
    return "border-[var(--border-subtle)] bg-[var(--bg-elevated)] text-[var(--text-tertiary)]";
  return "border-[var(--border-subtle)] bg-[var(--bg-elevated)] text-[var(--text-tertiary)]";
}

function statusGlyph(status: string): string {
  if (status.includes("SHIPPED") || status.includes("DONE") || status.includes("COMPLETE"))
    return "✓";
  if (status.includes("IN PROGRESS")) return "◐";
  if (status.includes("PROPOSED") || status.includes("PLANNED")) return "◯";
  if (status.includes("DEFERRED")) return "·";
  return "·";
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
    <div className="p-8 space-y-8 max-w-[1400px]">
      <PageHeader
        title="Projects"
        subtitle="Phase tracker do CONSTITUTION.md — cada Phase é um projecto"
        crumbs={[{ label: "Home", href: "/" }, { label: "Projects" }]}
      />

      <section>
        <h2 className="type-h3 mb-3">phases · {phases.length}</h2>
        {phases.length === 0 ? (
          <EmptyState
            icon="◯"
            title="Sem phases"
            description="Nenhuma Phase encontrada em CONSTITUTION.md."
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
            {phases.map((p, i) => (
              <div
                key={`${p.id}-${i}`}
                className={`p-4 rounded-lg border ${statusTone(p.status)}`}
              >
                <header className="flex items-center gap-2 mb-2">
                  <span aria-hidden className="text-base shrink-0">
                    {statusGlyph(p.status)}
                  </span>
                  <span className="type-mono-sm tracking-wider">{p.id}</span>
                  <span className="ml-auto type-mono-sm opacity-80">
                    {p.status}
                  </span>
                </header>
                <div className="type-body text-[var(--text-primary)]">{p.title}</div>
                {p.date && (
                  <div className="type-mono-sm text-[var(--text-tertiary)] mt-1">
                    {formatDate(p.date, "short")} · {formatDate(p.date, "relative")}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="card-purple p-5">
        <h2 className="type-h3 text-[var(--accent-primary)] mb-3">
          constitution outline
        </h2>
        <pre className="type-mono-sm text-[var(--text-secondary)] whitespace-pre-wrap leading-relaxed max-h-96 overflow-y-auto">
          {constitutionExcerpt || "(constitution não encontrada)"}
        </pre>
      </section>
    </div>
  );
}
