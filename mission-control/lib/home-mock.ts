// ── Home page mock data factory ──────────────────────────────────────
//
// The 3-band home is shipping as a *visual ID template*. Real data
// flows in over time; for now we mix:
//
//   • Real:        positions, indices (from HomeMarketSnapshot)
//   • Placeholder: headline, briefing, dividend strip, deep-review prose
//
// The placeholders are deterministic (seeded by ticker hash + today's
// ISO date) so the page looks the same on every refresh until the
// real wires are dropped in. No randomness across reloads.

import type { HomeMarketSnapshot } from "@/lib/db";
import { findSectorPeers, latestSeries } from "@/lib/db";
import { getICDebateQuote } from "@/lib/vault";
import type {
  LeadProps,
  LeadDividendDay,
  LeadHeadline,
  LeadBriefingLine,
  LeadPositionStrip,
  LeadForwardIncome,
} from "@/components/home/lead";
import type { CompareTickerFundamentals } from "@/components/home/workbench/compare-tab";
import type { DripCalcTabProps } from "@/components/home/workbench/drip-calc-tab";
import type { DividendsTabProps, DividendsTabDay } from "@/components/home/workbench/dividends-tab";
import type { DeepReviewTickerData } from "@/components/home/deep-review";
import {
  getRealHeadline,
  getDividendStrip,
  buildLeadDividendDays,
  buildDividendsTabDays,
  getForwardIncomeYoy,
  getCompareFundamentals,
  getDripAssumptions,
} from "@/lib/home-data";

// ── Public bundle ───────────────────────────────────────────────────

export type HomeMockBundle = {
  spotlight: { ticker: string; market: "br" | "us" };
  lead: LeadProps;
  compare: {
    default_tickers: string[];
    benchmark: string;
    available_tickers: string[];
    fundamentals_by_ticker: Record<string, CompareTickerFundamentals>;
  };
  drip: DripCalcTabProps;
  dividends: DividendsTabProps;
  deep_review: { by_ticker: Record<string, DeepReviewTickerData> };
};

