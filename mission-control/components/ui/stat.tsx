import { ReactNode } from "react";

type Props = {
  label: string;
  value: ReactNode;
  /** Sub-line under value */
  caption?: ReactNode;
  /** ▲ +2.3% — color-aware */
  delta?: { value: number; suffix?: string; format?: "percent" | "absolute" };
  /** Optional icon prefix to label */
  icon?: ReactNode;
  /** When true, makes value smaller (for tight grids) */
  compact?: boolean;
};

/**
 * Editorial stat block.
 * Label small caps tracked. Value mono tabular, larger weight.
 * No card background — just a top rule, broadsheet style.
 */
export default function Stat({ label, value, caption, delta, icon, compact }: Props) {
  return (
    <div className="border-t border-[var(--rule)] pt-3 px-1">
      <div className="flex items-center gap-2 mb-2">
        {icon && (
          <span className="type-mono-sm text-[var(--text-tertiary)]">
            {icon}
          </span>
        )}
        <h3 className="type-h3">{label}</h3>
      </div>
      <div
        className={
          "tabular text-[var(--text-primary)] " +
          (compact ? "type-h1" : "type-display")
        }
      >
        {value}
      </div>
      {(caption || delta) && (
        <div className="flex items-baseline gap-2 mt-1.5">
          {delta && <DeltaBadge {...delta} />}
          {caption && (
            <span className="type-caption text-[var(--text-tertiary)]">
              {caption}
            </span>
          )}
        </div>
      )}
    </div>
  );
}

function DeltaBadge({
  value,
  suffix = "%",
  format = "percent",
}: {
  value: number;
  suffix?: string;
  format?: "percent" | "absolute";
}) {
  const positive = value > 0;
  const negative = value < 0;
  const color = positive
    ? "text-[var(--gain)]"
    : negative
      ? "text-[var(--loss)]"
      : "text-[var(--neutral)]";
  const arrow = positive ? "▲" : negative ? "▼" : "—";
  const formatted =
    format === "percent"
      ? Math.abs(value).toFixed(1) + suffix
      : Math.abs(value).toFixed(2);
  return (
    <span className={`type-mono-sm ${color}`}>
      {arrow} {positive || negative ? formatted : "0"}
    </span>
  );
}
