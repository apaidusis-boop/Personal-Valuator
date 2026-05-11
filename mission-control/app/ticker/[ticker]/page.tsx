import type { Metadata } from "next";
import Link from "next/link";
import Database from "better-sqlite3";

import { DB_BR, DB_US } from "@/lib/paths";
import { listStrategyRuns } from "@/lib/db";
import { readCouncilStory } from "@/lib/vault";
import { formatCurrency, formatDate, formatPercent } from "@/lib/format";

import { PriceChart } from "@/components/charts";
import { FairTrajectoryChart } from "@/components/fair-trajectory-chart";
import { ConsensusPanel } from "@/components/consensus-panel";
import StancePill from "@/components/stance-pill";
import {
  Pill,
  pillVariantFromVerdict,
  pillVariantFromMarket,
} from "@/components/ui";

import TickerActions from "./ticker-actions";

export const dynamic = "force-dynamic";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ ticker: string }>;
}): Promise<Metadata> {
  const { ticker } = await params;
  return { title: `${ticker.toUpperCase()} · Mission Control` };
}

type Snapshot = {
  ticker: string;
  market: "br" | "us";
  name: string | null;
  sector: string | null;
  is_holding: boolean;
  price: number | null;
  price_date: string | null;
  position: { qty: number; entry: number; entry_date: string } | null;
  fundamentals: {
    pe: number | null;
    pb: number | null;
    dy: number | null;
    roe: number | null;
    eps: number | null;
    bvps: number | null;
    period_end: string | null;
  } | null;
  score: { score: number; passes: boolean; run_date: string } | null;
  divs_12m: number | null;
  fair_values: {
    method: string;
    fair_price: number | null;
    upside_pct: number | null;
  }[];
};

function fetchTicker(tk: string): Snapshot | null {
  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = new Database(file, { readonly: true, fileMustExist: true });
      const company = db
        .prepare("SELECT name, sector, is_holding FROM companies WHERE ticker=?")
        .get(tk) as { name: string; sector: string; is_holding: number } | undefined;
      if (!company) {
        db.close();
        continue;
      }
      const priceRow = db
        .prepare(
          "SELECT close, date FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1"
        )
        .get(tk) as { close: number; date: string } | undefined;

      let position: Snapshot["position"] = null;
      try {
        const p = db
          .prepare(
            "SELECT quantity, entry_price, entry_date FROM portfolio_positions WHERE ticker=? AND active=1"
          )
          .get(tk) as { quantity: number; entry_price: number; entry_date: string } | undefined;
        if (p) position = { qty: p.quantity, entry: p.entry_price, entry_date: p.entry_date };
      } catch {/* */}

      let fundamentals: Snapshot["fundamentals"] = null;
      try {
        const f = db
          .prepare(
            "SELECT pe, pb, dy, roe, eps, bvps, period_end FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1"
          )
          .get(tk) as Snapshot["fundamentals"];
        if (f) fundamentals = f;
      } catch {/* */}

      let score: Snapshot["score"] = null;
      try {
        const s = db
          .prepare(
            "SELECT score, passes_screen, run_date FROM scores WHERE ticker=? ORDER BY run_date DESC LIMIT 1"
          )
          .get(tk) as { score: number; passes_screen: number; run_date: string } | undefined;
        if (s) score = { score: s.score, passes: !!s.passes_screen, run_date: s.run_date };
      } catch {/* */}

      let divs_12m: number | null = null;
      try {
        const cutoff = new Date(Date.now() - 365 * 86400000).toISOString().slice(0, 10);
        const d = db
          .prepare(
            "SELECT COALESCE(SUM(amount),0) as s FROM dividends WHERE ticker=? AND ex_date >= ?"
          )
          .get(tk, cutoff) as { s: number } | undefined;
        divs_12m = d?.s || 0;
      } catch {/* */}

      let fair_values: Snapshot["fair_values"] = [];
      try {
        const rows = db
          .prepare(
            `SELECT method, fair_price, upside_pct FROM fair_value
             WHERE ticker = ?
             ORDER BY computed_at DESC, method`
          )
          .all(tk) as any[];
        // Keep one entry per method (first / freshest)
        const seen = new Set<string>();
        for (const r of rows) {
          if (seen.has(r.method)) continue;
          seen.add(r.method);
          fair_values.push({
            method: r.method,
            fair_price: r.fair_price,
            upside_pct: r.upside_pct,
          });
        }
      } catch {/* */}
      db.close();

      return {
        ticker: tk,
        market,
        name: company.name,
        sector: company.sector,
        is_holding: !!company.is_holding,
        price: priceRow?.close ?? null,
        price_date: priceRow?.date ?? null,
        position,
        fundamentals,
        score,
        divs_12m,
        fair_values,
      };
    } catch {/* skip */}
  }
  return null;
}

