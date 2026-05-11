import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { listCouncilOutputs, summariseCouncil, CouncilEntry } from "@/lib/vault";
import { formatDate } from "@/lib/format";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Research · Mission Control" };

// FII heuristic: BR tickers ending in 11 with sector containing "FII"/"Imobi" or
// when no sector available a fallback to the trailing "11" + non-bank/holding tag.
function isFii(e: CouncilEntry): boolean {
  if (e.market !== "br") return false;
  const sec = (e.sector || "").toLowerCase();
  if (sec.includes("fii") || sec.includes("imobil")) return true;
  return /11$/.test(e.ticker);
}

function isStock(e: CouncilEntry): boolean {
  return !isFii(e);
}

function stanceMeta(s: string): { label: string; bg: string; fg: string } {
  switch (s) {
    case "BUY":
      return { label: "Buy", bg: "var(--jpm-gain-soft)", fg: "var(--verdict-buy)" };
    case "HOLD":
      return { label: "Hold", bg: "var(--jpm-amber-soft)", fg: "var(--verdict-hold)" };
    case "AVOID":
      return { label: "Avoid", bg: "var(--jpm-loss-soft)", fg: "var(--verdict-avoid)" };
    case "NEEDS_DATA":
      return { label: "Needs data", bg: "var(--bg-overlay)", fg: "var(--text-tertiary)" };
    default:
      return { label: "Uncategorised", bg: "var(--bg-overlay)", fg: "var(--text-tertiary)" };
  }
}

export default function ResearchPage() {
  const all = listCouncilOutputs(500);
  const summary = summariseCouncil(all);
  const usEntries = all.filter((e) => e.market === "us");
  const brStocks = all.filter((e) => e.market === "br" && isStock(e));
  const brFiis = all.filter((e) => e.market === "br" && isFii(e));

  return (
    <div className="px-6 py-5 max-w-[1440px] mx-auto">
      {/* ── Hero ──────────────────────────────────────────────────── */}
      <header className="mb-6">
        <h1
          className="font-display"
          style={{
            fontSize: 28,
            fontWeight: 600,
            color: "var(--text-primary)",
            letterSpacing: "-0.005em",
            lineHeight: 1.15,
          }}
        >
          Our research
        </h1>
        <p
          className="type-body"
          style={{ marginTop: 4, color: "var(--text-tertiary)" }}
        >
          {summary.total > 0
            ? `Latest Council run · ${formatDate(summary.date, "medium")} · ${summary.total} dossiers`
            : "Sem run de Council"}
        </p>
      </header>

      {/* ── Stats ribbon ──────────────────────────────────────────── */}
      <section className="card p-5 mb-6">
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-px" style={{ background: "var(--border-subtle)" }}>
          <Stat label="Total dossiers" value={summary.total} />
          <Stat label="Buy" value={summary.buy} accent="var(--verdict-buy)" divide />
          <Stat label="Hold" value={summary.hold} accent="var(--verdict-hold)" divide />
          <Stat label="Avoid" value={summary.avoid} accent="var(--verdict-avoid)" divide />
          <Stat label="Needs data" value={summary.needs_data} accent="var(--text-tertiary)" divide />
        </div>
      </section>

      {/* ── United States ─────────────────────────────────────────── */}
      <ResearchSection
        title="United States"
        subtitle={`${usEntries.length} ações cobertas · NYSE/NASDAQ`}
        entries={usEntries}
        emptyText="Sem dossiers US"
      />

      {/* ── Brasil — Stocks ────────────────────────────────────────── */}
      <ResearchSection
        title="Brasil · Stocks"
        subtitle={`${brStocks.length} ações cobertas · B3`}
        entries={brStocks}
        emptyText="Sem dossiers de stocks BR"
      />

      {/* ── Brasil — FIIs ──────────────────────────────────────────── */}
      <ResearchSection
        title="Brasil · FIIs"
        subtitle={`${brFiis.length} fundos imobiliários cobertos`}
        entries={brFiis}
        emptyText="Sem dossiers de FII"
      />
    </div>
  );
}

// ─── Sub-components ────────────────────────────────────────────────────

