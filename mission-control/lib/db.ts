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

export type DividendEvent = {
  market: "br" | "us";
  ticker: string;
  ex_date: string;
  amount: number;
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
          `SELECT ticker, ex_date, amount FROM dividends
           WHERE ex_date BETWEEN ? AND ?
           ORDER BY ex_date LIMIT 30`
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
