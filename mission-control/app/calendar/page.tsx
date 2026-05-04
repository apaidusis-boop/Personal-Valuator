import { loadPersonas } from "@/lib/agents";
import { upcomingDividends } from "@/lib/db";

export const dynamic = "force-dynamic";

const SCHEDULE_TONE: Record<string, string> = {
  daily: "bg-purple-900/30 text-purple-300 border-purple-700/40",
  weekly: "bg-cyan-900/30 text-cyan-300 border-cyan-700/40",
  every: "bg-green-900/20 text-green-300 border-green-700/40",
  manual: "bg-zinc-900/40 text-zinc-500 border-zinc-700",
};

function tone(schedule: string): string {
  if (schedule.startsWith("daily")) return SCHEDULE_TONE.daily;
  if (schedule.startsWith("weekly")) return SCHEDULE_TONE.weekly;
  if (schedule.startsWith("every")) return SCHEDULE_TONE.every;
  return SCHEDULE_TONE.manual;
}

export default function CalendarPage() {
  const personas = loadPersonas().filter((p) => p.enabled);
  const dividends = upcomingDividends(60);

  // Group by schedule kind
  const groups: Record<string, typeof personas> = {
    daily: [],
    weekly: [],
    every: [],
    manual: [],
  };
  for (const p of personas) {
    const k = p.schedule.startsWith("daily")
      ? "daily"
      : p.schedule.startsWith("weekly")
      ? "weekly"
      : p.schedule.startsWith("every")
      ? "every"
      : "manual";
    groups[k].push(p);
  }

  return (
    <div className="p-8 space-y-6">
      <header className="border-b border-[#1f1f3d] pb-4">
        <h1 className="text-3xl font-light text-zinc-100">
          <span className="text-purple-400">▦</span> Calendar
        </h1>
        <p className="text-xs font-mono text-zinc-500 mt-1">
          Cron schedules dos agents + ex-dividend calendar.
        </p>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-4 gap-3">
        {(["daily", "weekly", "every", "manual"] as const).map((k) => (
          <div key={k} className="card p-4 rounded-lg">
            <h2 className="text-sm font-mono uppercase tracking-wider text-zinc-400 mb-3">
              {k} <span className="text-purple-400">({groups[k].length})</span>
            </h2>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {groups[k].map((p) => (
                <div
                  key={p.name}
                  className={`p-2 rounded border ${tone(p.schedule)}`}
                >
                  <div className="text-xs text-zinc-200 font-medium">
                    {p.employee_name}
                  </div>
                  <div className="text-[10px] text-zinc-500 font-mono">{p.title}</div>
                  <div className="text-[10px] font-mono mt-1 opacity-80">
                    {p.schedule}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </section>

      <section className="card-cyan p-5 rounded-lg">
        <h2 className="text-sm font-mono uppercase tracking-wider text-cyan-300 mb-3">
          💸 Próximos ex-dividend dates (60d) — {dividends.length}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
          {dividends.map((d, i) => (
            <div
              key={`${d.market}-${d.ticker}-${d.ex_date}-${i}`}
              className="flex items-center justify-between text-xs p-2 border border-[#1f1f3d] rounded font-mono"
            >
              <span className="text-purple-300">{d.ticker}</span>
              <span className="text-zinc-400">{d.ex_date}</span>
              <span className="text-cyan-300 tabular">
                {d.market === "br" ? "R$" : "$"}
                {d.amount.toFixed(4)}
              </span>
            </div>
          ))}
          {dividends.length === 0 && (
            <div className="col-span-full text-zinc-500 italic text-sm py-6 text-center">
              Sem ex-dates conhecidos nos próximos 60 dias.
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
