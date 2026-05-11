"use client";

import { useEffect, useState } from "react";

// BR: B3 09:00–18:00 (handles after-market separately, ignored here for now)
// US: NYSE/NASDAQ regular session 09:30–16:00 ET
// We compute against the wall clock and map to the venue's local time via UTC.

type MktState = {
  label: string;
  isOpen: boolean;
  status: string; // "open" | "closed"
  countdown: string; // "4h 12m → fecha" / "8h 42m → abre"
  localTime: string; // "10:42 BRT" / "11:18 ET"
};

// BRT = UTC-3 (no DST in BR since 2019). ET varies (EST -5 / EDT -4).
// We use the browser timezone helpers via Intl to keep ET correct.
function nowInZone(tz: string): {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  weekday: number;
  hhmm: string;
} {
  const d = new Date();
  const fmt = new Intl.DateTimeFormat("en-US", {
    timeZone: tz,
    hour12: false,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    weekday: "short",
  });
  const parts = Object.fromEntries(
    fmt.formatToParts(d).map((p) => [p.type, p.value])
  );
  const wkMap: Record<string, number> = {
    Sun: 0,
    Mon: 1,
    Tue: 2,
    Wed: 3,
    Thu: 4,
    Fri: 5,
    Sat: 6,
  };
  const hh = parts.hour === "24" ? "00" : parts.hour; // some locales use 24
  return {
    year: Number(parts.year),
    month: Number(parts.month),
    day: Number(parts.day),
    hour: Number(hh),
    minute: Number(parts.minute),
    weekday: wkMap[parts.weekday as string] ?? 0,
    hhmm: `${hh}:${parts.minute}`,
  };
}

function fmtCountdown(totalMin: number): string {
  if (totalMin < 0) totalMin = 0;
  const h = Math.floor(totalMin / 60);
  const m = totalMin % 60;
  if (h === 0) return `${m}m`;
  return `${h}h ${m.toString().padStart(2, "0")}m`;
}

function computeBR(): MktState {
  const t = nowInZone("America/Sao_Paulo");
  const minutesNow = t.hour * 60 + t.minute;
  const open = 9 * 60; // 09:00
  const close = 18 * 60; // 18:00
  const isWeekend = t.weekday === 0 || t.weekday === 6;
  let isOpen = false;
  let countdown = "";
  if (isWeekend) {
    // Minutes until Monday 09:00
    const daysToMon = t.weekday === 6 ? 2 : 1;
    const minsToMidnight = 24 * 60 - minutesNow;
    const minutesToOpen = minsToMidnight + (daysToMon - 1) * 24 * 60 + open;
    countdown = `${fmtCountdown(minutesToOpen)} → abre`;
  } else if (minutesNow < open) {
    countdown = `${fmtCountdown(open - minutesNow)} → abre`;
  } else if (minutesNow >= close) {
    // Until tomorrow 09:00 (or Mon if Friday)
    const daysToNext = t.weekday === 5 ? 3 : 1;
    const minsToMidnight = 24 * 60 - minutesNow;
    const minutesToOpen = minsToMidnight + (daysToNext - 1) * 24 * 60 + open;
    countdown = `${fmtCountdown(minutesToOpen)} → abre`;
  } else {
    isOpen = true;
    countdown = `${fmtCountdown(close - minutesNow)} → fecha`;
  }
  return {
    label: "B3",
    isOpen,
    status: isOpen ? "open" : "closed",
    countdown,
    localTime: `${t.hhmm} BRT`,
  };
}

function computeUS(): MktState {
  const t = nowInZone("America/New_York");
  const minutesNow = t.hour * 60 + t.minute;
  const open = 9 * 60 + 30; // 09:30
  const close = 16 * 60; // 16:00
  const isWeekend = t.weekday === 0 || t.weekday === 6;
  let isOpen = false;
  let countdown = "";
  if (isWeekend) {
    const daysToMon = t.weekday === 6 ? 2 : 1;
    const minsToMidnight = 24 * 60 - minutesNow;
    const minutesToOpen = minsToMidnight + (daysToMon - 1) * 24 * 60 + open;
    countdown = `${fmtCountdown(minutesToOpen)} → abre`;
  } else if (minutesNow < open) {
    countdown = `${fmtCountdown(open - minutesNow)} → abre`;
  } else if (minutesNow >= close) {
    const daysToNext = t.weekday === 5 ? 3 : 1;
    const minsToMidnight = 24 * 60 - minutesNow;
    const minutesToOpen = minsToMidnight + (daysToNext - 1) * 24 * 60 + open;
    countdown = `${fmtCountdown(minutesToOpen)} → abre`;
  } else {
    isOpen = true;
    countdown = `${fmtCountdown(close - minutesNow)} → fecha`;
  }
  return {
    label: "NYSE",
    isOpen,
    status: isOpen ? "open" : "closed",
    countdown,
    localTime: `${t.hhmm} ET`,
  };
}

export default function MarketClock() {
  const [br, setBr] = useState<MktState | null>(null);
  const [us, setUs] = useState<MktState | null>(null);

  useEffect(() => {
    const tick = () => {
      setBr(computeBR());
      setUs(computeUS());
    };
    tick();
    const id = setInterval(tick, 30 * 1000);
    return () => clearInterval(id);
  }, []);

  if (!br || !us) return null;

  return (
    <div
      className="hidden md:flex items-center gap-3 text-[11px] font-data"
      style={{ color: "var(--text-tertiary)" }}
      aria-label="Mercados"
    >
      <Pill state={br} />
      <span style={{ color: "var(--border-subtle)" }}>·</span>
      <Pill state={us} />
    </div>
  );
}

function Pill({ state }: { state: MktState }) {
  const dotColor = state.isOpen ? "var(--gain)" : "var(--text-disabled)";
  return (
    <span
      className="inline-flex items-center gap-1.5"
      title={`${state.label} · ${state.localTime}`}
    >
      <span
        aria-hidden
        style={{
          display: "inline-block",
          width: 7,
          height: 7,
          borderRadius: 999,
          background: dotColor,
          boxShadow: state.isOpen
            ? `0 0 6px ${dotColor}`
            : "none",
        }}
      />
      <span
        style={{
          color: "var(--text-secondary)",
          fontWeight: 600,
          letterSpacing: "0.02em",
        }}
      >
        {state.label}
      </span>
      <span style={{ color: "var(--text-tertiary)" }}>{state.countdown}</span>
    </span>
  );
}
