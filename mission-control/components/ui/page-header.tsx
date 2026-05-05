import Link from "next/link";
import { ReactNode } from "react";
import { formatDate, isStale } from "@/lib/format";

export type Crumb = { label: string; href?: string };

type Props = {
  title: string;
  subtitle?: string;
  crumbs?: Crumb[];
  /** Last-update timestamp; null = no badge; auto-detects stale. */
  freshness?: string | Date | number | null;
  freshnessLabel?: string;
  staleHours?: number;
  actions?: ReactNode;
};

/**
 * Editorial-style page header.
 * Title in serif. Subtitle as italic byline. Hard rule under — FT signature.
 */
export default function PageHeader({
  title,
  subtitle,
  crumbs,
  freshness,
  freshnessLabel,
  staleHours = 24,
  actions,
}: Props) {
  const stale =
    freshness !== undefined && freshness !== null && isStale(freshness, staleHours);
  return (
    <header className="mb-8">
      {crumbs && crumbs.length > 0 && (
        <nav
          className="type-mono-sm flex items-center gap-1 mb-3"
          aria-label="breadcrumb"
        >
          {crumbs.map((c, i) => {
            const last = i === crumbs.length - 1;
            return (
              <span key={i} className="flex items-center gap-1">
                {c.href && !last ? (
                  <Link
                    href={c.href}
                    className="text-[var(--text-tertiary)] hover:text-[var(--accent-glow)] transition-colors"
                  >
                    {c.label}
                  </Link>
                ) : (
                  <span
                    className={
                      last
                        ? "text-[var(--text-secondary)]"
                        : "text-[var(--text-tertiary)]"
                    }
                  >
                    {c.label}
                  </span>
                )}
                {!last && (
                  <span className="text-[var(--text-disabled)]">›</span>
                )}
              </span>
            );
          })}
        </nav>
      )}
      <div className="flex items-end justify-between gap-6">
        <div className="min-w-0">
          <h1 className="type-display">{title}</h1>
          {subtitle && (
            <p className="type-byline mt-1.5">{subtitle}</p>
          )}
        </div>
        <div className="flex items-center gap-3 shrink-0 pb-1">
          {freshness !== undefined && freshness !== null && (
            <span
              className={"pill " + (stale ? "pill-hold" : "pill-glow")}
              title={typeof freshness === "string" ? freshness : ""}
            >
              {!stale && (
                <span
                  className="w-1.5 h-1.5 rounded-full bg-current dot-live"
                  aria-hidden
                />
              )}
              {stale && <span aria-hidden>!</span>}
              {freshnessLabel || formatDate(freshness, "relative")}
            </span>
          )}
          {actions}
        </div>
      </div>
      <div className="rule-hard" />
    </header>
  );
}
