"use client";

/**
 * ReadyToBuyTile — Phase LL Sprint 3.1.
 *
 * Client component. Fetches /api/ready-to-buy?market=&limit= and renders a
 * tile with top tickers where action ∈ {BUY, STRONG_BUY} AND confidence !=
 * disputed (so the system never recommends acting on contradictory data).
 * One-glance "should I add right now" answer.
 */

import { useEffect, useState } from "react";
import Link from "next/link";

type Row = {
  market: "br" | "us";
  ticker: string;
  name: string | null;
  sector: string | null;
  current_price: number;
  our_fair: number | null;
  fair_price: number;
  action: string;
  confidence_label: string | null;
  our_upside_pct: number | null;
  upside_pct: number;
  computed_at: string;
};

function formatCurrency(v: number, market: "br" | "us"): string {
  const sym = market === "br" ? "R$" : "$";
  return `${sym}${v.toLocaleString(market === "br" ? "pt-BR" : "en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

function actionStyle(action: string): { bg: string; color: string } {
  // Phase MM "If only 5 things" #2 — Bloomberg Amber, NOT emerald green.
  // Generic green BUY pills are documented AI-slop signature.
  if (action === "STRONG_BUY") {
    return { bg: "var(--action-gold)", color: "white" };
  }
  if (action === "BUY") {
    return { bg: "var(--action-gold-soft)", color: "var(--action-gold-ink)" };
  }
  return { bg: "var(--bg-overlay)", color: "var(--text-secondary)" };
}

function confidenceLabel(c: string | null): { label: string; color: string } {
  if (!c) return { label: "—", color: "var(--text-tertiary)" };
  if (c === "cross_validated")
    return { label: "✓ verified", color: "var(--gain)" };
  if (c === "single_source")
    return { label: "single source", color: "var(--text-tertiary)" };
  if (c === "disputed")
    return { label: "✗ disputed", color: "var(--loss)" };
  return { label: c, color: "var(--text-tertiary)" };
}

export function ReadyToBuyTile({
  market,
  limit = 6,
}: {
  market?: "br" | "us";
  limit?: number;
}) {
  const [rows, setRows] = useState<Row[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    const qs = new URLSearchParams();
    if (market) qs.set("market", market);
    qs.set("limit", String(limit));
    fetch(`/api/ready-to-buy?${qs.toString()}`)
      .then((r) => r.json())
      .then((j) => alive && setRows(j.rows || []))
      .catch(() => {})
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [market, limit]);

  return (
    <section className="card p-5" aria-label="Ready to buy">
      <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
        <div className="flex items-center gap-3 flex-wrap">
          <h3 className="type-h3">Ready to buy</h3>
          <span
            className="text-[10px] uppercase tracking-wider"
            style={{ color: "var(--text-tertiary)" }}
          >
            {market ? market.toUpperCase() : "BR + US"} · ação BUY+ ·
            confiança não-disputada
          </span>
        </div>
        <Link
          href="/research"
          className="text-[12px] flex items-center gap-1 hover:underline"
          style={{ color: "var(--accent-primary)", fontWeight: 500 }}
        >
          ver universe →
        </Link>
      </div>

      {loading ? (
        <p
          className="text-xs italic py-4"
          style={{ color: "var(--text-tertiary)" }}
        >
          loading…
        </p>
      ) : rows.length === 0 ? (
        <p
          className="text-xs italic py-4"
          style={{ color: "var(--text-tertiary)" }}
        >
          Nenhum ticker passa actualmente o filtro BUY + confiança ≠ disputed.
          Ou não há fair_value v2 ainda computado, ou o mercado está
          maioritariamente acima do nosso fair (HOLD/TRIM).
        </p>
      ) : (
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
                  Ticker
                </th>
                <th
                  className="text-left font-medium py-2 uppercase tracking-wider text-[10px]"
                  style={{ fontFamily: "var(--font-sans)" }}
                >
                  Ação
                </th>
                <th
                  className="text-right font-medium py-2 uppercase tracking-wider text-[10px]"
                  style={{ fontFamily: "var(--font-sans)" }}
                >
                  Preço
                </th>
                <th
                  className="text-right font-medium py-2 uppercase tracking-wider text-[10px]"
                  style={{ fontFamily: "var(--font-sans)" }}
                >
                  our_fair
                </th>
                <th
                  className="text-right font-medium py-2 uppercase tracking-wider text-[10px]"
                  style={{ fontFamily: "var(--font-sans)" }}
                >
                  Upside
                </th>
                <th
                  className="text-right font-medium py-2 uppercase tracking-wider text-[10px]"
                  style={{ fontFamily: "var(--font-sans)" }}
                >
                  Conf.
                </th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => {
                const cur: "br" | "us" = r.market;
                const ourFair = r.our_fair ?? r.fair_price;
                const upside = r.our_upside_pct ?? r.upside_pct ?? 0;
                const upsideColor =
                  upside >= 20
                    ? "var(--gain)"
                    : upside >= 5
                      ? "var(--text-primary)"
                      : "var(--text-secondary)";
                const conf = confidenceLabel(r.confidence_label);
                const act = actionStyle(r.action);
                return (
                  <tr
                    key={`${r.market}-${r.ticker}`}
                    style={{
                      borderBottom: "1px solid var(--border-subtle)",
                    }}
                  >
                    <td className="py-2">
                      <Link
                        href={`/ticker/${r.ticker}`}
                        className="hover:underline"
                        style={{ color: "var(--text-primary)", fontWeight: 600 }}
                      >
                        {r.ticker}
                      </Link>
                      {r.sector && (
                        <span
                          className="ml-2 text-[10px] uppercase tracking-wider"
                          style={{ color: "var(--text-tertiary)" }}
                        >
                          {r.sector}
                        </span>
                      )}
                    </td>
                    <td className="py-2">
                      <span
                        className="text-[10px] font-semibold tracking-wider px-1.5 py-0.5 rounded uppercase"
                        style={{ background: act.bg, color: act.color }}
                      >
                        {r.action}
                      </span>
                    </td>
                    <td
                      className="text-right py-2 font-data tabular"
                      style={{ color: "var(--text-primary)" }}
                    >
                      {formatCurrency(r.current_price, cur)}
                    </td>
                    <td
                      className="text-right py-2 font-data tabular"
                      style={{ color: "var(--text-secondary)" }}
                    >
                      {formatCurrency(ourFair, cur)}
                    </td>
                    <td
                      className="text-right py-2 font-data tabular font-semibold"
                      style={{ color: upsideColor }}
                    >
                      {upside >= 0 ? "+" : ""}
                      {upside.toFixed(1)}%
                    </td>
                    <td
                      className="text-right py-2 text-[11px]"
                      style={{ color: conf.color }}
                    >
                      {conf.label}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