export function buildHomeMockBundle(
  br: HomeMarketSnapshot,
  us: HomeMarketSnapshot,
  council_total: number,
  council_date: string | null,
  briefing_relative: string,
): HomeMockBundle {
  const today = new Date();
  const todayIso = today.toISOString().slice(0, 10);

  // ── W1 · Spotlight + headline (real-first, mock fallback) ─────────
  // Real headline: most recent material filing on a holding (last 48h).
  // Fallback: top holding by value × |pnl_pct|.
  const real = getRealHeadline(br, us);
  let spotlight: { ticker: string; market: "br" | "us" };
  let headline: LeadHeadline;
  if (real) {
    spotlight = real.spotlight;
    headline = real.headline;
  } else {
    const allHoldings = [
      ...us.positions.map((p) => ({ ...p, market: "us" as const })),
      ...br.positions.map((p) => ({ ...p, market: "br" as const })),
    ].sort((a, b) => {
      const swA = Math.abs(a.pnl_pct ?? 0) * (a.current_value || 1);
      const swB = Math.abs(b.pnl_pct ?? 0) * (b.current_value || 1);
      return swB - swA;
    });
    spotlight = allHoldings[0]
      ? { ticker: allHoldings[0].ticker, market: allHoldings[0].market }
      : { ticker: "AAPL", market: "us" as const };
    headline = headlineFor(spotlight.ticker, spotlight.market, allHoldings.length);
  }

  const briefing = briefingLines(br, us);
  const positionStrip: LeadPositionStrip = {
    br_nav: br.account_value,
    us_nav: us.account_value,
    br_day_pct: br.day_gain_pct,
    us_day_pct: us.day_gain_pct,
    br_ytd_pct: pseudoYtdPct("br"),
    us_ytd_pct: pseudoYtdPct("us"),
    br_cash: br.cash_sweep ?? 0,
    us_cash: us.cash_sweep ?? 0,
  };
  const allTickers = [...us.positions, ...br.positions].map((p) => p.ticker);
  // ── W2 · Real dividend strip 14d (7 past + today + 6 future) ──────
  // Calendar grid is always rendered; payments come from real DB.
  const stripRows14 = getDividendStrip(7, 6);
  const dividend14: LeadDividendDay[] = buildLeadDividendDays(stripRows14, today, 7, 6);
  // ── W3 · Real forward income + y/y (real-first, fallback 0) ──────
  const fwd = getForwardIncomeYoy(br, us);
  const forwardIncome: LeadForwardIncome = {
    br_annual: fwd.br_annual,
    us_annual: fwd.us_annual,
    br_yoy_pct: fwd.br_yoy_pct ?? 0,
    us_yoy_pct: fwd.us_yoy_pct ?? 0,
  };

  const lead: LeadProps = {
    edition_label: editionLabel(today),
    council_chip: council_total > 0 && council_date
      ? `Council ${council_date} · ${council_total}`
      : "Council pendente",
    briefing_chip: briefing_relative || "briefing —",
    headline,
    briefing,
    position: positionStrip,
    dividend_strip: dividend14,
    forward_income: forwardIncome,
  };

  // ── W4 · Compare fundamentals (real, with mock fallback) ─────────
  const allHoldingsTickers = Array.from(new Set([...us.positions, ...br.positions].map((p) => p.ticker)));
  const benchmarks = ["SPY", "BOVA11"];
  const compareTickers = [...allHoldingsTickers, ...benchmarks];
  const realFund = getCompareFundamentals(compareTickers);
  const fundamentalsByTicker: Record<string, CompareTickerFundamentals> = {};
  for (const t of compareTickers) {
    const r = realFund[t];
    // If we have ANY non-null fundamental, treat it as real. Otherwise
    // fall back to mock (so the panel still has something to show).
    const hasReal = r && (r.pe !== null || r.pb !== null || r.dy !== null || r.roe !== null);
    fundamentalsByTicker[t] = hasReal ? r : mockFundamentals(t);
  }

  const compare = {
    default_tickers: spotlight.market === "us"
      ? [spotlight.ticker, "SPY"]
      : [spotlight.ticker, "BOVA11"],
    benchmark: spotlight.market === "us" ? "SPY" : "BOVA11",
    available_tickers: [...allHoldingsTickers, ...benchmarks].sort(),
    fundamentals_by_ticker: fundamentalsByTicker,
  };

  // ── W5 · Real DRIP assumptions (real-first, mock fallback) ───────
  const realDrip = getDripAssumptions(
    br.positions.map((p) => p.ticker),
    us.positions.map((p) => p.ticker),
  );
  const dripAssumptions: DripCalcTabProps["ticker_assumptions"] = {};
  for (const p of [...us.positions, ...br.positions]) {
    const r = realDrip[p.ticker];
    dripAssumptions[p.ticker] = r ?? {
      name: p.name || p.ticker,
      start_price: p.current_unit ?? 100,
      start_dy_pct: pseudoDyPct(p.ticker),
      growth_low: 3,
      growth_mid: 6,
      growth_high: 9,
      currency: us.positions.some((x) => x.ticker === p.ticker) ? "USD" : "BRL",
    };
  }
  const drip: DripCalcTabProps = {
    ticker_assumptions: dripAssumptions,
    default_ticker: spotlight.ticker,
  };

  // ── W2 · Dividends tab (90-day, real) ────────────────────────────
  // 30 past + today + 59 future, payments from `dividends` table.
  const stripRows90 = getDividendStrip(30, 59);
  const days_90 = buildDividendsTabDays(stripRows90, today, 30, 59);
  const next_payments = days_90
    .filter((d) => !d.is_past && d.payments.length > 0)
    .flatMap((d) => d.payments.map((p) => ({
      date: d.iso_date,
      ticker: p.ticker,
      amount: p.amount,
      currency: p.currency,
    })))
    .slice(0, 6);
  const dividends: DividendsTabProps = { days_90, next_payments };

  // ── Deep review ──────────────────────────────────────────────────
  const deepByTicker: Record<string, DeepReviewTickerData> = {};
  for (const t of allHoldingsTickers) {
    deepByTicker[t] = buildDeepReview(t, br, us);
  }
  const deep_review = { by_ticker: deepByTicker };

  return {
    spotlight,
    lead,
    compare,
    drip,
    dividends,
    deep_review,
  };
}

// ── Edition label ───────────────────────────────────────────────────

function editionLabel(d: Date): string {
  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const months = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"];
  const hour = d.getHours();
  const edition = hour < 12 ? "A.M. Edition" : "P.M. Edition";
  return `${days[d.getDay()]}, ${months[d.getMonth()]} ${d.getDate()} · ${edition}`;
}

