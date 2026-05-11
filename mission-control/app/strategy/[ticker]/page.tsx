import Link from "next/link";

import { listStrategyRuns } from "@/lib/db";
import { formatDate } from "@/lib/format";
import {
  PageHeader,
  Section,
  Pill,
  pillVariantFromVerdict,
  pillVariantFromMarket,
  EmptyState,
} from "@/components/ui";

export const dynamic = "force-dynamic";

const ENGINE_BLURB: Record<string, string> = {
  graham: "Deep value · Graham number, low PE/PB, ROE 15%, debt < 3× EBITDA",
  buffett: "Quality compounding · PE ≤ 20, PB ≤ 3, ROE 15%, ROIC 15%, Aristocrat",
  drip: "Dividend safety · SAFE/WATCH/RISK + yield floor (US 2.5%, BR 6%)",
  macro: "Top-down sector tilt · regime + sector multiplier",
  hedge: "Tactical defensive · quiet in expansion, active in late_cycle/recession",
};

export default async function StrategyTickerPage({
  params,
  searchParams,
}: {
  params: Promise<{ ticker: string }>;
  searchParams: Promise<{ market?: string }>;
}) {
  const { ticker } = await params;
  const { market } = await searchParams;
  const tk = ticker.toUpperCase();
  const m = market === "br" || market === "us" ? market : null;
  const runs = listStrategyRuns(tk, m, 50);

  const crumbs = [
    { label: "Allocation", href: "/allocation" },
    ...(m ? [{ label: m.toUpperCase() }] : []),
    { label: tk },
  ];

  if (!runs.length) {
    return (
      <div className="p-8 max-w-[1200px] space-y-8">
        <PageHeader title={tk} crumbs={crumbs} />
        <EmptyState
          icon="◯"
          title="Sem strategy runs"
          description="Este ticker ainda não foi avaliado pelos engines. Aguarda o próximo overnight backfill."
          action={
            <div className="flex gap-2">
              <Link
                href={`/ticker/${tk}`}
                className="pill pill-glow"
              >
                ver preço/fundamentals →
              </Link>
              <Link
                href="/allocation"
                className="pill pill-neutral"
              >
                ← allocation
              </Link>
            </div>
          }
        />
      </div>
    );
  }

  // Group by market (in case ticker exists in both)
  const byMarket = runs.reduce<Record<string, typeof runs>>((acc, r) => {
    (acc[r.market] = acc[r.market] || []).push(r);
    return acc;
  }, {});

  const latestTs = runs.reduce<string>((acc, r) => (r.run_ts > acc ? r.run_ts : acc), "");

  return (
    <div className="p-8 space-y-8 max-w-[1200px]">
      <PageHeader
        title={tk}
        subtitle="Engine outputs across all 5 strategies"
        crumbs={crumbs}
        freshness={latestTs}
        actions={
          <Link
            href={`/ticker/${tk}`}
            className="pill pill-glow"
          >
            ticker page →
          </Link>
        }
      />

      {Object.entries(byMarket).map(([mkt, rs]) => (
        <Section
          key={mkt}
          label={`${mkt} engines`}
          meta={
            <span className="flex items-center gap-2">
              <Pill variant={pillVariantFromMarket(mkt)}>{mkt.toUpperCase()}</Pill>
              <span>last run {formatDate(rs[0]?.run_ts, "relative")}</span>
            </span>
          }
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {rs.map((r) => (
              <details
                key={r.engine}
                className="card hover:border-[var(--border-strong)] transition-colors"
              >
                <summary className="cursor-pointer p-4 flex items-baseline justify-between gap-3 list-none">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="type-h2 capitalize text-[var(--text-primary)]">
                        {r.engine}
                      </h3>
                      <Pill variant={pillVariantFromVerdict(r.verdict)}>
                        {r.verdict}
                      </Pill>
                    </div>
                    <p className="type-caption text-[var(--text-tertiary)] truncate">
                      {ENGINE_BLURB[r.engine] || ""}
                    </p>
                  </div>
                  <div className="text-right shrink-0">
                    <div className="type-h2 tabular text-[var(--text-primary)]">
                      {(r.score * 100).toFixed(0)}
                      <span className="type-caption text-[var(--text-tertiary)] ml-1">/100</span>
                    </div>
                    {r.weight_suggestion > 0 && (
                      <div className="type-mono-sm text-[var(--accent-primary)]">
                        weight {(r.weight_suggestion * 100).toFixed(1)}%
                      </div>
                    )}
                  </div>
                </summary>
                <div className="px-4 pb-4 border-t border-[var(--border-subtle)]">
                  <RationaleView rationale={r.rationale} />
                </div>
              </details>
            ))}
          </div>
        </Section>
      ))}
    </div>
  );
}

