"use client";

// ── /stocks · Operate mode (IB-style blotter) ─────────────────────────
//
// Filters above the grid: market chips, sector multi-select, verdict
// chips, DY threshold. Dense table with ~12 columns, multi-sortable.
// Click row → side-sheet (existing behaviour from openTickerSheet).

import { useState, useMemo } from "react";
import type { StocksData, StockRow } from "@/lib/stocks-data";
import { TickerLogo, PercentDelta } from "../jpm-atoms";
import { formatCurrency } from "@/lib/format";
import { openTickerSheet } from "@/lib/ticker-sheet";

type SortKey =
  | "ticker" | "sector" | "verdict" | "qty" | "last"
  | "value" | "pnl" | "dy" | "pe" | "roe" | "fv_gap" | "weight";
type SortDir = "asc" | "desc";

const VERDICT_RANK: Record<string, number> = { BUY: 0, HOLD: 1, AVOID: 2, "N/A": 3 };

type KindFilter = "holdings" | "watchlist" | "all";

export function OperateMode({ data }: { data: StocksData }) {
  const [kindFilter, setKindFilter] = useState<KindFilter>("holdings");
  const [marketFilter, setMarketFilter] = useState<"all" | "br" | "us">("all");
  const [verdictFilter, setVerdictFilter] = useState<Set<"BUY" | "HOLD" | "AVOID" | "N/A">>(
    new Set(["BUY", "HOLD", "AVOID", "N/A"]),
  );
  const [sectorFilter, setSectorFilter] = useState<string>("all");
  const [minDy, setMinDy] = useState<number>(0);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<SortKey>("weight");
  const [dir, setDir] = useState<SortDir>("desc");

  const sectors = useMemo(() => {
    const s = new Set<string>();
    for (const r of data.rows) if (r.sector && r.sector !== "—") s.add(r.sector);
    return ["all", ...Array.from(s).sort()];
  }, [data.rows]);

  const rows = useMemo(() => {
    let xs = data.rows;
    if (kindFilter === "holdings") xs = xs.filter((r) => r.kind === "holding");
    else if (kindFilter === "watchlist") xs = xs.filter((r) => r.kind === "watchlist");
    if (marketFilter !== "all") xs = xs.filter((r) => r.market === marketFilter);
    if (sectorFilter !== "all") xs = xs.filter((r) => r.sector === sectorFilter);
    xs = xs.filter((r) => verdictFilter.has(r.verdict));
    if (minDy > 0) xs = xs.filter((r) => (r.dy ?? 0) >= minDy);
    if (search.trim()) {
      const q = search.trim().toUpperCase();
      xs = xs.filter((r) => r.ticker.includes(q) || r.name.toUpperCase().includes(q));
    }
    xs = [...xs].sort((a, b) => {
      const cmp = compare(a, b, sort);
      return dir === "asc" ? cmp : -cmp;
    });
    return xs;
  }, [data.rows, kindFilter, marketFilter, sectorFilter, verdictFilter, minDy, search, sort, dir]);

  function flip(k: SortKey) {
    if (sort === k) setDir(dir === "asc" ? "desc" : "asc");
    else { setSort(k); setDir("desc"); }
  }

  function toggleVerdict(v: "BUY" | "HOLD" | "AVOID" | "N/A") {
    const next = new Set(verdictFilter);
    if (next.has(v)) next.delete(v);
    else next.add(v);
    setVerdictFilter(next);
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
      {/* ── Filter bar ─────────────────────────────────── */}
      <div
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
          borderRadius: "var(--radius)",
          padding: "12px 16px",
          display: "flex",
          alignItems: "center",
          gap: 14,
          flexWrap: "wrap",
        }}
      >
        <input
          placeholder="Search…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            padding: "5px 10px",
            border: "1px solid var(--border-subtle)",
            borderRadius: 4,
            fontSize: 12,
            fontFamily: "var(--font-sans)",
            background: "var(--bg-overlay)",
            color: "var(--text-primary)",
            minWidth: 180,
          }}
        />
        <Group label="Kind">
          <Chip label={`Holdings (${data.n_holdings})`} active={kindFilter === "holdings"} onClick={() => setKindFilter("holdings")} />
          <Chip label={`Watchlist (${data.n_watchlist})`} active={kindFilter === "watchlist"} onClick={() => setKindFilter("watchlist")} />
          <Chip label={`All (${data.n_holdings + data.n_watchlist})`} active={kindFilter === "all"} onClick={() => setKindFilter("all")} />
        </Group>
        <Group label="Market">
          {(["all", "br", "us"] as const).map((m) => (
            <Chip key={m} label={m === "all" ? "All" : m.toUpperCase()} active={marketFilter === m} onClick={() => setMarketFilter(m)} />
          ))}
        </Group>
        <Group label="Sector">
          <select
            value={sectorFilter}
            onChange={(e) => setSectorFilter(e.target.value)}
            style={{
              padding: "4px 8px",
              border: "1px solid var(--border-subtle)",
              borderRadius: 4,
              fontSize: 11,
              fontFamily: "var(--font-sans)",
              background: "var(--bg-overlay)",
              color: "var(--text-primary)",
            }}
          >
            {sectors.map((s) => <option key={s} value={s}>{s === "all" ? "All sectors" : s}</option>)}
          </select>
        </Group>
        <Group label="Verdict">
          {(["BUY", "HOLD", "AVOID", "N/A"] as const).map((v) => (
            <Chip
              key={v}
              label={v}
              active={verdictFilter.has(v)}
              onClick={() => toggleVerdict(v)}
              tone={v === "BUY" ? "buy" : v === "HOLD" ? "hold" : v === "AVOID" ? "avoid" : "neutral"}
            />
          ))}
        </Group>
        <Group label="DY ≥">
          <input
            type="number"
            min={0}
            step={0.5}
            value={minDy}
            onChange={(e) => setMinDy(Math.max(0, Number(e.target.value) || 0))}
            style={{
              width: 70,
              padding: "4px 8px",
              border: "1px solid var(--border-subtle)",
              borderRadius: 4,
              fontSize: 11,
              fontFamily: "var(--font-mono)",
              background: "var(--bg-overlay)",
              color: "var(--text-primary)",
              textAlign: "right",
            }}
          />
          <span style={{ fontSize: 10, color: "var(--text-tertiary)" }}>%</span>
        </Group>
        <span className="type-byline" style={{ marginLeft: "auto" }}>
          {rows.length} de {data.rows.length}
        </span>
      </div>

      {/* ── Blotter table ───────────────────────────── */}
      <div
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
          borderRadius: "var(--radius)",
          overflowX: "auto",
        }}
      >
        <table className="data-table" style={{ minWidth: 1100 }}>
          <thead>
            <tr>
              <th style={{ minWidth: 130 }}><SortHeader label="Ticker" k="ticker" sort={sort} dir={dir} onClick={() => flip("ticker")} /></th>
              <th style={{ minWidth: 110 }}><SortHeader label="Sector" k="sector" sort={sort} dir={dir} onClick={() => flip("sector")} /></th>
              <th><SortHeader label="V." k="verdict" sort={sort} dir={dir} onClick={() => flip("verdict")} /></th>
              <th className="num"><SortHeader label="Qty" k="qty" sort={sort} dir={dir} onClick={() => flip("qty")} num /></th>
              <th className="num"><SortHeader label="Last" k="last" sort={sort} dir={dir} onClick={() => flip("last")} num /></th>
              <th className="num"><SortHeader label="Value" k="value" sort={sort} dir={dir} onClick={() => flip("value")} num /></th>
              <th className="num"><SortHeader label="P&L" k="pnl" sort={sort} dir={dir} onClick={() => flip("pnl")} num /></th>
              <th className="num"><SortHeader label="DY" k="dy" sort={sort} dir={dir} onClick={() => flip("dy")} num /></th>
              <th className="num"><SortHeader label="P/E" k="pe" sort={sort} dir={dir} onClick={() => flip("pe")} num /></th>
              <th className="num"><SortHeader label="ROE" k="roe" sort={sort} dir={dir} onClick={() => flip("roe")} num /></th>
              <th className="num"><SortHeader label="FV gap" k="fv_gap" sort={sort} dir={dir} onClick={() => flip("fv_gap")} num /></th>
              <th className="num"><SortHeader label="Weight" k="weight" sort={sort} dir={dir} onClick={() => flip("weight")} num /></th>
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr><td colSpan={12} style={{ textAlign: "center", padding: 24, color: "var(--text-tertiary)" }}>Sem resultados.</td></tr>
            ) : rows.map((r) => <Row key={r.ticker} row={r} />)}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function compare(a: StockRow, b: StockRow, k: SortKey): number {
  switch (k) {
    case "ticker": return a.ticker.localeCompare(b.ticker);
    case "sector": return (a.sector || "").localeCompare(b.sector || "");
    case "verdict": return (VERDICT_RANK[a.verdict] ?? 9) - (VERDICT_RANK[b.verdict] ?? 9);
    case "qty": return (a.quantity ?? 0) - (b.quantity ?? 0);
    case "last": return (a.last_price ?? 0) - (b.last_price ?? 0);
    case "value": return (a.current_value ?? 0) - (b.current_value ?? 0);
    case "pnl": return (a.pnl_pct ?? -Infinity) - (b.pnl_pct ?? -Infinity);
    case "dy": return (a.dy ?? -1) - (b.dy ?? -1);
    case "pe": return (a.pe ?? Infinity) - (b.pe ?? Infinity);
    case "roe": return (a.roe ?? -Infinity) - (b.roe ?? -Infinity);
    case "fv_gap": return (a.fv_gap_pct ?? 0) - (b.fv_gap_pct ?? 0);
    case "weight": return (a.weight_pct ?? 0) - (b.weight_pct ?? 0);
  }
}

