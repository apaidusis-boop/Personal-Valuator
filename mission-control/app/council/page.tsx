import Link from "next/link";

import {
  listCouncilOutputs,
  summariseCouncil,
  type CouncilEntry,
  type CouncilStance,
} from "@/lib/vault";
import { formatDate, formatPercent } from "@/lib/format";
import {
  PageHeader,
  Section,
  Pill,
  pillVariantFromMarket,
  EmptyState,
} from "@/components/ui";
import StancePill from "@/components/stance-pill";

export const dynamic = "force-dynamic";

const STANCE_ORDER: CouncilStance[] = ["AVOID", "HOLD", "BUY", "NEEDS_DATA", "UNKNOWN"];
const STANCE_LABEL: Record<CouncilStance, string> = {
  BUY: "buy",
  HOLD: "hold",
  AVOID: "avoid",
  NEEDS_DATA: "needs data",
  UNKNOWN: "uncategorised",
};

export default function CouncilIndexPage() {
  const all = listCouncilOutputs(500);
  const summary = summariseCouncil(all);
  const latest = all.filter((e) => e.date === summary.date);
  const previous = all.filter((e) => e.date && e.date !== summary.date);

  const grouped: Record<CouncilStance, CouncilEntry[]> = {
    BUY: [],
    HOLD: [],
    AVOID: [],
    NEEDS_DATA: [],
    UNKNOWN: [],
  };
  for (const e of latest) grouped[e.stance].push(e);

  return (
    <div className="p-8 space-y-8 max-w-[1400px]">
      <PageHeader
        title="Council"
        subtitle={`Synthetic IC dossiers · STORYT_3.0 · ${latest.length} reviewed`}
        crumbs={[{ label: "Home", href: "/" }, { label: "Council" }]}
        freshness={summary.date}
      />

      {latest.length === 0 ? (
        <EmptyState
          icon="◯"
          title="Sem dossiers do Council"
          description="O Council corre durante o overnight batch. Aguarda a próxima execução."
        />
      ) : (
        <>
          {/* Counts */}
          <section className="grid grid-cols-2 md:grid-cols-5 gap-3">
            <CountBox label="total" n={summary.total} />
            <CountBox label="buy" n={summary.buy} variant="buy" />
            <CountBox label="hold" n={summary.hold} variant="hold" />
            <CountBox label="avoid" n={summary.avoid} variant="avoid" />
            <CountBox label="needs data" n={summary.needs_data} />
          </section>

          {STANCE_ORDER.map((st) => {
            const items = grouped[st];
            if (items.length === 0) return null;
            return (
              <Section
                key={st}
                label={STANCE_LABEL[st]}
                meta={`${items.length}`}
              >
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
                  {items
                    .sort((a, b) => a.ticker.localeCompare(b.ticker))
                    .map((e) => (
                      <CouncilCard key={e.ticker} e={e} />
                    ))}
                </div>
              </Section>
            );
          })}

          {previous.length > 0 && (
            <Section
              label="Earlier runs"
              meta={`${previous.length}`}
            >
              <div className="card overflow-hidden">
                <div className="max-h-72 overflow-y-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-[var(--border-subtle)] sticky top-0 bg-[var(--bg-elevated)]">
                        <th className="text-left type-h3 px-3 py-2">date</th>
                        <th className="text-left type-h3 px-3 py-2">ticker</th>
                        <th className="text-left type-h3 px-3 py-2">stance</th>
                        <th className="text-left type-h3 px-3 py-2">conf</th>
                        <th className="text-left type-h3 px-3 py-2">sector</th>
                      </tr>
                    </thead>
                    <tbody className="type-mono-sm">
                      {previous.slice(0, 100).map((e) => (
                        <tr
                          key={`${e.ticker}-${e.date}`}
                          className="border-b border-[var(--border-subtle)] hover:bg-[var(--bg-overlay)] transition-colors"
                        >
                          <td className="px-3 py-1.5 text-[var(--text-tertiary)]">
                            {formatDate(e.date, "short")}
                          </td>
                          <td className="px-3 py-1.5">
                            <Link
                              href={`/council/${e.ticker}`}
                              className="text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors"
                            >
                              {e.ticker}
                            </Link>
                          </td>
                          <td className="px-3 py-1.5 text-[var(--text-secondary)]">
                            {e.stance}
                          </td>
                          <td className="px-3 py-1.5 text-[var(--text-tertiary)]">
                            {e.confidence}
                          </td>
                          <td className="px-3 py-1.5 text-[var(--text-tertiary)]">
                            {e.sector || "—"}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </Section>
          )}
        </>
      )}
    </div>
  );
}

function CountBox({
  label,
  n,
  variant,
}: {
  label: string;
  n: number;
  variant?: "buy" | "hold" | "avoid";
}) {
  const cls =
    variant === "buy"
      ? "border-[rgba(34,197,94,0.3)] text-[var(--verdict-buy)]"
      : variant === "hold"
      ? "border-[rgba(245,158,11,0.3)] text-[var(--verdict-hold)]"
      : variant === "avoid"
      ? "border-[rgba(239,68,68,0.3)] text-[var(--verdict-avoid)]"
      : "border-[var(--border-subtle)] text-[var(--text-primary)]";
  return (
    <div className={`card p-3 ${cls}`}>
      <div className="type-h3">{label}</div>
      <div className="type-display tabular mt-1">{n}</div>
    </div>
  );
}

function CouncilCard({ e }: { e: CouncilEntry }) {
  const mos =
    e.margin_of_safety && e.margin_of_safety !== 0
      ? formatPercent(e.margin_of_safety, 1, { fromFraction: true })
      : null;
  return (
    <Link
      href={`/council/${e.ticker}`}
      className="card p-4 hover:border-[var(--border-strong)] transition-colors block group"
    >
      <header className="flex items-center justify-between mb-2">
        <h3 className="type-mono text-[var(--accent-glow)] group-hover:text-[var(--text-primary)] transition-colors text-base">
          {e.ticker}
        </h3>
        <StancePill stance={e.stance} confidence={e.confidence} />
      </header>
      <div className="flex items-center gap-2 flex-wrap mb-2">
        <Pill variant={pillVariantFromMarket(e.market)}>
          {e.market.toUpperCase()}
        </Pill>
        {e.modo && (
          <span className="type-mono-sm text-[var(--text-tertiary)]">
            modo {e.modo}
          </span>
        )}
        {e.is_holding && <Pill variant="purple">holding</Pill>}
      </div>
      {(e.dissent_count > 0 || e.flag_count > 0) && (
        <div className="flex gap-2 mb-1.5">
          {e.dissent_count > 0 && (
            <Pill variant="hold">◇ {e.dissent_count} dissent</Pill>
          )}
          {e.flag_count > 0 && (
            <Pill variant="avoid">⚑ {e.flag_count} pre-pub</Pill>
          )}
        </div>
      )}
      {e.seats.length > 0 && (
        <p className="type-mono-sm text-[var(--text-tertiary)] truncate">
          {e.seats.slice(0, 4).join(" · ")}
          {e.seats.length > 4 && ` +${e.seats.length - 4}`}
        </p>
      )}
      {mos && (
        <p className="type-mono-sm text-[var(--text-secondary)] mt-1">
          MoS {mos}
        </p>
      )}
    </Link>
  );
}
