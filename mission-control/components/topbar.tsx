"use client";

import { Bell, Calendar } from "lucide-react";
import { useEffect, useState } from "react";
import GlobalSearch from "./global-search";
import MarketClock from "./market-clock";

/**
 * Fixed top bar — h-56 (var(--topbar-h)).
 * Sits to the right of the sidebar. Hosts:
 *  - global search (functional, navigates to side-sheet on Enter)
 *  - market clock (BR + US open/close countdown)
 *  - date stamp + bell + avatar
 */
export default function TopBar({ openActions = 0 }: { openActions?: number }) {
  const [dateStr, setDateStr] = useState("");

  useEffect(() => {
    setDateStr(
      new Date().toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
      })
    );
  }, []);

  return (
    <header
      className="fixed top-0 right-0 z-40 flex items-center justify-between px-6 gap-4"
      style={{
        height: "var(--topbar-h)",
        left: "var(--sidebar-w)",
        background: "var(--bg-canvas)",
        borderBottom: "1px solid var(--border-subtle)",
      }}
    >
      {/* Left: search ---------------------------------------- */}
      <GlobalSearch />

      {/* Right cluster --------------------------------------- */}
      <div className="flex items-center gap-5">
        <MarketClock />

        <div
          className="flex items-center gap-2 text-sm"
          style={{ color: "var(--text-tertiary)" }}
        >
          <Calendar size={13} />
          <span className="font-data">{dateStr || "—"}</span>
        </div>

        <button
          type="button"
          className="relative p-2 transition-colors"
          style={{ color: "var(--text-tertiary)" }}
          aria-label="Notifications"
        >
          <Bell size={17} />
          {openActions > 0 && (
            <span
              className="absolute top-1 right-1 w-2 h-2 rounded-full"
              style={{ background: "var(--val-gold)" }}
              aria-label={`${openActions} open actions`}
            />
          )}
        </button>

        <div
          className="w-8 h-8 rounded-full flex items-center justify-center"
          style={{
            background:
              "linear-gradient(135deg, var(--val-blue), var(--val-blue-deep))",
          }}
        >
          <span className="text-white text-xs font-semibold">U</span>
        </div>
      </div>
    </header>
  );
}
