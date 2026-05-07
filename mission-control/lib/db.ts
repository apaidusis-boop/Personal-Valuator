import Database from "better-sqlite3";
import { DB_BR, DB_US, DB_CHIEF } from "./paths";

// Read-only connections — we never write from the dashboard.
function openRO(file: string) {
  return new Database(file, { readonly: true, fileMustExist: true });
}

export type OpenAction = {
  id: number;
  market: "br" | "us";
  ticker: string;
  kind: string;
  description: string;
  created_at: string;
  status: string;
};

export function listOpenActions(limit = 60): OpenAction[] {
  const out: OpenAction[] = [];
  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = openRO(file);
      const rows = db
        .prepare(
          `SELECT id, ticker, kind, payload_json, created_at, status
           FROM watchlist_actions
           WHERE status = 'open'
           ORDER BY created_at DESC
           LIMIT ?`
        )
        .all(limit) as any[];
      for (const r of rows) {
        let desc: string = "";
        try {
          const p = r.payload_json ? JSON.parse(r.payload_json) : {};
          desc = p.description || p.threshold || JSON.stringify(p).slice(0, 90);
        } catch {
          desc = String(r.payload_json || "").slice(0, 90);
        }
        out.push({
          id: r.id,
          market,
          ticker: r.ticker,
          kind: r.kind,
          description: desc,
          created_at: r.created_at,
          status: r.status,
        });
      }
      db.close();
    } catch {
      /* table missing or DB locked — skip */
    }
  }
  return out.sort((a, b) => (b.created_at || "").localeCompare(a.created_at || ""));
}

export type PortfolioRow = {
  market: "br" | "us";
  ticker: string;
  name: string | null;
  sector: string | null;
  quantity: number;
  entry_price: number;
  price: number | null;
  cost: number;
  market_value: number | null;
  pnl_pct: number | null;
};

export function listPortfolio(): PortfolioRow[] {
  const out: PortfolioRow[] = [];
  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = openRO(file);
      const rows = db
        .prepare(
          `SELECT pp.ticker, pp.quantity, pp.entry_price,
            (SELECT close FROM prices WHERE ticker=pp.ticker
             ORDER BY date DESC LIMIT 1) AS px,
            c.name, c.sector
           FROM portfolio_positions pp
           LEFT JOIN companies c ON c.ticker = pp.ticker
           WHERE pp.active = 1
           ORDER BY pp.ticker`
        )
        .all() as any[];
      for (const r of rows) {
        const cost = r.quantity * r.entry_price;
        const mv = r.px ? r.quantity * r.px : null;
        const pnl = r.px && r.entry_price ? (r.px / r.entry_price - 1) * 100 : null;
        out.push({
          market,
          ticker: r.ticker,
          name: r.name,
          sector: r.sector,
          quantity: r.quantity,
          entry_price: r.entry_price,
          price: r.px,
          cost,
          market_value: mv,
          pnl_pct: pnl,
        });
      }
      db.close();
    } catch {
      /* skip */
    }
  }
  return out;
}

export type ChiefMessage = {
  id: number;
  chat_id: string;
  ts: string;
  role: string;
  content: string;
  tool_name: string | null;
};

export function listChiefMessages(chat_id?: string, limit = 50): ChiefMessage[] {
  try {
    const db = openRO(DB_CHIEF);
    let rows: any[];
    if (chat_id) {
      rows = db
        .prepare(
          `SELECT id, chat_id, ts, role, content, tool_name
           FROM messages WHERE chat_id = ? ORDER BY id DESC LIMIT ?`
        )
        .all(chat_id, limit) as any[];
    } else {
      rows = db
        .prepare(
          `SELECT id, chat_id, ts, role, content, tool_name
           FROM messages ORDER BY id DESC LIMIT ?`
        )
        .all(limit) as any[];
    }
    db.close();
    return rows.reverse() as ChiefMessage[];
  } catch {
    return [];
  }
}

export function listChatIds(): { chat_id: string; n_messages: number; last_ts: string }[] {
  try {
    const db = openRO(DB_CHIEF);
    const rows = db
      .prepare(
        `SELECT chat_id, COUNT(*) AS n, MAX(ts) AS last_ts
         FROM messages GROUP BY chat_id ORDER BY last_ts DESC`
      )
      .all() as any[];
    db.close();
    return rows.map((r) => ({ chat_id: r.chat_id, n_messages: r.n, last_ts: r.last_ts }));
  } catch {
    return [];
  }
}

