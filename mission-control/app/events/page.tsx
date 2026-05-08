import type { Metadata } from "next";
import Link from "next/link";

import {
  upcomingDividends,
  upcomingFilings,
  listRecentEvents,
  type DividendEvent,
  type UpcomingFiling,
  type FilingEvent,
} from "@/lib/db";
import { formatDate, formatCurrency } from "@/lib/format";

import EventTickerLink from "./ticker-link";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Events · Mission Control" };

// ─── Types ────────────────────────────────────────────────────────────

type CalEvent =
  | { kind: "dividend"; date: string; ticker: string; market: "br" | "us"; amount: number; pay_date: string | null; currency: string | null }
  | { kind: "earnings"; date: string; ticker: string; market: "br" | "us"; projected_kind: string; is_holding: boolean; name: string | null }
  | { kind: "filing"; date: string; ticker: string; market: "br" | "us"; filingKind: string; summary: string | null; url: string | null };

// ─── Page ─────────────────────────────────────────────────────────────

export default function EventsPage() {
  const divs = upcomingDividends(60);
  const earn = upcomingFilings(60);
  const recentFilings = listRecentEvents(40);

  // Combine into one stream sorted by date
  const upcoming: CalEvent[] = [
    ...divs.map<CalEvent>((d) => ({
      kind: "dividend",
      date: d.ex_date,
      ticker: d.ticker,
      market: d.market,
      amount: d.amount,
      pay_date: d.pay_date,
      currency: d.currency,
    })),
    ...earn.map<CalEvent>((e) => ({
      kind: "earnings",
      date: e.earnings_date,
      ticker: e.ticker,
      market: e.market,
      projected_kind: e.projected_kind,
      is_holding: e.is_holding,
      name: e.name,
    })),
  ].sort((a, b) => a.date.localeCompare(b.date));

  const recent: CalEvent[] = recentFilings.map((f) => ({
    kind: "filing",
    date: f.event_date,
    ticker: f.ticker,
    market: f.market,
    filingKind: f.kind,
    summary: f.summary,
    url: f.url,
  }));

  // Group upcoming by date
  const upcomingByDate = new Map<string, CalEvent[]>();
  for (const ev of upcoming) {
    if (!upcomingByDate.has(ev.date)) upcomingByDate.set(ev.date, []);
    upcomingByDate.get(ev.date)!.push(ev);
  }

  return (
    <div className="px-6 py-5 max-w-[1280px] mx-auto">
      {/* ── Hero ──────────────────────────────────────────────────── */}
      <header className="mb-6">
        <h1
          className="font-display"
          style={{
            fontSize: 28,
            fontWeight: 600,
            color: "var(--text-primary)",
            letterSpacing: "-0.005em",
            lineHeight: 1.15,
          }}
        >
          Events
        </h1>
        <p
          className="type-body"
          style={{ marginTop: 4, color: "var(--text-tertiary)" }}
        >
          Forward dividends · earnings · filings · 60 dias
        </p>
      </header>

      {/* ── Stats ribbon ──────────────────────────────────────────── */}
      <section className="card p-5 mb-6">
        <div className="grid grid-cols-3 gap-px" style={{ background: "var(--border-subtle)" }}>
          <RibbonStat label="Forward dividends" value={divs.length} unit="próx 60d" />
          <RibbonStat label="Upcoming earnings" value={earn.length} unit="próx 60d" divide />
          <RibbonStat label="Recent filings" value={recentFilings.length} unit="últimas" divide />
        </div>
      </section>

      {/* ── Upcoming timeline ─────────────────────────────────────── */}
      <section className="mb-8">
        <SectionHeader
          title="Upcoming"
          subtitle={`${upcoming.length} events · agrupado por dia`}
        />
        {upcoming.length === 0 ? (
          <div className="card p-8 text-center">
            <p className="type-body-sm italic" style={{ color: "var(--text-tertiary)" }}>
              Sem events nos próximos 60 dias.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {[...upcomingByDate.entries()].map(([date, events]) => (
              <DayBlock key={date} date={date} events={events} />
            ))}
          </div>
        )}
      </section>

      {/* ── Recent filings ────────────────────────────────────────── */}
      <section>
        <SectionHeader
          title="Recent filings"
          subtitle={`Últimos ${recent.length} fatos relevantes / 8-K / 10-Q`}
        />
        {recent.length === 0 ? (
          <div className="card p-8 text-center">
            <p className="type-body-sm italic" style={{ color: "var(--text-tertiary)" }}>
              Sem filings.
            </p>
          </div>
        ) : (
          <div className="card overflow-hidden">
            <table className="data-table">
              <thead>
                <tr>
                  <th style={{ width: 110 }}>Data</th>
                  <th style={{ width: 90 }}>Mkt</th>
                  <th style={{ width: 110 }}>Ticker</th>
                  <th style={{ width: 100 }}>Tipo</th>
                  <th>Resumo</th>
                </tr>
              </thead>
              <tbody>
                {recent.slice(0, 30).map((ev, i) =>
                  ev.kind === "filing" ? (
                    <tr key={`${ev.ticker}-${ev.date}-${i}`} style={{ cursor: "default" }}>
                      <td className="type-byline" style={{ color: "var(--text-tertiary)" }}>
                        {formatDate(ev.date, "short")}
                      </td>
                      <td>
                        <span
                          style={{
                            color: ev.market === "br" ? "var(--mkt-br)" : "var(--mkt-us)",
                            fontWeight: 600,
                            fontSize: 11,
                          }}
                        >
                          {ev.market.toUpperCase()}
                        </span>
                      </td>
                      <td>
                        <EventTickerLink ticker={ev.ticker} />
                      </td>
                      <td className="type-byline" style={{ color: "var(--text-secondary)" }}>
                        {ev.filingKind}
                      </td>
                      <td className="type-body-sm" style={{ color: "var(--text-primary)" }}>
                        {ev.summary || "—"}
                        {ev.url && (
                          <a
                            href={ev.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{ color: "var(--accent-primary)", marginLeft: 8, fontSize: 11 }}
                          >
                            ↗
                          </a>
                        )}
                      </td>
                    </tr>
                  ) : null
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

// ─── Sub-components ───────────────────────────────────────────────────

function SectionHeader({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="mb-3">
      <h2
        className="font-display"
        style={{
          fontSize: 18,
          fontWeight: 600,
          color: "var(--text-primary)",
          letterSpacing: "-0.005em",
        }}
      >
        {title}
      </h2>
      <p className="type-byline" style={{ marginTop: 2 }}>
        {subtitle}
      </p>
    </div>
  );
}

function DayBlock({ date, events }: { date: string; events: CalEvent[] }) {
  // Sort within day: earnings first, then dividends
  const sorted = [...events].sort((a, b) => {
    const order = (k: string) => (k === "earnings" ? 0 : k === "dividend" ? 1 : 2);
    return order(a.kind) - order(b.kind);
  });
  return (
    <div className="card overflow-hidden">
      <div
        className="px-5 py-3 flex items-baseline justify-between"
        style={{
          borderBottom: "1px solid var(--border-subtle)",
          background: "var(--bg-overlay)",
        }}
      >
        <h3
          className="font-display"
          style={{
            fontSize: 14,
            fontWeight: 600,
            color: "var(--text-primary)",
          }}
        >
          {formatDate(date, "medium")}
        </h3>
        <span className="type-byline">{events.length} event{events.length === 1 ? "" : "s"}</span>
      </div>
      <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
        {sorted.map((ev, i) => (
          <li
            key={i}
            className="px-5 py-3 flex items-center gap-3"
            style={{
              borderBottom: i === sorted.length - 1 ? "0" : "1px solid var(--border-subtle)",
            }}
          >
            <KindBadge kind={ev.kind} subkind={ev.kind === "earnings" ? ev.projected_kind : undefined} />
            <span
              style={{
                color: ev.market === "br" ? "var(--mkt-br)" : "var(--mkt-us)",
                fontWeight: 600,
                fontSize: 11,
                width: 22,
              }}
            >
              {ev.market.toUpperCase()}
            </span>
            <EventTickerLink ticker={ev.ticker} />
            <div className="flex-1 min-w-0">
              {ev.kind === "dividend" ? (
                <p
                  className="type-body-sm"
                  style={{ color: "var(--text-secondary)", margin: 0 }}
                >
                  Ex-dividend{" "}
                  <span style={{ color: "var(--text-primary)", fontWeight: 500 }}>
                    {formatCurrency(
                      ev.amount,
                      ev.market === "br" ? "BRL" : "USD",
                      4
                    )}
                  </span>
                  {ev.pay_date && (
                    <span style={{ color: "var(--text-tertiary)", marginLeft: 8 }}>
                      · paga {formatDate(ev.pay_date, "short")}
                    </span>
                  )}
                </p>
              ) : ev.kind === "earnings" ? (
                <p
                  className="type-body-sm"
                  style={{ color: "var(--text-secondary)", margin: 0 }}
                >
                  Earnings · projected{" "}
                  <span style={{ color: "var(--text-primary)", fontWeight: 500 }}>
                    {ev.projected_kind}
                  </span>
                  {ev.is_holding && (
                    <span
                      style={{ color: "var(--accent-primary)", marginLeft: 8, fontWeight: 500 }}
                    >
                      · HOLDING
                    </span>
                  )}
                  {ev.name && (
                    <span style={{ color: "var(--text-tertiary)", marginLeft: 8 }}>
                      · {ev.name}
                    </span>
                  )}
                </p>
              ) : null}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

function KindBadge({ kind, subkind }: { kind: "dividend" | "earnings" | "filing"; subkind?: string }) {
  const meta =
    kind === "dividend"
      ? { label: "DIV", bg: "var(--jpm-gain-soft)", fg: "var(--verdict-buy)" }
      : kind === "earnings"
      ? { label: subkind || "EPS", bg: "var(--jpm-blue-soft)", fg: "var(--accent-primary)" }
      : { label: "FILING", bg: "var(--bg-overlay)", fg: "var(--text-secondary)" };
  return (
    <span
      style={{
        background: meta.bg,
        color: meta.fg,
        padding: "3px 8px",
        borderRadius: 4,
        fontSize: 10,
        fontWeight: 600,
        letterSpacing: "0.03em",
        minWidth: 50,
        textAlign: "center",
        flexShrink: 0,
      }}
    >
      {meta.label}
    </span>
  );
}

function RibbonStat({
  label,
  value,
  unit,
  divide,
}: {
  label: string;
  value: number;
  unit?: string;
  divide?: boolean;
}) {
  return (
    <div
      style={{
        background: "var(--bg-elevated)",
        padding: "10px 16px",
      }}
    >
      <p className="type-caption" style={{ marginBottom: 4 }}>
        {label}
      </p>
      <p style={{ margin: 0, display: "flex", alignItems: "baseline", gap: 6 }}>
        <span
          className="font-display tabular"
          style={{ fontSize: 22, fontWeight: 600, color: "var(--text-primary)", lineHeight: 1.1 }}
        >
          {value}
        </span>
        {unit && (
          <span className="type-caption" style={{ color: "var(--text-tertiary)" }}>
            {unit}
          </span>
        )}
      </p>
    </div>
  );
}
