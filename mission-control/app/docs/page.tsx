import Link from "next/link";

import { listDossiers, listDeepdiveJSON } from "@/lib/vault";
import { formatDate } from "@/lib/format";
import { PageHeader, Section, Pill, EmptyState } from "@/components/ui";

export const dynamic = "force-dynamic";

export default function DocsPage() {
  const dossiers = listDossiers(40);
  const deepdiveJsons = listDeepdiveJSON(20);

  return (
    <div className="p-8 space-y-8 max-w-[1400px]">
      <PageHeader
        title="Docs"
        subtitle="Dossiers + raw deepdive JSON"
        crumbs={[{ label: "Home", href: "/" }, { label: "Docs" }]}
      />

      <Section
        label="Dossiers"
        meta={`${dossiers.length}`}
      >
        {dossiers.length === 0 ? (
          <EmptyState
            icon="◯"
            title="Sem dossiers"
            description="Corre um deep-dive para gerar um dossier no vault."
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {dossiers.map((d) => {
              const fm = d.data as Record<string, unknown>;
              const piotroski = fm.piotroski as number | undefined;
              const altman = fm.altman_z as number | undefined;
              const beneish = fm.beneish_m as number | undefined;
              const ticker = (fm.ticker as string | undefined) || d.title;
              return (
                <Link
                  key={d.path}
                  href={`/ticker/${ticker}`}
                  className="card-cyan p-4 hover:border-[var(--accent-glow)] transition-colors block group"
                >
                  <header className="flex items-center justify-between mb-2">
                    <h3 className="type-mono text-[var(--accent-glow)] group-hover:text-[var(--text-primary)] transition-colors font-medium">
                      {ticker}
                    </h3>
                    <span className="type-mono-sm text-[var(--text-tertiary)]">
                      {formatDate(d.modified, "relative")}
                    </span>
                  </header>
                  {(piotroski !== undefined ||
                    altman !== undefined ||
                    beneish !== undefined) && (
                    <div className="grid grid-cols-3 gap-1 mt-2">
                      <ScoreBox label="F" value={piotroski} max={9} />
                      <ScoreBox
                        label="Z"
                        value={altman}
                        threshold={2.99}
                        kind="hi"
                      />
                      <ScoreBox
                        label="M"
                        value={beneish}
                        threshold={-2.22}
                        kind="lo"
                      />
                    </div>
                  )}
                  {Boolean(fm.sector) && (
                    <div className="type-mono-sm text-[var(--text-tertiary)] mt-2">
                      {String(fm.sector)}
                    </div>
                  )}
                </Link>
              );
            })}
          </div>
        )}
      </Section>

      <Section
        label="Deepdive JSON history"
        meta={`${deepdiveJsons.length}`}
      >
        {deepdiveJsons.length === 0 ? (
          <EmptyState
            icon="◯"
            title="Sem deepdive JSON"
            description="Os deepdive JSON são gerados em reports/deepdive/ a cada execução."
          />
        ) : (
          <div className="card overflow-hidden">
            <div className="max-h-96 overflow-y-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-[var(--border-subtle)] sticky top-0 bg-[var(--bg-elevated)]">
                    <th className="text-left type-h3 px-4 py-2.5">ticker</th>
                    <th className="text-left type-h3 px-4 py-2.5">when</th>
                    <th className="text-left type-h3 px-4 py-2.5">path</th>
                  </tr>
                </thead>
                <tbody className="type-mono-sm">
                  {deepdiveJsons.map((j) => {
                    const date = `${j.ts.slice(0, 4)}-${j.ts.slice(4, 6)}-${j.ts.slice(6, 8)}`;
                    const time = `${j.ts.slice(9, 11)}:${j.ts.slice(11, 13)}`;
                    return (
                      <tr
                        key={j.path}
                        className="border-b border-[var(--border-subtle)] last:border-b-0 hover:bg-[var(--bg-overlay)]"
                      >
                        <td className="px-4 py-1.5">
                          <Link
                            href={`/ticker/${j.ticker}`}
                            className="text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors"
                          >
                            {j.ticker}
                          </Link>
                        </td>
                        <td className="px-4 py-1.5 text-[var(--text-secondary)]">
                          {formatDate(date, "short")} · {time}
                        </td>
                        <td className="px-4 py-1.5 text-[var(--text-tertiary)] truncate">
                          {j.path.split(/[\\/]/).slice(-2).join("/")}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </Section>
    </div>
  );
}

function ScoreBox({
  label,
  value,
  max,
  threshold,
  kind,
}: {
  label: string;
  value: number | undefined;
  max?: number;
  threshold?: number;
  kind?: "hi" | "lo";
}) {
  if (value == null) {
    return (
      <div className="px-2 py-1 rounded text-center type-mono-sm border border-[var(--border-subtle)] text-[var(--text-disabled)]">
        {label}: —
      </div>
    );
  }
  let cls =
    "border-[var(--border-subtle)] bg-[var(--bg-overlay)] text-[var(--text-secondary)]";
  if (max != null) {
    cls =
      value >= 7
        ? "border-[rgba(34,197,94,0.3)] bg-[rgba(34,197,94,0.06)] text-[var(--verdict-buy)]"
        : value >= 4
        ? "border-[rgba(245,158,11,0.3)] bg-[rgba(245,158,11,0.06)] text-[var(--verdict-hold)]"
        : "border-[rgba(239,68,68,0.3)] bg-[rgba(239,68,68,0.06)] text-[var(--verdict-avoid)]";
  } else if (threshold != null) {
    const ok = kind === "hi" ? value > threshold : value < threshold;
    cls = ok
      ? "border-[rgba(34,197,94,0.3)] bg-[rgba(34,197,94,0.06)] text-[var(--verdict-buy)]"
      : "border-[rgba(239,68,68,0.3)] bg-[rgba(239,68,68,0.06)] text-[var(--verdict-avoid)]";
  }
  return (
    <div className={`px-2 py-1 rounded text-center type-mono-sm border ${cls}`}>
      {label}: {typeof value === "number" ? value.toFixed(2) : value}
    </div>
  );
}
