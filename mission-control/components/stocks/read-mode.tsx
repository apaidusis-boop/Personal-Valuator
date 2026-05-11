"use client";

// ── /stocks · Read mode (magazine layout) ─────────────────────────────
//
// Left rail: scrollable holdings list. Sort + filter controls at the top.
// Right pane: TickerTearsheet for the focus ticker (verdict, fundamentals
// strip, performance paragraphs from DeepReview, peers, council, macro).
//
// Click an item in the rail → focus updates → tearsheet re-renders.

import { useState, useMemo } from "react";
import type { StocksData, StockRow } from "@/lib/stocks-data";
import { useFocusTicker } from "@/lib/focus-ticker";
import { TickerLogo, PercentDelta } from "../jpm-atoms";
import { TickerTearsheet } from "./ticker-tearsheet";

type SortKey = "weight" | "verdict" | "dy" | "pnl" | "ticker" | "fv_gap";
type KindFilter = "holdings" | "watchlist" | "all";

const VERDICT_RANK: Record<string, number> = { BUY: 0, HOLD: 1, AVOID: 2, "N/A": 3 };

export function ReadMode({ data }: { data: StocksData }) {
  const { focus, setFocus } = useFocusTicker();
  const [sort, setSort] = useState<SortKey>("weight");
  const [kindFilter, setKindFilter] = useState<KindFilter>("holdings");
  const [marketFilter, setMarketFilter] = useState<"all" | "br" | "us">("all");
  const [verdictFilter, setVerdictFilter] = useState<"all" | "BUY" | "HOLD" | "AVOID">("all");
  const [search, setSearch] = useState("");

  const filtered = useMemo(() => {
    let rows = data.rows;
    if (kindFilter === "holdings") rows = rows.filter((r) => r.kind === "holding");
    else if (kindFilter === "watchlist") rows = rows.filter((r) => r.kind === "watchlist");
    if (marketFilter !== "all") rows = rows.filter((r) => r.market === marketFilter);
    if (verdictFilter !== "all") rows = rows.filter((r) => r.verdict === verdictFilter);
    if (search.trim()) {
      const q = search.trim().toUpperCase();
      rows = rows.filter((r) => r.ticker.toUpperCase().includes(q) || r.name.toUpperCase().includes(q));
    }
    rows = [...rows].sort((a, b) => {
      switch (sort) {
        case "verdict": return (VERDICT_RANK[a.verdict] ?? 9) - (VERDICT_RANK[b.verdict] ?? 9);
        case "dy": return (b.dy ?? 0) - (a.dy ?? 0);
        case "pnl": return (b.pnl_pct ?? -Infinity) - (a.pnl_pct ?? -Infinity);
        case "ticker": return a.ticker.localeCompare(b.ticker);
        case "fv_gap": return (a.fv_gap_pct ?? 999) - (b.fv_gap_pct ?? 999);
        default:
          // Weight is null for watchlist; for non-holding rows weight sort
          // falls back to FV gap so the cheapest watchlist names float up
          if (a.weight_pct === null && b.weight_pct === null) {
            return (a.fv_gap_pct ?? 999) - (b.fv_gap_pct ?? 999);
          }
          return (b.weight_pct ?? 0) - (a.weight_pct ?? 0);
      }
    });
    return rows;
  }, [data.rows, kindFilter, marketFilter, verdictFilter, search, sort]);

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "minmax(280px, 320px) 1fr",
        gap: 18,
        alignItems: "start",
      }}
    >
      {/* ── Left rail ──────────────────────────────────── */}
      <aside
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
          borderRadius: "var(--radius)",
          overflow: "hidden",
          position: "sticky",
          top: 16,
          maxHeight: "calc(100vh - 100px)",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <RailHeader
          search={search}
          setSearch={setSearch}
          kindFilter={kindFilter}
          setKindFilter={setKindFilter}
          marketFilter={marketFilter}
          setMarketFilter={setMarketFilter}
          verdictFilter={verdictFilter}
          setVerdictFilter={setVerdictFilter}
          sort={sort}
          setSort={setSort}
          count={filtered.length}
          total={data.rows.length}
          n_holdings={data.n_holdings}
          n_watchlist={data.n_watchlist}
        />
        <div style={{ overflowY: "auto", flex: 1 }}>
          {filtered.length === 0 ? (
            <p className="type-byline" style={{ padding: 20, textAlign: "center" }}>
              Sem resultados.
            </p>
          ) : (
            filtered.map((r) => (
              <RailItem
                key={r.ticker}
                row={r}
                active={r.ticker === focus.ticker}
                onClick={() => setFocus(r.ticker, r.market)}
              />
            ))
          )}
        </div>
      </aside>

      {/* ── Right pane: tearsheet ─────────────────────── */}
      <div>
        <TickerTearsheet data={data} />
      </div>
    </div>
  );
}

