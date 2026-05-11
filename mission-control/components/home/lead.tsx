"use client";

// ── BAND 1 · THE LEAD ─────────────────────────────────────────────────
//
// Editorial-style top band — "what is true today?". Modeled after the
// front page of the Financial Times, with twists from JPM Self-Directed
// (account weather strip) and Robinhood (oversize hero numbers).
//
// Reading mode: passive. 30 seconds of skimming should answer the four
// questions a long-term DRIP investor asks every morning:
//
//   1. Did anything material happen in my universe? → Headline + dek
//   2. How did my book do?                          → Position strip
//   3. Who's paying me, when?                       → Dividend timeline
//   4. Where is my forward income headed?           → Forward income line
//
// The headline is the *story of the day*. It is selected by the spotlight
// pipeline (events table joined to portfolio_positions, ranked by
// severity × is_holding × recency). When nothing material happens we say
// "A QUIET TAPE" — silence is honest signal too.
//
// All data flowing into this component is plain props (server-rendered
// upstream). The component itself is "use client" only because it
// renders the focus-ticker chip which uses the context.

import { ReactNode } from "react";
import Link from "next/link";
import { ChevronRight } from "lucide-react";
import { TickerLogo, PercentDelta } from "../jpm-atoms";
import { formatCurrency } from "@/lib/format";

// ── Types ────────────────────────────────────────────────────────────

export type LeadHeadline = {
  kicker: string;          // e.g. "Holdings · Earnings"
  title: string;           // serif hero — 6-12 words
  dek: string;             // 1-2 sentence summary
  ticker: string | null;   // ticker chip (null = no spotlight, e.g. quiet tape)
  market: "br" | "us" | null;
  href?: string;           // deep-link to the underlying source (filing, etc.)
};

export type LeadBriefingLine = {
  label: "Markets" | "Money" | "Mail";
  body: string;            // single sentence
};

export type LeadPositionStrip = {
  br_nav: number;
  us_nav: number;
  br_day_pct: number | null;
  us_day_pct: number | null;
  br_ytd_pct: number;
  us_ytd_pct: number;
  br_cash: number;
  us_cash: number;
};

export type LeadDividendDay = {
  iso_date: string;        // YYYY-MM-DD
  weekday: string;         // "Mon", "Tue"...
  day_num: number;         // 1-31
  is_today: boolean;
  is_weekend: boolean;
  payments: { ticker: string; amount: number; currency: "BRL" | "USD" }[];
};

export type LeadForwardIncome = {
  br_annual: number;
  us_annual: number;
  br_yoy_pct: number;      // y/y change in forward annual income
  us_yoy_pct: number;
};

export type LeadProps = {
  edition_label: string;     // "Saturday, May 9 · A.M. Edition"
  council_chip: string;      // "Council 5/5"
  briefing_chip: string;     // "briefing 06:14"
  headline: LeadHeadline;
  briefing: LeadBriefingLine[];   // exactly 3 lines
  position: LeadPositionStrip;
  dividend_strip: LeadDividendDay[];  // 14 entries
  forward_income: LeadForwardIncome;
};

// ── Component ────────────────────────────────────────────────────────

export function Lead({
  edition_label,
  council_chip,
  briefing_chip,
  headline,
  briefing,
  position,
  dividend_strip,
  forward_income,
}: LeadProps) {
  return (
    <section
      className="lead"
      aria-label="The lead — what is true today"
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderRadius: "var(--radius)",
        boxShadow: "var(--shadow-sm)",
        overflow: "hidden",
      }}
    >
      {/* ── Masthead weather strip ─────────────────────────── */}
      <Masthead
        edition_label={edition_label}
        council_chip={council_chip}
        briefing_chip={briefing_chip}
      />

      {/* ── Hero headline + dek ───────────────────────────── */}
      <Headline {...headline} />

      {/* ── Briefing strip (3 lines: Markets · Money · Mail) ── */}
      <Briefing lines={briefing} />

      {/* ── Position snapshot strip ───────────────────────── */}
      <PositionStrip {...position} />

      {/* ── 14-day dividend timeline ──────────────────────── */}
      <DividendStrip days={dividend_strip} />

      {/* ── Forward income line — the polar star ──────────── */}
      <ForwardIncome {...forward_income} />
    </section>
  );
}