// ============================================================
// Recent events — CVM fatos relevantes (BR) + SEC 8-K/10-K (US)
// ============================================================
export type FilingEvent = {
  id: number;
  market: "br" | "us";
  ticker: string;
  event_date: string;
  source: "cvm" | "sec" | string;
  kind: string;
  summary: string | null;
  url: string | null;
};

/** Pull the most recent N filings across both DBs, newest first. */
export function listRecentEvents(limit = 12): FilingEvent[] {
  const out: FilingEvent[] = [];
  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = openRO(file);
      const rows = db
        .prepare(
          `SELECT id, ticker, event_date, source, kind, summary, url
           FROM events
           ORDER BY event_date DESC, id DESC
           LIMIT ?`
        )
        .all(limit * 2) as any[];
      for (const r of rows) {
        out.push({
          id: r.id,
          market,
          ticker: r.ticker,
          event_date: r.event_date,
          source: r.source,
          kind: r.kind,
          summary: r.summary,
          url: r.url,
        });
      }
      db.close();
    } catch {
      /* table missing — skip */
    }
  }
  return out
    .sort((a, b) => (b.event_date || "").localeCompare(a.event_date || "") || b.id - a.id)
    .slice(0, limit);
}

export type DividendEvent = {
  market: "br" | "us";
  ticker: string;
  ex_date: string;
  pay_date: string | null;
  amount: number;
  currency: string | null;
};

export function upcomingDividends(days = 45): DividendEvent[] {
  const today = new Date().toISOString().slice(0, 10);
  const cutoff = new Date(Date.now() + days * 86400000).toISOString().slice(0, 10);
  const out: DividendEvent[] = [];
  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = openRO(file);
      const rows = db
        .prepare(
          `SELECT ticker, ex_date, pay_date, amount, currency FROM dividends
           WHERE ex_date BETWEEN ? AND ?
           ORDER BY ex_date LIMIT 60`
        )
        .all(today, cutoff) as any[];
      for (const r of rows) out.push({ market, ...r });
      db.close();
    } catch {
      /* skip */
    }
  }
  return out.sort((a, b) => a.ex_date.localeCompare(b.ex_date));
}

// ============================================================
// Upcoming filings — projected from earnings_calendar
// ============================================================
export type UpcomingFiling = {
  market: "br" | "us";
  ticker: string;
  earnings_date: string;
  projected_kind: string;     // "10-Q" / "10-K" / "ITR" / "DFP"
  is_holding: boolean;
  name: string | null;
};

/** Project the filing kind from market + earnings date. US: 10-K when month >= Q4 close
 *  (Jan-Mar) and the prior period was annual; otherwise 10-Q. BR: ITR (Q1-Q3) / DFP (Q4). */
function projectFilingKind(market: "br" | "us", isoDate: string): string {
  const month = parseInt(isoDate.slice(5, 7), 10);
  if (market === "us") {
    // US 10-K is filed within ~60d of fiscal year-end. Most calendar-FY filers report
    // Q4 in late Jan-early Mar (10-K) and Q1-Q3 quarterly (10-Q).
    if (month >= 1 && month <= 3) return "10-K";
    return "10-Q";
  }
  // BR ITRs are due 45d after Q1/Q2/Q3 end → reports land in May / Aug / Nov.
  // DFPs are due 90d after Q4 end → reports land in March-April.
  if (month >= 1 && month <= 4) return "DFP";
  return "ITR";
}

export function upcomingFilings(days = 90): UpcomingFiling[] {
  const today = new Date().toISOString().slice(0, 10);
  const cutoff = new Date(Date.now() + days * 86400000).toISOString().slice(0, 10);
  const out: UpcomingFiling[] = [];
  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = openRO(file);
      const rows = db
        .prepare(
          `SELECT e.ticker, e.earnings_date, c.is_holding, c.name
           FROM earnings_calendar e LEFT JOIN companies c ON e.ticker = c.ticker
           WHERE e.earnings_date BETWEEN ? AND ?
           ORDER BY e.earnings_date ASC`
        )
        .all(today, cutoff) as any[];
      for (const r of rows) {
        out.push({
          market,
          ticker: r.ticker,
          earnings_date: r.earnings_date,
          projected_kind: projectFilingKind(market, r.earnings_date),
          is_holding: !!r.is_holding,
          name: r.name,
        });
      }
      db.close();
    } catch {
      /* skip */
    }
  }
  return out.sort((a, b) => a.earnings_date.localeCompare(b.earnings_date));
}

