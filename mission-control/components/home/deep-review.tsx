"use client";

// ── BAND 3 · THE DEEP REVIEW ─────────────────────────────────────────
//
// Reading mode: active. 5-10 minutes when there's time. Editorial register
// like the FT weekend long-read, but anchored to a specific ticker.
//
// Synced to focus-ticker context: when user picks a ticker in the
// Workbench, this band re-renders. Default ticker = headline spotlight.
//
// Five sections:
//   1. Spotlight header — logo + name + verdict pill + one-line stance
//   2. "How it has performed" — 3-4 paragraphs, deterministic template
//      (no LLM in v1; a templater fills sector-specific phrasing)
//   3. "Competitors at this moment" — 3-5 peers with key metrics
//   4. "What the council said" — quote from latest synthetic_ic
//   5. "Macro overlay" — single-line regime call

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { useFocusTicker } from "@/lib/focus-ticker";
import { TickerLogo, PercentDelta } from "../jpm-atoms";

// ── Types ────────────────────────────────────────────────────────────

export type DeepReviewTickerData = {
  ticker: string;
  name: string;
  sector: string;
  market: "br" | "us";
  verdict: "BUY" | "HOLD" | "AVOID" | "N/A";
  one_line_stance: string;        // "Compounder de qualidade · margem de segurança intacta"
  performance: {
    ytd_pct: number | null;
    sector_ytd_pct: number | null;
    benchmark_ytd_pct: number | null;
    one_yr_pct: number | null;
    five_yr_pct: number | null;
    review_paragraphs: string[];   // 3-4 paragraphs of templated prose
  };
  peers: {
    ticker: string;
    name: string;
    pe: number | null;
    pb: number | null;
    dy: number | null;
    roe: number | null;
    is_self: boolean;
  }[];
  council_quote: {
    persona: string;     // "Buffett" / "Druckenmiller" / etc.
    text: string;        // 1-2 sentences
    date: string;        // YYYY-MM-DD
  } | null;
  macro_overlay: {
    regime: string;       // "Late-cycle US"
    sector_score: number; // -1 to +1
    line: string;         // "Late-cycle US, financials no neutral mode → JPM merece prémio sobre tangible book mas não 3x."
  };
};

export type DeepReviewProps = {
  by_ticker: Record<string, DeepReviewTickerData>;
};

// ── Component ────────────────────────────────────────────────────────

export function DeepReview({ by_ticker }: DeepReviewProps) {
  const { focus } = useFocusTicker();
  const data = by_ticker[focus.ticker];

  if (!data) {
    return (
      <section
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
          borderRadius: "var(--radius)",
          padding: 24,
          textAlign: "center",
          color: "var(--text-tertiary)",
        }}
      >
        <p className="type-h3" style={{ marginBottom: 6 }}>The Deep Review</p>
        <p className="type-byline">
          Sem dossier para <span style={{ fontFamily: "var(--font-mono)", color: "var(--text-secondary)" }}>{focus.ticker}</span>.
          Selecciona um ticker no Workbench.
        </p>
      </section>
    );
  }

  return (
    <section
      aria-label="The deep review"
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderRadius: "var(--radius)",
        boxShadow: "var(--shadow-sm)",
        overflow: "hidden",
      }}
    >
      {/* Section masthead */}
      <div
        style={{
          padding: "12px 24px",
          borderBottom: "1px solid var(--border-subtle)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          background: "var(--bg-overlay)",
        }}
      >
        <p
          className="type-h3"
          style={{
            color: "var(--accent-primary)",
            letterSpacing: "0.12em",
          }}
        >
          The Deep Review · in focus
        </p>
        <Link
          href={`/ticker/${data.ticker}`}
          style={{
            fontSize: 11,
            color: "var(--accent-primary)",
            fontWeight: 500,
            display: "inline-flex",
            alignItems: "center",
            gap: 2,
            textDecoration: "none",
          }}
        >
          Full dossier <ArrowRight size={11} />
        </Link>
      </div>

      <div style={{ padding: "22px 24px" }}>
        <SpotlightHeader data={data} />
        <Performance data={data} />
        <PeerSection data={data} />
        <CouncilQuote data={data} />
        <MacroOverlay data={data} />
      </div>
    </section>
  );
}

