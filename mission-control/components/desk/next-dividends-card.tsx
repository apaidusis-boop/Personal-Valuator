"use client";

// ── Desk · Right rail · Next dividends ───────────────────────────────
//
// Vertical stacked list, 1 row per upcoming payment (real `dividends`
// from BR + US, ex_date in next 30 days). Click → setFocus to that
// ticker so the big chart updates.

import { useFocusTicker } from "@/lib/focus-ticker";
import type { DividendEvent } from "@/lib/db";

export function NextDividendsCard({ items }: { items: DividendEvent[] }) {
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
          background: "var(--jpm-gain-soft)",
        }}
      >
        <p className="type-h3" style={{ color: "var(--verdict-buy)", letterSpacing: "0.1em" }}>
          Next dividends
        </p>
        <p className="type-byline" style={{ marginTop: 2 }}>
          Próximos 30 dias · {items.length}
        </p>
      </header>

      <div style={{ overflowY: "auto", flex: 1, padding: "4px 0" }}>
        {items.length === 0 ? (
          <p className="type-byline" style={{ padding: 14, textAlign: "center" }}>
            Sem dividendos confirmados.
          </p>
        ) : (
          items.map((d) => {
            const isActive = d.ticker === focus.ticker;
            const sym = d.currency === "BRL" ? "R$" : "$";
            return (
              <button
                key={`${d.ticker}-${d.ex_date}`}
                onClick={() => setFocus(d.ticker, d.market)}
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
                  <span
                    className="font-data"
                    style={{ fontSize: 12, fontWeight: 700, color: isActive ? "var(--action-gold-deep)" : "var(--text-primary)" }}
                  >
                    {d.ticker}
                  </span>
                  <span style={{ fontSize: 10, color: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>
                    ex {formatShort(d.ex_date)}
                  </span>
                </div>
                <div style={{ textAlign: "right" }}>
                  <span
                    className="font-data"
                    style={{ fontSize: 13, fontWeight: 700, color: "var(--verdict-buy)" }}
                  >
                    {sym}{d.amount.toFixed(2)}
                  </span>
                </div>
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
