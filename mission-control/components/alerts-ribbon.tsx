"use client";

import { useEffect, useState } from "react";
import { Bell, FileText, Banknote, BarChart2 } from "lucide-react";
import Link from "next/link";
import { openTickerSheet } from "@/lib/ticker-sheet";

type Summary = {
  div_next7: number;
  div_next30: number;
  earn_next7: number;
  earn_next30: number;
  filings_recent: number;
  expected_payout_next30: Record<string, number>;
};

type Calendar = {
  dividends: {
    ticker: string;
    market: "br" | "us";
    ex_date: string;
    amount: number;
    currency: string;
    payout: number | null;
    is_holding: boolean;
  }[];
  earnings: {
    ticker: string;
    market: "br" | "us";
    earnings_date: string;
    is_holding: boolean;
  }[];
  filings: {
    ticker: string;
    market: "br" | "us";
    event_date: string;
    source: string;
    kind: string;
    summary: string;
    is_holding: boolean;
  }[];
  summary: Summary;
};

function fmtCurrency(v: number, currency: string): string {
  const sym = currency === "BRL" ? "R$" : "$";
  return `${sym}${v.toLocaleString(currency === "BRL" ? "pt-BR" : "en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

function daysUntil(iso: string): number {
  const t = new Date();
  t.setHours(0, 0, 0, 0);
  const d = new Date(iso + "T00:00:00");
  return Math.round((d.getTime() - t.getTime()) / 86400000);
}

function relativeDayLabel(iso: string): string {
  const n = daysUntil(iso);
  if (n === 0) return "hoje";
  if (n === 1) return "amanhã";
  if (n < 0) return `há ${-n}d`;
  return `em ${n}d`;
}

export default function AlertsRibbon() {
  const [data, setData] = useState<Calendar | null>(null);

  useEffect(() => {
    fetch("/api/calendar?days=30&filings_days=7")
      .then((r) => r.json())
      .then(setData)
      .catch(() => {});
  }, []);

  if (!data) {
    return (
      <div
        className="card p-3 text-xs"
        style={{ color: "var(--text-tertiary)", fontStyle: "italic" }}
      >
        carregando agenda…
      </div>
    );
  }

  const nextDiv = data.dividends.find((d) => d.is_holding);
  const nextEarn = data.earnings.find((e) => e.is_holding);
  const lastFiling = data.filings.find((f) => f.is_holding);
  const totals = Object.entries(data.summary.expected_payout_next30 || {});

  return (
    <div
      className="card overflow-hidden"
      style={{ background: "var(--bg-elevated)" }}
    >
      <div
        className="flex items-center gap-3 px-4 py-2 text-[11px] uppercase tracking-wider"
        style={{
          color: "var(--text-tertiary)",
          borderBottom: "1px solid var(--border-subtle)",
          fontFamily: "var(--font-sans)",
        }}
      >
        <Bell size={11} />
        <span style={{ fontWeight: 600 }}>Agenda · 30 dias</span>
        <span style={{ color: "var(--border-subtle)" }}>·</span>
        <span>
          {data.summary.div_next30} divs · {data.summary.earn_next30} earnings
          · {data.summary.filings_recent} filings 7d
        </span>
        {totals.length > 0 && (
          <>
            <span style={{ color: "var(--border-subtle)" }}>·</span>
            <span>
              receitas previstas{" "}
              <span style={{ color: "var(--gain, #16a34a)", fontFamily: "var(--font-mono)" }}>
                {totals
                  .map(([cur, v]) => fmtCurrency(v, cur))
                  .join(" + ")}
              </span>
            </span>
          </>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 divide-x" style={{ borderColor: "var(--border-subtle)" }}>
        {/* Next dividend */}
        <RibbonCell
          icon={<Banknote size={13} />}
          accent="var(--gain, #16a34a)"
          label="Próx. dividendo"
          empty={!nextDiv}
        >
          {nextDiv && (
            <button
              type="button"
              onClick={() => openTickerSheet(nextDiv.ticker)}
              className="w-full text-left"
            >
              <div className="flex items-baseline gap-2">
                <span
                  className="font-data"
                  style={{ color: "var(--text-primary)", fontWeight: 700, fontSize: 13 }}
                >
                  {nextDiv.ticker}
                </span>
                <span style={{ color: "var(--text-tertiary)", fontSize: 10 }}>
                  ex-date {relativeDayLabel(nextDiv.ex_date)}
                </span>
              </div>
              <p className="font-data text-[11px]" style={{ color: "var(--text-secondary)", marginTop: 2 }}>
                {nextDiv.payout !== null
                  ? `${fmtCurrency(nextDiv.amount, nextDiv.currency)}/share → ${fmtCurrency(
                      nextDiv.payout,
                      nextDiv.currency
                    )}`
                  : `${fmtCurrency(nextDiv.amount, nextDiv.currency)}/share`}
              </p>
            </button>
          )}
        </RibbonCell>

        {/* Next earnings */}
        <RibbonCell
          icon={<BarChart2 size={13} />}
          accent="var(--val-blue, #1e40af)"
          label="Próx. earnings"
          empty={!nextEarn}
        >
          {nextEarn && (
            <button
              type="button"
              onClick={() => openTickerSheet(nextEarn.ticker)}
              className="w-full text-left"
            >
              <div className="flex items-baseline gap-2">
                <span
                  className="font-data"
                  style={{ color: "var(--text-primary)", fontWeight: 700, fontSize: 13 }}
                >
                  {nextEarn.ticker}
                </span>
                <span style={{ color: "var(--text-tertiary)", fontSize: 10 }}>
                  call {relativeDayLabel(nextEarn.earnings_date)}
                </span>
              </div>
              <p className="font-data text-[11px]" style={{ color: "var(--text-secondary)", marginTop: 2 }}>
                {nextEarn.earnings_date}
              </p>
            </button>
          )}
        </RibbonCell>

        {/* Most recent filing */}
        <RibbonCell
          icon={<FileText size={13} />}
          accent="var(--val-gold, #ca8a04)"
          label="Filing recente"
          empty={!lastFiling}
        >
          {lastFiling && (
            <button
              type="button"
              onClick={() => openTickerSheet(lastFiling.ticker)}
              className="w-full text-left"
            >
              <div className="flex items-baseline gap-2">
                <span
                  className="font-data"
                  style={{ color: "var(--text-primary)", fontWeight: 700, fontSize: 13 }}
                >
                  {lastFiling.ticker}
                </span>
                <span style={{ color: "var(--text-tertiary)", fontSize: 10 }}>
                  {lastFiling.source} · {lastFiling.kind} · {relativeDayLabel(lastFiling.event_date)}
                </span>
              </div>
              <p
                className="text-[11px]"
                style={{
                  color: "var(--text-secondary)",
                  marginTop: 2,
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                }}
                title={lastFiling.summary}
              >
                {lastFiling.summary || "—"}
              </p>
            </button>
          )}
        </RibbonCell>
      </div>

      <div
        className="px-4 py-2 text-[11px] flex items-center justify-end gap-3"
        style={{
          color: "var(--text-tertiary)",
          borderTop: "1px solid var(--border-subtle)",
          background: "var(--bg-canvas)",
        }}
      >
        <Link href="/events" className="hover:underline" style={{ color: "var(--accent-primary)" }}>
          ver agenda completa →
        </Link>
        <Link href="/filings" className="hover:underline" style={{ color: "var(--accent-primary)" }}>
          filings (CVM + SEC) →
        </Link>
      </div>
    </div>
  );
}

function RibbonCell({
  icon,
  accent,
  label,
  empty,
  children,
}: {
  icon: React.ReactNode;
  accent: string;
  label: string;
  empty: boolean;
  children?: React.ReactNode;
}) {
  return (
    <div className="px-4 py-3" style={{ borderColor: "var(--border-subtle)" }}>
      <div className="flex items-center gap-1.5 mb-1.5" style={{ color: accent }}>
        {icon}
        <span
          className="text-[10px] uppercase tracking-wider"
          style={{ fontWeight: 600 }}
        >
          {label}
        </span>
      </div>
      {empty ? (
        <p className="text-[11px] italic" style={{ color: "var(--text-tertiary)" }}>
          nenhum nas próximas semanas
        </p>
      ) : (
        children
      )}
    </div>
  );
}