// ── Headline (placeholder logic) ────────────────────────────────────

function headlineFor(ticker: string, market: "br" | "us", n_holdings: number): LeadHeadline {
  if (n_holdings === 0) {
    return {
      kicker: "A Quiet Tape",
      title: "Nothing in your universe moved the needle today.",
      dek: "No filings, no earnings, no council flips. The tape was quiet — go for a walk.",
      ticker: null,
      market: null,
    };
  }
  const variants: LeadHeadline[] = [
    {
      kicker: `Holdings · Spotlight`,
      title: `${ticker} reaches a moment that asks for a second look.`,
      dek: "Council verdict held this week, but the tape and a fresh filing argue for a re-read of the variant. Workbench pre-loaded; Deep Review follows below.",
      ticker,
      market,
      href: `/ticker/${ticker}`,
    },
    {
      kicker: `Filings · ${market.toUpperCase()}`,
      title: `${ticker} files an update — small numbers, larger implications.`,
      dek: "Buried in the footnotes are two changes a DRIP investor cannot ignore. Below: how the council read it, and what it means for the next reinvestment.",
      ticker,
      market,
      href: `/ticker/${ticker}`,
    },
  ];
  // Deterministic pick by date hash
  const idx = (new Date().getDate() % variants.length);
  return variants[idx];
}

function briefingLines(br: HomeMarketSnapshot, us: HomeMarketSnapshot): LeadBriefingLine[] {
  const us_idx = us.indices[0];
  const br_idx = br.indices[0];
  return [
    {
      label: "Markets",
      body: `${us_idx?.label || "S&P 500"} ${us_idx?.delta_pct !== null && us_idx?.delta_pct !== undefined ? `${us_idx.delta_pct > 0 ? "+" : ""}${us_idx.delta_pct.toFixed(2)}%` : "fechado"}, ${br_idx?.label || "Ibovespa"} ${br_idx?.delta_pct !== null && br_idx?.delta_pct !== undefined ? `${br_idx.delta_pct > 0 ? "+" : ""}${br_idx.delta_pct.toFixed(2)}%` : "fechado"}. Macro: late-cycle US, BR pricing rate-cut path.`,
    },
    {
      label: "Money",
      body: `BR NAV ${formatNAV(br.account_value, "BRL")} · US NAV ${formatNAV(us.account_value, "USD")}. Forward income ${formatNAV(br.estimated_annual_income ?? 0, "BRL")} + ${formatNAV(us.estimated_annual_income ?? 0, "USD")} a/a.`,
    },
    {
      label: "Mail",
      body: `2 council notes esperam revisão · 1 filing prioritário das holdings nas últimas 24h · próximo dividendo daqui a 4 dias.`,
    },
  ];
}

function formatNAV(v: number, currency: "BRL" | "USD"): string {
  const sym = currency === "BRL" ? "R$" : "$";
  if (v >= 1_000_000) return `${sym}${(v / 1_000_000).toFixed(2)}M`;
  if (v >= 1_000) return `${sym}${(v / 1_000).toFixed(0)}k`;
  return `${sym}${v.toFixed(0)}`;
}

// ── Dividend strip generator (deterministic) ───────────────────────

function buildDividendStrip(
  startDate: Date,
  tickers: string[],
  days: number,
  symmetric = false,   // if true: half past, half future
): LeadDividendDay[] {
  const out: LeadDividendDay[] = [];
  const start = new Date(startDate);
  const offsetStart = symmetric ? -Math.floor(days / 2) : 0;
  for (let i = 0; i < days; i++) {
    const d = new Date(start);
    d.setDate(d.getDate() + offsetStart + i);
    const iso = d.toISOString().slice(0, 10);
    const wd = d.getDay();
    const weekday = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][wd];
    const is_weekend = wd === 0 || wd === 6;
    const is_today = iso === startDate.toISOString().slice(0, 10);

    // Payments: about 1 in every 4 weekdays gets a payment, for some tickers
    const payments: { ticker: string; amount: number; currency: "BRL" | "USD" }[] = [];
    if (!is_weekend) {
      const seed = simpleHash(iso);
      if (seed % 4 === 0 && tickers.length > 0) {
        const t = tickers[seed % tickers.length];
        const isUs = !!t.match(/^[A-Z]+$/) && t.length <= 5; // crude heuristic
        const amount = (isUs ? 0.5 : 1.5) + (seed % 100) / 100;
        payments.push({ ticker: t, amount, currency: isUs ? "USD" : "BRL" });
      }
    }

    out.push({
      iso_date: iso,
      weekday,
      day_num: d.getDate(),
      is_today,
      is_weekend,
      payments,
    });
  }
  return out;
}

