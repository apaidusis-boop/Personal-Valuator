"use client";

// ── Desk · Positions blotter ─────────────────────────────────────────
//
// Compact IB-style table. Click a row → setFocus → big chart updates.
// Active row gets a gold left-border (matches /desk header focus chip).

import { useState, useMemo } from "react";
import { useFocusTicker } from "@/lib/focus-ticker";
import { TickerLogo, PercentDelta } from "../jpm-atoms";
import { formatCurrency } from "@/lib/format";
import type { DeskPosition } from "@/lib/desk-data";

type SortKey = "weight" | "pnl" | "ticker" | "value";
type SortDir = "asc" | "desc";

export function PositionsBlotter({ positions }: { positions: DeskPosition[] }) {
  const { focus, setFocus } = useFocusTicker();
  const [marketFilter, setMarketFilter] = useState<"all" | "br" | "us">("all");
  const [sort, setSort] = useState<SortKey>("weight");
  const [dir, setDir] = useState<SortDir>("desc");

  const rows = useMemo(() => {
    let xs = positions;
    if (marketFilter !== "all") xs = xs.filter((p) => p.market === marketFilter);
    xs = [...xs].sort((a, b) => {
      let cmp = 0;
      if (sort === "weight") cmp = a.weight_pct - b.weight_pct;
      else if (sort === "pnl") cmp = (a.pnl_pct ?? -Infinity) - (b.pnl_pct ?? -Infinity);
      else if (sort === "ticker") cmp = a.ticker.localeCompare(b.ticker);
      else if (sort === "value") cmp = a.current_value - b.current_value;
      return dir === "asc" ? cmp : -cmp;
    });
    return xs;
  }, [positions, marketFilter, sort, dir]);

  function flip(k: SortKey) {
    if (sort === k) setDir(dir === "asc" ? "desc" : "asc");
    else { setSort(k); setDir("desc"); }
  }

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
      {/* Toolbar */}
      <div
        style={{
          padding: "8px 14px",
          borderBottom: "1px solid var(--border-subtle)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 10,
          background: "var(--bg-overlay)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span className="type-h3" style={{ color: "var(--text-tertiary)" }}>Positions</span>
          <div className="segmented" role="tablist" aria-label="Mercado" style={{ padding: 2 }}>
            {(["all", "br", "us"] as const).map((m) => (
              <button
                key={m}
                data-active={marketFilter === m}
                onClick={() => setMarketFilter(m)}
                style={{ padding: "3px 10px", fontSize: 11 }}
              >
                {m === "all" ? "All" : m.toUpperCase()}
              </button>
            ))}
          </div>
        </div>
        <span className="type-byline">{rows.length} rows</span>
      </div>

      {/* Table — scrollable area */}
      <div style={{ overflowY: "auto", flex: 1 }}>
        <table className="data-table" style={{ fontSize: 12 }}>
          <thead style={{ position: "sticky", top: 0, background: "var(--bg-elevated)", zIndex: 1 }}>
            <tr>
              <th style={{ paddingLeft: 14 }}><SortHeader label="Ticker" k="ticker" sort={sort} dir={dir} onClick={() => flip("ticker")} /></th>
              <th>Sector</th>
              <th className="num">Last</th>
              <th className="num"><SortHeader label="Value" k="value" sort={sort} dir={dir} onClick={() => flip("value")} num /></th>
              <th className="num"><SortHeader label="P&L" k="pnl" sort={sort} dir={dir} onClick={() => flip("pnl")} num /></th>
              <th className="num" style={{ paddingRight: 14 }}><SortHeader label="Weight" k="weight" sort={sort} dir={dir} onClick={() => flip("weight")} num /></th>
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr><td colSpan={6} style={{ padding: 20, textAlign: "center", color: "var(--text-tertiary)" }}>Sem posições.</td></tr>
            ) : rows.map((p) => {
              const isActive = p.ticker === focus.ticker;
              const currency: "BRL" | "USD" = p.market === "br" ? "BRL" : "USD";
              return (
                <tr
                  key={p.ticker}
                  onClick={() => setFocus(p.ticker, p.market)}
                  style={{
                    background: isActive ? "var(--action-gold-soft)" : undefined,
                    borderLeft: isActive ? "3px solid var(--action-gold)" : "3px solid transparent",
                  }}
                >
                  <td style={{ paddingLeft: 14 }}>
                    <div className="flex items-center gap-2">
                      <TickerLogo ticker={p.ticker} size="sm" />
                      <span
                        className="font-data"
                        style={{ fontWeight: isActive ? 700 : 600, color: isActive ? "var(--action-gold-deep)" : "var(--text-primary)" }}
                      >
                        {p.ticker}
                      </span>
                      <span
                        style={{
                          fontSize: 9, fontWeight: 700, letterSpacing: "0.04em",
                          padding: "1px 5px", borderRadius: 3,
                          background: p.market === "br" ? "var(--jpm-gain-soft)" : "var(--jpm-blue-soft)",
                          color: p.market === "br" ? "var(--mkt-br)" : "var(--mkt-us)",
                        }}
                      >
                        {p.market.toUpperCase()}
                      </span>
                    </div>
                  </td>
                  <td style={{ color: "var(--text-secondary)", fontSize: 11, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: 130 }}>
                    {p.sector || "—"}
                  </td>
                  <td className="num" style={{ color: "var(--text-secondary)", fontSize: 11 }}>
                    {p.current_unit !== null ? p.current_unit.toFixed(2) : "—"}
                  </td>
                  <td className="num" style={{ fontWeight: 500 }}>
                    {formatCurrency(p.current_value, currency, 0)}
                  </td>
                  <td className="num"><PercentDelta pct={p.pnl_pct} inline /></td>
                  <td className="num" style={{ paddingRight: 14 }}>
                    {p.weight_pct.toFixed(1)}%
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function SortHeader({
  label, k, sort, dir, onClick, num,
}: {
  label: string; k: SortKey; sort: SortKey; dir: SortDir; onClick: () => void; num?: boolean;
}) {
  const active = sort === k;
  return (
    <button
      onClick={onClick}
      style={{
        background: "transparent", border: 0, cursor: "pointer", padding: 0,
        font: "inherit", color: active ? "var(--text-primary)" : "var(--text-tertiary)",
        textTransform: "inherit", letterSpacing: "inherit",
        display: "inline-flex", alignItems: "center", gap: 3,
        flexDirection: num ? "row-reverse" : "row",
      }}
    >
      {label}
      {active ? <span style={{ fontSize: 8 }}>{dir === "asc" ? "▲" : "▼"}</span> : null}
    </button>
  );
}
