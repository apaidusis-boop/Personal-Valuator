/**
 * Mission Control — Express API Server
 *
 * Expõe os dados das DBs SQLite e do vault como REST API para consumo por
 * frontends externos (Vite/React). A lógica de leitura é partilhada com o
 * Next.js via imports directos de ../lib/.
 *
 * PORT: 3001 (configurável via API_PORT env var)
 * CORS: localhost:5173 + localhost:5174 (Vite dev) + localhost:3000 (Next.js)
 *
 * Arranque: npm run api  (ou  npm run api:watch  para hot-reload)
 */

import express, { Request, Response } from "express";
import cors from "cors";
import Database from "better-sqlite3";
import { spawn } from "node:child_process";
import path from "node:path";
import fs from "node:fs";

// Partilha a lógica já testada no Next.js — sem duplicação.
import {
  listOpenActions,
  listAllPositions,
  upcomingDividends,
  listStrategyRuns,
  getRFTotal,
} from "../lib/db";
import {
  readBriefingMeta,
  listCouncilOutputs,
  readCouncilStory,
  summariseCouncil,
  loadLatestAllocation,
  listAutoMemory,
  listDailyEntries,
  readTopicScores,
} from "../lib/vault";
import { loadAgentStatus, loadPersonas, listDepartments } from "../lib/agents";
import { DB_BR, DB_US, II_ROOT } from "../lib/paths";

// ── Setup ─────────────────────────────────────────────────────────────────────

const app = express();
const PORT = Number(process.env.API_PORT || 3001);

app.use(
  cors({
    origin: [
      "http://localhost:5173",
      "http://localhost:5174",
      "http://localhost:3000",
      "http://127.0.0.1:5173",
    ],
  })
);
app.use(express.json());

// ── Helpers ───────────────────────────────────────────────────────────────────

function openRO(file: string) {
  return new Database(file, { readonly: true, fileMustExist: true });
}

function getCompany(ticker: string, market: "br" | "us") {
  const file = market === "br" ? DB_BR : DB_US;
  try {
    const db = openRO(file);
    const row = db
      .prepare("SELECT * FROM companies WHERE ticker = ?")
      .get(ticker.toUpperCase());
    db.close();
    return row ?? null;
  } catch {
    return null;
  }
}

function getLatestFundamentals(ticker: string, market: "br" | "us") {
  const file = market === "br" ? DB_BR : DB_US;
  try {
    const db = openRO(file);
    const row = db
      .prepare(
        "SELECT * FROM fundamentals WHERE ticker = ? ORDER BY period_end DESC LIMIT 1"
      )
      .get(ticker.toUpperCase());
    db.close();
    return row ?? null;
  } catch {
    return null;
  }
}

function getLatestScore(ticker: string, market: "br" | "us") {
  const file = market === "br" ? DB_BR : DB_US;
  try {
    const db = openRO(file);
    const row = db
      .prepare(
        "SELECT * FROM scores WHERE ticker = ? ORDER BY run_date DESC LIMIT 1"
      )
      .get(ticker.toUpperCase()) as any;
    db.close();
    if (!row) return null;
    return {
      ...row,
      details: row.details_json ? JSON.parse(row.details_json) : {},
    };
  } catch {
    return null;
  }
}

function getPosition(ticker: string, market: "br" | "us") {
  const file = market === "br" ? DB_BR : DB_US;
  try {
    const db = openRO(file);
    const row = db
      .prepare(
        "SELECT * FROM portfolio_positions WHERE ticker = ? AND active = 1"
      )
      .get(ticker.toUpperCase());
    db.close();
    return row ?? null;
  } catch {
    return null;
  }
}

function getPrices(ticker: string, market: "br" | "us", days = 365) {
  const file = market === "br" ? DB_BR : DB_US;
  try {
    const db = openRO(file);
    const cutoff = new Date(Date.now() - days * 86_400_000)
      .toISOString()
      .slice(0, 10);
    const rows = db
      .prepare(
        "SELECT date, close, volume FROM prices WHERE ticker = ? AND date >= ? ORDER BY date ASC"
      )
      .all(ticker.toUpperCase(), cutoff);
    db.close();
    return rows;
  } catch {
    return [];
  }
}

