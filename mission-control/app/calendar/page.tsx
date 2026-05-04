import Link from "next/link";

import { loadPersonas } from "@/lib/agents";
import { upcomingDividends } from "@/lib/db";
import { formatDate, humanizeSchedule } from "@/lib/format";
import {
  PageHeader,
  Section,
  Pill,
  pillVariantFromMarket,
  EmptyState,
} from "@/components/ui";

export const dynamic = "force-dynamic";

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
    <div className="p-8 space-y-8 max-w-[1400px]">
      <PageHeader
        title="Calendar"
        subtitle="Cron schedules dos agentes + ex-dividend calendar"
        crumbs={[{ label: "Home", href: "/" }, { label: "Calendar" }]}
      />

      <Section label="Agent schedules" meta={`${personas.length} active`}>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          {(["daily", "weekly", "every", "manual"] as const).map((k) => (
            <div key={k} className="card p-4">
              <header className="flex items-center justify-between mb-3">
                <h3 className="type-h3">{k}</h3>
                <span className="type-mono-sm text-[var(--text-tertiary)]">
                  {groups[k].length}
                </span>
              </header>
              <ul className="space-y-2 max-h-96 overflow-y-auto">
                {groups[k].map((p) => (
                  <li
                    key={p.name}
                    className="border-l-2 border-[var(--border-strong)] pl-3 py-1.5 hover:bg-[var(--bg-overlay)] rounded-r transition-colors"
                  >
                    <div className="type-body-sm text-[var(--text-primary)] font-medium">
                      {p.employee_name}
                    </div>
                    <div className="type-mono-sm text-[var(--text-tertiary)]">
                      {p.title}
                    </div>
                    <div className="type-mono-sm text-[var(--accent-glow)] mt-1">
                      {humanizeSchedule(p.schedule)}
                    </div>
                  </li>
                ))}
                {groups[k].length === 0 && (
                  <li className="type-mono-sm text-[var(--text-disabled)] italic px-2 py-2">
                    none
                  </li>
                )}
              </ul>
            </div>
          ))}
        </div>
      </Section>

      <Section
        label="Ex-dividend dates"
        meta={`next 60 days · ${dividends.length}`}
      >
        {dividends.length === 0 ? (
          <EmptyState
            icon="◯"
            title="Sem ex-dividend dates"
            description="Nenhum dividendo ex-date conhecido nos próximos 60 dias."
          />
        ) : (
          <div className="card overflow-hidden">
            <div className="max-h-[28rem] overflow-y-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-[var(--border-subtle)] sticky top-0 bg-[var(--bg-elevated)]">
                    <th className="text-left type-h3 px-4 py-2.5">ticker</th>
                    <th className="text-left type-h3 px-4 py-2.5">market</th>
                    <th className="text-left type-h3 px-4 py-2.5">ex-date</th>
                    <th className="text-right type-h3 px-4 py-2.5">amount</th>
                  </tr>
                </thead>
                <tbody className="type-mono">
                  {dividends.map((d, i) => (
                    <tr
                      key={`${d.market}-${d.ticker}-${d.ex_date}-${i}`}
                      className="border-b border-[var(--border-subtle)] last:border-b-0 hover:bg-[var(--bg-overlay)] transition-colors"
                    >
                      <td className="px-4 py-2">
                        <Link
                          href={`/ticker/${d.ticker}`}
                          className="text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors"
                        >
                          {d.ticker}
                        </Link>
                      </td>
                      <td className="px-4 py-2">
                        <Pill variant={pillVariantFromMarket(d.market)}>
                          {d.market.toUpperCase()}
                        </Pill>
                      </td>
                      <td className="px-4 py-2 text-[var(--text-secondary)]">
                        {formatDate(d.ex_date, "short")}
                        <span className="text-[var(--text-disabled)] ml-2">
                          ({formatDate(d.ex_date, "relative")})
                        </span>
                      </td>
                      <td className="px-4 py-2 text-right text-[var(--text-primary)] tabular">
                        {d.market === "br" ? "R$" : "$"}
                        {d.amount.toFixed(d.market === "br" ? 4 : 3)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </Section>
    </div>
  );
}