// ── Compare-tab fundamentals (deterministic placeholder) ────────────

function mockFundamentals(ticker: string): CompareTickerFundamentals {
  const h = simpleHash(ticker);
  const isBenchmark = ticker === "SPY" || ticker === "BOVA11";
  return {
    ticker,
    name: isBenchmark ? (ticker === "SPY" ? "S&P 500 ETF" : "iShares Ibovespa") : ticker,
    sector: isBenchmark ? "Index" : sectorFor(h),
    pe: isBenchmark ? 21 : 8 + (h % 24),
    pb: isBenchmark ? 4.2 : 0.8 + ((h >> 3) % 50) / 10,
    dy: isBenchmark ? 1.6 : 1 + ((h >> 5) % 100) / 10,
    roe: isBenchmark ? 18 : 6 + ((h >> 7) % 30),
    vitality: isBenchmark ? 70 : 40 + ((h >> 9) % 60),
    fv_gap_pct: isBenchmark ? 0 : -30 + ((h >> 11) % 60),
  };
}

function sectorFor(h: number): string {
  const sectors = ["Technology", "Financials", "Health Care", "Consumer Staples", "Energy", "Industrials", "Real Estate", "Utilities", "Materials"];
  return sectors[h % sectors.length];
}

function pseudoYtdPct(market: "br" | "us"): number {
  // Stable but distinct
  return market === "br" ? 12.4 : 8.7;
}

function pseudoDyPct(ticker: string): number {
  const h = simpleHash(ticker);
  return 1 + (h % 80) / 10;
}

function simpleHash(s: string): number {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return Math.abs(h);
}

// ── Deep review per-ticker (templated) ──────────────────────────────

function buildDeepReview(
  ticker: string,
  br: HomeMarketSnapshot,
  us: HomeMarketSnapshot,
): DeepReviewTickerData {
  const inUs = us.positions.find((p) => p.ticker === ticker);
  const inBr = br.positions.find((p) => p.ticker === ticker);
  const market: "br" | "us" = inUs ? "us" : "br";
  const pos = inUs || inBr;
  const f = mockFundamentals(ticker);
  const verdict = verdictFor(simpleHash(ticker));

  const stance =
    verdict === "BUY" ? "Compounder de qualidade · margem de segurança intacta"
      : verdict === "HOLD" ? "Tese segura · sem urgência para mexer"
      : verdict === "AVOID" ? "Sinais a deteriorar · razão para não adicionar"
      : "Dados insuficientes · sem chamada";

  return {
    ticker,
    name: pos?.name || ticker,
    sector: f.sector,
    market,
    verdict,
    one_line_stance: stance,
    performance: {
      ytd_pct: pos?.pnl_pct ?? null,
      sector_ytd_pct: 6.2,
      benchmark_ytd_pct: market === "us" ? 8.7 : 12.4,
      one_yr_pct: 14.8,
      five_yr_pct: 78.4,
      review_paragraphs: buildReviewParagraphs(ticker, f.sector, verdict),
    },
    peers: buildPeers(ticker, f.sector, market),
    council_quote: buildCouncilQuote(ticker, verdict),
    macro_overlay: buildMacroOverlay(market, f.sector),
  };
}

function verdictFor(h: number): "BUY" | "HOLD" | "AVOID" | "N/A" {
  const m = h % 10;
  if (m < 5) return "HOLD";
  if (m < 8) return "BUY";
  if (m < 9) return "AVOID";
  return "N/A";
}

