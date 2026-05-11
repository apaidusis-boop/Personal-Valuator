"use client";

// ── BAND 2 · THE WORKBENCH ────────────────────────────────────────────
//
// Bloomberg/Interactive-Brokers register. This is where the user *does
// things* — manipulates, projects, speculates. Not passive reading.
//
// Single workbench with 4 tabs (Compare · DRIP Calc · Positions · Dividends).
// Tab choice persists to URL hash so a copy/paste link reopens the same
// view. Defaults to Compare with the focus ticker pre-loaded.
//
// Visual register:
//  - Denser, monospaced numbers, terminal-style segmented tabs
//  - Subtle amber accent (--action-gold) on the active tab to nod at the
//    Bloomberg amber — NOT for verdict, just for "active surface"
//  - Hairline borders, not soft shadows; this band is the workshop, not
//    the shop window

import { useState, useEffect, ReactNode } from "react";
import { CompareTab, type CompareTabProps } from "./workbench/compare-tab";
import { DripCalcTab, type DripCalcTabProps } from "./workbench/drip-calc-tab";
import { PositionsTab, type PositionsTabProps } from "./workbench/positions-tab";
import { DividendsTab, type DividendsTabProps } from "./workbench/dividends-tab";

type TabKey = "compare" | "drip" | "positions" | "dividends";

const TAB_LABELS: Record<TabKey, string> = {
  compare: "Compare",
  drip: "DRIP Calc",
  positions: "Positions",
  dividends: "Dividends",
};

const TAB_KICKERS: Record<TabKey, string> = {
  compare: "Side-by-side",
  drip: "Reactive projection",
  positions: "Blotter",
  dividends: "90-day calendar",
};

export type WorkbenchProps = {
  compare: CompareTabProps;
  drip: DripCalcTabProps;
  positions: PositionsTabProps;
  dividends: DividendsTabProps;
};

export function Workbench({ compare, drip, positions, dividends }: WorkbenchProps) {
  const [tab, setTab] = useState<TabKey>("compare");
  const [hydrated, setHydrated] = useState(false);

  // Hydrate from URL hash; persist on change
  useEffect(() => {
    const h = window.location.hash.replace("#wb-", "");
    if (h === "compare" || h === "drip" || h === "positions" || h === "dividends") {
      setTab(h);
    }
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    const url = new URL(window.location.href);
    url.hash = `wb-${tab}`;
    window.history.replaceState({}, "", url.toString());
  }, [tab, hydrated]);

  return (
    <section
      aria-label="The workbench — what if?"
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderRadius: "var(--radius)",
        boxShadow: "var(--shadow-sm)",
        overflow: "hidden",
      }}
    >
      {/* ── Tab strip ─────────────────────────────────────── */}
      <div
        role="tablist"
        aria-label="Workbench tabs"
        style={{
          display: "flex",
          alignItems: "stretch",
          borderBottom: "1px solid var(--border-subtle)",
          background: "var(--bg-overlay)",
        }}
      >
        <span
          className="type-h3"
          style={{
            padding: "16px 20px",
            color: "var(--text-tertiary)",
            display: "inline-flex",
            alignItems: "center",
            borderRight: "1px solid var(--border-subtle)",
            background: "var(--bg-elevated)",
            minWidth: 140,
          }}
        >
          The Workbench
        </span>
        {(Object.keys(TAB_LABELS) as TabKey[]).map((k) => {
          const active = k === tab;
          return (
            <button
              key={k}
              role="tab"
              aria-selected={active}
              onClick={() => setTab(k)}
              style={{
                padding: "12px 20px",
                background: active ? "var(--bg-elevated)" : "transparent",
                color: active ? "var(--text-primary)" : "var(--text-tertiary)",
                border: 0,
                borderRight: "1px solid var(--border-subtle)",
                borderTop: active ? `2px solid var(--action-gold)` : "2px solid transparent",
                cursor: "pointer",
                display: "flex",
                flexDirection: "column",
                alignItems: "flex-start",
                gap: 1,
                transition: "all var(--motion-fast)",
                fontFamily: "var(--font-sans)",
              }}
              onMouseEnter={(e) => {
                if (!active) e.currentTarget.style.color = "var(--text-secondary)";
              }}
              onMouseLeave={(e) => {
                if (!active) e.currentTarget.style.color = "var(--text-tertiary)";
              }}
            >
              <span
                style={{
                  fontSize: 9,
                  letterSpacing: "0.08em",
                  textTransform: "uppercase",
                  fontWeight: 600,
                  color: active ? "var(--action-gold-deep)" : "var(--text-tertiary)",
                }}
              >
                {TAB_KICKERS[k]}
              </span>
              <span style={{ fontSize: 14, fontWeight: 600 }}>{TAB_LABELS[k]}</span>
            </button>
          );
        })}
        <div style={{ flex: 1 }} />
      </div>

      {/* ── Active tab body ──────────────────────────────── */}
      <TabPanel active={tab === "compare"}>
        <CompareTab {...compare} />
      </TabPanel>
      <TabPanel active={tab === "drip"}>
        <DripCalcTab {...drip} />
      </TabPanel>
      <TabPanel active={tab === "positions"}>
        <PositionsTab {...positions} />
      </TabPanel>
      <TabPanel active={tab === "dividends"}>
        <DividendsTab {...dividends} />
      </TabPanel>
    </section>
  );
}

function TabPanel({ active, children }: { active: boolean; children: ReactNode }) {
  if (!active) return null;
  return <div role="tabpanel">{children}</div>;
}
