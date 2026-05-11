import Link from "next/link";

import { loadLatestAllocation } from "@/lib/vault";
import { formatDate, formatPercent } from "@/lib/format";
import {
  PageHeader,
  Section,
  Pill,
  pillVariantFromVerdict,
  pillVariantFromMarket,
  EmptyState,
} from "@/components/ui";

export const dynamic = "force-dynamic";

export default function AllocationPage() {
  const us = loadLatestAllocation("us");
  const br = loadLatestAllocation("br");

  const latestDate = [us?.date, br?.date].filter(Boolean).sort().reverse()[0] || null;

  return (
    <div className="p-8 space-y-8 max-w-[1400px]">
      <PageHeader
        title="Allocation"
        subtitle="Proposta combinada — 5 strategy engines × 2 mercados, com macro overlay e tactical hedge"
        crumbs={[{ label: "Home", href: "/" }, { label: "Allocation" }]}
        freshness={latestDate}
        staleHours={48}
      />

      {!us && !br ? (
        <EmptyState
          icon="◯"
          title="Nenhuma alocação encontrada"
          description="A proposta é gerada pelo overnight backfill. Pode demorar até a próxima execução noturna."
          action={
            <Link
              href="/docs"
              className="type-mono-sm text-[var(--accent-glow)] hover:text-[var(--text-primary)]"
            >
              ver docs →
            </Link>
          }
        />
      ) : (
        <div className="space-y-12">
          {us && <AllocSection data={us} />}
          {br && <AllocSection data={br} />}
        </div>
      )}
    </div>
  );
}

