"use client";

// ── WORKBENCH · DRIP CALCULATOR TAB ─────────────────────────────────
//
// Reactive graph calculator. Sliders update <100ms because everything
// is client-side. The compounding math is intentionally simple: if the
// user wants the full damper-Gordon mix they hit `ii drip --ticker X`
// on the CLI. Here we just want to *feel* the curve.
//
// Inputs:
//   - Initial investment
//   - Horizon (5 / 10 / 15 / 20 / 30 yrs)
//   - DRIP %
//   - Dividend growth scenario (low / mid / high)
//
// Outputs:
//   - Shares-over-time (line)
//   - Annual income year by year (bars)
//   - Cash-payback summary numbers
//
// MOCK MODE: ticker dropdown shows BR + US holdings; assumptions
// (start price, start DY, baseline growth) are seeded by ticker hash
// when no live data is wired. Real wiring replaces `assumptionsFor()`.

import { useState, useMemo } from "react";
import { useFocusTicker } from "@/lib/focus-ticker";

type Growth = "low" | "mid" | "high";

export type DripCalcTabProps = {
  // Tickers available with their *seeded* assumptions. Real-data wire
  // later just replaces this map without touching the UI.
  ticker_assumptions: Record<string, {
    name: string;
    start_price: number;
    start_dy_pct: number;
    growth_low: number;   // %/yr
    growth_mid: number;
    growth_high: number;
    currency: "BRL" | "USD";
  }>;
  default_ticker: string;
};

export function DripCalcTab({ ticker_assumptions, default_ticker }: DripCalcTabProps) {
  const { focus } = useFocusTicker();
  const initialTicker = ticker_assumptions[focus.ticker] ? focus.ticker : default_ticker;

  const [ticker, setTicker] = useState(initialTicker);
  const [investment, setInvestment] = useState(10000);
  const [horizon, setHorizon] = useState(20);
  const [dripPct, setDripPct] = useState(100);
  const [growth, setGrowth] = useState<Growth>("mid");

  const a = ticker_assumptions[ticker] || {
    name: ticker,
    start_price: 100,
    start_dy_pct: 3,
    growth_low: 3,
    growth_mid: 6,
    growth_high: 9,
    currency: "USD" as const,
  };

  const projection = useMemo(
    () => project(a, investment, horizon, dripPct, growth),
    [a, investment, horizon, dripPct, growth],
  );

  const tickerOptions = useMemo(() => Object.keys(ticker_assumptions).sort(), [ticker_assumptions]);

  return (
    <div style={{ padding: "16px 20px 20px" }}>
      {/* ── Inputs row ─────────────────────────────────── */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr 1fr 1fr",
          gap: 14,
          marginBottom: 18,
          background: "var(--bg-overlay)",
          padding: 14,
          borderRadius: "var(--radius-sm)",
          border: "1px solid var(--border-subtle)",
        }}
      >
        <Field label="Ticker">
          <select
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            style={selectStyle}
          >
            {tickerOptions.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </Field>

        <Field label={`Investimento (${a.currency})`}>
          <input
            type="number"
            min={500}
            step={500}
            value={investment}
            onChange={(e) => setInvestment(Math.max(500, Number(e.target.value) || 0))}
            style={inputStyle}
          />
        </Field>

        <Field label={`Horizonte · ${horizon} anos`}>
          <input
            type="range"
            min={5}
            max={30}
            step={1}
            value={horizon}
            onChange={(e) => setHorizon(Number(e.target.value))}
            style={{ width: "100%" }}
          />
        </Field>

        <Field label={`DRIP · ${dripPct}%`}>
          <input
            type="range"
            min={0}
            max={100}
            step={5}
            value={dripPct}
            onChange={(e) => setDripPct(Number(e.target.value))}
            style={{ width: "100%" }}
          />
        </Field>

        <Field label="Crescimento de div.">
          <div className="segmented" style={{ width: "100%", justifyContent: "stretch" }}>
            {(["low", "mid", "high"] as Growth[]).map((g) => (
              <button
                key={g}
                data-active={g === growth}
                onClick={() => setGrowth(g)}
                style={{ flex: 1, padding: "5px 0", textTransform: "capitalize" }}
              >
                {g}
              </button>
            ))}
          </div>
          <p className="type-byline" style={{ marginTop: 4 }}>
            {growth === "low" ? `${a.growth_low.toFixed(1)}% a/a` : growth === "mid" ? `${a.growth_mid.toFixed(1)}% a/a` : `${a.growth_high.toFixed(1)}% a/a`}
          </p>
        </Field>
      </div>

      {/* ── Outputs: 3 panels ─────────────────────────── */}
      <div className="grid grid-cols-12 gap-5">
        <ChartPanel title="Shares ao longo do tempo" sub="Acumulação por reinvestimento">
          <SharesChart
            shares={projection.shares}
            startShares={projection.start_shares}
          />
        </ChartPanel>

        <ChartPanel title="Annual income" sub="Pagamento bruto por ano">
          <IncomeBars
            income={projection.annual_income}
            currency={a.currency}
          />
        </ChartPanel>

        <ChartPanel title="Resumo" sub="Payback e final state">
          <SummaryBlock projection={projection} a={a} horizon={horizon} />
        </ChartPanel>
      </div>
    </div>
  );
}

