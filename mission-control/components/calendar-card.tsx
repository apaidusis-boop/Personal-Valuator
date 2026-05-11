"use client";

import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight, Calendar as CalIcon } from "lucide-react";
import { openTickerSheet } from "@/lib/ticker-sheet";

type DivItem = {
  ticker: string;
  market: "br" | "us";
  ex_date: string;
  pay_date: string | null;
  amount: number;
  currency: string;
  shares: number | null;
  payout: number | null;
  is_holding: boolean;
};
type EarnItem = {
  ticker: string;
  market: "br" | "us";
  earnings_date: string;
  period_type: string | null;
  estimate_eps: number | null;
  is_holding: boolean;
};
type FilingItem = {
  ticker: string;
  market: "br" | "us";
  event_date: string;
  source: string;
  kind: string;
  summary: string;
  url: string | null;
  is_holding: boolean;
};

type CalendarPayload = {
  dividends: DivItem[];
  earnings: EarnItem[];
  filings: FilingItem[];
};

const MONTH_NAMES_PT = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
];
const DOW_PT = ["D", "S", "T", "Q", "Q", "S", "S"];

// ── Helpers ──────────────────────────────────────────────────────────

function fmtCurrency(v: number, currency: string): string {
  const sym = currency === "BRL" ? "R$" : "$";
  return `${sym}${v.toLocaleString(currency === "BRL" ? "pt-BR" : "en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

function fmtBRDate(iso: string): string {
  const d = new Date(iso + "T00:00:00");
  return `${String(d.getDate()).padStart(2, "0")}/${String(
    d.getMonth() + 1
  ).padStart(2, "0")}/${d.getFullYear()}`;
}

// ── Main component ──────────────────────────────────────────────────

export default function CalendarCard() {
  const [data, setData] = useState<CalendarPayload | null>(null);
  const [cursor, setCursor] = useState<{ year: number; month: number }>(() => {
    const t = new Date();
    return { year: t.getFullYear(), month: t.getMonth() };
  });
  const [selected, setSelected] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/calendar?days=120&filings_days=14")
      .then((r) => r.json())
      .then((j) => setData(j))
      .catch(() => {});
  }, []);

  // Build map: yyyy-mm-dd → { divs, earns, filings }
  const dayMap = new Map<
    string,
    { divs: DivItem[]; earns: EarnItem[]; filings: FilingItem[] }
  >();
  if (data) {
    for (const d of data.dividends) {
      if (!dayMap.has(d.ex_date)) dayMap.set(d.ex_date, { divs: [], earns: [], filings: [] });
      dayMap.get(d.ex_date)!.divs.push(d);
    }
    for (const e of data.earnings) {
      if (!dayMap.has(e.earnings_date))
        dayMap.set(e.earnings_date, { divs: [], earns: [], filings: [] });
      dayMap.get(e.earnings_date)!.earns.push(e);
    }
    for (const f of data.filings) {
      if (!dayMap.has(f.event_date))
        dayMap.set(f.event_date, { divs: [], earns: [], filings: [] });
      dayMap.get(f.event_date)!.filings.push(f);
    }
  }

  // First day of month (Sunday-indexed)
  const firstDow = new Date(cursor.year, cursor.month, 1).getDay();
  const daysInMonth = new Date(cursor.year, cursor.month + 1, 0).getDate();
  const today = new Date().toISOString().slice(0, 10);

  // 6×7 grid (max 42 cells) — leading blanks then days
  const cells: (number | null)[] = Array(firstDow).fill(null);
  for (let d = 1; d <= daysInMonth; d++) cells.push(d);
  while (cells.length % 7 !== 0) cells.push(null);

  function isoForCell(d: number): string {
    return `${cursor.year}-${String(cursor.month + 1).padStart(2, "0")}-${String(
      d
    ).padStart(2, "0")}`;
  }

  function shiftMonth(delta: number) {
    setCursor((c) => {
      const m = c.month + delta;
      if (m < 0) return { year: c.year - 1, month: 11 };
      if (m > 11) return { year: c.year + 1, month: 0 };
      return { year: c.year, month: m };
    });
    setSelected(null);
  }

  const selectedDay = selected ? dayMap.get(selected) : null;

  return (
    <div className="card p-4">
      <div className="flex items-center justify-between mb-3">
        <h2 className="type-h3 flex items-center gap-2">
          <CalIcon size={14} style={{ color: "var(--accent-primary)" }} />
          Calendário · próximos eventos
        </h2>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => shiftMonth(-1)}
            className="p-1 rounded transition-colors"
            style={{ color: "var(--text-tertiary)" }}
            aria-label="Mês anterior"
          >
            <ChevronLeft size={14} />
          </button>
          <span
            className="font-data text-xs"
            style={{ color: "var(--text-secondary)", minWidth: 110, textAlign: "center" }}
          >
            {MONTH_NAMES_PT[cursor.month]} {cursor.year}
          </span>
          <button
            type="button"
            onClick={() => shiftMonth(1)}
            className="p-1 rounded transition-colors"
            style={{ color: "var(--text-tertiary)" }}
            aria-label="Próximo mês"
          >
            <ChevronRight size={14} />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-7 gap-1 mb-2">
        {DOW_PT.map((d, i) => (
          <div
            key={i}
            className="text-center text-[10px] uppercase font-data py-1"
            style={{ color: "var(--text-tertiary)" }}
          >
            {d}
          </div>
        ))}
      </div>

      <div className="grid grid-cols-7 gap-1">
        {cells.map((cell, i) => {
          if (cell === null) return <div key={i} />;
          const iso = isoForCell(cell);
          const day = dayMap.get(iso);
          const hasDiv = day && day.divs.length > 0;
          const hasEarn = day && day.earns.length > 0;
          const hasFiling = day && day.filings.length > 0;
          const isToday = iso === today;
          const isSelected = iso === selected;
          const hasAny = hasDiv || hasEarn || hasFiling;

          return (
            <button
              key={i}
              type="button"
              onClick={() => setSelected(isSelected ? null : iso)}
              className="relative rounded text-xs transition-colors"
              style={{
                aspectRatio: "1",
                background: isSelected
                  ? "var(--accent-primary)"
                  : isToday
                  ? "var(--bg-overlay)"
                  : hasAny
                  ? "var(--bg-elevated)"
                  : "transparent",
                color: isSelected
                  ? "white"
                  : isToday
                  ? "var(--text-primary)"
                  : hasAny
                  ? "var(--text-primary)"
                  : "var(--text-tertiary)",
                border: isToday && !isSelected ? "1px solid var(--accent-primary)" : "1px solid transparent",
                cursor: hasAny ? "pointer" : "default",
                fontWeight: isToday || hasAny ? 600 : 400,
              }}
              disabled={!hasAny}
            >
              <span style={{ fontSize: 11 }}>{cell}</span>
              {hasAny && (
                <span
                  className="absolute bottom-1 left-1/2 -translate-x-1/2 flex items-center gap-[2px]"
                  aria-hidden
                >
                  {hasDiv && (
                    <span
                      style={{
                        display: "inline-block",
                        width: 4,
                        height: 4,
                        borderRadius: 999,
                        background: isSelected
                          ? "white"
                          : "var(--gain, #16a34a)",
                      }}
                    />
                  )}
                  {hasEarn && (
                    <span
                      style={{
                        display: "inline-block",
                        width: 4,
                        height: 4,
                        borderRadius: 999,
                        background: isSelected
                          ? "white"
                          : "var(--val-blue, #1e40af)",
                      }}
                    />
                  )}
                  {hasFiling && (
                    <span
                      style={{
                        display: "inline-block",
                        width: 4,
                        height: 4,
                        borderRadius: 999,
                        background: isSelected
                          ? "white"
                          : "var(--val-gold, #ca8a04)",
                      }}
                    />
                  )}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Legend */}
      <div className="flex items-center gap-4 mt-3 text-[10px]" style={{ color: "var(--text-tertiary)" }}>
        <span className="flex items-center gap-1">
          <span style={{ width: 6, height: 6, background: "var(--gain, #16a34a)", borderRadius: 999, display: "inline-block" }} />
          Dividendo
        </span>
        <span className="flex items-center gap-1">
          <span style={{ width: 6, height: 6, background: "var(--val-blue, #1e40af)", borderRadius: 999, display: "inline-block" }} />
          Earnings
        </span>
        <span className="flex items-center gap-1">
          <span style={{ width: 6, height: 6, background: "var(--val-gold, #ca8a04)", borderRadius: 999, display: "inline-block" }} />
          Filing
        </span>
      </div>

      {/* Selected-day bubble */}
      {selectedDay && selected && (
        <div
          className="mt-4 rounded p-3 space-y-2"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <p
            className="type-byline"
            style={{ color: "var(--text-secondary)", fontWeight: 600 }}
          >
            {fmtBRDate(selected)}
          </p>

          {selectedDay.divs.map((d) => (
            <button
              key={`d-${d.market}-${d.ticker}`}
              type="button"
              onClick={() => openTickerSheet(d.ticker)}
              className="w-full text-left flex items-center justify-between gap-2 py-1 px-2 rounded transition-colors"
              style={{ background: "transparent" }}
            >
              <span className="flex items-center gap-2">
                <span
                  style={{
                    width: 6,
                    height: 6,
                    background: "var(--gain, #16a34a)",
                    borderRadius: 999,
                    display: "inline-block",
                  }}
                />
                <span
                  className="font-data"
                  style={{ color: "var(--text-primary)", fontWeight: 600, fontSize: 12 }}
                >
                  {d.ticker}
                </span>
                <span style={{ color: "var(--text-tertiary)", fontSize: 11 }}>
                  ex-date · {fmtCurrency(d.amount, d.currency)} / share
                </span>
              </span>
              {d.payout !== null && d.shares !== null ? (
                <span
                  className="font-data"
                  style={{ color: "var(--gain, #16a34a)", fontSize: 12, fontWeight: 600 }}
                >
                  {d.shares.toLocaleString("pt-BR", {
                    maximumFractionDigits: 0,
                  })} × {fmtCurrency(d.amount, d.currency)} = {fmtCurrency(d.payout, d.currency)}
                </span>
              ) : (
                <span style={{ color: "var(--text-tertiary)", fontSize: 11 }}>watchlist</span>
              )}
            </button>
          ))}

          {selectedDay.earns.map((e) => (
            <button
              key={`e-${e.market}-${e.ticker}`}
              type="button"
              onClick={() => openTickerSheet(e.ticker)}
              className="w-full text-left flex items-center justify-between gap-2 py-1 px-2 rounded transition-colors"
            >
              <span className="flex items-center gap-2">
                <span
                  style={{
                    width: 6,
                    height: 6,
                    background: "var(--val-blue, #1e40af)",
                    borderRadius: 999,
                    display: "inline-block",
                  }}
                />
                <span
                  className="font-data"
                  style={{ color: "var(--text-primary)", fontWeight: 600, fontSize: 12 }}
                >
                  {e.ticker}
                </span>
                <span style={{ color: "var(--text-tertiary)", fontSize: 11 }}>
                  earnings call {e.period_type ? `· ${e.period_type}` : ""}
                </span>
              </span>
              {e.estimate_eps !== null && (
                <span className="font-data" style={{ color: "var(--text-secondary)", fontSize: 12 }}>
                  est. EPS {e.estimate_eps.toFixed(2)}
                </span>
              )}
            </button>
          ))}

          {selectedDay.filings.map((f, idx) => (
            <button
              key={`f-${f.market}-${f.ticker}-${idx}`}
              type="button"
              onClick={() => openTickerSheet(f.ticker)}
              className="w-full text-left py-1 px-2 rounded transition-colors"
            >
              <div className="flex items-center gap-2 mb-1">
                <span
                  style={{
                    width: 6,
                    height: 6,
                    background: "var(--val-gold, #ca8a04)",
                    borderRadius: 999,
                    display: "inline-block",
                  }}
                />
                <span
                  className="font-data"
                  style={{ color: "var(--text-primary)", fontWeight: 600, fontSize: 12 }}
                >
                  {f.ticker}
                </span>
                <span
                  className="text-[10px] uppercase font-data px-1.5 py-0.5 rounded"
                  style={{
                    background: f.source === "sec" ? "var(--val-blue-soft, var(--bg-overlay))" : "var(--val-gold-soft, var(--bg-overlay))",
                    color: "var(--text-secondary)",
                  }}
                >
                  {f.source} · {f.kind}
                </span>
              </div>
              <p className="text-[11px]" style={{ color: "var(--text-tertiary)", lineHeight: 1.4 }}>
                {f.summary}
              </p>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