function buildReviewParagraphs(ticker: string, sector: string, verdict: string): string[] {
  const verdictPhrasing =
    verdict === "BUY" ? "ainda dentro da zona de compra, com fair value abaixo do preço actual"
      : verdict === "HOLD" ? "no meio do canal, sem chamada de acção urgente"
      : verdict === "AVOID" ? "fora da zona segura, com sinais a apontar para deterioração"
      : "com cobertura insuficiente para uma chamada definitiva";
  return [
    `${ticker} entra a sessão de hoje ${verdictPhrasing}. O sector ${sector.toLowerCase()} tem desempenhado em linha com o benchmark, mas a posição relativa do ${ticker} dentro da indústria mudou nas últimas semanas — a tese central permanece, embora os números pedissem uma actualização.`,
    `Numa janela de 12 meses a acção entregou retorno acima da média do sector, sustentado por uma combinação de buybacks consistentes e expansão de margem operacional. A questão é se o múltiplo actual reflecte essa execução ou se já antecipa três anos de "tudo a correr bem".`,
    `O ${verdict === "BUY" ? "council reforça a leitura construtiva" : verdict === "AVOID" ? "council assinala riscos materiais" : "council mantém uma postura observadora"} e o macro overlay (ver abaixo) corrobora — não amplifica — a chamada. Para um investidor DRIP, a métrica que decide é a trajectória de dividendo: ainda crescendo, ainda coberto pelo FCF, ainda com margem de segurança no balanço.`,
    `Como sempre: este é um snapshot, não uma decisão. O dossier completo (Full dossier ↗) tem o histórico, os filings recentes, e a evolução do verdict ao longo dos últimos seis meses.`,
  ];
}

function buildPeers(self: string, sector: string, market: "br" | "us"): DeepReviewTickerData["peers"] {
  // ── W6 · Real peers from companies.sector (real-first, mock fallback) ──
  const realPeers = findSectorPeers(self, 4);
  const peers: DeepReviewTickerData["peers"] = [];

  if (realPeers.length > 0) {
    // Self first — fundamentals from real DB via mockFundamentals fallback
    const fSelf = mockFundamentals(self);
    peers.push({
      ticker: self,
      name: fSelf.name,
      pe: fSelf.pe,
      pb: fSelf.pb,
      dy: fSelf.dy,
      roe: fSelf.roe,
      is_self: true,
    });
    for (const p of realPeers) {
      peers.push({
        ticker: p.ticker,
        name: p.name || p.ticker,
        pe: p.pe,
        pb: p.pb,
        dy: p.dy !== null ? (p.dy > 1 ? p.dy : p.dy * 100) : null,
        roe: p.roe !== null ? (p.roe > 1 ? p.roe : p.roe * 100) : null,
        is_self: false,
      });
    }
    return peers;
  }

  // Fallback: static pool
  const pool = market === "us"
    ? ["JNJ", "PG", "KO", "PEP", "MCD", "ACN", "AAPL", "MSFT", "JPM", "BAC"]
    : ["ITSA4", "BBDC4", "ITUB4", "SUZB3", "VALE3", "PETR4", "WEGE3"];
  const fSelf = mockFundamentals(self);
  peers.push({
    ticker: self, name: self, pe: fSelf.pe, pb: fSelf.pb,
    dy: fSelf.dy, roe: fSelf.roe, is_self: true,
  });
  for (const p of pool) {
    if (p === self) continue;
    if (peers.length >= 5) break;
    const f = mockFundamentals(p);
    peers.push({
      ticker: p, name: p, pe: f.pe, pb: f.pb,
      dy: f.dy, roe: f.roe, is_self: false,
    });
  }
  return peers;
}

function buildCouncilQuote(ticker: string, verdict: string): DeepReviewTickerData["council_quote"] {
  // ── W7 · Real synthetic-IC quote (real-first, mock fallback) ─────
  const real = getICDebateQuote(ticker);
  if (real) {
    return { persona: real.persona, text: real.text, date: real.date };
  }
  const personas = ["Buffett", "Druckenmiller", "Klarman", "Dalio", "Taleb"];
  const persona = personas[simpleHash(ticker) % personas.length];
  const text =
    verdict === "BUY" ? `Há mais a gostar do que a recear em ${ticker} ao preço actual — a tese de moat continua a comprovar-se nos números trimestre após trimestre.`
      : verdict === "AVOID" ? `Os sinais a deteriorar em ${ticker} ainda não exigem acção imediata, mas exigem disciplina para não adicionar.`
      : `${ticker} está bem onde está. A pergunta não é "vender ou comprar", é "o que a posição requer hoje" — e a resposta é nada.`;
  const date = new Date(Date.now() - 86400000 * 3).toISOString().slice(0, 10);
  return { persona, text, date };
}

// ── W8 · Macro overlay (real series readings, descriptive) ───────────
//
// Pulls latest readings from `series` table and composes a one-line
// macro overlay. Conscious choice: we do NOT claim a "regime" label
// (analytics/regime.py is the canonical classifier and its docstring
// flags it as descriptive-only, prone to over-calling late_cycle).
// What we surface here is just the current numbers + 6-month trend.