// ── Layout primitives ──────────────────────────────────────────────

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label
        style={{
          display: "block",
          fontSize: 9,
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          fontWeight: 600,
          color: "var(--text-tertiary)",
          marginBottom: 6,
          fontFamily: "var(--font-sans)",
        }}
      >
        {label}
      </label>
      {children}
    </div>
  );
}

const selectStyle: React.CSSProperties = {
  width: "100%",
  padding: "6px 8px",
  border: "1px solid var(--border-subtle)",
  borderRadius: 4,
  fontSize: 13,
  fontFamily: "var(--font-mono)",
  background: "var(--bg-elevated)",
  color: "var(--text-primary)",
};

const inputStyle: React.CSSProperties = {
  ...selectStyle,
  textAlign: "right",
};

function ChartPanel({ title, sub, children }: { title: string; sub: string; children: React.ReactNode }) {
  return (
    <div className="col-span-12 lg:col-span-4">
      <div
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
          borderRadius: "var(--radius-sm)",
          padding: 14,
          height: 280,
          display: "flex",
          flexDirection: "column",
        }}
      >
        <p className="type-h3" style={{ marginBottom: 2 }}>{title}</p>
        <p className="type-byline" style={{ marginBottom: 10 }}>{sub}</p>
        <div style={{ flex: 1, minHeight: 0 }}>{children}</div>
      </div>
    </div>
  );
}

// ── Projection math ────────────────────────────────────────────────

type Projection = {
  start_shares: number;
  end_shares: number;
  shares: number[];               // length = horizon + 1
  annual_income: number[];        // length = horizon (year-by-year payment)
  cash_payback_year: number | null;
  shares_double_year: number | null;
  end_market_value: number;
  end_annual_income: number;
};

function project(
  a: { start_price: number; start_dy_pct: number; growth_low: number; growth_mid: number; growth_high: number },
  investment: number,
  horizon: number,
  dripPct: number,
  growthChoice: Growth,
): Projection {
  const growth = (growthChoice === "low" ? a.growth_low : growthChoice === "mid" ? a.growth_mid : a.growth_high) / 100;
  const dripFrac = dripPct / 100;
  const startShares = investment / a.start_price;

  const shares: number[] = [startShares];
  const annualIncome: number[] = [];
  let curShares = startShares;
  // Assume price grows at a slower rate than divs (compounder framing)
  let curPrice = a.start_price;
  let curDPS = (a.start_dy_pct / 100) * a.start_price;
  let cumIncomeReceived = 0;

  let cashPaybackYear: number | null = null;
  let sharesDoubleYear: number | null = null;

  for (let y = 1; y <= horizon; y++) {
    curDPS = curDPS * (1 + growth);
    curPrice = curPrice * (1 + growth * 0.5); // price grows at half div pace, soft assumption
    const yearIncome = curShares * curDPS;
    annualIncome.push(yearIncome);

    const reinvested = yearIncome * dripFrac;
    const cashKept = yearIncome * (1 - dripFrac);
    cumIncomeReceived += yearIncome; // total dollars yielded (cash + reinvested)

    curShares += reinvested / curPrice;
    shares.push(curShares);

    if (cashPaybackYear === null && cumIncomeReceived >= investment) cashPaybackYear = y;
    if (sharesDoubleYear === null && curShares >= 2 * startShares) sharesDoubleYear = y;
  }

  return {
    start_shares: startShares,
    end_shares: curShares,
    shares,
    annual_income: annualIncome,
    cash_payback_year: cashPaybackYear,
    shares_double_year: sharesDoubleYear,
    end_market_value: curShares * curPrice,
    end_annual_income: annualIncome[annualIncome.length - 1] || 0,
  };
}