// ── Rail header ─────────────────────────────────────────────────────

function RailHeader({
  search, setSearch,
  kindFilter, setKindFilter,
  marketFilter, setMarketFilter,
  verdictFilter, setVerdictFilter,
  sort, setSort,
  count, total,
  n_holdings, n_watchlist,
}: {
  search: string; setSearch: (v: string) => void;
  kindFilter: KindFilter; setKindFilter: (v: KindFilter) => void;
  marketFilter: "all" | "br" | "us"; setMarketFilter: (v: "all" | "br" | "us") => void;
  verdictFilter: "all" | "BUY" | "HOLD" | "AVOID"; setVerdictFilter: (v: "all" | "BUY" | "HOLD" | "AVOID") => void;
  sort: SortKey; setSort: (v: SortKey) => void;
  count: number; total: number;
  n_holdings: number; n_watchlist: number;
}) {
  return (
    <div style={{ padding: 12, borderBottom: "1px solid var(--border-subtle)", background: "var(--bg-overlay)" }}>
      <input
        placeholder="Procurar ticker ou nome..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{
          width: "100%",
          padding: "6px 10px",
          border: "1px solid var(--border-subtle)",
          borderRadius: 4,
          fontSize: 12,
          fontFamily: "var(--font-sans)",
          background: "var(--bg-elevated)",
          color: "var(--text-primary)",
          marginBottom: 10,
        }}
      />
      {/* Kind filter — Holdings / Watchlist / All */}
      <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 8 }}>
        <FilterChip
          label={`Holdings (${n_holdings})`}
          active={kindFilter === "holdings"}
          onClick={() => setKindFilter("holdings")}
        />
        <FilterChip
          label={`Watchlist (${n_watchlist})`}
          active={kindFilter === "watchlist"}
          onClick={() => setKindFilter("watchlist")}
        />
        <FilterChip
          label={`All (${n_holdings + n_watchlist})`}
          active={kindFilter === "all"}
          onClick={() => setKindFilter("all")}
        />
      </div>
      <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 8 }}>
        <FilterChip label="Todos" active={marketFilter === "all"} onClick={() => setMarketFilter("all")} />
        <FilterChip label="BR" active={marketFilter === "br"} onClick={() => setMarketFilter("br")} />
        <FilterChip label="US" active={marketFilter === "us"} onClick={() => setMarketFilter("us")} />
      </div>
      <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 8 }}>
        <FilterChip label="All verdicts" active={verdictFilter === "all"} onClick={() => setVerdictFilter("all")} />
        <FilterChip label="BUY" active={verdictFilter === "BUY"} onClick={() => setVerdictFilter("BUY")} tone="buy" />
        <FilterChip label="HOLD" active={verdictFilter === "HOLD"} onClick={() => setVerdictFilter("HOLD")} tone="hold" />
        <FilterChip label="AVOID" active={verdictFilter === "AVOID"} onClick={() => setVerdictFilter("AVOID")} tone="avoid" />
      </div>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <select
          value={sort}
          onChange={(e) => setSort(e.target.value as SortKey)}
          style={{
            padding: "4px 8px",
            border: "1px solid var(--border-subtle)",
            borderRadius: 4,
            fontSize: 11,
            fontFamily: "var(--font-sans)",
            background: "var(--bg-elevated)",
            color: "var(--text-primary)",
          }}
        >
          <option value="weight">Sort: peso</option>
          <option value="verdict">Sort: verdict</option>
          <option value="dy">Sort: DY</option>
          <option value="pnl">Sort: P&L %</option>
          <option value="fv_gap">Sort: FV gap</option>
          <option value="ticker">Sort: ticker</option>
        </select>
        <p className="type-byline">{count} de {total}</p>
      </div>
    </div>
  );
}

