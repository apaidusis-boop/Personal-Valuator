import type { Metadata } from "next";
import Link from "next/link";

import {
  listCouncilOutputs,
  summariseCouncil,
  type CouncilEntry,
  type CouncilStance,
} from "@/lib/vault";
import { formatDate } from "@/lib/format";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Council · Mission Control" };

const STANCE_ORDER: CouncilStance[] = [
  "BUY",
  "HOLD",
  "AVOID",
  "NEEDS_DATA",
  "UNKNOWN",
];

const STANCE_LABEL: Record<CouncilStance, string> = {
  BUY: "Buy",
  HOLD: "Hold",
  AVOID: "Avoid",
  NEEDS_DATA: "Needs data",
  UNKNOWN: "Uncategorised",
};

function stanceVariant(s: CouncilStance): "buy" | "hold" | "avoid" | "na" {
  switch (s) {
    case "BUY":
      return "buy";
    case "HOLD":
      return "hold";
    case "AVOID":
      return "avoid";
    default:
      return "na";
  }
}

function stanceColor(s: CouncilStance): string {
  switch (s) {
    case "BUY":
      return "var(--verdict-buy)";
    case "HOLD":
      return "var(--verdict-hold)";
    case "AVOID":
      return "var(--verdict-avoid)";
    default:
      return "var(--verdict-na)";
  }
}

