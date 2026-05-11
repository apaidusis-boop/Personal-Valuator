"use client";

// ── WORKBENCH · POSITIONS TAB ────────────────────────────────────────
//
// IB-density blotter with ~7 columns. Click a row → side-sheet (existing
// behaviour). Sortable headers. Top-of-page chip strip switches the
// market without touching focus-ticker context.
//
// Note: this tab consumes BOTH markets (BR + US). The chip strip lets
// the user flip without leaving the workbench.

import { useState, useMemo } from "react";
import type { HomePosition } from "../../home-view";
import { TickerLogo, PercentDelta } from "../../jpm-atoms";
import { formatCurrency } from "@/lib/format";
import { openTickerSheet } from "@/lib/ticker-sheet";
import { useFocusTicker } from "@/lib/focus-ticker";

export type PositionsTabProps = {
  br_positions: HomePosition[];
  us_positions: HomePosition[];
};

type SortKey = "value" | "pnl" | "weight" | "ticker";
type SortDir = "asc" | "desc";

export function PositionsTab({ br_positions, us_positions }: PositionsTabProps) {
  const [market, setMarket] = useState<"br" | "us">("us");
  const [sort, setSort] = useState<SortKey>("value");
  const [dir, setDir] = useState<SortDir>("desc");
  const { setFocus } = useFocusTicker();

  const rows = market === "br" ? br_positions : us_positions;
  const currency: "BRL" | "USD" = market === "br" ? "BRL" : "USD";

  const sortedRows = useMemo(() => {
    const copy = [...rows];
    const totalValue = copy.reduce((s, r) => s + r.current_value, 0) || 1;
    copy.sort((a, b) => {
      let av: number | string = 0;
      let bv: number | string = 0;
      if (sort === "value") { av = a.current_value; bv = b.current_value; }
      else if (sort === "pnl") { av = a.pnl_pct ?? -Infinity; bv = b.pnl_pct ?? -Infinity; }
      else if (sort === "weight") { av = a.current_value / totalValue; bv = b.current_value / totalValue; }
      else if (sort === "ticker") { av = a.ticker; bv = b.ticker; }
      const cmp = (typeof av === "string" && typeof bv === "string")
        ? av.localeCompare(bv as string)
        : ((av as number) - (bv as number));
      return dir === "asc" ? cmp : -cmp;
    });
    return copy;
  }, [rows, sort, dir]);

  const totalValue = sortedRows.reduce((s, r) => s + r.current_value, 0) || 1;

  function flip(key: SortKey) {
    if (sort === key) setDir(dir === "asc" ? "desc" : "asc");
    else { setSort(key); setDir("desc"); }
  }

  return (
    <div style={{ padding: "16px 20px 20px" }}>
      {/* ── Toolbar: market chip + count + sort hint ──────── */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: 12,
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <div className="segmented" role="tablist" aria-label="Mercado">
          <button data-active={market === "br"} onClick={() => setMarket("br")}>
            Brasil <span style={{ marginLeft: 6, fontSize: 10, color: "var(--text-tertiary)" }}>BRL</span>
          </button>
          <button data-active={market === "us"} onClick={() => setMarket("us")}>
            EUA <span style={{ marginLeft: 6, fontSize: 10, color: "var(--text-tertiary)" }}>USD</span>
          </button>
        </div>
        <p className="type-byline">
          {sortedRows.length} posições · ordenadas por{" "}
          <span style={{ color: "var(--text-secondary)", fontWeight: 600 }}>
            {sort === "value" ? "valor" : sort === "pnl" ? "P&L %" : sort === "weight" ? "peso" : "ticker"}
          </span>
        </p>
      </div>

      {/* ── Blotter table ─────────────────────────────────── */}
      <table className="data-table">
        <thead>
          <tr>
            <th><SortHeader label="Security" active={sort === "ticker"} dir={dir} onClick={() => flip("ticker")} /></th>
            <th>Sector</th>
            <th className="num">Qty</th>
            <th className="num">Last</th>
            <th className="num"><SortHeader label="Value" active={sort === "value"} dir={dir} onClick={() => flip("value")} num /></th>
            <th className="num"><SortHeader label="P&L" active={sort === "pnl"} dir={dir} onClick={() => flip("pnl")} num /></th>
            <th className="num"><SortHeader label="Weight" active={sort === "weight"} dir={dir} onClick={() => flip("weight")} num /></th>
          </tr>
        </thead>
        <tbody>
          {sortedRows.length === 0 ? (
            <tr>
              <td colSpan={7} style={{ textAlign: "center", padding: 24, color: "var(--text-tertiary)" }}>
                Sem posições neste mercado.
              </td>
            </tr>
          ) : (
            sortedRows.map((p) => {
              const weight = (p.current_value / totalValue) * 100;
              const totalAbs = p.current_value - p.cost_basis;
              return (
                <tr
                  key={p.ticker}
                  onClick={() => {
                    setFocus(p.ticker, market);
                    openTickerSheet(p.ticker);
                  }}
                >
                  <td>
                    <div className="flex items-center gap-3">
                      <TickerLogo ticker={p.ticker} size="sm" />
                      <div>
                        <p
                          className="font-data"
                          style={{ fontWeight: 600, color: "var(--text-primary)", fontSize: 13, marginBottom: 2 }}
                        >
                          {p.ticker}
                        </p>
                        <p className="type-byline" style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: 220 }}>
                          {p.name}
                        </p>
                      </div>
                    </div>
                  </td>
                  <td style={{ color: "var(--text-secondary)", fontSize: 12 }}>
                    {p.sector || "—"}
                  </td>
                  <td className="num" style={{ color: "var(--text-secondary)" }}>
                    {p.quantity !== null ? p.quantity.toFixed(0) : "—"}
                  </td>
                  <td className="num" style={{ color: "var(--text-secondary)" }}>
                    {p.current_unit !== null ? p.current_unit.toFixed(2) : "—"}
                  </td>
                  <td className="num" style={{ color: "var(--text-primary)", fontWeight: 500 }}>
                    {formatCurrency(p.current_value, currency, 2)}
                  </td>
                  <td className="num">
                    <PercentDelta pct={p.pnl_pct} abs={totalAbs} currency={currency} />
                  </td>
                  <td className="num" style={{ color: "var(--text-primary)" }}>
                    <WeightBar pct={weight} />
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}

function SortHeader({
  label,
  active,
  dir,
  onClick,
  num,
}: {
  label: string;
  active: boolean;
  dir: SortDir;
  onClick: () => void;
  num?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      style={{
        background: "transparent",
        border: 0,
        cursor: "pointer",
        padding: 0,
        font: "inherit",
        color: active ? "var(--text-primary)" : "var(--text-tertiary)",
        textTransform: "inherit",
        letterSpacing: "inherit",
        display: "inline-flex",
        alignItems: "center",
        gap: 4,
        flexDirection: num ? "row-reverse" : "row",
      }}
    >
      {label}
      {active ? <span style={{ fontSize: 8 }}>{dir === "asc" ? "▲" : "▼"}</span> : null}
    </button>
  );
}

function WeightBar({ pct }: { pct: number }) {
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 8, justifyContent: "flex-end" }}>
      <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, minWidth: 42, textAlign: "right" }}>
        {pct.toFixed(1)}%
      </span>
      <span
        aria-hidden
        style={{
          width: 48,
          height: 4,
          background: "var(--bg-overlay)",
          borderRadius: 2,
          overflow: "hidden",
          flexShrink: 0,
        }}
      >
        <span
          style={{
            display: "block",
            width: `${Math.min(100, Math.max(0, pct))}%`,
            height: "100%",
            background: "var(--accent-primary)",
          }}
        />
      </span>
    </span>
  );
}
