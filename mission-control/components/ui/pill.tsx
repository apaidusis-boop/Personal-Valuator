import { ReactNode } from "react";

export type PillVariant =
  | "buy"
  | "hold"
  | "avoid"
  | "na"
  | "mkt-br"
  | "mkt-us"
  | "neutral"
  | "glow"
  | "purple";

const CLASS: Record<PillVariant, string> = {
  buy: "pill pill-buy",
  hold: "pill pill-hold",
  avoid: "pill pill-avoid",
  na: "pill pill-na",
  "mkt-br": "pill pill-mkt-br",
  "mkt-us": "pill pill-mkt-us",
  neutral: "pill pill-neutral",
  glow: "pill pill-glow",
  purple: "pill pill-purple",
};

export function pillVariantFromVerdict(v: string | null | undefined): PillVariant {
  switch ((v || "").toUpperCase()) {
    case "BUY":
      return "buy";
    case "HOLD":
      return "hold";
    case "AVOID":
    case "SELL":
      return "avoid";
    default:
      return "na";
  }
}

export function pillVariantFromMarket(m: "br" | "us" | string | null | undefined): PillVariant {
  if (m === "br") return "mkt-br";
  if (m === "us") return "mkt-us";
  return "neutral";
}

type Props = {
  variant?: PillVariant;
  children: ReactNode;
  className?: string;
  title?: string;
};

export default function Pill({ variant = "neutral", children, className = "", title }: Props) {
  return (
    <span className={`${CLASS[variant]} ${className}`} title={title}>
      {children}
    </span>
  );
}