// ── Sections ─────────────────────────────────────────────────────────

function SpotlightHeader({ data }: { data: DeepReviewTickerData }) {
  const verdictClass =
    data.verdict === "BUY" ? "pill-buy"
      : data.verdict === "HOLD" ? "pill-hold"
      : data.verdict === "AVOID" ? "pill-avoid" : "pill-na";
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 22, flexWrap: "wrap" }}>
      <TickerLogo ticker={data.ticker} size="md" />
      <div style={{ flex: 1, minWidth: 0 }}>
        <p
          className="type-h3"
          style={{ color: data.market === "br" ? "var(--mkt-br)" : "var(--mkt-us)", marginBottom: 2 }}
        >
          {data.sector} · {data.market.toUpperCase()}
        </p>
        <h2
          style={{
            fontFamily: "var(--font-display)",
            fontSize: 26,
            lineHeight: 1.15,
            fontWeight: 700,
            color: "var(--text-primary)",
            letterSpacing: "-0.015em",
            marginBottom: 4,
          }}
        >
          {data.ticker} · {data.name}
        </h2>
        <p
          style={{
            fontFamily: "var(--font-display)",
            fontSize: 14,
            color: "var(--text-secondary)",
            fontStyle: "italic",
          }}
        >
          {data.one_line_stance}
        </p>
      </div>
      <span className={`pill pill-solid ${verdictClass}`} style={{ fontSize: 12 }}>
        {data.verdict}
      </span>
    </div>
  );
}

function Performance({ data }: { data: DeepReviewTickerData }) {
  const { performance } = data;
  return (
    <div style={{ marginBottom: 26 }}>
      <SectionTitle title="How it has performed" sub="Year-to-date através das lentes do sector + benchmark" />

      {/* Performance numbers strip */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(5, 1fr)",
          gap: 14,
          padding: "14px 16px",
          background: "var(--bg-overlay)",
          border: "1px solid var(--border-subtle)",
          borderRadius: "var(--radius-sm)",
          marginBottom: 16,
        }}
      >
        <PerfBox label="YTD" value={performance.ytd_pct} highlight />
        <PerfBox label={`Sector YTD`} value={performance.sector_ytd_pct} />
        <PerfBox label="Benchmark YTD" value={performance.benchmark_ytd_pct} />
        <PerfBox label="1Y" value={performance.one_yr_pct} />
        <PerfBox label="5Y" value={performance.five_yr_pct} />
      </div>

      {/* Editorial paragraphs */}
      <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: "70ch" }}>
        {performance.review_paragraphs.map((para, i) => (
          <p
            key={i}
            style={{
              fontFamily: "var(--font-display)",
              fontSize: 15,
              lineHeight: 1.6,
              color: "var(--text-secondary)",
            }}
          >
            {para}
          </p>
        ))}
      </div>
    </div>
  );
}

function PerfBox({ label, value, highlight }: { label: string; value: number | null; highlight?: boolean }) {
  return (
    <div
      style={{
        borderLeft: highlight ? "2px solid var(--accent-primary)" : "1px solid var(--border-subtle)",
        paddingLeft: 10,
      }}
    >
      <p
        style={{
          fontSize: 9,
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          color: "var(--text-tertiary)",
          fontWeight: 600,
          marginBottom: 4,
        }}
      >
        {label}
      </p>
      <span style={{ fontSize: 16 }}>
        <PercentDelta pct={value} inline />
      </span>
    </div>
  );
}

