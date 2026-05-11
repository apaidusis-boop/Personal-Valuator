"use client";

// ── /stocks · top-level view ──────────────────────────────────────────
//
// Page mode toggle: "Read" (magazine — sidebar + per-ticker tearsheet)
// vs "Operate" (IB-style blotter grid). Mode persists to URL hash so a
// copy/paste link reopens the same view.
//
// Shared state across modes:
//   - selected ticker (for Read mode tearsheet) — defaults to highest weight
//   - filter set (sector, market, verdict) — used by both modes

import { useState, useEffect } from "react";
import type { StocksData } from "@/lib/stocks-data";
import { ReadMode } from "./read-mode";
import { OperateMode } from "./operate-mode";
import { FocusTickerProvider } from "@/lib/focus-ticker";

type Mode = "read" | "operate";

export function StocksView({ data }: { data: StocksData }) {
  const [mode, setMode] = useState<Mode>("read");
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const h = window.location.hash.replace(/^#/, "");
    if (h === "operate" || h === "read") setMode(h);
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    const url = new URL(window.location.href);
    url.hash = mode;
    window.history.replaceState({}, "", url.toString());
  }, [mode, hydrated]);

  const initialTicker = data.rows[0]?.ticker || "AAPL";
  const initialMarket = data.rows[0]?.market || "us";

  return (
    <FocusTickerProvider initialTicker={initialTicker} initialMarket={initialMarket}>
      <div className="px-6 py-5 max-w-[1440px] mx-auto" style={{ display: "flex", flexDirection: "column", gap: 18 }}>
        <Header
          mode={mode}
          setMode={setMode}
          n_holdings={data.n_holdings}
          n_watchlist={data.n_watchlist}
          br_nav={data.br_nav}
          us_nav={data.us_nav}
        />
        {mode === "read" ? <ReadMode data={data} /> : <OperateMode data={data} />}
      </div>
    </FocusTickerProvider>
  );
}

// ── Header — masthead + mode toggle ──────────────────────────────────

function Header({
  mode,
  setMode,
  n_holdings,
  n_watchlist,
  br_nav,
  us_nav,
}: {
  mode: Mode;
  setMode: (m: Mode) => void;
  n_holdings: number;
  n_watchlist: number;
  br_nav: number;
  us_nav: number;
}) {
  return (
    <header
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderRadius: "var(--radius)",
        padding: "14px 20px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexWrap: "wrap",
        gap: 12,
      }}
    >
      <div>
        <p
          className="type-h3"
          style={{ color: "var(--accent-primary)", letterSpacing: "0.12em", marginBottom: 4 }}
        >
          Stocks · todas as ações
        </p>
        <h1
          style={{
            fontFamily: "var(--font-display)",
            fontSize: 24,
            lineHeight: 1.15,
            fontWeight: 700,
            color: "var(--text-primary)",
            letterSpacing: "-0.015em",
          }}
        >
          {n_holdings + n_watchlist} tickers · BR + EUA
        </h1>
        <p className="type-byline" style={{ marginTop: 2 }}>
          {n_holdings} holdings · {n_watchlist} watchlist · NAV BR R${formatCompact(br_nav)} · US ${formatCompact(us_nav)}
        </p>
      </div>
      <div className="segmented" role="tablist" aria-label="Mode">
        <button data-active={mode === "read"} onClick={() => setMode("read")}>
          Read
        </button>
        <button data-active={mode === "operate"} onClick={() => setMode("operate")}>
          Operate
        </button>
      </div>
    </header>
  );
}

function formatCompact(v: number): string {
  if (v >= 1_000_000) return (v / 1_000_000).toFixed(2) + "M";
  if (v >= 1_000) return (v / 1_000).toFixed(0) + "k";
  return v.toFixed(0);
}
