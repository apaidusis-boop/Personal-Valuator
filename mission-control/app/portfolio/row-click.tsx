"use client";

// Tiny client-side bridge: wraps a portfolio row so clicking it opens the
// ticker side-sheet drawer. The portfolio page itself is a server component
// (better-sqlite3 access), so the click handler lives in this leaf.

import { ReactNode } from "react";
import { openTickerSheet } from "@/lib/ticker-sheet";

export default function PortfolioRowClick({
  ticker,
  children,
}: {
  ticker: string | null;
  children: ReactNode;
}) {
  if (!ticker) return <>{children}</>;
  return (
    <span
      onClick={(e) => {
        e.stopPropagation();
        openTickerSheet(ticker);
      }}
      style={{ cursor: "pointer" }}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          openTickerSheet(ticker);
        }
      }}
    >
      {children}
    </span>
  );
}