// ── Sub-blocks ───────────────────────────────────────────────────────

function Masthead({
  edition_label,
  council_chip,
  briefing_chip,
}: {
  edition_label: string;
  council_chip: string;
  briefing_chip: string;
}) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "10px 20px",
        background: "var(--jpm-ink)",
        color: "#F4F6F8",
        fontFamily: "var(--font-sans)",
        fontSize: 11,
        letterSpacing: "0.08em",
        textTransform: "uppercase",
        fontWeight: 600,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <span style={{ color: "#F4F6F8" }}>Mission Control</span>
        <span style={{ color: "rgba(244,246,248,0.4)" }}>·</span>
        <span style={{ color: "rgba(244,246,248,0.7)", fontWeight: 500 }}>
          {edition_label}
        </span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 10, fontWeight: 500 }}>
        <span style={{ color: "rgba(244,246,248,0.7)" }}>{council_chip}</span>
        <span style={{ color: "rgba(244,246,248,0.4)" }}>·</span>
        <span style={{ color: "rgba(244,246,248,0.7)" }}>{briefing_chip}</span>
      </div>
    </div>
  );
}

function Headline({ kicker, title, dek, ticker, market, href }: LeadHeadline) {
  return (
    <div style={{ padding: "28px 24px 22px", borderBottom: "1px solid var(--border-subtle)" }}>
      <div className="grid grid-cols-12 gap-6 items-start">
        <div className="col-span-12 lg:col-span-9">
          <p
            className="type-h3"
            style={{ marginBottom: 10, color: "var(--jpm-blue)" }}
          >
            {kicker}
          </p>
          <h1
            style={{
              fontFamily: "var(--font-display)",
              fontSize: 34,
              lineHeight: 1.12,
              fontWeight: 700,
              letterSpacing: "-0.02em",
              color: "var(--text-primary)",
              marginBottom: 12,
              maxWidth: "60ch",
            }}
          >
            {href ? (
              <Link href={href} style={{ color: "inherit", textDecoration: "none" }}>
                {title}
              </Link>
            ) : (
              title
            )}
          </h1>
          <p
            style={{
              fontFamily: "var(--font-display)",
              fontSize: 16,
              lineHeight: 1.55,
              color: "var(--text-secondary)",
              fontWeight: 400,
              fontStyle: "italic",
              maxWidth: "70ch",
            }}
          >
            {dek}
          </p>
        </div>
        {/* Spotlight ticker chip — right column on desktop */}
        {ticker && market ? (
          <div className="col-span-12 lg:col-span-3" style={{ display: "flex", justifyContent: "flex-end" }}>
            <SpotlightChip ticker={ticker} market={market} />
          </div>
        ) : null}
      </div>
    </div>
  );
}

function SpotlightChip({ ticker, market }: { ticker: string; market: "br" | "us" }) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 12,
        padding: "12px 16px",
        background: "var(--bg-overlay)",
        border: "1px solid var(--border-subtle)",
        borderRadius: "var(--radius)",
        minWidth: 180,
      }}
    >
      <TickerLogo ticker={ticker} size="md" />
      <div>
        <p
          className="type-h3"
          style={{ marginBottom: 2, color: "var(--text-tertiary)" }}
        >
          Spotlight
        </p>
        <p
          className="font-data"
          style={{
            fontSize: 16,
            fontWeight: 700,
            color: "var(--text-primary)",
            letterSpacing: "0.02em",
          }}
        >
          {ticker}
          <span
            style={{
              fontSize: 10,
              fontWeight: 600,
              marginLeft: 6,
              padding: "1px 6px",
              borderRadius: 999,
              background: market === "br" ? "var(--jpm-gain-soft)" : "var(--jpm-blue-soft)",
              color: market === "br" ? "var(--mkt-br)" : "var(--mkt-us)",
              fontFamily: "var(--font-sans)",
            }}
          >
            {market.toUpperCase()}
          </span>
        </p>
      </div>
    </div>
  );
}

