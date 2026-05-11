"use client";

// ── Desk · Right rail · Next filings ─────────────────────────────────
//
// Earnings calendar → projected filing kind (10-Q / 10-K / ITR / DFP).
// Holdings get a small dot accent. Click → setFocus.

import { useFocusTicker } from "@/lib/focus-ticker";
import type { UpcomingFiling } from "@/lib/db";

export function NextFilingsCard({ items }: { items: UpcomingFiling[] }) {
  const { setFocus, focus } = useFocusTicker();

  return (
    <section
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderRadius: "var(--radius)",
        boxShadow: "var(--shadow-sm)",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
      }}
    >
      <header
        style={{
          padding: "10px 14px",
          borderBottom: "1px solid var(--border-subtle)",
          background: "var(--jpm-blue-soft)",
        }}
      >
        <p className="type-h3" style={{ color: "var(--mkt-us)", letterSpacing: "0.1em" }}>
          Next filings
        </p>
        <p className="type-byline" style={{ marginTop: 2 }}>
          Próximos 30 dias · {items.length}
        </p>
      </header>

      <div style={{ overflowY: "auto", flex: 1, padding: "4px 0" }}>
        {items.length === 0 ? (
          <p className="type-byline" style={{ padding: 14, textAlign: "center" }}>
            Sem earnings agendados.
          </p>
        ) : (
          items.map((f) => {
            const isActive = f.ticker === focus.ticker;
            return (
              <button
                key={`${f.ticker}-${f.earnings_date}`}
                onClick={() => setFocus(f.ticker, f.market)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  width: "100%",
                  padding: "10px 14px",
                  background: isActive ? "var(--action-gold-soft)" : "transparent",
                  border: 0,
                  borderLeft: isActive ? "3px solid var(--action-gold)" : "3px solid transparent",
                  borderBottom: "1px solid var(--border-subtle)",
                  cursor: "pointer",
                  textAlign: "left",
                  fontFamily: "var(--font-sans)",
                  transition: "background var(--motion-fast)",
                }}
                onMouseEnter={(e) => { if (!isActive) e.currentTarget.style.background = "var(--bg-overlay)"; }}
                onMouseLeave={(e) => { if (!isActive) e.currentTarget.style.background = "transparent"; }}
              >
                <div style={{ display: "flex", flexDirection: "column", gap: 2, minWidth: 0 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                    {f.is_holding ? <span style={{ width: 6, height: 6, borderRadius: 999, background: "var(--accent-primary)" }} aria-label="holding" /> : null}
                    <span
                      className="font-data"
                      style={{ fontSize: 12, fontWeight: 700, color: isActive ? "var(--action-gold-deep)" : "var(--text-primary)" }}
                    >
                      {f.ticker}
                    </span>
                  </div>
                  <span style={{ fontSize: 10, color: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>
                    {formatShort(f.earnings_date)}
                  </span>
                </div>
                <span
                  style={{
                    fontSize: 10, fontWeight: 700, letterSpacing: "0.04em",
                    padding: "2px 7px", borderRadius: 3,
                    background: f.market === "br" ? "var(--jpm-gain-soft)" : "var(--jpm-blue-soft)",
                    color: f.market === "br" ? "var(--mkt-br)" : "var(--mkt-us)",
                    fontFamily: "var(--font-sans)",
                  }}
                >
                  {f.projected_kind}
                </span>
              </button>
            );
          })
        )}
      </div>
    </section>
  );
}

function formatShort(iso: string): string {
  if (!iso || iso.length < 10) return iso;
  return `${iso.slice(8, 10)}/${iso.slice(5, 7)}`;
}
