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

export default function PageHeader({
  title,
  subtitle,
  crumbs,
  freshness,
  freshnessLabel,
  staleHours = 24,
  actions,
}: Props) {
  const stale = freshness !== undefined && freshness !== null && isStale(freshness, staleHours);
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
                  <span className={last ? "text-[var(--text-secondary)]" : "text-[var(--text-tertiary)]"}>
                    {c.label}
                  </span>
                )}
                {!last && <span className="text-[var(--text-disabled)]">›</span>}
              </span>
            );
          })}
        </nav>
      )}
      <div className="flex items-start justify-between gap-6">
        <div>
          <h1 className="type-h1 text-[var(--text-primary)]">{title}</h1>
          {subtitle && (
            <p className="type-body-sm text-[var(--text-secondary)] mt-1">
              {subtitle}
            </p>
          )}
        </div>
        <div className="flex items-center gap-3 shrink-0">
          {freshness !== undefined && freshness !== null && (
            <span
              className={
                "pill " + (stale ? "pill-hold" : "pill-glow")
              }
              title={typeof freshness === "string" ? freshness : ""}
            >
              {!stale && <span className="w-1.5 h-1.5 rounded-full bg-[var(--accent-glow)] dot-live" />}
              {stale && <span aria-hidden>⚑</span>}
              {freshnessLabel || formatDate(freshness, "relative")}
            </span>
          )}
          {actions}
        </div>
      </div>
    </header>
  );
}
