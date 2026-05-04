import Link from "next/link";
import Database from "better-sqlite3";

import { DB_BR, DB_US } from "@/lib/paths";
import { listStrategyRuns } from "@/lib/db";
import { readCouncilStory } from "@/lib/vault";
import { formatCurrency, formatDate, formatPercent, formatNumber } from "@/lib/format";

import { PriceChart } from "@/components/charts";
import StancePill from "@/components/stance-pill";
import {
  PageHeader,
  Section,
  Pill,
  pillVariantFromVerdict,
  pillVariantFromMarket,
  EmptyState,
} from "@/components/ui";

import TickerActions from "./ticker-actions";

export const dynamic = "force-dynamic";

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
      <div className="p-8 max-w-[1200px] space-y-6">
        <PageHeader
          title={tk}
          crumbs={[{ label: "Home", href: "/" }, { label: tk }]}
        />
        <EmptyState
          icon="◯"
          title="Ticker não encontrado"
          description="Não está em nenhuma das DBs (BR ou US)."
          action={
            <Link href="/" className="pill pill-glow">
              ← back to home
            </Link>
          }
        />
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
    <div className="p-8 space-y-8 max-w-[1200px]">
      {/* Header — ticker + price + delta */}
      <PageHeader
        title={tk}
        subtitle={`${snap.name || ""} · ${snap.sector || "?"} · ${snap.is_holding ? "holding" : "watchlist"}`}
        crumbs={[{ label: "Home", href: "/" }, { label: tk }]}
        freshness={snap.price_date}
        actions={
          <div className="text-right">
            {snap.price !== null && (
              <div className="type-display tabular text-[var(--text-primary)]">
                {formatCurrency(snap.price, cur as any, 2)}
              </div>
            )}
            <div className="flex items-center gap-2 justify-end mt-1">
              <Pill variant={pillVariantFromMarket(snap.market)}>
                {snap.market.toUpperCase()}
              </Pill>
              {pnlPct !== null && (
                <span
                  className={`type-mono-sm ${
                    pnlPct >= 0
                      ? "text-[var(--gain)]"
                      : "text-[var(--loss)]"
                  }`}
                >
                  {pnlPct >= 0 ? "▲" : "▼"} {formatPercent(Math.abs(pnlPct), 1)} vs entry
                </span>
              )}
            </div>
          </div>
        }
      />

      <TickerActions ticker={tk} />

      {/* Council strip */}
      {council && (
        <Link
          href={`/council/${tk}`}
          className="card-purple p-4 flex items-center justify-between hover:border-[rgba(139,92,246,0.4)] transition-colors group"
        >
          <div className="flex items-center gap-4 flex-wrap">
            <span className="type-h3">⚖ council</span>
            <StancePill stance={council.entry.stance} confidence={council.entry.confidence} size="md" />
            <span className="type-mono-sm text-[var(--text-tertiary)]">
              {formatDate(council.entry.date, "relative")}
            </span>
            {council.entry.dissent_count > 0 && (
              <Pill variant="hold">
                {council.entry.dissent_count} dissent
              </Pill>
            )}
            {council.entry.flag_count > 0 && (
              <Pill variant="avoid">
                ⚑ {council.entry.flag_count}
              </Pill>
            )}
          </div>
          <span className="type-mono-sm text-[var(--text-secondary)] group-hover:text-[var(--accent-glow)] transition-colors">
            view storytelling →
          </span>
        </Link>
      )}

      {/* Price chart */}
      <Section label="Price · 365D">
        <div className="card p-5">
          <PriceChart ticker={tk} days={365} height={280} />
        </div>
      </Section>

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

      {/* Strategy breakdown */}
      {strategyRuns.length > 0 && (
        <Section
          label="Strategy breakdown"
          meta={
            topStrategy
              ? `top: ${topStrategy.engine} ${(topStrategy.score * 100).toFixed(0)}/100`
              : ""
          }
          action={
            <Link
              href={`/strategy/${tk}?market=${snap.market}`}
              className="type-mono-sm text-[var(--accent-glow)] hover:text-[var(--text-primary)] transition-colors"
            >
              full engine breakdown →
            </Link>
          }
        >
          <div className="card p-4">
            <div className="flex flex-wrap gap-2">
              {strategyRuns
                .filter((r) => r.market === snap.market)
                .map((r) => (
                  <span
                    key={r.engine}
                    className="flex items-center gap-2 type-mono-sm px-3 py-1.5 rounded border border-[var(--border-subtle)]"
                  >
                    <span className="text-[var(--text-tertiary)] capitalize">{r.engine}</span>
                    <span className="text-[var(--text-primary)]">
                      {(r.score * 100).toFixed(0)}
                    </span>
                    <Pill variant={pillVariantFromVerdict(r.verdict)}>{r.verdict}</Pill>
                  </span>
                ))}
            </div>
          </div>
        </Section>
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
          ? "border-[rgba(34,197,94,0.3)] bg-[rgba(34,197,94,0.04)]"
          : "border-[rgba(239,68,68,0.3)] bg-[rgba(239,68,68,0.04)]"
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
