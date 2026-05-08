import type { Metadata } from "next";
import Database from "better-sqlite3";
import { ArrowRight, BellPlus, Sparkles } from "lucide-react";

import { listAlerts, type Alert } from "@/lib/alerts";
import { listFairValue, type FairValueRow } from "@/lib/db";
import { DB_BR, DB_US } from "@/lib/paths";
import { formatCurrency, formatDate } from "@/lib/format";
import { Suggestions, List, History } from "./alerts-client";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Alerts · Mission Control" };

// ─── Suggestion engine ─────────────────────────────────────────────────
// "Preço justo de entrada": for each fair_value row, if current price is
// within 5% above the fair price OR already below it, suggest a "below"
// alert at the fair price (entry signal). We dedupe against existing
// active alerts.

type Suggestion = {
  ticker: string;
  market: "br" | "us";
  fair_price: number;
  current_price: number;
  upside_pct: number;
  method: string;
  computed_at: string;
  // The alert we'd create
  threshold: number;
  direction: "above" | "below";
  rationale: string;
};

function readCurrentPrice(market: "br" | "us", ticker: string): number | null {
  const file = market === "br" ? DB_BR : DB_US;
  try {
    const db = new Database(file, { readonly: true, fileMustExist: true });
    const r = db
      .prepare("SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1")
      .get(ticker) as { close: number } | undefined;
    db.close();
    return r?.close ?? null;
  } catch {
    return null;
  }
}

function buildSuggestions(activeAlerts: Alert[]): Suggestion[] {
  const fairs = listFairValue();
  const existing = new Set(
    activeAlerts.map((a) => `${a.ticker}:${a.kind}`)
  );
  const out: Suggestion[] = [];
  for (const f of fairs) {
    if (existing.has(`${f.ticker}:fair_value_entry`)) continue;
    const px = readCurrentPrice(f.market, f.ticker);
    if (px === null) continue;
    // Only suggest when price is meaningfully near fair price
    // (within 10% above OR up to 25% below).
    const gapPct = ((px - f.fair_price) / f.fair_price) * 100;
    if (gapPct > 10) continue;            // current price is way above fair; no entry signal
    if (gapPct < -25) continue;           // already deep value; user already aware
    out.push({
      ticker: f.ticker,
      market: f.market,
      fair_price: f.fair_price,
      current_price: px,
      upside_pct: f.upside_pct,
      method: f.method,
      computed_at: f.computed_at,
      threshold: f.fair_price,
      direction: "below",
      rationale:
        gapPct >= 0
          ? `Currently ${gapPct.toFixed(1)}% above fair (${f.method}). Wait for entry.`
          : `Already ${Math.abs(gapPct).toFixed(1)}% below fair — close to a buy.`,
    });
  }
  // Sort: closest to fair first
  return out.sort((a, b) => {
    const ga = Math.abs(a.current_price - a.fair_price) / a.fair_price;
    const gb = Math.abs(b.current_price - b.fair_price) / b.fair_price;
    return ga - gb;
  });
}

// ─── Page ─────────────────────────────────────────────────────────────

export default function AlertsPage() {
  const all = listAlerts();
  const active = all.filter((a) => a.status === "active");
  const dismissed = all.filter((a) => a.status === "dismissed");
  const triggered = all.filter((a) => a.status === "triggered");
  const suggestions = buildSuggestions(active);

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
          Alerts
        </h1>
        <p
          className="type-body"
          style={{ marginTop: 4, color: "var(--text-tertiary)" }}
        >
          Price alerts + auto-suggested entry triggers vindos da fair-value engine.
        </p>
      </header>

      {/* ── Stats ribbon ──────────────────────────────────────────── */}
      <section className="card p-5 mb-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-px" style={{ background: "var(--border-subtle)" }}>
          <RibbonStat label="Active" value={active.length} accent="var(--verdict-buy)" />
          <RibbonStat label="Triggered" value={triggered.length} accent="var(--accent-primary)" divide />
          <RibbonStat label="Auto-suggested" value={suggestions.length} accent="var(--verdict-hold)" divide />
          <RibbonStat label="Dismissed" value={dismissed.length} divide />
        </div>
      </section>

      {/* ── Auto-suggested ────────────────────────────────────────── */}
      <section className="mb-8">
        <SectionHeader
          title="Auto-suggested entries"
          subtitle="Computado de scoring/fair_value.py · click 'Set' para activar"
          icon={<Sparkles size={14} />}
        />
        {suggestions.length === 0 ? (
          <div className="card p-8 text-center">
            <p className="type-body-sm italic" style={{ color: "var(--text-tertiary)" }}>
              Sem sugestões abertas. Todos os fair-values estão fora de gama ou já têm alerta.
            </p>
          </div>
        ) : (
          <Suggestions suggestions={suggestions} />
        )}
      </section>

      {/* ── Active alerts ─────────────────────────────────────────── */}
      <section className="mb-8">
        <SectionHeader
          title="Active alerts"
          subtitle={`${active.length} a monitorizar`}
          icon={<BellPlus size={14} />}
        />
        {active.length === 0 ? (
          <div className="card p-8 text-center">
            <p className="type-body-sm italic" style={{ color: "var(--text-tertiary)" }}>
              Sem alerts activos. Cria um a partir do side-sheet de qualquer ticker.
            </p>
          </div>
        ) : (
          <List alerts={active} />
        )}
      </section>

      {/* ── Triggered + Dismissed (collapsed) ─────────────────────── */}
      {(triggered.length > 0 || dismissed.length > 0) && (
        <section className="mb-8">
          <SectionHeader
            title="History"
            subtitle={`${triggered.length} triggered · ${dismissed.length} dismissed`}
          />
          <History alerts={[...triggered, ...dismissed]} />
        </section>
      )}
    </div>
  );
}

// ─── Sub-components ───────────────────────────────────────────────────

function SectionHeader({
  title,
  subtitle,
  icon,
}: {
  title: string;
  subtitle: string;
  icon?: React.ReactNode;
}) {
  return (
    <div className="mb-3 flex items-baseline justify-between gap-2 flex-wrap">
      <div className="flex items-baseline gap-2">
        {icon && <span style={{ color: "var(--accent-primary)" }}>{icon}</span>}
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
      </div>
      <p className="type-byline">{subtitle}</p>
    </div>
  );
}

function RibbonStat({
  label,
  value,
  accent,
  divide,
}: {
  label: string;
  value: number;
  accent?: string;
  divide?: boolean;
}) {
  return (
    <div style={{ background: "var(--bg-elevated)", padding: "10px 16px" }}>
      <p className="type-caption" style={{ marginBottom: 4 }}>
        {label}
      </p>
      <p
        className="font-display tabular"
        style={{
          fontSize: 22,
          fontWeight: 600,
          color: accent || "var(--text-primary)",
          margin: 0,
          lineHeight: 1.1,
        }}
      >
        {value}
      </p>
    </div>
  );
}
