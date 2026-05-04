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

export default function Section({ label, meta, action, children, dense }: Props) {
  return (
    <section className="mb-8">
      <header className={`flex items-center justify-between ${dense ? "mb-2" : "mb-3"}`}>
        <div className="flex items-baseline gap-3">
          <h2 className="type-h3">{label}</h2>
          {meta && (
            <span className="type-mono-sm text-[var(--text-tertiary)]">
              {meta}
            </span>
          )}
        </div>
        {action}
      </header>
      {children}
    </section>
  );
}