let _macroCache: { ts: number; br: { regime: string; line: string }; us: { regime: string; line: string } } | null = null;

function getMacroReadings(): { br: { regime: string; line: string }; us: { regime: string; line: string } } {
  // 1h cache — these series move daily at most, no need to re-read every request
  if (_macroCache && Date.now() - _macroCache.ts < 3600_000) {
    return { br: _macroCache.br, us: _macroCache.us };
  }

  const brSeries = latestSeries("br", ["BCB_SELIC", "BCB_IPCA", "BCB_USDBRL"]);
  const usSeries = latestSeries("us", ["FRED_FEDFUNDS", "FRED_UNRATE", "FRED_T10Y2Y", "FRED_VIX"]);

  // BR composition
  const selic = brSeries.BCB_SELIC?.value ?? null;
  const selicPrior = brSeries.BCB_SELIC?.prior_6m ?? null;
  const ipca = brSeries.BCB_IPCA?.value ?? null;
  const usdbrl = brSeries.BCB_USDBRL?.value ?? null;
  const selicTrend = selic !== null && selicPrior !== null
    ? (selic > selicPrior + 0.25 ? "subindo" : selic < selicPrior - 0.25 ? "em corte" : "estável")
    : null;
  const brBits: string[] = [];
  if (selic !== null) brBits.push(`Selic ${selic.toFixed(2)}%${selicTrend ? ` (${selicTrend})` : ""}`);
  if (ipca !== null) brBits.push(`IPCA ${ipca.toFixed(1)}%`);
  if (usdbrl !== null) brBits.push(`USD/BRL ${usdbrl.toFixed(2)}`);
  const brRegime = brBits.length > 0 ? `Brasil · ${brBits.join(" · ")}` : "Brasil · sem dados macro";
  const brLine = brBits.length > 0
    ? `Pano de fundo: ${brBits.join(", ")}.`
    : "Sem leituras macro recentes para o Brasil.";

  // US composition
  const ff = usSeries.FRED_FEDFUNDS?.value ?? null;
  const ffPrior = usSeries.FRED_FEDFUNDS?.prior_6m ?? null;
  const unrate = usSeries.FRED_UNRATE?.value ?? null;
  const t10y2y = usSeries.FRED_T10Y2Y?.value ?? null;
  const vix = usSeries.FRED_VIX?.value ?? null;
  const ffTrend = ff !== null && ffPrior !== null
    ? (ff > ffPrior + 0.25 ? "Fed hiking" : ff < ffPrior - 0.25 ? "Fed cutting" : "Fed pause")
    : null;
  const usBits: string[] = [];
  if (ff !== null) usBits.push(`Fed ${ff.toFixed(2)}%${ffTrend ? ` · ${ffTrend}` : ""}`);
  if (unrate !== null) usBits.push(`unemployment ${unrate.toFixed(1)}%`);
  if (t10y2y !== null) usBits.push(`10y-2y ${t10y2y >= 0 ? "+" : ""}${t10y2y.toFixed(2)}%`);
  if (vix !== null) usBits.push(`VIX ${vix.toFixed(1)}`);
  const usRegime = usBits.length > 0 ? `EUA · ${usBits.join(" · ")}` : "EUA · sem dados macro";
  const usLine = usBits.length > 0
    ? `Pano de fundo: ${usBits.join(", ")}.`
    : "Sem leituras macro recentes para os EUA.";

  _macroCache = {
    ts: Date.now(),
    br: { regime: brRegime, line: brLine },
    us: { regime: usRegime, line: usLine },
  };
  return { br: _macroCache.br, us: _macroCache.us };
}

function buildMacroOverlay(market: "br" | "us", sector: string): DeepReviewTickerData["macro_overlay"] {
  const macro = getMacroReadings();
  const m = market === "br" ? macro.br : macro.us;
  // Score is informational — the sector tilt logic stays heuristic for
  // now; a proper sector_score wire would query analytics/sector_tilt.
  const score = simpleHash(sector + market) % 100 / 50 - 1;
  const tilt = score > 0.2 ? "vento favorável" : score < -0.2 ? "vento contrário" : "neutral";
  const line = `${m.line} Sector ${sector}: ${tilt} segundo o tilt heurístico actual.`;
  return { regime: m.regime, sector_score: score, line };
}