export default async function TickerPage({
  params,
}: {
  params: Promise<{ ticker: string }>;
}) {
  const { ticker } = await params;
  const tk = ticker.toUpperCase().replace(/\.SA$/, "");
  const snap = fetchTicker(tk);
  const council = readCouncilStory(tk);
  const strategyRuns = listStrategyRuns(tk, null, 20);

  if (!snap) {
    return (
      <div className="p-5 max-w-[1200px] space-y-5">
        <div>
          <h1
            className="font-display text-xl font-bold"
            style={{ color: "var(--text-primary)" }}
          >
            {tk}
          </h1>
          <p
            className="text-xs mt-0.5"
            style={{ color: "var(--text-tertiary)" }}
          >
            <Link
              href="/"
              className="hover:underline"
              style={{ color: "var(--accent-glow)" }}
            >
              Home
            </Link>{" "}
            · {tk}
          </p>
        </div>
        <div
          className="p-12 rounded text-center space-y-3"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <p
            className="text-sm"
            style={{ color: "var(--text-secondary)" }}
          >
            Ticker não encontrado
          </p>
          <p
            className="text-xs italic"
            style={{ color: "var(--text-tertiary)" }}
          >
            {tk} não está em nenhuma das DBs (BR ou US).
          </p>
          <Link
            href="/"
            className="inline-block text-[10px] hover:underline"
            style={{ color: "var(--accent-glow)" }}
          >
            ← voltar à Home
          </Link>
        </div>
      </div>
    );
  }

  const cur = snap.market === "br" ? "BRL" : "USD";
  const pnlPct =
    snap.price && snap.position
      ? (snap.price / snap.position.entry - 1) * 100
      : null;
  const yoc =
    snap.position && snap.divs_12m
      ? (snap.divs_12m / snap.position.entry) * 100
      : null;

  // Best strategy verdict (highest score among engines)
  const topStrategy = strategyRuns
    .filter((r) => r.engine !== "hedge")
    .sort((a, b) => b.score - a.score)[0];

  return (
    <div className="p-5 space-y-5 max-w-[1280px]">
      {/* Header — ticker + price + delta ----------------------- */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h1
              className="font-display text-2xl font-bold"
              style={{ color: "var(--text-primary)" }}
            >
              {tk}
            </h1>
            <Pill variant={pillVariantFromMarket(snap.market)}>
              {snap.market.toUpperCase()}
            </Pill>
            {snap.is_holding && <span className="pill pill-gold">HOLDING</span>}
          </div>
          <p
            className="text-xs mt-1"
            style={{ color: "var(--text-tertiary)" }}
          >
            <Link
              href="/"
              className="hover:underline"
              style={{ color: "var(--accent-glow)" }}
            >
              Home
            </Link>{" "}
            · {snap.name || tk} {snap.sector ? ` · ${snap.sector}` : ""}{" "}
            {snap.price_date
              ? ` · cotação ${formatDate(snap.price_date, "relative")}`
              : ""}
          </p>
        </div>
        {snap.price !== null && (
          <div className="text-right">
            <div
              className="font-display text-2xl font-bold tabular"
              style={{ color: "var(--text-primary)" }}
            >
              {formatCurrency(snap.price, cur as "BRL" | "USD", 2)}
            </div>
            {pnlPct !== null && (
              <div
                className="text-xs font-data mt-1"
                style={{
                  color:
                    pnlPct >= 0 ? "var(--gain)" : "var(--loss)",
                }}
              >
                {pnlPct >= 0 ? "▲" : "▼"} {formatPercent(Math.abs(pnlPct), 1)} vs entry
              </div>
            )}
          </div>
        )}
      </div>

      <TickerActions ticker={tk} />

      {/* Council strip ----------------------------------------- */}
      {council && (
        <Link
          href={`/council/${tk}`}
          className="block p-4 rounded transition-colors group"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
            borderTop: "2px solid var(--val-gold)",
          }}
        >
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <div className="flex items-center gap-3 flex-wrap">
              <span
                className="text-[10px] font-semibold tracking-wider uppercase"
                style={{ color: "var(--text-label)" }}
              >
                ⚖ Council
              </span>
              <StancePill
                stance={council.entry.stance}
                confidence={council.entry.confidence}
                size="md"
              />
              <span
                className="text-[10px]"
                style={{ color: "var(--text-tertiary)" }}
              >
                {formatDate(council.entry.date, "relative")}
              </span>
              {council.entry.dissent_count > 0 && (
                <span className="pill pill-hold">
                  {council.entry.dissent_count} dissent
                </span>
              )}
              {council.entry.flag_count > 0 && (
                <span className="pill pill-avoid">
                  ⚑ {council.entry.flag_count}
                </span>
              )}
            </div>
            <span
              className="text-[10px] group-hover:underline"
              style={{ color: "var(--accent-glow)" }}
            >
              ver dossier completo →
            </span>
          </div>
        </Link>
      )}

      {/* Fair value strip --------------------------------------- */}
      {snap.fair_values.length > 0 && (
        <FairValueStrip
          rows={snap.fair_values}
          currentPrice={snap.price}
          currency={cur as "BRL" | "USD"}
        />
      )}

      {/* Phase LL Sprint 3.2 — Multi-house consensus blender ---- */}
      <ConsensusPanel ticker={tk} />

      {/* Phase LL Sprint 3.3 — Fair value trajectory (5y) ------- */}
      <div
        className="rounded p-5"
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
        }}
      >
        <FairTrajectoryChart ticker={tk} height={260} />
      </div>

      {/* Price chart (preserved — short-term price action) ------ */}
      <div
        className="rounded p-5"
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
        }}
      >
        <PriceChart ticker={tk} days={365 * 3} height={240} />
      </div>

      {/* Stats grid: position / fundamentals / screen */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {snap.position ? (
          <PositionCard
            qty={snap.position.qty}
            entry={snap.position.entry}
            entryDate={snap.position.entry_date}
            currentPrice={snap.price}
            divs12m={snap.divs_12m}
            yoc={yoc}
            currency={cur as any}
          />
        ) : (
          <div className="card p-5 flex flex-col items-center text-center gap-2">
            <div className="type-h3">position</div>
            <p className="type-body-sm text-[var(--text-tertiary)] italic">
              Sem posição activa. {snap.is_holding ? "" : "Em watchlist."}
            </p>
          </div>
        )}

        {snap.fundamentals ? (
          <FundamentalsCard f={snap.fundamentals} />
        ) : (
          <div className="card p-5 flex flex-col items-center text-center gap-2">
            <div className="type-h3">fundamentals</div>
            <p className="type-body-sm text-[var(--text-tertiary)] italic">
              Sem dados de fundamentals.
            </p>
          </div>
        )}

        {snap.score ? (
          <ScreenCard score={snap.score} />
        ) : (
          <div className="card p-5 flex flex-col items-center text-center gap-2">
            <div className="type-h3">screen</div>
            <p className="type-body-sm text-[var(--text-tertiary)] italic">
              Sem screen run.
            </p>
          </div>
        )}
      </div>

      {/* Strategy breakdown ------------------------------------ */}
      {strategyRuns.length > 0 && (
        <div
          className="rounded p-4"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
            <div className="flex items-center gap-3 flex-wrap">
              <h3
                className="text-[10px] font-semibold tracking-wider uppercase"
                style={{ color: "var(--text-label)" }}
              >
                Strategy engines
              </h3>
              {topStrategy && (
                <span
                  className="text-[10px]"
                  style={{ color: "var(--text-tertiary)" }}
                >
                  top: {topStrategy.engine} {(topStrategy.score * 100).toFixed(0)}/100
                </span>
              )}
            </div>
            <Link
              href={`/strategy/${tk}?market=${snap.market}`}
              className="text-[10px] hover:underline"
              style={{ color: "var(--accent-glow)" }}
            >
              breakdown completo →
            </Link>
          </div>
          <div className="flex flex-wrap gap-2">
            {strategyRuns
              .filter((r) => r.market === snap.market)
              .map((r) => (
                <span
                  key={r.engine}
                  className="flex items-center gap-2 text-[11px] font-data px-3 py-1.5 rounded"
                  style={{
                    background: "var(--bg-overlay)",
                    border: "1px solid var(--border-subtle)",
                  }}
                >
                  <span
                    className="capitalize"
                    style={{ color: "var(--text-tertiary)" }}
                  >
                    {r.engine}
                  </span>
                  <span style={{ color: "var(--text-primary)" }}>
                    {(r.score * 100).toFixed(0)}
                  </span>
                  <Pill variant={pillVariantFromVerdict(r.verdict)}>
                    {r.verdict}
                  </Pill>
                </span>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}

function PositionCard({
  qty,
  entry,
  entryDate,
  currentPrice,
  divs12m,
  yoc,
  currency,
}: {
  qty: number;
  entry: number;
  entryDate: string;
  currentPrice: number | null;
  divs12m: number | null;
  yoc: number | null;
  currency: "BRL" | "USD";
}) {
  const cost = qty * entry;
  const mv = currentPrice !== null ? qty * currentPrice : null;
  const pnl = mv !== null ? mv - cost : null;
  const pnlPct = mv !== null ? (mv / cost - 1) * 100 : null;

  return (
    <div className="card p-5 space-y-2.5">
      <h3 className="type-h3">position</h3>
      <div className="type-display tabular text-[var(--text-primary)]">
        {qty}
      </div>
      <p className="type-mono-sm text-[var(--text-tertiary)]">
        @ {formatCurrency(entry, currency, 2)} · {formatDate(entryDate, "short")}
      </p>
      <div className="divider-soft my-2" />
      <KvRow k="cost" v={formatCurrency(cost, currency, 0)} />
      {mv !== null && <KvRow k="mv" v={formatCurrency(mv, currency, 0)} />}
      {pnl !== null && (
        <KvRow
          k="pnl"
          v={`${formatCurrency(pnl, currency, 0)} (${formatPercent(pnlPct!, 1, { signed: true })})`}
          color={pnl >= 0 ? "gain" : "loss"}
        />
      )}
      {yoc !== null && divs12m !== null && (
        <KvRow
          k="yoc"
          v={`${formatPercent(yoc, 2)} (${formatCurrency(divs12m * qty, currency, 2)})`}
          color="purple"
        />
      )}
    </div>
  );
}

function FundamentalsCard({
  f,
}: {
  f: NonNullable<Snapshot["fundamentals"]>;
}) {
  return (
    <div className="card p-5 space-y-2.5">
      <h3 className="type-h3">fundamentals</h3>
      <div className="grid grid-cols-2 gap-x-4 gap-y-1.5 type-mono">
        <Metric label="P/E" value={f.pe} />
        <Metric label="P/B" value={f.pb} />
        <Metric label="DY" value={f.dy} fmt="pct-fraction" />
        <Metric label="ROE" value={f.roe} fmt="pct-fraction" />
        <Metric label="EPS" value={f.eps} />
        <Metric label="BVPS" value={f.bvps} />
      </div>
      <p className="type-mono-sm text-[var(--text-tertiary)]">
        period {f.period_end || "—"}
      </p>
    </div>
  );
}

function ScreenCard({ score }: { score: NonNullable<Snapshot["score"]> }) {
  const passes = score.passes;
  return (
    <div
      className={`p-5 rounded-lg border ${
        passes
          ? "border-[var(--jpm-gain)] bg-[var(--jpm-gain-soft)]"
          : "border-[var(--jpm-loss)] bg-[var(--jpm-loss-soft)]"
      } space-y-2.5`}
    >
      <h3 className="type-h3">screen</h3>
      <div
        className={`type-display tabular ${
          passes ? "text-[var(--verdict-buy)]" : "text-[var(--verdict-avoid)]"
        }`}
      >
        {(score.score * 100).toFixed(0)}
      </div>
      <Pill variant={passes ? "buy" : "avoid"}>
        {passes ? "✓ passes" : "✗ fails"}
      </Pill>
      <p className="type-mono-sm text-[var(--text-tertiary)]">
        {formatDate(score.run_date, "relative")}
      </p>
    </div>
  );
}

function KvRow({
  k,
  v,
  color,
}: {
  k: string;
  v: string;
  color?: "gain" | "loss" | "purple" | undefined;
}) {
  const cl =
    color === "gain"
      ? "text-[var(--gain)]"
      : color === "loss"
      ? "text-[var(--loss)]"
      : color === "purple"
      ? "text-[var(--accent-primary)]"
      : "text-[var(--text-primary)]";
  return (
    <div className="flex items-baseline justify-between type-mono-sm">
      <span className="text-[var(--text-tertiary)]">{k}</span>
      <span className={`tabular ${cl}`}>{v}</span>
    </div>
  );
}

function FairValueStrip({
  rows,
  currentPrice,
  currency,
}: {
  rows: { method: string; fair_price: number | null; upside_pct: number | null }[];
  currentPrice: number | null;
  currency: "BRL" | "USD";
}) {
  // Average upside across methods (ignore nulls)
  const valid = rows.filter((r) => r.upside_pct !== null);
  const avgUpside =
    valid.length > 0
      ? valid.reduce((s, r) => s + (r.upside_pct ?? 0), 0) / valid.length
      : null;
  const avgFair =
    rows.filter((r) => r.fair_price !== null).length > 0
      ? rows.reduce((s, r) => s + (r.fair_price ?? 0), 0) /
        rows.filter((r) => r.fair_price !== null).length
      : null;

  const accentColor =
    avgUpside === null
      ? "var(--text-tertiary)"
      : avgUpside > 10
      ? "var(--gain)"
      : avgUpside < -10
      ? "var(--loss)"
      : "var(--neutral, var(--text-secondary))";

  return (
    <div
      className="rounded p-5"
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderTop: `2px solid ${accentColor}`,
      }}
    >
      <div className="flex items-start justify-between gap-4 flex-wrap mb-4">
        <div>
          <h3
            className="text-[10px] font-semibold tracking-wider uppercase"
            style={{ color: "var(--text-label)" }}
          >
            ⚖ Fair value · upside vs preço actual
          </h3>
          <p className="type-byline mt-1">
            {rows.length} método{rows.length === 1 ? "" : "s"} ·{" "}
            {currentPrice !== null
              ? `preço actual ${formatCurrency(currentPrice, currency, 2)}`
              : "preço n/d"}
          </p>
        </div>
        {avgUpside !== null && (
          <div className="text-right">
            <div
              className="font-display text-2xl tabular font-bold"
              style={{ color: accentColor }}
            >
              {avgUpside >= 0 ? "+" : ""}
              {avgUpside.toFixed(1)}%
            </div>
            <p className="type-mono-sm" style={{ color: "var(--text-tertiary)" }}>
              upside médio
              {avgFair !== null
                ? ` · alvo ${formatCurrency(avgFair, currency, 2)}`
                : ""}
            </p>
          </div>
        )}
      </div>

      <table className="data-table">
        <thead>
          <tr>
            <th>Método</th>
            <th className="num">Preço justo</th>
            <th className="num">Upside</th>
            <th className="num">Margem segurança</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => {
            const ms =
              currentPrice !== null && r.fair_price !== null && r.fair_price > 0
                ? ((r.fair_price - currentPrice) / r.fair_price) * 100
                : null;
            const upColor =
              r.upside_pct === null
                ? "var(--text-tertiary)"
                : r.upside_pct > 0
                ? "var(--gain)"
                : "var(--loss)";
            return (
              <tr key={r.method} style={{ cursor: "default" }}>
                <td>
                  <span
                    className="font-data"
                    style={{ color: "var(--text-primary)", fontWeight: 600 }}
                  >
                    {r.method}
                  </span>
                </td>
                <td className="num">
                  {r.fair_price !== null
                    ? formatCurrency(r.fair_price, currency, 2)
                    : "—"}
                </td>
                <td className="num" style={{ color: upColor, fontWeight: 600 }}>
                  {r.upside_pct !== null
                    ? `${r.upside_pct >= 0 ? "+" : ""}${r.upside_pct.toFixed(1)}%`
                    : "—"}
                </td>
                <td className="num" style={{ color: "var(--text-secondary)" }}>
                  {ms !== null ? `${ms.toFixed(1)}%` : "—"}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function Metric({
  label,
  value,
  fmt = "num",
}: {
  label: string;
  value: number | null;
  fmt?: "num" | "pct-fraction";
}) {
  if (value === null || value === undefined) {
    return (
      <div>
        <div className="type-mono-sm text-[var(--text-tertiary)]">{label}</div>
        <div className="text-[var(--text-disabled)]">—</div>
      </div>
    );
  }
  const display =
    fmt === "pct-fraction"
      ? `${(value * 100).toFixed(1)}%`
      : Math.abs(value) < 1
      ? value.toFixed(3)
      : value.toFixed(2);
  return (
    <div>
      <div className="type-mono-sm text-[var(--text-tertiary)]">{label}</div>
      <div className="text-[var(--text-primary)]">{display}</div>
    </div>
  );
}