function AllocSection({ data }: { data: NonNullable<ReturnType<typeof loadLatestAllocation>> }) {
  const sorted = Object.entries(data.target_weights).sort((a, b) => b[1] - a[1]);
  const hedge = data.hedge_overlay;
  const macro = data.macro_overlay;

  return (
    <article>
      <header className="flex items-end justify-between mb-4 pb-3 border-b border-[var(--border-subtle)]">
        <div>
          <h2 className="type-h2">{data.market.toUpperCase()}</h2>
          <p className="type-caption text-[var(--text-tertiary)] mt-0.5">
            {sorted.length} candidates · {data.conflicts.length} conflicts
          </p>
        </div>
        <Pill variant={data.market === "br" ? "mkt-br" : "mkt-us"}>
          {formatDate(data.date, "medium")}
        </Pill>
      </header>

      {/* Bucket weights row */}
      <div className="mb-6 flex flex-wrap gap-1.5 items-center">
        <span className="type-h3 mr-2">buckets</span>
        {Object.entries(data.bucket_weights).map(([k, v]) => (
          <Pill key={k} variant="purple">
            {k} {formatPercent(v as number, 0, { fromFraction: true })}
          </Pill>
        ))}
      </div>

      {/* Macro & Hedge bar */}
      <div className="mb-6 flex flex-wrap gap-3 items-center">
        <span className="type-h3">macro</span>
        <Pill variant="glow">{macro.regime || "?"}</Pill>
        <span className="type-mono-sm text-[var(--text-tertiary)]">
          confidence {macro.confidence || "?"}
        </span>
        {macro.tilt_up?.length > 0 && (
          <span className="type-caption text-[var(--text-secondary)]">
            <span className="text-[var(--text-tertiary)]">tilt up:</span>{" "}
            {macro.tilt_up.join(" · ")}
          </span>
        )}
        {macro.tilt_down?.length > 0 && (
          <span className="type-caption text-[var(--text-secondary)]">
            <span className="text-[var(--text-tertiary)]">tilt down:</span>{" "}
            {macro.tilt_down.join(" · ")}
          </span>
        )}
      </div>

      {hedge?.active && (
        <div className="card-danger p-4 mb-6">
          <div className="flex items-center gap-3 flex-wrap">
            <Pill variant="avoid">⚑ hedge on</Pill>
            <span className="type-body-sm">
              <span className="text-[var(--text-tertiary)]">size </span>
              <span className="text-[var(--verdict-avoid)] type-mono">
                {(hedge.hedge_size_pct * 100).toFixed(0)}%
              </span>
              <span className="text-[var(--text-tertiary)]"> via </span>
              <span className="text-[var(--verdict-hold)] type-mono">
                {(hedge.instruments || []).join(", ")}
              </span>
            </span>
            <span className="type-mono-sm text-[var(--text-tertiary)]">
              regime {hedge.regime}
            </span>
          </div>
        </div>
      )}

      {/* Two-column: weights + conflicts */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Target weights — 3 cols */}
        <div className="lg:col-span-3">
          <Section
            label="Target weights"
            meta={`top ${Math.min(15, sorted.length)} of ${sorted.length}`}
            dense
          >
            <div className="card overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-[var(--border-subtle)]">
                    <th className="text-left type-h3 px-4 py-2.5">ticker</th>
                    <th className="text-right type-h3 px-4 py-2.5">weight</th>
                    <th className="text-left type-h3 px-4 py-2.5"></th>
                  </tr>
                </thead>
                <tbody className="type-mono">
                  {sorted.slice(0, 15).map(([t, w]) => (
                    <tr
                      key={t}
                      className="border-b border-[var(--border-subtle)] last:border-b-0 hover:bg-[var(--bg-overlay)] transition-colors"
                    >
                      <td className="px-4 py-2">
                        <Link
                          href={`/strategy/${t}?market=${data.market}`}
                          className="text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors"
                        >
                          {t}
                        </Link>
                      </td>
                      <td className="px-4 py-2 text-right tabular text-[var(--text-primary)]">
                        {(w * 100).toFixed(1)}%
                      </td>
                      <td className="px-4 py-2 w-1/3">
                        <div className="h-1.5 rounded-full bg-[var(--bg-overlay)] overflow-hidden">
                          <div
                            className="h-full rounded-full transition-all"
                            style={{
                              width: `${Math.min(w * 400, 100)}%`,
                              background:
                                "linear-gradient(90deg, var(--accent-primary), var(--accent-glow))",
                            }}
                          />
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Section>
        </div>

        {/* Conflicts — 2 cols */}
        <div className="lg:col-span-2">
          <Section
            label="Conflicts"
            meta={`${data.conflicts.length}`}
            dense
          >
            {data.conflicts.length > 0 ? (
              <div className="card p-4 space-y-2 max-h-96 overflow-y-auto">
                <p className="type-caption text-[var(--text-tertiary)] mb-2">
                  Tickers where engines disagree (BUY + AVOID at the same time).
                </p>
                {data.conflicts.slice(0, 12).map((c) => (
                  <div
                    key={c.ticker}
                    className="border-l-2 border-[var(--verdict-hold)]/40 pl-3 py-1.5"
                  >
                    <Link
                      href={`/strategy/${c.ticker}?market=${data.market}`}
                      className="type-mono text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors"
                    >
                      {c.ticker}
                    </Link>
                    <div className="mt-1.5 flex flex-wrap gap-1">
                      {Object.entries(c.verdicts).map(([eng, v]) => (
                        <Pill
                          key={eng}
                          variant={pillVariantFromVerdict(v as string)}
                        >
                          {eng}={String(v).toLowerCase()}
                        </Pill>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="card p-6 text-center">
                <p className="type-body-sm text-[var(--text-tertiary)]">
                  Sem conflitos. Engines em consenso.
                </p>
              </div>
            )}
          </Section>
        </div>
      </div>

      {data.notes.length > 0 && (
        <footer className="mt-6 pt-3 border-t border-[var(--border-subtle)]">
          {data.notes.map((n, i) => (
            <p
              key={i}
              className="type-mono-sm text-[var(--text-tertiary)]"
            >
              · {n}
            </p>
          ))}
        </footer>
      )}
    </article>
  );
}
