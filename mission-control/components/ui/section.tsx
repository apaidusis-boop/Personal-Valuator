import { ReactNode } from "react";

type Props = {
  label: string;
  meta?: ReactNode;
  /** Right-side action (e.g., "view all →") */
  action?: ReactNode;
  children: ReactNode;
  /** Spacing under section label, default tight */
  dense?: boolean;
};

/**
 * Editorial-style section.
 * Heading in uppercase tracked sans, rule extends to action on the right —
 * FT supplements / WSJ section dividers vibe.
 */
export default function Section({ label, meta, action, children, dense }: Props) {
  return (
    <section className={dense ? "mb-5" : "mb-8"}>
      <header
        className={`flex items-center gap-3 ${dense ? "mb-2" : "mb-3"}`}
      >
        <h2 className="type-h3 shrink-0">{label}</h2>
        {meta && (
          <span className="type-mono-sm text-[var(--text-tertiary)] shrink-0">
            {meta}
          </span>
        )}
        <span className="flex-1 h-px bg-[var(--border-subtle)]" aria-hidden />
        {action && <div className="shrink-0">{action}</div>}
      </header>
      {children}
    </section>
  );
}
