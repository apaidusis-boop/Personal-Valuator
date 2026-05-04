import Link from "next/link";
import Database from "better-sqlite3";
import { DB_BR, DB_US } from "@/lib/paths";
import { PriceChart } from "@/components/charts";
import { readCouncilStory } from "@/lib/vault";
import StancePill from "@/components/stance-pill";
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

  if (!snap) {
    return (
      <div className="p-8">
        <h1 className="text-2xl text-zinc-100">{tk}</h1>
        <p className="text-zinc-500 mt-2">Ticker não encontrado em nenhuma DB.</p>
        <Link href="/" className="text-cyan-300 underline text-sm mt-4 inline-block">
          ← back home
        </Link>
      </div>
    );
  }

  const cur = snap.market === "br" ? "R$" : "US$";
  const pnlPct =
    snap.price && snap.position
      ? ((snap.price / snap.position.entry - 1) * 100).toFixed(1)
      : null;
  const yoc =
    snap.position && snap.divs_12m
      ? ((snap.divs_12m / snap.position.entry) * 100).toFixed(2)
      : null;

  return (
    <div className="p-8 space-y-6">
      <header className="flex items-end justify-between border-b border-[#1f1f3d] pb-4">
        <div>
          <Link href="/" className="text-[10px] font-mono text-zinc-500 hover:text-cyan-300">
            ← Home
          </Link>
          <h1 className="text-3xl font-light text-zinc-100 mt-1">
            <span className="text-cyan-300 font-mono">{tk}</span>
            <span className="ml-3 text-base text-zinc-400">{snap.name}</span>
          </h1>
          <div className="text-xs font-mono text-zinc-500 mt-1">
            {snap.sector} · {snap.market.toUpperCase()} · {snap.is_holding ? "holding" : "watchlist"}
          </div>
        </div>
        <div className="text-right">
          {snap.price && (
            <div className="text-2xl font-light text-zinc-100 tabular">
              {cur}{snap.price.toFixed(2)}
            </div>
          )}
          {pnlPct && (
            <div className={`text-sm font-mono tabular ${
              parseFloat(pnlPct) >= 0 ? "text-green-400" : "text-red-400"
            }`}>
              {parseFloat(pnlPct) >= 0 ? "+" : ""}{pnlPct}%
            </div>
          )}
          <div className="text-[10px] font-mono text-zinc-500 mt-0.5">
            {snap.price_date}
          </div>
        </div>
      </header>

      <TickerActions ticker={tk} />

      {council && (
        <Link
          href={`/council/${tk}`}
          className="card-purple p-4 rounded-lg flex items-center justify-between hover:border-purple-400/60 transition-colors"
        >
          <div className="flex items-center gap-3">
            <span className="text-[10px] font-mono uppercase tracking-wider text-purple-300">
              ⚖ Council ({council.entry.date})
            </span>
            <StancePill stance={council.entry.stance} confidence={council.entry.confidence} size="md" />
            {(council.entry.dissent_count > 0 || council.entry.flag_count > 0) && (
              <span className="text-[10px] font-mono text-zinc-500">
                {council.entry.dissent_count > 0 && (
                  <span className="text-orange-300 mr-2">{council.entry.dissent_count} dissent</span>
                )}
                {council.entry.flag_count > 0 && (
                  <span className="text-red-300">{council.entry.flag_count} pre-pub</span>
                )}
              </span>
            )}
          </div>
          <span className="text-[10px] font-mono text-zinc-500">view storytelling →</span>
        </Link>
      )}

      {/* Price chart */}
      <section className="card p-5 rounded-lg">
        <PriceChart ticker={tk} days={365} height={280} />
      </section>

      {/* Stats grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {snap.position && (
          <div className="card-cyan p-4 rounded-lg">
            <h3 className="text-[10px] font-mono uppercase tracking-wider text-cyan-300 mb-2">
              Position
            </h3>
            <div className="text-2xl text-zinc-100 tabular">{snap.position.qty}</div>
            <div className="text-xs text-zinc-400 font-mono mt-1">
              @ {cur}{snap.position.entry.toFixed(2)} · since {snap.position.entry_date}
            </div>
            <div className="text-xs text-zinc-400 font-mono mt-1">
              cost: {cur}{(snap.position.qty * snap.position.entry).toLocaleString()}
            </div>
            {snap.price && (
              <div className="text-xs text-zinc-200 font-mono mt-1">
                mv: {cur}{(snap.position.qty * snap.price).toLocaleString()}
              </div>
            )}
            {yoc && (
              <div className="text-xs text-purple-300 font-mono mt-1">
                YoC: {yoc}% (12m divs {cur}{(snap.divs_12m! * snap.position.qty).toFixed(2)})
              </div>
            )}
          </div>
        )}

        {snap.fundamentals && (
          <div className="card-purple p-4 rounded-lg">
            <h3 className="text-[10px] font-mono uppercase tracking-wider text-purple-300 mb-2">
              Fundamentals
            </h3>
            <div className="grid grid-cols-2 gap-2 text-xs font-mono">
              <Stat label="P/E" v={snap.fundamentals.pe} />
              <Stat label="P/B" v={snap.fundamentals.pb} />
              <Stat label="DY" v={snap.fundamentals.dy} pct />
              <Stat label="ROE" v={snap.fundamentals.roe} pct />
              <Stat label="EPS" v={snap.fundamentals.eps} />
              <Stat label="BVPS" v={snap.fundamentals.bvps} />
            </div>
            <div className="text-[10px] text-zinc-500 mt-2 font-mono">
              {snap.fundamentals.period_end}
            </div>
          </div>
        )}

        {snap.score && (
          <div className={`p-4 rounded-lg border ${
            snap.score.passes
              ? "border-green-700/40 bg-green-900/10"
              : "border-red-700/40 bg-red-900/10"
          }`}>
            <h3 className="text-[10px] font-mono uppercase tracking-wider mb-2 text-zinc-400">
              Screen
            </h3>
            <div className={`text-3xl font-light tabular ${
              snap.score.passes ? "text-green-300" : "text-red-300"
            }`}>
              {snap.score.score.toFixed(2)}
            </div>
            <div className="text-xs font-mono mt-1">
              {snap.score.passes ? "✓ passes" : "✗ fails"}
            </div>
            <div className="text-[10px] text-zinc-500 mt-1 font-mono">
              {snap.score.run_date}
            </div>
          </div>
        )}
      </section>
    </div>
  );
}

function Stat({ label, v, pct }: { label: string; v: number | null; pct?: boolean }) {
  if (v == null) return (
    <div>
      <div className="text-[10px] text-zinc-500">{label}</div>
      <div className="text-zinc-600">—</div>
    </div>
  );
  const display = pct ? `${(v * 100).toFixed(1)}%` : v.toFixed(2);
  return (
    <div>
      <div className="text-[10px] text-zinc-500">{label}</div>
      <div className="text-zinc-200">{display}</div>
    </div>
  );
}
