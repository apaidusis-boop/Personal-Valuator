import type { CouncilStance } from "@/lib/vault";

const STANCE_TONE: Record<CouncilStance, string> = {
  BUY: "bg-green-900/40 text-green-300 border-green-700/50",
  HOLD: "bg-yellow-900/30 text-yellow-300 border-yellow-700/40",
  AVOID: "bg-red-900/40 text-red-300 border-red-700/50",
  NEEDS_DATA: "bg-zinc-800/60 text-zinc-400 border-zinc-700/50",
  UNKNOWN: "bg-zinc-900/40 text-zinc-500 border-zinc-800/50",
};

const CONFIDENCE_TONE: Record<string, string> = {
  high: "text-green-300",
  medium: "text-yellow-300",
  low: "text-orange-300",
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
  const tone = STANCE_TONE[stance] ?? STANCE_TONE.UNKNOWN;
  const text =
    size === "lg" ? "text-base" : size === "md" ? "text-sm" : "text-[11px]";
  const pad =
    size === "lg" ? "px-3 py-1.5" : size === "md" ? "px-2.5 py-1" : "px-2 py-0.5";
  const confTone =
    confidence && CONFIDENCE_TONE[confidence.toLowerCase()]
      ? CONFIDENCE_TONE[confidence.toLowerCase()]
      : "text-zinc-400";
  return (
    <span className={`inline-flex items-center gap-1.5 rounded border font-mono uppercase tracking-wider ${tone} ${text} ${pad}`}>
      <span>{stance}</span>
      {confidence && confidence !== "—" && (
        <span className={`text-[10px] normal-case ${confTone}`}>· {confidence}</span>
      )}
    </span>
  );
}