function RationaleView({ rationale }: { rationale: any }) {
  if (!rationale || typeof rationale !== "object") {
    return null;
  }

  // Pattern 1: details object with verdict/value/threshold per criterion (graham/buffett/drip)
  const details = rationale.details;
  if (details && typeof details === "object") {
    const entries = Object.entries(details);
    return (
      <div className="mt-3 space-y-1">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5">
          {entries.map(([key, val]: [string, any]) => (
            <CriterionRow key={key} name={key} val={val} />
          ))}
        </div>
        {rationale.passes !== undefined && (
          <div className="mt-3 pt-2 border-t border-[var(--border-subtle)] type-mono-sm text-[var(--text-tertiary)]">
            passes {rationale.passes}/{rationale.applicable} applicable criteria
          </div>
        )}
      </div>
    );
  }

  // Pattern 2: flat dict (macro/hedge)
  return (
    <div className="mt-3 space-y-1">
      {Object.entries(rationale).map(([k, v]) => (
        <div
          key={k}
          className="flex items-baseline justify-between type-mono-sm"
        >
          <span className="text-[var(--text-tertiary)]">{k}</span>
          <span className="text-[var(--text-primary)]">
            {Array.isArray(v) ? v.join(" · ") : String(v ?? "—")}
          </span>
        </div>
      ))}
    </div>
  );
}

function CriterionRow({ name, val }: { name: string; val: any }) {
  if (!val || typeof val !== "object") {
    return (
      <div className="flex items-baseline justify-between type-mono-sm">
        <span className="text-[var(--text-tertiary)]">{name}</span>
        <span className="text-[var(--text-primary)]">{String(val ?? "—")}</span>
      </div>
    );
  }
  const verdict = val.verdict;
  const value = val.value;
  const threshold = val.threshold;

  const symbol =
    verdict === "pass" ? "✓" : verdict === "fail" ? "✗" : "·";
  const color =
    verdict === "pass"
      ? "text-[var(--verdict-buy)]"
      : verdict === "fail"
      ? "text-[var(--verdict-avoid)]"
      : "text-[var(--text-tertiary)]";

  return (
    <div className="flex items-baseline justify-between type-mono-sm gap-3">
      <span className="flex items-center gap-2 min-w-0">
        <span className={`shrink-0 ${color}`} aria-hidden>
          {symbol}
        </span>
        <span className="text-[var(--text-secondary)] truncate">{name}</span>
      </span>
      <span className="text-[var(--text-primary)] shrink-0">
        {fmtVal(value)}{" "}
        {threshold !== undefined && threshold !== null && (
          <span className="text-[var(--text-tertiary)]">
            ({verdict === "pass" ? "≥" : verdict === "fail" ? "✗" : ""} {fmtVal(threshold)})
          </span>
        )}
      </span>
    </div>
  );
}

function fmtVal(v: any): string {
  if (v === null || v === undefined) return "—";
  if (typeof v === "number") {
    if (Math.abs(v) < 1) return v.toFixed(3);
    return v.toFixed(2);
  }
  if (typeof v === "boolean") return v ? "yes" : "no";
  return String(v);
}