function Briefing({ lines }: { lines: LeadBriefingLine[] }) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(3, 1fr)",
        borderBottom: "1px solid var(--border-subtle)",
      }}
    >
      {lines.map((line, i) => (
        <div
          key={line.label}
          style={{
            padding: "14px 20px",
            borderRight: i < 2 ? "1px solid var(--border-subtle)" : "none",
            display: "flex",
            alignItems: "baseline",
            gap: 10,
            minHeight: 52,
          }}
        >
          <span
            className="type-h3"
            style={{ color: "var(--jpm-blue)", flexShrink: 0, minWidth: 56 }}
          >
            {line.label}
          </span>
          <span className="type-body-sm" style={{ color: "var(--text-secondary)" }}>
            {line.body}
          </span>
        </div>
      ))}
    </div>
  );
}

function PositionStrip(p: LeadPositionStrip) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(2, 1fr)",
        borderBottom: "1px solid var(--border-subtle)",
      }}
    >
      <NavBlock
        label="Carteira Brasil · BRL"
        nav={p.br_nav}
        currency="BRL"
        day_pct={p.br_day_pct}
        ytd_pct={p.br_ytd_pct}
        cash={p.br_cash}
        accent="var(--mkt-br)"
        rightBorder
      />
      <NavBlock
        label="Carteira EUA · USD"
        nav={p.us_nav}
        currency="USD"
        day_pct={p.us_day_pct}
        ytd_pct={p.us_ytd_pct}
        cash={p.us_cash}
        accent="var(--mkt-us)"
      />
    </div>
  );
}

function NavBlock({
  label,
  nav,
  currency,
  day_pct,
  ytd_pct,
  cash,
  accent,
  rightBorder,
}: {
  label: string;
  nav: number;
  currency: "BRL" | "USD";
  day_pct: number | null;
  ytd_pct: number;
  cash: number;
  accent: string;
  rightBorder?: boolean;
}) {
  return (
    <div
      style={{
        padding: "16px 20px",
        borderRight: rightBorder ? "1px solid var(--border-subtle)" : "none",
      }}
    >
      <p
        className="type-h3"
        style={{
          marginBottom: 8,
          color: accent,
          borderLeft: `2px solid ${accent}`,
          paddingLeft: 8,
        }}
      >
        {label}
      </p>
      <div style={{ display: "flex", alignItems: "baseline", gap: 16, flexWrap: "wrap" }}>
        <span
          className="font-data"
          style={{
            fontSize: 22,
            fontWeight: 700,
            color: "var(--text-primary)",
            letterSpacing: "-0.01em",
          }}
        >
          {formatCurrency(nav, currency, 0)}
        </span>
        <Stat label="Hoje">
          <PercentDelta pct={day_pct} inline />
        </Stat>
        <Stat label="YTD">
          <PercentDelta pct={ytd_pct} inline />
        </Stat>
        <Stat label="Cash">
          <span className="font-data" style={{ fontSize: 12, color: "var(--text-secondary)" }}>
            {formatCurrency(cash, currency, 0)}
          </span>
        </Stat>
      </div>
    </div>
  );
}

function Stat({ label, children }: { label: string; children: ReactNode }) {
  return (
    <span style={{ display: "inline-flex", flexDirection: "column", gap: 0 }}>
      <span
        style={{
          fontSize: 9,
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          color: "var(--text-tertiary)",
          fontFamily: "var(--font-sans)",
          fontWeight: 600,
        }}
      >
        {label}
      </span>
      <span style={{ fontSize: 13 }}>{children}</span>
    </span>
  );
}

function DividendStrip({ days }: { days: LeadDividendDay[] }) {
  return (
    <div
      style={{
        padding: "16px 20px",
        borderBottom: "1px solid var(--border-subtle)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: 12,
        }}
      >
        <p className="type-h3" style={{ color: "var(--text-tertiary)" }}>
          Dividend timeline · próximos 14 dias
        </p>
        <Link
          href="/calendar"
          style={{
            fontSize: 11,
            color: "var(--accent-primary)",
            fontWeight: 500,
            display: "inline-flex",
            alignItems: "center",
            gap: 2,
            textDecoration: "none",
          }}
        >
          Calendar <ChevronRight size={11} />
        </Link>
      </div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(14, 1fr)",
          gap: 4,
        }}
      >
        {days.map((d) => (
          <DividendCell key={d.iso_date} day={d} />
        ))}
      </div>
    </div>
  );
}