// ============================================================
// Fair value — latest computed target price + upside %
// ============================================================
export type FairValueRow = {
  market: "br" | "us";
  ticker: string;
  method: string;
  fair_price: number;
  current_price: number;
  upside_pct: number;
  computed_at: string;
};

export function listFairValue(market?: "br" | "us"): FairValueRow[] {
  const out: FairValueRow[] = [];
  for (const [m, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    if (market && market !== m) continue;
    try {
      const db = openRO(file);
      const rows = db
        .prepare(
          `SELECT ticker, method, fair_price, current_price, upside_pct, computed_at
           FROM fair_value
           WHERE computed_at = (
             SELECT MAX(computed_at) FROM fair_value f2
             WHERE f2.ticker = fair_value.ticker AND f2.method = fair_value.method
           )
           ORDER BY upside_pct DESC`
        )
        .all() as any[];
      for (const r of rows) out.push({ market: m, ...r });
      db.close();
    } catch {
      /* table missing — skip */
    }
  }
  return out;
}

export function fairValueByTicker(ticker: string): FairValueRow | null {
  const t = ticker.toUpperCase();
  for (const [m, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = openRO(file);
      const r = db
        .prepare(
          `SELECT ticker, method, fair_price, current_price, upside_pct, computed_at
           FROM fair_value WHERE ticker = ?
           ORDER BY computed_at DESC LIMIT 1`
        )
        .get(t) as any;
      db.close();
      if (r) return { market: m, ...r };
    } catch {
      /* skip */
    }
  }
  return null;
}

// ============================================================
// Verdict deltas — what changed after a recent filing
// ============================================================
export type VerdictDelta = {
  market: "br" | "us";
  ticker: string;
  date: string;
  prior_action: string | null;
  new_action: string;
  prior_score: number | null;
  new_score: number | null;
  triggered_by: string;
  triggered_url: string | null;
};

export function recentVerdictDeltas(days = 7): VerdictDelta[] {
  const cutoff = new Date(Date.now() - days * 86400000).toISOString().slice(0, 10);
  const out: VerdictDelta[] = [];
  for (const [market, file] of [["br", DB_BR], ["us", DB_US]] as const) {
    try {
      const db = openRO(file);
      const rows = db
        .prepare(
          `SELECT ticker, date, prior_action, new_action, prior_score, new_score,
                  triggered_by, triggered_url
           FROM verdict_delta
           WHERE date >= ?
           ORDER BY date DESC, computed_at DESC`
        )
        .all(cutoff) as any[];
      for (const r of rows) out.push({ market, ...r });
      db.close();
    } catch {
      /* table missing — skip */
    }
  }
  return out;
}

// ============================================================
// Strategy runs (output of strategies/* engines, persisted by overnight backfill)
// ============================================================
export type StrategyRun = {
  market: "br" | "us";
  ticker: string;
  engine: string;
  score: number;
  verdict: string;
  weight_suggestion: number;
  rationale: any;
  run_id: string;
  run_ts: string;
};

export function listStrategyRuns(
  ticker: string | null = null,
  market: "br" | "us" | null = null,
  limit = 100
): StrategyRun[] {
  const out: StrategyRun[] = [];
  const tk = ticker ? ticker.toUpperCase() : null;
  for (const [m, file] of [
    ["br", DB_BR],
    ["us", DB_US],
  ] as const) {
    if (market && market !== m) continue;
    try {
      const db = openRO(file);
      const where: string[] = [];
      const params: any[] = [];
      if (tk) {
        where.push("ticker = ?");
        params.push(tk);
      }
      // Only the latest run_id per ticker × engine
      const sql = `
        SELECT ticker, engine, score, verdict, weight_suggestion,
               rationale_json, run_id, run_ts
        FROM strategy_runs s1
        WHERE run_ts = (
          SELECT MAX(run_ts) FROM strategy_runs s2
          WHERE s2.ticker = s1.ticker AND s2.engine = s1.engine
        )
        ${where.length ? "AND " + where.join(" AND ") : ""}
        ORDER BY ticker, engine
        LIMIT ?`;
      params.push(limit);
      const rows = db.prepare(sql).all(...params) as any[];
      db.close();
      for (const r of rows) {
        let rationale: any = {};
        try {
          rationale = r.rationale_json ? JSON.parse(r.rationale_json) : {};
        } catch {}
        out.push({
          market: m,
          ticker: r.ticker,
          engine: r.engine,
          score: r.score ?? 0,
          verdict: r.verdict ?? "N/A",
          weight_suggestion: r.weight_suggestion ?? 0,
          rationale,
          run_id: r.run_id,
          run_ts: r.run_ts,
        });
      }
    } catch {
      /* skip — strategy_runs table may not exist yet */
    }
  }
  return out;
}

export function strategyVerdictByTicker(
  market: "br" | "us" | null = null
): Record<string, Record<string, string>> {
  /** Returns { ticker: { engine: verdict } } — useful for quick badges. */
  const runs = listStrategyRuns(null, market, 1000);
  const out: Record<string, Record<string, string>> = {};
  for (const r of runs) {
    if (!out[r.ticker]) out[r.ticker] = {};
    out[r.ticker][r.engine] = r.verdict;
  }
  return out;
}

// ============================================================
// Unified portfolio — equities + FIIs + ETFs + fixed income
// ============================================================

export type AssetClass =
  | "equity"
  | "fii"
  | "etf"
  | "tesouro"
  | "debenture"
  | "cra"
  | "lca"
  | "fundo";

export type UnifiedPosition = {
  id: string;
  market: "br" | "us";
  asset_class: AssetClass;
  group_label: string;
  ticker: string | null;
  name: string;
  sector: string | null;
  quantity: number | null;
  entry_unit: number | null;
  current_unit: number | null;
  cost_basis: number;
  current_value: number;
  pnl_abs: number;
  pnl_pct: number | null;
  maturity_date: string | null;
  rate: string | null;
  weight_pct: number;
};

const FII_SECTORS = new Set([
  "Logística",
  "Shopping",
  "Papel (CRI)",
  "Híbrido",
  "Corporativo",
  "Tijolo",
  "Residencial",
]);

function classifyEquity(sector: string | null): "equity" | "fii" | "etf" {
  if (!sector) return "equity";
  if (sector.startsWith("ETF")) return "etf";
  if (FII_SECTORS.has(sector)) return "fii";
  return "equity";
}

const GROUP_LABELS: Record<string, string> = {
  equity: "Ações",
  fii: "FIIs",
  etf: "ETFs",
  us_equity: "US Equities",
  tesouro: "Tesouro Direto",
  debenture: "Debêntures",
  cra: "CRAs",
  lca: "LCAs",
  fundo: "Fundos",
};

// Display order for groups
const GROUP_ORDER: string[] = [
  "Ações",
  "US Equities",
  "FIIs",
  "ETFs",
  "Tesouro Direto",
  "Debêntures",
  "CRAs",
  "LCAs",
  "Fundos",
];

export function listAllPositions(): UnifiedPosition[] {
  const out: UnifiedPosition[] = [];

  // BR equities / FIIs / ETFs
  try {
    const db = openRO(DB_BR);
    const rows = db
      .prepare(
        `SELECT pp.ticker, pp.quantity, pp.entry_price,
          (SELECT close FROM prices WHERE ticker=pp.ticker ORDER BY date DESC LIMIT 1) AS px,
          c.name, c.sector
         FROM portfolio_positions pp
         LEFT JOIN companies c ON c.ticker = pp.ticker
         WHERE pp.active = 1
         ORDER BY pp.ticker`
      )
      .all() as any[];
    for (const r of rows) {
      const ac = classifyEquity(r.sector);
      const cost = r.quantity * r.entry_price;
      const mv = r.px != null ? r.quantity * r.px : cost;
      out.push({
        id: `br_${r.ticker}`,
        market: "br",
        asset_class: ac,
        group_label: GROUP_LABELS[ac],
        ticker: r.ticker,
        name: r.name || r.ticker,
        sector: r.sector,
        quantity: r.quantity,
        entry_unit: r.entry_price,
        current_unit: r.px ?? null,
        cost_basis: cost,
        current_value: mv,
        pnl_abs: mv - cost,
        pnl_pct: r.px != null ? ((r.px / r.entry_price) - 1) * 100 : null,
        maturity_date: null,
        rate: null,
        weight_pct: 0,
      });
    }
    db.close();
  } catch { /* skip */ }

  // US equities
  try {
    const db = openRO(DB_US);
    const rows = db
      .prepare(
        `SELECT pp.ticker, pp.quantity, pp.entry_price,
          (SELECT close FROM prices WHERE ticker=pp.ticker ORDER BY date DESC LIMIT 1) AS px,
          c.name, c.sector
         FROM portfolio_positions pp
         LEFT JOIN companies c ON c.ticker = pp.ticker
         WHERE pp.active = 1
         ORDER BY pp.ticker`
      )
      .all() as any[];
    for (const r of rows) {
      const cost = r.quantity * r.entry_price;
      const mv = r.px != null ? r.quantity * r.px : cost;
      out.push({
        id: `us_${r.ticker}`,
        market: "us",
        asset_class: "equity",
        group_label: "US Equities",
        ticker: r.ticker,
        name: r.name || r.ticker,
        sector: r.sector,
        quantity: r.quantity,
        entry_unit: r.entry_price,
        current_unit: r.px ?? null,
        cost_basis: cost,
        current_value: mv,
        pnl_abs: mv - cost,
        pnl_pct: r.px != null ? ((r.px / r.entry_price) - 1) * 100 : null,
        maturity_date: null,
        rate: null,
        weight_pct: 0,
      });
    }
    db.close();
  } catch { /* skip */ }

  // BR fixed income
  try {
    const db = openRO(DB_BR);
    const rows = db
      .prepare(
        `SELECT id, name, kind, indexador, spread_taxa, cdi_pct,
                entry_date, maturity_date, quantity, entry_unit_price,
                valor_aplicado, valor_atual
         FROM fixed_income_positions
         ORDER BY kind, name`
      )
      .all() as any[];
    for (const r of rows) {
      let rate: string | null = null;
      if (r.cdi_pct) {
        rate = `${(r.cdi_pct * 100).toFixed(0)}% CDI`;
      } else if (r.spread_taxa && r.indexador) {
        rate = `${r.indexador} +${(r.spread_taxa * 100).toFixed(2)}%`;
      } else if (r.indexador) {
        rate = r.indexador;
      }
      const entry_unit =
        r.entry_unit_price ??
        (r.quantity ? r.valor_aplicado / r.quantity : null);
      const current_unit = r.quantity ? r.valor_atual / r.quantity : null;
      out.push({
        id: `rf_${r.id}`,
        market: "br",
        asset_class: r.kind as AssetClass,
        group_label: GROUP_LABELS[r.kind] ?? r.kind,
        ticker: null,
        name: r.name,
        sector: null,
        quantity: r.quantity ?? null,
        entry_unit,
        current_unit,
        cost_basis: r.valor_aplicado,
        current_value: r.valor_atual,
        pnl_abs: r.valor_atual - r.valor_aplicado,
        pnl_pct: r.valor_aplicado
          ? ((r.valor_atual / r.valor_aplicado) - 1) * 100
          : null,
        maturity_date: r.maturity_date ?? null,
        rate,
        weight_pct: 0,
      });
    }
    db.close();
  } catch { /* skip */ }

  // Compute weight_pct within each market separately (BRL vs USD can't sum)
  const brTotal = out
    .filter((p) => p.market === "br")
    .reduce((s, p) => s + p.current_value, 0);
  const usTotal = out
    .filter((p) => p.market === "us")
    .reduce((s, p) => s + p.current_value, 0);
  for (const p of out) {
    const total = p.market === "br" ? brTotal : usTotal;
    p.weight_pct = total > 0 ? (p.current_value / total) * 100 : 0;
  }

  // Sort by group display order, then by current_value desc within group
  out.sort((a, b) => {
    const oa = GROUP_ORDER.indexOf(a.group_label);
    const ob = GROUP_ORDER.indexOf(b.group_label);
    if (oa !== ob) return (oa < 0 ? 99 : oa) - (ob < 0 ? 99 : ob);
    return b.current_value - a.current_value;
  });

  return out;
}

export function getRFTotal(): number {
  try {
    const db = openRO(DB_BR);
    const r = db
      .prepare(
        "SELECT COALESCE(SUM(valor_atual), 0) AS total FROM fixed_income_positions"
      )
      .get() as any;
    db.close();
    return r?.total ?? 0;
  } catch {
    return 0;
  }
}
