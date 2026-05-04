/**
 * Formatting helpers — dates, numbers, currency.
 * Centralized so every page renders dates the same way.
 */

const RTF_PT = new Intl.RelativeTimeFormat("pt-BR", { numeric: "auto" });
const RTF_EN = new Intl.RelativeTimeFormat("en", { numeric: "auto" });

const PT_MONTHS_SHORT = [
  "jan", "fev", "mar", "abr", "mai", "jun",
  "jul", "ago", "set", "out", "nov", "dez",
];

export type DateMode = "relative" | "short" | "medium" | "iso" | "datetime";

function parseLooseDate(input: string | Date | number): Date | null {
  if (input instanceof Date) return isNaN(input.getTime()) ? null : input;
  if (typeof input === "number") {
    // Accept seconds OR ms
    const d = input > 1e12 ? new Date(input) : new Date(input * 1000);
    return isNaN(d.getTime()) ? null : d;
  }
  if (typeof input === "string") {
    if (!input) return null;
    // YYYY-MM-DD only — append T00 to keep local interpretation safe
    if (/^\d{4}-\d{2}-\d{2}$/.test(input)) {
      const d = new Date(input + "T00:00:00");
      return isNaN(d.getTime()) ? null : d;
    }
    // YYYY-MM-DD HH:MM[:SS] — replace space with T
    if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}/.test(input)) {
      const d = new Date(input.replace(" ", "T"));
      return isNaN(d.getTime()) ? null : d;
    }
    const d = new Date(input);
    return isNaN(d.getTime()) ? null : d;
  }
  return null;
}

export function formatDate(
  input: string | Date | number | null | undefined,
  mode: DateMode = "relative",
  locale: "pt" | "en" = "pt"
): string {
  if (input === null || input === undefined || input === "") return "—";
  const d = parseLooseDate(input);
  if (!d) return String(input);
  const now = Date.now();
  const diffMs = d.getTime() - now;
  const absMin = Math.abs(diffMs / 60000);

  switch (mode) {
    case "iso":
      return d.toISOString().slice(0, 10);
    case "short":
      return locale === "pt"
        ? `${d.getDate()} ${PT_MONTHS_SHORT[d.getMonth()]}`
        : d.toLocaleDateString("en", { month: "short", day: "numeric" });
    case "medium":
      return locale === "pt"
        ? `${d.getDate()} ${PT_MONTHS_SHORT[d.getMonth()]} ${d.getFullYear()}`
        : d.toLocaleDateString("en", {
            month: "short",
            day: "numeric",
            year: "numeric",
          });
    case "datetime": {
      const datePart = formatDate(d, "short", locale);
      const time = `${String(d.getHours()).padStart(2, "0")}:${String(
        d.getMinutes()
      ).padStart(2, "0")}`;
      return `${datePart} · ${time}`;
    }
    case "relative":
    default: {
      const rtf = locale === "pt" ? RTF_PT : RTF_EN;
      if (absMin < 1) return locale === "pt" ? "agora" : "now";
      if (absMin < 60) return rtf.format(Math.round(diffMs / 60000), "minute");
      const absH = absMin / 60;
      if (absH < 24) return rtf.format(Math.round(diffMs / 3600000), "hour");
      const absD = absH / 24;
      if (absD < 7) return rtf.format(Math.round(diffMs / 86400000), "day");
      if (absD < 31) return rtf.format(Math.round(diffMs / (86400000 * 7)), "week");
      // Older than a month → fall back to short
      return formatDate(d, "short", locale);
    }
  }
}

/** Returns true when the date is more than `staleHours` old. */
export function isStale(
  input: string | Date | number | null | undefined,
  staleHours = 24
): boolean {
  const d = parseLooseDate(input as any);
  if (!d) return true;
  return Date.now() - d.getTime() > staleHours * 3600000;
}

export function formatCurrency(
  value: number | null | undefined,
  currency: "BRL" | "USD" = "USD",
  digits = 2
): string {
  if (value === null || value === undefined || isNaN(value as number)) return "—";
  if (currency === "BRL") {
    return value.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
      maximumFractionDigits: digits,
    });
  }
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: digits,
  });
}

export function formatPercent(
  value: number | null | undefined,
  digits = 1,
  options: { signed?: boolean; fromFraction?: boolean } = {}
): string {
  if (value === null || value === undefined || isNaN(value as number)) return "—";
  const v = options.fromFraction ? value * 100 : value;
  const sign = options.signed && v > 0 ? "+" : "";
  return `${sign}${v.toFixed(digits)}%`;
}

export function formatNumber(
  value: number | null | undefined,
  options: { compact?: boolean; signed?: boolean; digits?: number } = {}
): string {
  if (value === null || value === undefined || isNaN(value as number)) return "—";
  const digits = options.digits ?? 0;
  if (options.compact) {
    const abs = Math.abs(value);
    if (abs >= 1e9) return (value / 1e9).toFixed(1).replace(/\.0$/, "") + "B";
    if (abs >= 1e6) return (value / 1e6).toFixed(1).replace(/\.0$/, "") + "M";
    if (abs >= 1e3) return (value / 1e3).toFixed(1).replace(/\.0$/, "") + "k";
  }
  const sign = options.signed && value > 0 ? "+" : "";
  return sign + value.toLocaleString("en-US", { maximumFractionDigits: digits });
}

/** Humanizes schedule strings like "daily 09:30", "every 6h", "weekly tue 14:00". */
export function humanizeSchedule(s: string | null | undefined): string {
  if (!s) return "—";
  const txt = s.trim().toLowerCase();
  if (txt === "manual" || txt === "off" || txt === "disabled") return "manual";
  if (/^daily\s+\d{1,2}:\d{2}/.test(txt)) {
    const m = txt.match(/(\d{1,2}:\d{2})/);
    return m ? `every day · ${m[1]}` : txt;
  }
  if (/^weekly\s+/.test(txt)) {
    return txt.replace(/^weekly\s+/, "weekly · ");
  }
  if (/^every\s+\d+/.test(txt)) {
    return txt.replace(/^every\s+/, "every ");
  }
  return s;
}
