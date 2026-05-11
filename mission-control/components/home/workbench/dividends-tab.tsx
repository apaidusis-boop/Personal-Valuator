"use client";

// ── WORKBENCH · DIVIDENDS TAB ────────────────────────────────────────
//
// 90-day horizontal timeline of dividend payments, past + future. Hover
// each day to see ticker breakdown. Below the timeline a small list of
// the next 6 confirmed payments — one row per payment.
//
// MOCK MODE: takes the same `LeadDividendDay[]` shape but expanded to
// 90 entries. Real wire later.

import { useMemo } from "react";

export type DividendsTabPayment = {
  ticker: string;
  amount: number;
  currency: "BRL" | "USD";
  status: "paid" | "ex" | "scheduled";
};

export type DividendsTabDay = {
  iso_date: string;
  weekday: string;
  day_num: number;
  is_today: boolean;
  is_past: boolean;
  payments: DividendsTabPayment[];
};

export type DividendsTabProps = {
  days_90: DividendsTabDay[];
  next_payments: { date: string; ticker: string; amount: number; currency: "BRL" | "USD" }[];
};

export function DividendsTab({ days_90, next_payments }: DividendsTabProps) {
  // Bucket by month for visual grouping
  const months = useMemo(() => bucketByMonth(days_90), [days_90]);

  return (
    <div style={{ padding: "16px 20px 20px" }}>
      <p className="type-h3" style={{ marginBottom: 4 }}>
        Dividend timeline · 90 dias
      </p>
      <p className="type-byline" style={{ marginBottom: 16 }}>
        Cinza · pago ou ex-div passado · Verde · futuro confirmado · Azul · hoje
      </p>

      {/* Month-bucketed strip */}
      <div style={{ display: "flex", flexDirection: "column", gap: 14, marginBottom: 22 }}>
        {months.map((m) => (
          <MonthRow key={m.label} month={m} />
        ))}
      </div>

      {/* Next payments list */}
      <p className="type-h3" style={{ marginBottom: 8 }}>
        Próximos 6 pagamentos
      </p>
      <table className="data-table" style={{ fontSize: 13 }}>
        <thead>
          <tr>
            <th>Data</th>
            <th>Ticker</th>
            <th className="num">Valor</th>
            <th className="num">Currency</th>
          </tr>
        </thead>
        <tbody>
          {next_payments.length === 0 ? (
            <tr><td colSpan={4} style={{ padding: 16, textAlign: "center", color: "var(--text-tertiary)" }}>Sem pagamentos confirmados.</td></tr>
          ) : next_payments.slice(0, 6).map((p) => (
            <tr key={`${p.ticker}-${p.date}`} style={{ cursor: "default" }}>
              <td className="font-data" style={{ fontSize: 12, color: "var(--text-secondary)" }}>{p.date}</td>
              <td>
                <span className="font-data" style={{ fontSize: 13, fontWeight: 700, color: "var(--text-primary)" }}>
                  {p.ticker}
                </span>
              </td>
              <td className="num" style={{ color: "var(--verdict-buy)", fontWeight: 600 }}>
                {p.currency === "BRL" ? "R$" : "$"}{p.amount.toFixed(2)}
              </td>
              <td className="num" style={{ color: "var(--text-tertiary)", fontSize: 11 }}>
                {p.currency}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

type Month = { label: string; days: DividendsTabDay[] };

function bucketByMonth(days: DividendsTabDay[]): Month[] {
  const buckets: Record<string, DividendsTabDay[]> = {};
  for (const d of days) {
    const key = d.iso_date.slice(0, 7); // YYYY-MM
    if (!buckets[key]) buckets[key] = [];
    buckets[key].push(d);
  }
  const monthName = (k: string) => {
    const [y, m] = k.split("-");
    const names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return `${names[Number(m) - 1]} ${y}`;
  };
  return Object.keys(buckets).sort().map((k) => ({ label: monthName(k), days: buckets[k] }));
}

function MonthRow({ month }: { month: Month }) {
  return (
    <div>
      <p className="type-h3" style={{ color: "var(--accent-primary)", marginBottom: 6 }}>
        {month.label}
      </p>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${month.days.length}, minmax(28px, 1fr))`,
          gap: 2,
        }}
      >
        {month.days.map((d) => (
          <DivCell key={d.iso_date} day={d} />
        ))}
      </div>
    </div>
  );
}

function DivCell({ day }: { day: DividendsTabDay }) {
  const has = day.payments.length > 0;
  const total_amt = day.payments.reduce((s, p) => s + p.amount, 0);

  let bg = "transparent";
  let fg = "var(--text-tertiary)";
  let border = "1px solid var(--border-subtle)";

  if (day.is_today) {
    bg = "var(--jpm-blue-soft)";
    fg = "var(--jpm-blue)";
    border = "1px solid var(--jpm-blue)";
  } else if (has && day.is_past) {
    bg = "var(--bg-overlay)";
    fg = "var(--text-tertiary)";
  } else if (has && !day.is_past) {
    bg = "var(--jpm-gain-soft)";
    fg = "var(--verdict-buy)";
    border = "1px solid rgba(21,168,97,0.4)";
  }

  const tooltip = has
    ? `${day.iso_date} — ${day.payments.map((p) => `${p.ticker} (${p.currency === "BRL" ? "R$" : "$"}${p.amount.toFixed(2)})`).join(" · ")}`
    : day.iso_date;

  return (
    <div
      title={tooltip}
      style={{
        height: 38,
        borderRadius: "var(--radius-sm)",
        background: bg,
        border,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        cursor: has ? "help" : "default",
      }}
    >
      <span
        style={{
          fontSize: 11,
          fontFamily: "var(--font-mono)",
          fontWeight: 600,
          color: fg,
          lineHeight: 1,
        }}
      >
        {day.day_num}
      </span>
      {has ? (
        <span style={{ fontSize: 8, color: fg, marginTop: 2 }}>
          ●{day.payments.length > 1 ? day.payments.length : ""}
        </span>
      ) : null}
    </div>
  );
}