function PeerSection({ data }: { data: DeepReviewTickerData }) {
  return (
    <div style={{ marginBottom: 26 }}>
      <SectionTitle title="Competitors at this moment" sub={`Pares no sector ${data.sector} · onde estás na fila`} />
      <table className="data-table" style={{ fontSize: 13 }}>
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Name</th>
            <th className="num">P/E</th>
            <th className="num">P/B</th>
            <th className="num">DY</th>
            <th className="num">ROE</th>
          </tr>
        </thead>
        <tbody>
          {data.peers.map((p) => (
            <tr
              key={p.ticker}
              style={{
                cursor: "default",
                background: p.is_self ? "var(--jpm-blue-soft)" : undefined,
              }}
            >
              <td>
                <span
                  className="font-data"
                  style={{
                    fontSize: 13,
                    fontWeight: p.is_self ? 700 : 600,
                    color: p.is_self ? "var(--jpm-blue)" : "var(--text-primary)",
                  }}
                >
                  {p.ticker} {p.is_self ? <span style={{ fontSize: 9, marginLeft: 4 }}>YOU</span> : null}
                </span>
              </td>
              <td style={{ color: "var(--text-secondary)" }}>{p.name}</td>
              <td className="num">{p.pe !== null ? p.pe.toFixed(1) : "—"}</td>
              <td className="num">{p.pb !== null ? p.pb.toFixed(2) : "—"}</td>
              <td className="num">{p.dy !== null ? p.dy.toFixed(1) + "%" : "—"}</td>
              <td className="num">{p.roe !== null ? p.roe.toFixed(1) + "%" : "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function CouncilQuote({ data }: { data: DeepReviewTickerData }) {
  if (!data.council_quote) return null;
  const q = data.council_quote;
  return (
    <div style={{ marginBottom: 26 }}>
      <SectionTitle title="What the council said" sub={`Synthetic IC · ${q.date}`} />
      <blockquote
        style={{
          margin: 0,
          padding: "16px 22px",
          borderLeft: "3px solid var(--action-gold)",
          background: "var(--action-gold-soft)",
          borderRadius: "0 var(--radius-sm) var(--radius-sm) 0",
        }}
      >
        <p
          style={{
            fontFamily: "var(--font-display)",
            fontSize: 16,
            lineHeight: 1.55,
            fontStyle: "italic",
            color: "var(--action-gold-ink)",
            marginBottom: 8,
          }}
        >
          “{q.text}”
        </p>
        <p
          style={{
            fontFamily: "var(--font-sans)",
            fontSize: 11,
            fontWeight: 600,
            letterSpacing: "0.08em",
            textTransform: "uppercase",
            color: "var(--action-gold-deep)",
          }}
        >
          — {q.persona}
        </p>
      </blockquote>
    </div>
  );
}

function MacroOverlay({ data }: { data: DeepReviewTickerData }) {
  const score = data.macro_overlay.sector_score;
  const tone = score > 0.2 ? "tail" : score < -0.2 ? "head" : "neutral";
  const toneColor =
    tone === "tail" ? "var(--gain)" : tone === "head" ? "var(--loss)" : "var(--text-tertiary)";
  const toneLabel =
    tone === "tail" ? "TAILWIND" : tone === "head" ? "HEADWIND" : "NEUTRAL";

  return (
    <div>
      <SectionTitle title="Macro overlay" sub="Regime e sector tilt" />
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 14,
          padding: 14,
          background: "var(--bg-overlay)",
          border: "1px solid var(--border-subtle)",
          borderRadius: "var(--radius-sm)",
          flexWrap: "wrap",
        }}
      >
        <span
          style={{
            fontSize: 10,
            fontWeight: 700,
            letterSpacing: "0.1em",
            padding: "3px 10px",
            background: "var(--bg-elevated)",
            border: `1px solid ${toneColor}`,
            color: toneColor,
            borderRadius: 999,
          }}
        >
          {toneLabel}
        </span>
        <span
          className="font-data"
          style={{ fontSize: 13, fontWeight: 600, color: "var(--text-secondary)" }}
        >
          {data.macro_overlay.regime}
        </span>
        <span style={{ fontFamily: "var(--font-display)", fontStyle: "italic", color: "var(--text-secondary)", fontSize: 14, flex: 1, minWidth: 200 }}>
          {data.macro_overlay.line}
        </span>
      </div>
    </div>
  );
}

// ── Section title primitive ─────────────────────────────────────────

function SectionTitle({ title, sub }: { title: string; sub: string }) {
  return (
    <div style={{ marginBottom: 12 }}>
      <h3
        style={{
          fontFamily: "var(--font-display)",
          fontSize: 18,
          lineHeight: 1.25,
          fontWeight: 700,
          color: "var(--text-primary)",
          letterSpacing: "-0.005em",
          marginBottom: 2,
          paddingBottom: 4,
          borderBottom: "1px solid var(--border-subtle)",
          display: "inline-block",
        }}
      >
        {title}
      </h3>
      <p className="type-byline" style={{ marginTop: 4 }}>{sub}</p>
    </div>
  );
}
