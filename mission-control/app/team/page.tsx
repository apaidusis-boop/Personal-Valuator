import { listDepartments } from "@/lib/agents";

export const dynamic = "force-dynamic";

const MISSION =
  "Construir uma sala-de-controlo pessoal de investimentos 100% local — onde " +
  "agentes silenciosos vigiam B3 + NYSE/NASDAQ, propõem ações com critérios " +
  "verificáveis, e nunca escondem o raciocínio. Filosofia DRIP / Buffett / Graham. " +
  "In-house first: tudo que rode localmente não usa tokens Claude.";

function statusDot(s: string | null | undefined) {
  if (s === "ok") return "bg-green-400 dot-live";
  if (s === "no_action") return "bg-zinc-500";
  if (s === "failed") return "bg-red-400 dot-fail";
  return "bg-zinc-700";
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
    <div className="p-8 space-y-6">
      <header className="flex items-end justify-between border-b border-[#1f1f3d] pb-4">
        <div>
          <h1 className="text-3xl font-light text-zinc-100">
            <span className="text-purple-400">◉</span> Team
          </h1>
          <p className="text-xs font-mono text-zinc-500 mt-1">
            {enabled}/{total} agentes activos · {departments.length} departamentos
          </p>
        </div>
      </header>

      {/* Mission */}
      <section className="card-purple p-6 rounded-lg">
        <div className="text-[10px] font-mono uppercase tracking-[0.2em] text-purple-400 mb-3">
          MISSION
        </div>
        <p className="text-zinc-200 italic leading-relaxed text-lg">
          &ldquo;{MISSION}&rdquo;
        </p>
      </section>

      {/* Founder + Chief */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="card-cyan p-5 rounded-lg">
          <div className="text-[10px] font-mono uppercase tracking-[0.2em] text-cyan-300 mb-3">
            Founder
          </div>
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-cyan-900/40 grid place-items-center text-2xl">
              👤
            </div>
            <div>
              <div className="text-zinc-100 font-medium">Founder · Human</div>
              <div className="text-xs text-zinc-400">
                Decisões finais, capital, tese.
              </div>
            </div>
          </div>
        </div>

        {chief && (
          <div className="card-purple p-5 rounded-lg">
            <div className="text-[10px] font-mono uppercase tracking-[0.2em] text-purple-300 mb-3">
              Chief of Staff
            </div>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-purple-900/40 grid place-items-center text-2xl">
                🐙
              </div>
              <div className="flex-1">
                <div className="text-zinc-100 font-medium">
                  {chief.employee_name}{" "}
                  <span className="text-purple-300 text-sm font-mono">
                    · {chief.title}
                  </span>
                </div>
                <div className="text-xs text-zinc-400">{chief.bio}</div>
              </div>
            </div>
          </div>
        )}
      </section>

      {/* Departments */}
      <section className="space-y-4">
        {departments.map((dept) => (
          <div key={dept.name} className="card p-5 rounded-lg">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300">
                {dept.name}
              </h2>
              <span className="tag text-zinc-400">{dept.members.length}</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {dept.members.map((m) => (
                <div
                  key={m.name}
                  className="border border-[#1f1f3d] rounded-md p-3 hover:border-purple-700/50 transition-colors"
                >
                  <div className="flex items-center gap-2 mb-2">
                    <span
                      className={`w-2 h-2 rounded-full ${statusDot(
                        m.status?.last_status
                      )}`}
                    ></span>
                    <span className="text-zinc-100 font-medium text-sm">
                      {m.employee_name}
                    </span>
                    {!m.enabled && (
                      <span className="ml-auto tag text-zinc-500">disabled</span>
                    )}
                  </div>
                  <div className="text-[11px] font-mono text-cyan-300 mb-1">{m.title}</div>
                  <div className="text-xs text-zinc-400 line-clamp-3">{m.bio}</div>
                  <div className="flex items-center justify-between mt-2 text-[10px] font-mono text-zinc-500">
                    <span>↳ reports to {m.reports_to}</span>
                    <span>{m.schedule}</span>
                  </div>
                  {m.status && (
                    <div className="mt-1 text-[10px] font-mono text-zinc-500">
                      runs {m.status.run_count} · failed {m.status.failed_count}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