function getConvictionScores(market?: "br" | "us") {
  const out: any[] = [];
  for (const [m, file] of [
    ["br", DB_BR],
    ["us", DB_US],
  ] as const) {
    if (market && market !== m) continue;
    try {
      const db = openRO(file);
      const rows = db
        .prepare(
          "SELECT ticker, score, breakdown_json FROM conviction_scores ORDER BY score DESC"
        )
        .all() as any[];
      for (const r of rows) {
        out.push({
          market: m,
          ticker: r.ticker,
          score: r.score,
          breakdown: r.breakdown_json ? JSON.parse(r.breakdown_json) : {},
        });
      }
      db.close();
    } catch {
      /* table may not exist */
    }
  }
  return out;
}

function updateActionStatus(
  id: number,
  market: "br" | "us",
  status: "resolved" | "ignored"
) {
  const file = market === "br" ? DB_BR : DB_US;
  try {
    const db = new Database(file);
    db.prepare(
      "UPDATE watchlist_actions SET status = ? WHERE id = ?"
    ).run(status, id);
    db.close();
    return true;
  } catch {
    return false;
  }
}

// ── Health ────────────────────────────────────────────────────────────────────

app.get("/api/health", (_req: Request, res: Response) => {
  res.json({
    status: "ok",
    ts: new Date().toISOString(),
    ii_root: II_ROOT,
    dbs: {
      br: fs.existsSync(DB_BR),
      us: fs.existsSync(DB_US),
    },
  });
});

// ── Portfolio ─────────────────────────────────────────────────────────────────

app.get("/api/portfolio/positions", (_req: Request, res: Response) => {
  res.json(listAllPositions());
});

app.get("/api/portfolio/summary", (_req: Request, res: Response) => {
  const positions = listAllPositions();
  const rfTotal = getRFTotal();

  const br = positions.filter((p) => p.market === "br");
  const us = positions.filter((p) => p.market === "us");
  const brMV = br.reduce((s, p) => s + p.current_value, 0);
  const usMV = us.reduce((s, p) => s + p.current_value, 0);
  const brCost = br.reduce((s, p) => s + p.cost_basis, 0);
  const usCost = us.reduce((s, p) => s + p.cost_basis, 0);

  res.json({
    br: {
      market_value: brMV,
      market_value_plus_rf: brMV + rfTotal,
      cost: brCost,
      pnl_abs: brMV - brCost,
      pnl_pct: brCost > 0 ? ((brMV - brCost) / brCost) * 100 : 0,
      rf_total: rfTotal,
      n_positions: br.length,
    },
    us: {
      market_value: usMV,
      cost: usCost,
      pnl_abs: usMV - usCost,
      pnl_pct: usCost > 0 ? ((usMV - usCost) / usCost) * 100 : 0,
      n_positions: us.length,
    },
  });
});

// ── Actions ───────────────────────────────────────────────────────────────────

app.get("/api/actions", (req: Request, res: Response) => {
  const limit = Number(req.query.limit || 60);
  res.json(listOpenActions(limit));
});

app.patch("/api/actions/:id", (req: Request, res: Response) => {
  const id = Number(req.params.id);
  const market = req.query.market as "br" | "us";
  const { status } = req.body as { status?: "resolved" | "ignored" };

  if (!market || !["br", "us"].includes(market)) {
    return res.status(400).json({ error: "market must be br or us" });
  }
  if (!status || !["resolved", "ignored"].includes(status)) {
    return res
      .status(400)
      .json({ error: "status must be resolved or ignored" });
  }

  const ok = updateActionStatus(id, market, status);
  res.json({ ok });
});

// ── Council ───────────────────────────────────────────────────────────────────

app.get("/api/council", (req: Request, res: Response) => {
  const limit = Number(req.query.limit || 200);
  const market = req.query.market as "br" | "us" | undefined;
  let entries = listCouncilOutputs(limit);
  if (market) entries = entries.filter((e) => e.market === market);
  const summary = summariseCouncil(entries);
  res.json({ entries, summary });
});

app.get("/api/council/:ticker", (req: Request, res: Response) => {
  const story = readCouncilStory(req.params.ticker);
  if (!story) return res.status(404).json({ error: "not found" });
  res.json(story);
});