function Row({ row }: { row: StockRow }) {
  const verdictColor = row.verdict === "BUY" ? "var(--verdict-buy)"
    : row.verdict === "HOLD" ? "var(--verdict-hold)"
    : row.verdict === "AVOID" ? "var(--verdict-avoid)" : "var(--verdict-na)";
  const currency: "BRL" | "USD" = row.market === "br" ? "BRL" : "USD";
  return (
    <tr onClick={() => openTickerSheet(row.ticker)}>
      <td>
        <div className="flex items-center gap-2">
          <TickerLogo ticker={row.ticker} size="sm" />
          <div>
            <div style={{ display: "flex", alignItems: "baseline", gap: 5 }}>
              <p className="font-data" style={{ fontWeight: 700, fontSize: 12, color: "var(--text-primary)" }}>{row.ticker}</p>
              {row.kind === "watchlist" ? (
                <span style={{
                  fontSize: 8, fontWeight: 700, letterSpacing: "0.06em",
                  color: "var(--text-tertiary)", border: "1px solid var(--border-subtle)",
                  borderRadius: 2, padding: "0 4px",
                }}>WL</span>
              ) : null}
            </div>
            <p className="type-byline" style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: 130 }}>{row.name}</p>
          </div>
        </div>
      </td>
      <td style={{ fontSize: 12, color: "var(--text-secondary)" }}>{row.sector}</td>
      <td>
        <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: "0.06em", color: verdictColor }}>
          ●{row.verdict}
        </span>
      </td>
      <td className="num">{row.quantity !== null ? row.quantity.toFixed(0) : "—"}</td>
      <td className="num">{row.last_price !== null ? row.last_price.toFixed(2) : "—"}</td>
      <td className="num" style={{ fontWeight: 500 }}>
        {row.current_value !== null ? formatCurrency(row.current_value, currency, 0) : "—"}
      </td>
      <td className="num"><PercentDelta pct={row.pnl_pct} inline /></td>
      <td className="num">{row.dy !== null ? row.dy.toFixed(1) + "%" : "—"}</td>
      <td className="num">{row.pe !== null ? row.pe.toFixed(1) : "—"}</td>
      <td className="num">{row.roe !== null ? row.roe.toFixed(1) + "%" : "—"}</td>
      <td className="num" style={{
        color: row.fv_gap_pct === null ? "var(--text-tertiary)"
          : row.fv_gap_pct < 0 ? "var(--gain)"
          : row.fv_gap_pct > 0 ? "var(--loss)" : "var(--text-secondary)",
      }}>
        {row.fv_gap_pct !== null ? `${row.fv_gap_pct >= 0 ? "+" : ""}${row.fv_gap_pct.toFixed(0)}%` : "—"}
      </td>
      <td className="num">{row.weight_pct !== null ? row.weight_pct.toFixed(1) + "%" : "—"}</td>
    </tr>
  );
}