function DividendCell({ day }: { day: LeadDividendDay }) {
  const has_payment = day.payments.length > 0;
  const total_count = day.payments.length;
  const tooltip = has_payment
    ? day.payments
        .map((p) => `${p.ticker}: ${p.currency === "BRL" ? "R$" : "$"}${p.amount.toFixed(2)}`)
        .join(" · ")
    : "Sem pagamentos";
  return (
    <div
      title={`${day.iso_date} — ${tooltip}`}
      style={{
        padding: "8px 4px",
        borderRadius: "var(--radius-sm)",
        textAlign: "center",
        background: day.is_today
          ? "var(--jpm-blue-soft)"
          : has_payment
          ? "var(--bg-overlay)"
          : "transparent",
        border: day.is_today
          ? "1px solid var(--jpm-blue)"
          : "1px solid var(--border-subtle)",
        opacity: day.is_weekend && !has_payment ? 0.5 : 1,
        minHeight: 56,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-between",
        gap: 4,
        cursor: has_payment ? "help" : "default",
      }}
    >
      <span
        style={{
          fontSize: 9,
          fontFamily: "var(--font-sans)",
          fontWeight: 600,
          color: day.is_today ? "var(--jpm-blue)" : "var(--text-tertiary)",
          textTransform: "uppercase",
          letterSpacing: "0.04em",
        }}
      >
        {day.weekday}
      </span>
      <span
        className="font-data"
        style={{
          fontSize: 14,
          fontWeight: day.is_today ? 700 : 600,
          color: day.is_today ? "var(--jpm-blue)" : "var(--text-primary)",
          lineHeight: 1,
        }}
      >
        {day.day_num}
      </span>
      {has_payment ? (
        <span
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 2,
            fontSize: 9,
            fontFamily: "var(--font-mono)",
            fontWeight: 600,
            color: "var(--verdict-buy)",
          }}
        >
          ●{total_count > 1 ? `×${total_count}` : ""}
        </span>
      ) : (
        <span style={{ fontSize: 9, color: "transparent" }}>·</span>
      )}
    </div>
  );
}

function ForwardIncome({
  br_annual,
  us_annual,
  br_yoy_pct,
  us_yoy_pct,
}: LeadForwardIncome) {
  return (
    <div
      style={{
        padding: "16px 20px 18px",
        background: "var(--bg-overlay)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexWrap: "wrap",
        gap: 16,
      }}
    >
      <div style={{ display: "flex", alignItems: "baseline", gap: 16, flexWrap: "wrap" }}>
        <p className="type-h3" style={{ color: "var(--text-tertiary)" }}>
          Forward annual income · DRIP polar star
        </p>
      </div>
      <div style={{ display: "flex", alignItems: "baseline", gap: 24 }}>
        <ForwardBlock
          flag="BR"
          amount={br_annual}
          currency="BRL"
          yoy={br_yoy_pct}
          accent="var(--mkt-br)"
        />
        <span style={{ color: "var(--text-tertiary)", fontSize: 14 }}>+</span>
        <ForwardBlock
          flag="US"
          amount={us_annual}
          currency="USD"
          yoy={us_yoy_pct}
          accent="var(--mkt-us)"
        />
      </div>
    </div>
  );
}

function ForwardBlock({
  flag,
  amount,
  currency,
  yoy,
  accent,
}: {
  flag: string;
  amount: number;
  currency: "BRL" | "USD";
  yoy: number;
  accent: string;
}) {
  return (
    <div style={{ display: "inline-flex", alignItems: "baseline", gap: 8 }}>
      <span
        style={{
          fontSize: 10,
          fontWeight: 700,
          letterSpacing: "0.08em",
          color: accent,
          background: "var(--bg-elevated)",
          border: `1px solid ${accent}`,
          padding: "2px 6px",
          borderRadius: 4,
        }}
      >
        {flag}
      </span>
      <span
        className="font-data"
        style={{ fontSize: 18, fontWeight: 700, color: "var(--text-primary)" }}
      >
        {formatCurrency(amount, currency, 0)}
      </span>
      <span style={{ fontSize: 11 }}>
        <PercentDelta pct={yoy} inline />
      </span>
      <span
        style={{
          fontSize: 9,
          color: "var(--text-tertiary)",
          letterSpacing: "0.06em",
          textTransform: "uppercase",
          fontWeight: 600,
        }}
      >
        y/y
      </span>
    </div>
  );
}