// ── Ticker detail ─────────────────────────────────────────────────────────────

app.get("/api/ticker/:ticker", (req: Request, res: Response) => {
  const ticker = req.params.ticker.toUpperCase();
  // Auto-detect market if not supplied: check both DBs
  let market = req.query.market as "br" | "us" | undefined;
  if (!market) {
    const brCompany = getCompany(ticker, "br");
    market = brCompany ? "br" : "us";
  }

  const company = getCompany(ticker, market);
  const fundamentals = getLatestFundamentals(ticker, market);
  const score = getLatestScore(ticker, market);
  const position = getPosition(ticker, market);
  const recentPrices = getPrices(ticker, market, 5);
  const lastPrice = (recentPrices as any[]).at(-1) ?? null;

  res.json({
    ticker,
    market,
    company,
    fundamentals,
    score,
    position,
    last_price: lastPrice,
  });
});

// ── Prices ────────────────────────────────────────────────────────────────────

app.get("/api/prices/:ticker", (req: Request, res: Response) => {
  const ticker = req.params.ticker.toUpperCase();
  const market = (req.query.market as "br" | "us") || "br";
  const days = Number(req.query.days || 365);
  res.json(getPrices(ticker, market, days));
});

// ── Dividends ─────────────────────────────────────────────────────────────────

app.get("/api/dividends", (req: Request, res: Response) => {
  const days = Number(req.query.days || 45);
  res.json(upcomingDividends(days));
});

// ── Briefing ──────────────────────────────────────────────────────────────────

app.get("/api/briefing", (_req: Request, res: Response) => {
  res.json(readBriefingMeta());
});

// ── Agents ────────────────────────────────────────────────────────────────────

app.get("/api/agents", (_req: Request, res: Response) => {
  res.json(loadAgentStatus());
});

app.get("/api/agents/personas", (_req: Request, res: Response) => {
  res.json(loadPersonas());
});

app.get("/api/agents/departments", (_req: Request, res: Response) => {
  res.json(listDepartments());
});

// ── Strategy ──────────────────────────────────────────────────────────────────

app.get("/api/strategy/:ticker", (req: Request, res: Response) => {
  const ticker = req.params.ticker.toUpperCase();
  const market = (req.query.market as "br" | "us") || null;
  res.json(listStrategyRuns(ticker, market));
});

// ── Allocation ────────────────────────────────────────────────────────────────

app.get("/api/allocation/:market", (req: Request, res: Response) => {
  const market = req.params.market as "br" | "us";
  if (!["br", "us"].includes(market)) {
    return res.status(400).json({ error: "market must be br or us" });
  }
  const data = loadLatestAllocation(market);
  if (!data) return res.status(404).json({ error: "no allocation data found" });
  res.json(data);
});

// ── Memory ────────────────────────────────────────────────────────────────────

app.get("/api/memory/auto", (req: Request, res: Response) => {
  const limit = Number(req.query.limit || 100);
  res.json(listAutoMemory(limit));
});

app.get("/api/memory/daily", (req: Request, res: Response) => {
  const limit = Number(req.query.limit || 60);
  res.json(listDailyEntries(limit));
});

// ── Topics ────────────────────────────────────────────────────────────────────

app.get("/api/topics", (_req: Request, res: Response) => {
  const data = readTopicScores();
  if (!data) return res.status(404).json({ error: "no topic scores" });
  res.json(data);
});

// ── Conviction scores ─────────────────────────────────────────────────────────

app.get("/api/conviction", (req: Request, res: Response) => {
  const market = req.query.market as "br" | "us" | undefined;
  res.json(getConvictionScores(market));
});

// ── Chat — spawn Fiel Escudeiro ───────────────────────────────────────────────

