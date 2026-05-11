"use client";

// Click → opens the ticker side-sheet drawer instead of navigating away.
// Server-side parent renders these as leaves so the page stays a server
// component and we keep DB access fast.

import { openTickerSheet } from "@/lib/ticker-sheet";

export default function EventTickerLink({ ticker }: { ticker: string }) {
  return (
    <button
      type="button"
      onClick={() => openTickerSheet(ticker)}
      style={{
        background: "transparent",
        border: 0,
        padding: 0,
        cursor: "pointer",
        color: "var(--accent-primary)",
        fontWeight: 600,
        fontSize: 13,
        fontFamily: "var(--font-mono)",
        letterSpacing: "0.02em",
      }}
      onMouseEnter={(e) => (e.currentTarget.style.textDecoration = "underline")}
      onMouseLeave={(e) => (e.currentTarget.style.textDecoration = "none")}
    >
      {ticker}
    </button>
  );
}