// ── Sub-charts ─────────────────────────────────────────────────────

function SharesChart({ shares, startShares }: { shares: number[]; startShares: number }) {
  const W = 320;
  const H = 200;
  const PAD_L = 36;
  const PAD_R = 8;
  const PAD_T = 8;
  const PAD_B = 22;

  const minY = Math.min(...shares);
  const maxY = Math.max(...shares);
  const yRange = maxY - minY || 1;

  const xPos = (i: number) => PAD_L + (i / Math.max(1, shares.length - 1)) * (W - PAD_L - PAD_R);
  const yPos = (v: number) => PAD_T + (1 - (v - minY) / yRange) * (H - PAD_T - PAD_B);

  const path = shares.map((v, i) => `${i === 0 ? "M" : "L"}${xPos(i).toFixed(1)},${yPos(v).toFixed(1)}`).join(" ");
  const fillPath = `${path} L${xPos(shares.length - 1)},${H - PAD_B} L${xPos(0)},${H - PAD_B} Z`;

  // 2× line
  const doubleY = startShares * 2;
  const drawDoubleLine = doubleY <= maxY && doubleY >= minY;

  return (
    <svg viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" style={{ width: "100%", height: "100%" }}>
      <defs>
        <linearGradient id="sharesFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="var(--jpm-blue)" stopOpacity="0.18" />
          <stop offset="100%" stopColor="var(--jpm-blue)" stopOpacity="0.02" />
        </linearGradient>
      </defs>
      <path d={fillPath} fill="url(#sharesFill)" />
      <path d={path} fill="none" stroke="var(--jpm-blue)" strokeWidth={2} strokeLinejoin="round" />
      {drawDoubleLine ? (
        <>
          <line
            x1={PAD_L}
            x2={W - PAD_R}
            y1={yPos(doubleY)}
            y2={yPos(doubleY)}
            stroke="var(--action-gold)"
            strokeWidth={1}
            strokeDasharray="3 3"
          />
          <text
            x={W - PAD_R - 4}
            y={yPos(doubleY) - 4}
            textAnchor="end"
            style={{ fontSize: 9, fill: "var(--action-gold-deep)", fontFamily: "var(--font-mono)", fontWeight: 700 }}
          >
            2× shares
          </text>
        </>
      ) : null}

      {/* y-axis labels: start, end */}
      <text x={PAD_L - 6} y={yPos(minY) + 3} textAnchor="end" style={{ fontSize: 9, fill: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>{minY.toFixed(0)}</text>
      <text x={PAD_L - 6} y={yPos(maxY) + 3} textAnchor="end" style={{ fontSize: 9, fill: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>{maxY.toFixed(0)}</text>

      <text x={PAD_L} y={H - 6} style={{ fontSize: 9, fill: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>Y0</text>
      <text x={W - PAD_R} y={H - 6} textAnchor="end" style={{ fontSize: 9, fill: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>Y{shares.length - 1}</text>
    </svg>
  );
}

function IncomeBars({ income, currency }: { income: number[]; currency: "BRL" | "USD" }) {
  const W = 320;
  const H = 200;
  const PAD_L = 40;
  const PAD_R = 8;
  const PAD_T = 8;
  const PAD_B = 22;
  const max = Math.max(...income, 1);
  const barW = ((W - PAD_L - PAD_R) / income.length) * 0.7;
  const gap = ((W - PAD_L - PAD_R) / income.length) * 0.3;
  const fmt = (v: number) =>
    `${currency === "BRL" ? "R$" : "$"}${
      v >= 1000 ? (v / 1000).toFixed(1) + "k" : v.toFixed(0)
    }`;

  return (
    <svg viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" style={{ width: "100%", height: "100%" }}>
      {income.map((v, i) => {
        const h = ((v / max) * (H - PAD_T - PAD_B)) || 0;
        const x = PAD_L + i * (barW + gap) + gap / 2;
        return (
          <rect
            key={i}
            x={x}
            y={H - PAD_B - h}
            width={barW}
            height={h}
            fill="var(--jpm-gain)"
            opacity={0.4 + (i / income.length) * 0.6}
            rx={1}
          />
        );
      })}
      <text x={PAD_L - 6} y={PAD_T + 8} textAnchor="end" style={{ fontSize: 9, fill: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>{fmt(max)}</text>
      <text x={PAD_L - 6} y={H - PAD_B + 4} textAnchor="end" style={{ fontSize: 9, fill: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>0</text>
      <text x={PAD_L} y={H - 6} style={{ fontSize: 9, fill: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>Y1</text>
      <text x={W - PAD_R} y={H - 6} textAnchor="end" style={{ fontSize: 9, fill: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>Y{income.length}</text>
    </svg>
  );
}

function SummaryBlock({
  projection,
  a,
  horizon,
}: {
  projection: Projection;
  a: { currency: "BRL" | "USD"; name: string };
  horizon: number;
}) {
  const cur = a.currency === "BRL" ? "R$" : "$";
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10, height: "100%", justifyContent: "space-around" }}>
      <Row
        label="Cash payback"
        value={projection.cash_payback_year !== null ? `Ano ${projection.cash_payback_year}` : `> ${horizon}y`}
        accent="var(--accent-primary)"
      />
      <Row
        label="2× shares"
        value={projection.shares_double_year !== null ? `Ano ${projection.shares_double_year}` : `> ${horizon}y`}
        accent="var(--action-gold-deep)"
      />
      <Row
        label="Shares finais"
        value={`${projection.end_shares.toFixed(0)}`}
        sub={`de ${projection.start_shares.toFixed(0)}`}
      />
      <Row
        label="Annual income final"
        value={`${cur}${formatLargeNumber(projection.end_annual_income)}`}
      />
      <Row
        label="Market value final"
        value={`${cur}${formatLargeNumber(projection.end_market_value)}`}
      />
    </div>
  );
}

function Row({ label, value, sub, accent }: { label: string; value: string; sub?: string; accent?: string }) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "baseline",
        justifyContent: "space-between",
        paddingBottom: 8,
        borderBottom: "1px solid var(--border-subtle)",
        gap: 12,
      }}
    >
      <span
        style={{
          fontSize: 10,
          letterSpacing: "0.06em",
          textTransform: "uppercase",
          color: "var(--text-tertiary)",
          fontWeight: 600,
        }}
      >
        {label}
      </span>
      <span style={{ display: "inline-flex", alignItems: "baseline", gap: 4 }}>
        {sub ? (
          <span style={{ fontSize: 10, color: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>{sub}</span>
        ) : null}
        <span
          className="font-data"
          style={{ fontSize: 14, fontWeight: 700, color: accent || "var(--text-primary)" }}
        >
          {value}
        </span>
      </span>
    </div>
  );
}

function formatLargeNumber(v: number): string {
  if (v >= 1_000_000) return (v / 1_000_000).toFixed(1) + "M";
  if (v >= 1_000) return (v / 1_000).toFixed(1) + "k";
  return v.toFixed(0);
}