export default function CouncilIndexPage() {
  const all = listCouncilOutputs(500);
  const summary = summariseCouncil(all);
  const latest = all.filter((e) => e.date === summary.date);
  const previous = all.filter((e) => e.date && e.date !== summary.date);

  const grouped: Record<CouncilStance, CouncilEntry[]> = {
    BUY: [],
    HOLD: [],
    AVOID: [],
    NEEDS_DATA: [],
    UNKNOWN: [],
  };
  for (const e of latest) grouped[e.stance].push(e);

  return (
    <div className="p-5 space-y-5">
      {/* Header --------------------------------------------- */}
      <div>
        <h1
          className="font-display text-xl font-bold"
          style={{ color: "var(--text-primary)" }}
        >
          Council
        </h1>
        <p
          className="text-xs mt-0.5"
          style={{ color: "var(--text-tertiary)" }}
        >
          Synthetic IC dossiers · STORYT 3.0 ·{" "}
          {summary.date !== "—" ? formatDate(summary.date, "medium") : "sem run"} ·{" "}
          {latest.length} reviewed
        </p>
      </div>

      {latest.length === 0 ? (
        <div
          className="p-12 rounded text-center"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <p
            className="text-sm italic"
            style={{ color: "var(--text-tertiary)" }}
          >
            Sem dossiers do Council. Corre durante o overnight batch.
          </p>
        </div>
      ) : (
        <>
          {/* Stance counts -------------------------------------- */}
          <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
            <CountBlock label="TOTAL" n={summary.total} />
            <CountBlock label="BUY" n={summary.buy} variant="buy" />
            <CountBlock label="HOLD" n={summary.hold} variant="hold" />
            <CountBlock label="AVOID" n={summary.avoid} variant="avoid" />
            <CountBlock
              label="NEEDS DATA"
              n={summary.needs_data}
              variant="na"
            />
          </div>

          {/* Stance groups -------------------------------------- */}
          {STANCE_ORDER.map((st) => {
            const items = grouped[st];
            if (items.length === 0) return null;
            const accent = stanceColor(st);
            return (
              <section
                key={st}
                className="rounded overflow-hidden"
                style={{
                  background: "var(--bg-elevated)",
                  border: "1px solid var(--border-subtle)",
                  borderTop: `2px solid ${accent}`,
                }}
              >
                <div
                  className="px-4 py-3 flex items-center justify-between"
                  style={{ borderBottom: "1px solid var(--border-subtle)" }}
                >
                  <div className="flex items-center gap-3">
                    <h2
                      className="text-sm font-semibold"
                      style={{ color: "var(--text-primary)" }}
                    >
                      {STANCE_LABEL[st]}
                    </h2>
                    <span
                      className={`pill pill-solid pill-${stanceVariant(st)}`}
                    >
                      {items.length}
                    </span>
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-px"
                  style={{ background: "var(--border-subtle)" }}
                >
                  {items
                    .sort((a, b) => a.ticker.localeCompare(b.ticker))
                    .map((e) => (
                      <CouncilCard key={e.ticker} e={e} />
                    ))}
                </div>
              </section>
            );
          })}

          {/* Earlier runs --------------------------------------- */}
          {previous.length > 0 && (
            <section
              className="rounded overflow-hidden"
              style={{
                background: "var(--bg-elevated)",
                border: "1px solid var(--border-subtle)",
              }}
            >
              <div
                className="px-4 py-3 flex items-center justify-between"
                style={{ borderBottom: "1px solid var(--border-subtle)" }}
              >
                <h2
                  className="text-sm font-semibold"
                  style={{ color: "var(--text-primary)" }}
                >
                  Earlier runs
                </h2>
                <span
                  className="text-[10px]"
                  style={{ color: "var(--text-tertiary)" }}
                >
                  {previous.length} entradas
                </span>
              </div>
              <div className="max-h-[360px] overflow-y-auto">
                <table className="w-full">
                  <thead className="sticky top-0">
                    <tr
                      className="text-[10px]"
                      style={{
                        color: "var(--text-label)",
                        background: "var(--bg-overlay)",
                        borderBottom: "1px solid var(--border-subtle)",
                      }}
                    >
                      <th className="text-left px-4 py-2 font-semibold">
                        Data
                      </th>
                      <th className="text-left px-3 py-2 font-semibold">
                        Ticker
                      </th>
                      <th className="text-center px-3 py-2 font-semibold">
                        Stance
                      </th>
                      <th className="text-center px-3 py-2 font-semibold">
                        Conf
                      </th>
                      <th className="text-left px-3 py-2 font-semibold">
                        Setor
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {previous.slice(0, 120).map((e) => (
                      <tr
                        key={`${e.ticker}-${e.date}`}
                        className="hover:bg-[var(--jpm-card-hover)] transition-colors"
                        style={{
                          borderBottom: "1px solid var(--border-subtle)",
                        }}
                      >
                        <td
                          className="px-4 py-1.5 text-xs font-data"
                          style={{ color: "var(--text-tertiary)" }}
                        >
                          {formatDate(e.date, "short")}
                        </td>
                        <td className="px-3 py-1.5">
                          <Link
                            href={`/council/${e.ticker}`}
                            className="text-xs font-data font-bold hover:underline"
                            style={{ color: "var(--text-primary)" }}
                          >
                            {e.ticker}
                          </Link>
                        </td>
                        <td className="px-3 py-1.5 text-center">
                          <span
                            className={`pill pill-${stanceVariant(e.stance)}`}
                          >
                            {e.stance.replace("_", " ")}
                          </span>
                        </td>
                        <td
                          className="px-3 py-1.5 text-center text-xs font-data"
                          style={{ color: "var(--text-secondary)" }}
                        >
                          {e.confidence}
                        </td>
                        <td
                          className="px-3 py-1.5 text-xs"
                          style={{ color: "var(--text-tertiary)" }}
                        >
                          {e.sector || "—"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}
        </>
      )}
    </div>
  );
}

// ─── Components ──────────────────────────────────────────────────────

function CountBlock({
  label,
  n,
  variant,
}: {
  label: string;
  n: number;
  variant?: "buy" | "hold" | "avoid" | "na";
}) {
  const color =
    variant === "buy"
      ? "var(--verdict-buy)"
      : variant === "hold"
      ? "var(--verdict-hold)"
      : variant === "avoid"
      ? "var(--verdict-avoid)"
      : variant === "na"
      ? "var(--verdict-na)"
      : "var(--text-primary)";
  return (
    <div
      className="p-4 rounded"
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
      }}
    >
      <p
        className="text-[10px] font-semibold tracking-wider uppercase mb-1.5"
        style={{ color: "var(--text-label)" }}
      >
        {label}
      </p>
      <p className="text-2xl font-display font-bold" style={{ color }}>
        {n}
      </p>
    </div>
  );
}

function CouncilCard({ e }: { e: CouncilEntry }) {
  const accent = stanceColor(e.stance);
  return (
    <Link
      href={`/council/${e.ticker}`}
      className="block p-4 hover:bg-[var(--jpm-card-hover)] transition-colors"
      style={{ background: "var(--bg-elevated)" }}
    >
      <div className="flex items-center justify-between mb-2">
        <h3
          className="text-base font-data font-bold"
          style={{ color: "var(--text-primary)" }}
        >
          {e.ticker}
        </h3>
        <span className={`pill pill-solid pill-${stanceVariant(e.stance)}`}>
          {e.stance.replace("_", " ")}
        </span>
      </div>
      <div className="flex items-center gap-2 flex-wrap mb-2">
        {e.market && (
          <span
            className={`pill pill-${e.market === "br" ? "mkt-br" : "mkt-us"}`}
          >
            {String(e.market).toUpperCase()}
          </span>
        )}
        {e.is_holding && <span className="pill pill-gold">HOLDING</span>}
        {e.modo && (
          <span
            className="text-[10px]"
            style={{ color: "var(--text-tertiary)" }}
          >
            modo {e.modo}
          </span>
        )}
      </div>
      {(e.dissent_count > 0 || e.flag_count > 0) && (
        <div className="flex gap-2 mb-1.5">
          {e.dissent_count > 0 && (
            <span className="pill pill-hold">
              ◇ {e.dissent_count} dissent
            </span>
          )}
          {e.flag_count > 0 && (
            <span className="pill pill-avoid">⚑ {e.flag_count} flag</span>
          )}
        </div>
      )}
      {e.philosophy_primary && (
        <p
          className="text-[11px] leading-snug truncate"
          style={{ color: "var(--text-tertiary)" }}
          title={e.philosophy_primary}
        >
          {e.philosophy_primary}
        </p>
      )}
      {e.margin_of_safety !== null && (
        <p
          className="text-[11px] font-data mt-1"
          style={{ color: "var(--text-secondary)" }}
        >
          MoS{" "}
          <span style={{ color: accent }}>
            {(e.margin_of_safety * 100).toFixed(1)}%
          </span>
        </p>
      )}
    </Link>
  );
}