function FilterChip({
  label, active, onClick, tone,
}: {
  label: string; active: boolean; onClick: () => void; tone?: "buy" | "hold" | "avoid";
}) {
  const toneColor = tone === "buy" ? "var(--verdict-buy)"
    : tone === "hold" ? "var(--verdict-hold)"
    : tone === "avoid" ? "var(--verdict-avoid)" : "var(--text-tertiary)";
  return (
    <button
      onClick={onClick}
      style={{
        padding: "3px 9px",
        background: active ? (tone ? toneColor : "var(--accent-primary)") : "transparent",
        color: active ? "white" : (tone ? toneColor : "var(--text-secondary)"),
        border: `1px solid ${tone ? toneColor : "var(--border-subtle)"}`,
        borderRadius: 999,
        fontSize: 10,
        fontWeight: 600,
        letterSpacing: "0.04em",
        cursor: "pointer",
        fontFamily: "var(--font-sans)",
      }}
    >
      {label}
    </button>
  );
}

// ── Rail item ────────────────────────────────────────────────────────

function RailItem({ row, active, onClick }: { row: StockRow; active: boolean; onClick: () => void }) {
  const verdictColor = row.verdict === "BUY" ? "var(--verdict-buy)"
    : row.verdict === "HOLD" ? "var(--verdict-hold)"
    : row.verdict === "AVOID" ? "var(--verdict-avoid)" : "var(--verdict-na)";
  return (
    <button
      onClick={onClick}
      style={{
        width: "100%",
        textAlign: "left",
        padding: "10px 12px",
        background: active ? "var(--jpm-blue-soft)" : "transparent",
        borderLeft: active ? "3px solid var(--jpm-blue)" : "3px solid transparent",
        borderBottom: "1px solid var(--border-subtle)",
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        gap: 10,
        font: "inherit",
        color: "var(--text-primary)",
        transition: "background var(--motion-fast)",
      }}
      onMouseEnter={(e) => { if (!active) (e.currentTarget.style.background = "var(--bg-overlay)"); }}
      onMouseLeave={(e) => { if (!active) (e.currentTarget.style.background = "transparent"); }}
    >
      <TickerLogo ticker={row.ticker} size="sm" />
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 6 }}>
          <span style={{ display: "inline-flex", alignItems: "baseline", gap: 5 }}>
            <span
              className="font-data"
              style={{ fontSize: 12, fontWeight: 700, color: active ? "var(--jpm-blue)" : "var(--text-primary)" }}
            >
              {row.ticker}
            </span>
            {row.kind === "watchlist" ? (
              <span
                style={{
                  fontSize: 8,
                  fontWeight: 700,
                  letterSpacing: "0.06em",
                  color: "var(--text-tertiary)",
                  border: "1px solid var(--border-subtle)",
                  borderRadius: 2,
                  padding: "0 4px",
                }}
              >
                WL
              </span>
            ) : null}
          </span>
          <span
            style={{
              fontSize: 9,
              fontWeight: 700,
              letterSpacing: "0.06em",
              color: verdictColor,
            }}
          >
            ●{row.verdict}
          </span>
        </div>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 6 }}>
          <span
            className="type-byline"
            style={{
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
              maxWidth: 140,
            }}
          >
            {row.name}
          </span>
          <span style={{ fontSize: 10 }}>
            {row.kind === "holding" ? (
              <PercentDelta pct={row.pnl_pct} inline />
            ) : row.fv_gap_pct !== null ? (
              <span
                className="font-data"
                style={{
                  fontSize: 10,
                  color: row.fv_gap_pct < 0 ? "var(--gain)"
                    : row.fv_gap_pct > 0 ? "var(--loss)" : "var(--text-tertiary)",
                  fontWeight: 600,
                }}
              >
                FV {row.fv_gap_pct >= 0 ? "+" : ""}{row.fv_gap_pct.toFixed(0)}%
              </span>
            ) : null}
          </span>
        </div>
      </div>
    </button>
  );
}