// ── Filter UI primitives ─────────────────────────────────────────────

function Group({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
      <span style={{
        fontSize: 9, letterSpacing: "0.08em", textTransform: "uppercase",
        color: "var(--text-tertiary)", fontWeight: 600,
      }}>{label}</span>
      {children}
    </div>
  );
}

function Chip({
  label, active, onClick, tone,
}: {
  label: string; active: boolean; onClick: () => void;
  tone?: "buy" | "hold" | "avoid" | "neutral";
}) {
  const c = tone === "buy" ? "var(--verdict-buy)"
    : tone === "hold" ? "var(--verdict-hold)"
    : tone === "avoid" ? "var(--verdict-avoid)"
    : tone === "neutral" ? "var(--text-tertiary)"
    : "var(--accent-primary)";
  return (
    <button
      onClick={onClick}
      style={{
        padding: "3px 9px",
        background: active ? c : "transparent",
        color: active ? "white" : c,
        border: `1px solid ${c}`,
        borderRadius: 999,
        fontSize: 10,
        fontWeight: 700,
        letterSpacing: "0.04em",
        cursor: "pointer",
        fontFamily: "var(--font-sans)",
      }}
    >
      {label}
    </button>
  );
}

function SortHeader({
  label, k, sort, dir, onClick, num,
}: {
  label: string; k: SortKey; sort: SortKey; dir: SortDir;
  onClick: () => void; num?: boolean;
}) {
  const active = sort === k;
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
        gap: 3,
        flexDirection: num ? "row-reverse" : "row",
      }}
    >
      {label}
      {active ? <span style={{ fontSize: 8 }}>{dir === "asc" ? "▲" : "▼"}</span> : null}
    </button>
  );
}
