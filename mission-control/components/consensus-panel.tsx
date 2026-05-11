"use client";

/**
 * ConsensusPanel — Phase LL Sprint 3.2.
 *
 * Renders the multi-house target table user described in the dashboard
 * vision: "Nossa $14.50 | BTG $15 | XP $17 | Suno $14 | WS $16 | Consensus $15.30".
 *
 * Reads /api/consensus/[ticker] which spawns scoring.consensus_target.
 * If only `our_fair` is available (most BR holdings outside Suno/XP coverage),
 * shows the panel with N=1 and surfaces "(adicione cobertura de mais casas
 * para triangular)" — never hides; always informative.
 */

import { useEffect, useState } from "react";

type House = {
  source: string;
  target: number;
  recency_days: number | null;
  stance: string | null;
  confidence: number | null;
  published_at?: string;
};

type ApiResponse = {
  ticker: string;
  market: "br" | "us";
  our_fair: number | null;
  consensus_fair: number | null;
  current_price: number | null;
  n_sources: number;
  houses: House[];
  blended: { median: number; mean: number; weighted: number };
  dispersion: number;
  upside_blended_pct: number | null;
  computed_at: string;
};

function formatCurrency(v: number, market: "br" | "us"): string {
  const sym = market === "br" ? "R$" : "$";
  return `${sym}${v.toLocaleString(market === "br" ? "pt-BR" : "en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

function recencyLabel(days: number | null): string {
  if (days == null) return "—";
  if (days === 0) return "hoje";
  if (days === 1) return "ontem";
  if (days < 7) return `${days}d`;
  if (days < 30) return `${Math.floor(days / 7)}sem`;
  if (days < 365) return `${Math.floor(days / 30)}m`;
  return `${(days / 365).toFixed(1)}a`;
}

function sourceLabel(s: string): string {
  // Normalize internal source codes to user-facing labels
  const lower = s.toLowerCase();
  if (lower === "our_fair") return "Nossa";
  if (lower.includes("suno")) return "Suno";
  if (lower.includes("xp")) return "XP";
  if (lower.includes("btg")) return "BTG";
  if (lower.includes("wallstreet") || lower.includes("wall_street") || lower.includes("ws"))
    return "Wall Street";
  if (lower.includes("finclass")) return "Finclass";
  return s;
}

function stanceBadge(stance: string | null): { label: string; color: string } {
  if (!stance) return { label: "—", color: "var(--text-tertiary)" };
  const s = stance.toLowerCase();
  if (s === "bull" || s === "buy") return { label: "BULL", color: "var(--gain)" };
  if (s === "bear" || s === "sell") return { label: "BEAR", color: "var(--loss)" };
  if (s === "neutral" || s === "hold") return { label: "NEUTRAL", color: "var(--text-secondary)" };
  return { label: stance.toUpperCase().slice(0, 8), color: "var(--text-secondary)" };
}

export function ConsensusPanel({ ticker }: { ticker: string }) {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    fetch(`/api/consensus/${ticker}`)
      .then((r) => r.json())
      .then((j) => {
        if (!alive) return;
        if (j.error) setErr(j.error);
        else setData(j);
      })
      .catch((e) => alive && setErr(String(e)))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [ticker]);

  if (loading) {
    return (
      <div
        className="rounded p-5 text-xs"
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
          color: "var(--text-tertiary)",
        }}
      >
        loading consenso…
      </div>
    );
  }
  if (err || !data) {
    return (
      <div
        className="rounded p-5 text-xs italic"
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
          color: "var(--text-tertiary)",
        }}
      >
        {err || "sem dados de consenso (sem fair_value computado ainda)"}
      </div>
    );
  }

  const upside = data.upside_blended_pct;
  const upsideColor =
    upside == null
      ? "var(--text-tertiary)"
      : upside >= 5
        ? "var(--gain)"
        : upside <= -5
          ? "var(--loss)"
          : "var(--text-secondary)";

  return (
    <div
      className="rounded p-5"
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
      }}
    >
      <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
        <h3
          className="text-[10px] font-semibold tracking-wider uppercase"
          style={{ color: "var(--text-label)" }}
        >
          Consenso fair price · {data.n_sources} fonte
          {data.n_sources !== 1 ? "s" : ""}
        </h3>
        {data.current_price && (
          <span
            className="text-[10px] font-data"
            style={{ color: "var(--text-tertiary)" }}
          >
            preço actual {formatCurrency(data.current_price, data.market)}
          </span>
        )}
      </div>

      {/* Houses table */}
      <div className="overflow-x-auto">
        <table className="w-full text-[12px]">
          <thead>
            <tr
              style={{
                color: "var(--text-tertiary)",
                borderBottom: "1px solid var(--border-subtle)",
              }}
            >
              <th
                className="text-left font-medium py-2 uppercase tracking-wider text-[10px]"
                style={{ fontFamily: "var(--font-sans)" }}
              >
                Fonte
              </th>
              <th
                className="text-right font-medium py-2 uppercase tracking-wider text-[10px]"
                style={{ fontFamily: "var(--font-sans)" }}
              >
                Target
              </th>
              <th
                className="text-right font-medium py-2 uppercase tracking-wider text-[10px]"
                style={{ fontFamily: "var(--font-sans)" }}
              >
                Stance
              </th>
              <th
                className="text-right font-medium py-2 uppercase tracking-wider text-[10px]"
                style={{ fontFamily: "var(--font-sans)" }}
              >
                Idade
              </th>
            </tr>
          </thead>
          <tbody>
            {data.houses.map((h, i) => {
              const badge = stanceBadge(h.stance);
              const isOurs = h.source === "our_fair";
              return (
                <tr
                  key={`${h.source}-${i}`}
                  style={{
                    borderBottom: "1px solid var(--border-subtle)",
                    background: isOurs ? "var(--bg-overlay)" : "transparent",
                  }}
                >
                  <td
                    className="py-2"
                    style={{
                      color: isOurs ? "var(--accent-glow)" : "var(--text-primary)",
                      fontWeight: isOurs ? 600 : 400,
                    }}
                  >
                    {sourceLabel(h.source)}
                  </td>
                  <td
                    className="text-right py-2 font-data tabular"
                    style={{ color: "var(--text-primary)" }}
                  >
                    {formatCurrency(h.target, data.market)}
                  </td>
                  <td className="text-right py-2">
                    <span
                      className="text-[10px] font-semibold tracking-wider"
                      style={{ color: badge.color }}
                    >
                      {badge.label}
                    </span>
                  </td>
                  <td
                    className="text-right py-2 text-[11px] font-data"
                    style={{ color: "var(--text-tertiary)" }}
                  >
                    {recencyLabel(h.recency_days)}
                  </td>
                </tr>
              );
            })}
          </tbody>
          <tfoot>
            <tr
              style={{
                borderTop: "2px solid var(--accent-glow)",
              }}
            >
              <td
                className="py-3 text-[10px] uppercase tracking-wider font-semibold"
                style={{ color: "var(--text-label)" }}
              >
                Mediana
              </td>
              <td
                className="text-right py-3 font-data tabular font-bold"
                style={{ color: "var(--text-primary)", fontSize: 14 }}
              >
                {formatCurrency(data.blended.median, data.market)}
              </td>
              <td
                className="text-right py-3 text-[11px] font-data"
                style={{ color: "var(--text-tertiary)" }}
              >
                ponderada {formatCurrency(data.blended.weighted, data.market)}
              </td>
              <td
                className="text-right py-3 text-[11px] font-data"
                style={{ color: upsideColor }}
              >
                {upside == null
                  ? "—"
                  : `${upside >= 0 ? "+" : ""}${upside.toFixed(1)}% vs preço`}
              </td>
            </tr>
          </tfoot>
        </table>
      </div>

      {/* Footer: dispersion + provenance hint */}
      <div
        className="flex items-center gap-6 flex-wrap text-[11px] pt-3 mt-2"
        style={{
          color: "var(--text-tertiary)",
          borderTop: "1px solid var(--border-subtle)",
        }}
      >
        <span>
          dispersão{" "}
          <span
            className="font-data"
            style={{ color: "var(--text-secondary)" }}
          >
            {(data.dispersion * 100).toFixed(1)}%
          </span>
        </span>
        <span>
          mediana / média{" "}
          <span
            className="font-data"
            style={{ color: "var(--text-secondary)" }}
          >
            {formatCurrency(data.blended.median, data.market)} /{" "}
            {formatCurrency(data.blended.mean, data.market)}
          </span>
        </span>
        {data.n_sources < 3 && (
          <span style={{ color: "var(--text-tertiary)" }} className="italic">
            extract_targets re-pass para puxar BTG/XP/Suno PTs em falta
          </span>
        )}
      </div>
    </div>
  );
}
