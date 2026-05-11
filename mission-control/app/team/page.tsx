import { listDepartments } from "@/lib/agents";
import { humanizeSchedule } from "@/lib/format";
import { PageHeader, Section, Pill } from "@/components/ui";

export const dynamic = "force-dynamic";

const MISSION =
  "Construir uma sala-de-controlo pessoal de investimentos 100% local — onde " +
  "agentes silenciosos vigiam B3 + NYSE/NASDAQ, propõem ações com critérios " +
  "verificáveis, e nunca escondem o raciocínio. Filosofia DRIP / Buffett / Graham. " +
  "In-house first: tudo que rode localmente não usa tokens Claude.";

function statusDot(s: string | null | undefined) {
  if (s === "ok") return "bg-[var(--verdict-buy)] dot-live";
  if (s === "no_action") return "bg-[var(--text-tertiary)]";
  if (s === "failed") return "bg-[var(--verdict-avoid)] dot-fail";
  return "bg-[var(--text-disabled)]";
}

export default function TeamPage() {
  const departments = listDepartments();
  const total = departments.reduce((n, d) => n + d.members.length, 0);
  const enabled = departments.reduce(
    (n, d) => n + d.members.filter((m) => m.enabled).length,
    0
  );

  // Find Antonio Carlos (Chief of Staff)
  const chief = departments
    .flatMap((d) => d.members)
    .find((m) => m.name === "antonio_carlos");

  return (
    <div className="p-8 space-y-8 max-w-[1400px]">
      <PageHeader
        title="Team"
        subtitle={`${enabled}/${total} agentes activos · ${departments.length} departamentos`}
        crumbs={[{ label: "Home", href: "/" }, { label: "Team" }]}
      />

      {/* Mission */}
      <section className="card-purple p-6">
        <div className="type-h3 text-[var(--accent-primary)] mb-3">mission</div>
        <p className="type-body text-[var(--text-primary)] italic leading-relaxed">
          &ldquo;{MISSION}&rdquo;
        </p>
      </section>

      {/* Founder + Chief */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="card-cyan p-5">
          <div className="type-h3 text-[var(--accent-glow)] mb-3">founder</div>
          <div className="flex items-center gap-3">
            <div
              className="w-12 h-12 rounded-full grid place-items-center type-h2"
              style={{ background: "rgba(6,182,212,0.15)" }}
            >
              <span aria-hidden>◉</span>
            </div>
            <div>
              <div className="type-body text-[var(--text-primary)] font-medium">
                Founder · Human
              </div>
              <div className="type-body-sm text-[var(--text-secondary)]">
                Decisões finais, capital, tese.
              </div>
            </div>
          </div>
        </div>

        {chief && (
          <div className="card-purple p-5">
            <div className="type-h3 text-[var(--accent-primary)] mb-3">
              chief of staff
            </div>
            <div className="flex items-center gap-3">
              <div
                className="w-12 h-12 rounded-full grid place-items-center type-h2"
                style={{ background: "rgba(139,92,246,0.15)" }}
              >
                <span aria-hidden>◈</span>
              </div>
              <div className="flex-1">
                <div className="type-body text-[var(--text-primary)] font-medium">
                  {chief.employee_name}{" "}
                  <span className="type-mono-sm text-[var(--accent-primary)]">
                    · {chief.title}
                  </span>
                </div>
                <div className="type-body-sm text-[var(--text-secondary)] line-clamp-2">
                  {chief.bio}
                </div>
              </div>
            </div>
          </div>
        )}
      </section>

      {/* Departments */}
      {departments.map((dept) => (
        <Section
          key={dept.name}
          label={dept.name}
          meta={`${dept.members.filter((m) => m.enabled).length}/${dept.members.length}`}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
            {dept.members.map((m) => (
              <div
                key={m.name}
                className="card p-4 hover:border-[var(--border-strong)] transition-colors"
              >
                <header className="flex items-center gap-2 mb-2">
                  <span
                    className={`w-1.5 h-1.5 rounded-full shrink-0 ${statusDot(
                      m.status?.last_status
                    )}`}
                    aria-hidden
                  />
                  <span className="type-body text-[var(--text-primary)] font-medium">
                    {m.employee_name}
                  </span>
                  {!m.enabled && (
                    <Pill variant="neutral" className="ml-auto">
                      disabled
                    </Pill>
                  )}
                </header>
                <div className="type-mono-sm text-[var(--accent-glow)] mb-1.5">
                  {m.title}
                </div>
                <p className="type-body-sm text-[var(--text-secondary)] line-clamp-3">
                  {m.bio}
                </p>
                <footer className="flex items-center justify-between mt-2 type-mono-sm text-[var(--text-tertiary)]">
                  <span>↳ {m.reports_to}</span>
                  <span>{humanizeSchedule(m.schedule)}</span>
                </footer>
                {m.status && m.status.run_count > 0 && (
                  <div className="mt-1 type-mono-sm text-[var(--text-tertiary)]">
                    {m.status.run_count} runs ·{" "}
                    {m.status.failed_count > 0 ? (
                      <span className="text-[var(--verdict-avoid)]">
                        {m.status.failed_count} failed
                      </span>
                    ) : (
                      <span className="text-[var(--verdict-buy)]">no fails</span>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </Section>
      ))}
    </div>
  );
}
