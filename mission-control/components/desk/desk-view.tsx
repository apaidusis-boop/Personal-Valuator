"use client";

// ── /desk · 4-pane Bloomberg layout ───────────────────────────────────
//
// Inspired by patterns from overnight Bloomberg research (Launchpad,
// multi-pane Worksheets). Synced by focus-ticker:
//   - clicking a position row updates the big chart
//   - clicking a dividend or filing row updates the big chart
//
// Grid:
//   ┌─────────────────────────────────────┬──────────────┐
//   │ BigChart (focus ticker)             │ NextDividends│
//   │ (60% height)                        │              │
//   ├─────────────────────────────────────┤              │
//   │ PositionsBlotter (compact)          ├──────────────┤
//   │ (40% height)                        │ NextFilings  │
//   └─────────────────────────────────────┴──────────────┘

import type { DeskData } from "@/lib/desk-data";
import { FocusTickerProvider } from "@/lib/focus-ticker";
import { BigChart } from "./big-chart";
import { PositionsBlotter } from "./positions-blotter";
import { NextDividendsCard } from "./next-dividends-card";
import { NextFilingsCard } from "./next-filings-card";
import { DeskHeader } from "./desk-header";

export function DeskView({ data }: { data: DeskData }) {
  return (
    <FocusTickerProvider
      initialTicker={data.initial_focus_ticker}
      initialMarket={data.initial_focus_market}
    >
      <div
        className="px-4 py-4 max-w-[1600px] mx-auto"
        style={{ display: "flex", flexDirection: "column", gap: 12, minHeight: "calc(100vh - 80px)" }}
      >
        <DeskHeader
          br_nav={data.br_nav}
          us_nav={data.us_nav}
          n_positions={data.positions.length}
        />

        {/* Main 4-pane grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "minmax(0, 1fr) 280px",
            gridTemplateRows: "minmax(320px, 1fr) minmax(280px, auto)",
            gap: 12,
            flex: 1,
          }}
        >
          {/* Top-left: Big chart */}
          <div style={{ gridColumn: 1, gridRow: 1 }}>
            <BigChart positions={data.positions} />
          </div>

          {/* Bottom-left: Positions blotter */}
          <div style={{ gridColumn: 1, gridRow: 2 }}>
            <PositionsBlotter positions={data.positions} />
          </div>

          {/* Right rail: 2 stacked cards */}
          <div style={{ gridColumn: 2, gridRow: 1, minHeight: 0 }}>
            <NextDividendsCard items={data.next_dividends} />
          </div>
          <div style={{ gridColumn: 2, gridRow: 2, minHeight: 0 }}>
            <NextFilingsCard items={data.next_filings} />
          </div>
        </div>
      </div>
    </FocusTickerProvider>
  );
}