function ResearchSection({
  title,
  subtitle,
  entries,
  emptyText,
}: {
  title: string;
  subtitle: string;
  entries: CouncilEntry[];
  emptyText: string;
}) {
  if (entries.length === 0) {
    return (
      <section className="mb-8">
        <SectionHeader title={title} subtitle={subtitle} />
        <div className="card p-8 text-center">
          <p className="type-body-sm italic" style={{ color: "var(--text-tertiary)" }}>
            {emptyText}
          </p>
        </div>
      </section>
    );
  }

  // Sort: BUY first, then HOLD, then AVOID, then by date desc
  const order = (s: string) => (s === "BUY" ? 0 : s === "HOLD" ? 1 : s === "AVOID" ? 2 : 3);
  const sorted = [...entries].sort((a, b) => {
    const o = order(a.stance) - order(b.stance);
    if (o !== 0) return o;
    return b.date.localeCompare(a.date);
  });

  return (
    <section className="mb-8">
      <SectionHeader title={title} subtitle={subtitle} />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sorted.map((e) => (
          <ResearchCard key={e.ticker} e={e} />
        ))}
      </div>
    </section>
  );
}

function SectionHeader({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="flex items-baseline justify-between mb-3 flex-wrap gap-2">
      <div>
        <h2
          className="font-display"
          style={{
            fontSize: 18,
            fontWeight: 600,
            color: "var(--text-primary)",
            letterSpacing: "-0.005em",
          }}
        >
          {title}
        </h2>
        <p className="type-byline" style={{ marginTop: 2 }}>
          {subtitle}
        </p>
      </div>
      <Link
        href="/council"
        className="text-[12px] flex items-center gap-1 hover:underline"
        style={{ color: "var(--accent-primary)", fontWeight: 500 }}
      >
        See all research <ArrowRight size={12} />
      </Link>
    </div>
  );
}

function ResearchCard({ e }: { e: CouncilEntry }) {
  const meta = stanceMeta(e.stance);
  return (
    <Link
      href={`/council/${e.ticker}`}
      className="card p-5 block transition-shadow"
      style={{ minHeight: 168 }}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <h3
            className="font-display"
            style={{
              fontSize: 16,
              fontWeight: 600,
              color: "var(--text-primary)",
              margin: 0,
            }}
          >
            {e.ticker}
          </h3>
          <p
            className="type-byline"
            style={{
              marginTop: 2,
              color: "var(--text-tertiary)",
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
              maxWidth: 220,
            }}
          >
            {e.sector || "—"}
            {e.is_holding ? " · holding" : ""}
          </p>
        </div>
        <span
          style={{
            background: meta.bg,
            color: meta.fg,
            padding: "3px 10px",
            borderRadius: 999,
            fontSize: 11,
            fontWeight: 600,
            whiteSpace: "nowrap",
          }}
        >
          {meta.label}
        </span>
      </div>

      {e.philosophy_primary && (
        <p
          className="type-body-sm"
          style={{
            color: "var(--text-secondary)",
            display: "-webkit-box",
            WebkitLineClamp: 3,
            WebkitBoxOrient: "vertical",
            overflow: "hidden",
            margin: "0 0 12px 0",
          }}
        >
          {e.philosophy_primary}
        </p>
      )}

      <div
        className="flex items-center justify-between"
        style={{
          marginTop: 12,
          paddingTop: 12,
          borderTop: "1px solid var(--border-subtle)",
        }}
      >
        <span className="type-byline">
          {e.date ? formatDate(e.date, "short") : "sem data"}
          {e.confidence && e.confidence !== "—" ? ` · conf ${e.confidence}` : ""}
        </span>
        <span
          className="text-[11px] flex items-center gap-1"
          style={{ color: "var(--accent-primary)", fontWeight: 500 }}
        >
          read <ArrowRight size={11} />
        </span>
      </div>
    </Link>
  );
}

function Stat({
  label,
  value,
  accent,
  divide,
}: {
  label: string;
  value: number;
  accent?: string;
  divide?: boolean;
}) {
  return (
    <div
      style={{
        background: "var(--bg-elevated)",
        padding: "10px 16px",
      }}
    >
      <p className="type-caption" style={{ marginBottom: 4 }}>
        {label}
      </p>
      <p
        className="font-display tabular"
        style={{
          fontSize: 22,
          fontWeight: 600,
          color: accent || "var(--text-primary)",
          margin: 0,
          lineHeight: 1.1,
        }}
      >
        {value}
      </p>
    </div>
  );
}
