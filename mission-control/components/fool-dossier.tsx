// Fool.com-style recommendation template renderer.
// Server-renderable. Markdown component stays compatible (no client-only APIs).
// Parser lives in lib/fool.ts so server pages can call it.

import Markdown from "./markdown";
import type { FoolFields } from "@/lib/fool";

export type { FoolFields };

// ─── Component ───────────────────────────────────────────────────────

export function FoolDossier({
  ticker,
  fields,
  stance,
}: {
  ticker: string;
  fields: FoolFields;
  stance?: string;
}) {
  // If no Fool-style content was extracted, render nothing — the caller
  // falls back to the raw transcript.
  const hasContent =
    fields.foolish_thesis.length > 0 ||
    fields.what_company_does ||
    fields.why_buy ||
    fields.bottom_line;
  if (!hasContent) return null;

  return (
    <article className="space-y-5">
      {/* ── Foolish thesis ─────────────────────────────────────── */}
      {fields.foolish_thesis.length > 0 && (
        <FoolSection title="Foolish thesis" accent="primary">
          <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: 10 }}>
            {fields.foolish_thesis.map((bullet, i) => (
              <li
                key={i}
                style={{
                  display: "flex",
                  gap: 12,
                  paddingLeft: 0,
                  alignItems: "baseline",
                }}
              >
                <span
                  aria-hidden
                  style={{
                    flexShrink: 0,
                    fontFamily: "var(--font-mono)",
                    color: "var(--accent-primary)",
                    fontWeight: 600,
                    fontSize: 13,
                    minWidth: 18,
                  }}
                >
                  {i + 1}.
                </span>
                <p
                  style={{
                    margin: 0,
                    fontSize: 14,
                    color: "var(--text-secondary)",
                    lineHeight: 1.55,
                  }}
                >
                  {bullet}
                </p>
              </li>
            ))}
          </ul>
        </FoolSection>
      )}

      {/* ── Analyst projections ribbon ─────────────────────────── */}
      {(fields.investing_type ||
        fields.est_annualized_return ||
        fields.est_max_drawdown) && (
        <FoolSection title="Analyst projections" accent="muted" compact>
          <div className="grid grid-cols-1 md:grid-cols-3" style={{ gap: 0 }}>
            <ProjectionStat label="Investing type" value={fields.investing_type} />
            <ProjectionStat
              label="Est. annualized return"
              value={fields.est_annualized_return}
              divide
            />
            <ProjectionStat
              label="Est. max drawdown"
              value={fields.est_max_drawdown}
              divide
            />
          </div>
        </FoolSection>
      )}

      {/* ── What X does ────────────────────────────────────────── */}
      {fields.what_company_does && (
        <FoolSection title={`What ${ticker} does`}>
          <Markdown source={fields.what_company_does} />
        </FoolSection>
      )}

      {/* ── Why it's a buy ─────────────────────────────────────── */}
      {fields.why_buy && (
        <FoolSection title="Why it's a buy" accent="gain">
          <Markdown source={fields.why_buy} />
        </FoolSection>
      )}

      {/* ── What could go wrong ────────────────────────────────── */}
      {fields.what_could_go_wrong && (
        <FoolSection title="What could go wrong" accent="loss">
          <Markdown source={fields.what_could_go_wrong} />
        </FoolSection>
      )}

      {/* ── Who else to watch ──────────────────────────────────── */}
      {fields.who_else_to_watch && (
        <FoolSection title="Who else to watch">
          <Markdown source={fields.who_else_to_watch} />
        </FoolSection>
      )}

      {/* ── Bottom line + Portfolio fit (paired) ───────────────── */}
      {(fields.bottom_line || fields.portfolio_fit) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {fields.bottom_line && (
            <FoolSection title="Bottom line" accent="primary">
              <Markdown source={fields.bottom_line} />
            </FoolSection>
          )}
          {fields.portfolio_fit && (
            <FoolSection title="Portfolio fit">
              <Markdown source={fields.portfolio_fit} />
            </FoolSection>
          )}
        </div>
      )}

      {/* ── What our team thinks ───────────────────────────────── */}
      {fields.what_team_thinks && (
        <FoolSection title="What our team thinks" accent="primary">
          <Markdown source={fields.what_team_thinks} />
        </FoolSection>
      )}
    </article>
  );
}

// ─── Sub-components ──────────────────────────────────────────────────

function FoolSection({
  title,
  children,
  accent = "default",
  compact = false,
}: {
  title: string;
  children: React.ReactNode;
  accent?: "default" | "primary" | "gain" | "loss" | "muted";
  compact?: boolean;
}) {
  const borderTop =
    accent === "primary"
      ? "2px solid var(--accent-primary)"
      : accent === "gain"
      ? "2px solid var(--verdict-buy)"
      : accent === "loss"
      ? "2px solid var(--verdict-avoid)"
      : "1px solid var(--border-subtle)";

  return (
    <section
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderTop,
        borderRadius: "var(--radius)",
        padding: compact ? "16px 20px" : "24px",
        boxShadow: "var(--shadow-sm)",
      }}
    >
      <h3
        className="type-h3"
        style={{ marginBottom: compact ? 8 : 14 }}
      >
        {title}
      </h3>
      {children}
    </section>
  );
}

function ProjectionStat({
  label,
  value,
  divide,
}: {
  label: string;
  value: string | null;
  divide?: boolean;
}) {
  return (
    <div
      style={{
        padding: "8px 16px",
        borderLeft: divide ? "1px solid var(--border-subtle)" : "0",
      }}
    >
      <p className="type-caption" style={{ marginBottom: 4 }}>
        {label}
      </p>
      <p
        className="font-data tabular"
        style={{
          fontSize: 14,
          fontWeight: 600,
          color: value ? "var(--text-primary)" : "var(--text-disabled)",
          margin: 0,
        }}
      >
        {value || "—"}
      </p>
    </div>
  );
}
