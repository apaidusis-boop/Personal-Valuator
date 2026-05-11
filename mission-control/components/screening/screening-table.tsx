"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { Search } from "lucide-react";

export type ScreeningRow = {
  ticker: string;
  market: string;
  sector: string | null;
  stance: string;
  confidence: string;
  flag_count: number;
  philosophy_primary: string | null;
  is_holding: boolean;
};

const STANCE_FILTERS = [
  { id: "ALL", label: "Todos" },
  { id: "BUY", label: "Buy" },
  { id: "HOLD", label: "Hold" },
  { id: "AVOID", label: "Avoid" },
  { id: "NEEDS_DATA", label: "Needs data" },
] as const;

const MARKET_FILTERS = [
  { id: "ALL", label: "Todos" },
  { id: "br", label: "BR" },
  { id: "us", label: "US" },
] as const;

function stanceVariant(s: string): "buy" | "hold" | "avoid" | "na" {
  switch (s) {
    case "BUY":
      return "buy";
    case "HOLD":
      return "hold";
    case "AVOID":
      return "avoid";
    default:
      return "na";
  }
}

export function ScreeningTable({ rows }: { rows: ScreeningRow[] }) {
  const [query, setQuery] = useState("");
  const [stance, setStance] = useState<string>("ALL");
  const [market, setMarket] = useState<string>("ALL");
  const [holdingsOnly, setHoldingsOnly] = useState(false);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return rows.filter((r) => {
      if (stance !== "ALL" && r.stance !== stance) return false;
      if (market !== "ALL" && r.market !== market) return false;
      if (holdingsOnly && !r.is_holding) return false;
      if (q) {
        const hay = (
          r.ticker +
          " " +
          (r.sector || "") +
          " " +
          (r.philosophy_primary || "")
        ).toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
  }, [rows, query, stance, market, holdingsOnly]);

  return (
    <div className="space-y-3">
      {/* Filter row -------------------------------------------- */}
      <div className="flex flex-wrap items-center gap-3">
        <div
          className="flex items-center gap-2 rounded px-3 py-2 flex-1 min-w-[280px] max-w-[480px]"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <Search size={14} style={{ color: "var(--text-label)" }} />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Filtrar por ticker, setor, filosofia…"
            className="bg-transparent text-sm outline-none flex-1"
            style={{ color: "var(--text-primary)" }}
          />
          {query && (
            <button
              type="button"
              onClick={() => setQuery("")}
              className="text-[10px] px-1.5"
              style={{ color: "var(--text-tertiary)" }}
              aria-label="Clear"
            >
              ×
            </button>
          )}
        </div>

        <FilterChips
          options={[...STANCE_FILTERS]}
          value={stance}
          onChange={setStance}
        />
        <FilterChips
          options={[...MARKET_FILTERS]}
          value={market}
          onChange={setMarket}
        />

        <label
          className="flex items-center gap-1.5 text-xs cursor-pointer select-none"
          style={{ color: "var(--text-tertiary)" }}
        >
          <input
            type="checkbox"
            checked={holdingsOnly}
            onChange={(e) => setHoldingsOnly(e.target.checked)}
            className="w-3.5 h-3.5 accent-[var(--val-gold)]"
          />
          só holdings
        </label>

        <span
          className="text-[10px] ml-auto"
          style={{ color: "var(--text-tertiary)" }}
        >
          {filtered.length} de {rows.length}
        </span>
      </div>

      {/* Table -------------------------------------------------- */}
      <div
        className="rounded overflow-hidden"
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
        }}
      >
        {filtered.length > 0 ? (
          <div className="max-h-[68vh] overflow-y-auto">
            <table className="w-full">
              <thead className="sticky top-0">
                <tr
                  className="text-[10px]"
                  style={{
                    color: "var(--text-label)",
                    background: "rgba(11,19,36,0.95)",
                    borderBottom: "1px solid var(--border-subtle)",
                  }}
                >
                  <th className="text-left px-4 py-2.5 font-semibold">Ticker</th>
                  <th className="text-left px-3 py-2.5 font-semibold">Mercado</th>
                  <th className="text-left px-3 py-2.5 font-semibold">Setor</th>
                  <th className="text-center px-3 py-2.5 font-semibold">Verdict</th>
                  <th className="text-center px-3 py-2.5 font-semibold">Confidence</th>
                  <th className="text-center px-3 py-2.5 font-semibold">Flags</th>
                  <th className="text-left px-3 py-2.5 font-semibold">Filosofia</th>
                  <th className="text-right px-4 py-2.5 font-semibold">Status</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((e) => (
                  <tr
                    key={`${e.ticker}-${e.market}`}
                    className="hover:bg-[var(--bg-overlay)]/30 transition-colors"
                    style={{ borderBottom: "1px solid rgba(45,55,72,0.4)" }}
                  >
                    <td className="px-4 py-2.5">
                      <Link
                        href={`/ticker/${e.ticker}`}
                        className="text-sm font-data font-bold hover:underline"
                        style={{ color: "var(--text-primary)" }}
                      >
                        {e.ticker}
                      </Link>
                    </td>
                    <td className="px-3 py-2.5">
                      {e.market && (
                        <span
                          className={`pill pill-${e.market === "br" ? "mkt-br" : "mkt-us"}`}
                        >
                          {String(e.market).toUpperCase()}
                        </span>
                      )}
                    </td>
                    <td
                      className="px-3 py-2.5 text-xs"
                      style={{ color: "var(--text-tertiary)" }}
                    >
                      {e.sector || "—"}
                    </td>
                    <td className="px-3 py-2.5 text-center">
                      <span
                        className={`pill pill-solid pill-${stanceVariant(e.stance)}`}
                      >
                        {e.stance.replace("_", " ")}
                      </span>
                    </td>
                    <td
                      className="px-3 py-2.5 text-center text-xs font-data"
                      style={{ color: "var(--text-secondary)" }}
                    >
                      {e.confidence}
                    </td>
                    <td
                      className="px-3 py-2.5 text-center text-xs font-data"
                      style={{ color: "var(--text-tertiary)" }}
                    >
                      {e.flag_count > 0 ? `⚑${e.flag_count}` : "—"}
                    </td>
                    <td
                      className="px-3 py-2.5 text-[11px]"
                      style={{ color: "var(--text-tertiary)" }}
                    >
                      {e.philosophy_primary || "—"}
                    </td>
                    <td className="px-4 py-2.5 text-right">
                      {e.is_holding ? (
                        <span
                          className="pill pill-gold"
                          style={{ fontSize: "9px" }}
                        >
                          HOLDING
                        </span>
                      ) : (
                        <span
                          className="text-[10px]"
                          style={{ color: "var(--text-disabled)" }}
                        >
                          watch
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p
            className="px-4 py-8 text-xs italic text-center"
            style={{ color: "var(--text-tertiary)" }}
          >
            Nenhum ativo bate com os filtros.
          </p>
        )}
      </div>
    </div>
  );
}

function FilterChips({
  options,
  value,
  onChange,
}: {
  options: readonly { id: string; label: string }[];
  value: string;
  onChange: (id: string) => void;
}) {
  return (
    <div className="flex items-center gap-1">
      {options.map((opt) => {
        const active = opt.id === value;
        return (
          <button
            key={opt.id}
            type="button"
            onClick={() => onChange(opt.id)}
            className="text-[10px] px-2 py-1 rounded uppercase tracking-wider font-semibold transition-colors"
            style={
              active
                ? {
                    background: "rgba(201,161,91,0.15)",
                    color: "var(--val-gold)",
                    border: "1px solid rgba(201,161,91,0.4)",
                  }
                : {
                    background: "transparent",
                    color: "var(--text-tertiary)",
                    border: "1px solid var(--border-subtle)",
                  }
            }
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}