app.post("/api/chat", (req: Request, res: Response) => {
  const { message, chat_id = "mission-control" } =
    req.body as { message?: string; chat_id?: string };

  if (!message?.trim()) {
    return res.status(400).json({ error: "empty message" });
  }

  // Resolve Python — prefer .venv311 (Python 3.11 non-Store) to avoid
  // STATUS_DLL_INIT_FAILED (0xC0000142) from the Store Python AppContainer.
  const venv311 = path.join(II_ROOT, ".venv311", "Scripts", "python.exe");
  const venv = path.join(II_ROOT, ".venv", "Scripts", "python.exe");
  const pyPath = fs.existsSync(venv311)
    ? venv311
    : fs.existsSync(venv)
    ? venv
    : null;

  if (!pyPath) {
    return res.status(500).json({
      error: `Python venv not found. Expected: ${venv311}. Create with: py -3.11 -m venv .venv311`,
    });
  }

  // Strip WindowsApps from PATH to prevent Store Python stub hijacking.
  const systemRoot = process.env.SystemRoot || "C:\\Windows";
  const filteredPath = (process.env.PATH || "")
    .split(path.delimiter)
    .filter((p) => p && !/WindowsApps/i.test(p))
    .join(path.delimiter);
  const safePath = [
    path.join(systemRoot, "System32"),
    systemRoot,
    path.join(systemRoot, "System32", "Wbem"),
    filteredPath,
  ].join(path.delimiter);

  // Clean env — drop vars that corrupt DLL search in child Python process.
  const cleanEnv: Record<string, string> = {};
  for (const [k, v] of Object.entries(process.env)) {
    if (v === undefined) continue;
    if (["PYTHONHOME", "PYTHONPATH", "VIRTUAL_ENV"].includes(k)) continue;
    cleanEnv[k] = v;
  }

  const proc = spawn(
    pyPath,
    [
      "-X", "utf8",
      "-m", "agents.fiel_escudeiro",
      "--chat-id", chat_id.trim(),
      message.trim(),
    ],
    {
      cwd: II_ROOT,
      env: {
        ...cleanEnv,
        PATH: safePath,
        PYTHONIOENCODING: "utf-8",
        PYTHONUTF8: "1",
        FIEL_ESCUDEIRO_PERMISSION_MODE:
          process.env.FIEL_ESCUDEIRO_PERMISSION_MODE || "bypassPermissions",
        FIEL_ESCUDEIRO_MAX_BUDGET_USD:
          process.env.FIEL_ESCUDEIRO_MAX_BUDGET_USD || "3.00",
      } as unknown as NodeJS.ProcessEnv,
    }
  );

  let stdout = "";
  let stderr = "";

  // 10-min cap — matches the Python-side subprocess timeout.
  const timer = setTimeout(() => {
    proc.kill();
    if (!res.headersSent) {
      res.status(504).json({ error: "timeout (10 min)", stderr: stderr.slice(-500) });
    }
  }, 600_000);

  proc.stdout.on("data", (d) => (stdout += d.toString()));
  proc.stderr.on("data", (d) => (stderr += d.toString()));

  proc.on("close", (code) => {
    clearTimeout(timer);
    if (res.headersSent) return;

    const lines = stdout.split("\n");
    const headerIdx = lines.findIndex((l) => l.startsWith("[fiel-escudeiro]"));
    const answer =
      headerIdx >= 0
        ? lines.slice(headerIdx + 1).join("\n").trim()
        : stdout.trim();

    if (code === 0 && answer) {
      res.json({ reply: answer, chat_id });
    } else {
      res.status(500).json({
        error: `escudeiro exited ${code}`,
        stderr: stderr.slice(-2000),
        stdout_tail: stdout.slice(-500),
      });
    }
  });

  proc.on("error", (e) => {
    clearTimeout(timer);
    if (!res.headersSent) {
      res.status(500).json({ error: `spawn failed: ${e.message}` });
    }
  });
});

// ── Start ─────────────────────────────────────────────────────────────────────

app.listen(PORT, () => {
  console.log(`[api] Mission Control API — http://localhost:${PORT}`);
  console.log(`[api] II_ROOT = ${II_ROOT}`);
  console.log(`[api] DB_BR exists: ${fs.existsSync(DB_BR)}`);
  console.log(`[api] DB_US exists: ${fs.existsSync(DB_US)}`);
  console.log(`[api] Routes: health, portfolio, actions, council, ticker, prices, dividends, briefing, agents, strategy, allocation, memory, topics, conviction, chat`);
});
