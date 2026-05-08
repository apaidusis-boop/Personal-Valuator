import type { CouncilStance } from "@/lib/vault";

const STANCE_COLOR: Record<CouncilStance, string> = {
  BUY: "var(--verdict-buy)",
  HOLD: "var(--verdict-hold)",
  AVOID: "var(--verdict-avoid)",
  NEEDS_DATA: "var(--verdict-na)",
  UNKNOWN: "var(--verdict-na)",
};

const STANCE_BG: Record<CouncilStance, string> = {
  BUY: "rgba(76,175,80,0.12)",
  HOLD: "rgba(201,161,91,0.12)",
  AVOID: "rgba(239,83,80,0.12)",
  NEEDS_DATA: "rgba(156,163,175,0.10)",
  UNKNOWN: "rgba(156,163,175,0.10)",
};

const CONFIDENCE_COLOR: Record<string, string> = {
  high: "var(--verdict-buy)",
  medium: "var(--verdict-hold)",
  low: "var(--qual-degraded)",
};

export default function StancePill({
  stance,
  confidence,
  size = "sm",
}: {
  stance: CouncilStance;
  confidence?: string;
  size?: "sm" | "md" | "lg";
}) {
  const fontSize =
    size === "lg" ? "13px" : size === "md" ? "12px" : "10px";
  const padding =
    size === "lg" ? "4px 12px" : size === "md" ? "3px 10px" : "2px 8px";
  const color = STANCE_COLOR[stance] ?? STANCE_COLOR.UNKNOWN;
  const bg = STANCE_BG[stance] ?? STANCE_BG.UNKNOWN;
  const confColor =
    confidence && CONFIDENCE_COLOR[confidence.toLowerCase()]
      ? CONFIDENCE_COLOR[confidence.toLowerCase()]
      : "var(--text-tertiary)";
  return (
    <span
      className="inline-flex items-center gap-1.5 font-semibold uppercase tracking-wider rounded"
      style={{
        background: bg,
        color,
        fontSize,
        padding,
        letterSpacing: "0.04em",
      }}
    >
      <span>{stance.replace("_", " ")}</span>
      {confidence && confidence !== "—" && (
        <span
          className="font-normal normal-case"
          style={{ color: confColor, fontSize: "10px" }}
        >
          · {confidence}
        </span>
      )}
    </span>
  );
}
