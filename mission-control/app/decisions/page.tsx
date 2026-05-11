import type { Metadata } from "next";
import Link from "next/link";
import { listVerdicts } from "@/lib/db";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Decisions · Mission Control" };

function fmtPct(v: number | null, digits = 1) {
  if (v === null || v === undefined || Number.isNaN(v)) return "—";
  const s = v.toFixed(digits);
  return v > 0 ? `+${s}%` : `${s}%`;
}

function pctColor(v: number | null): string {
  if (v === null) return "var(--text-tertiary)";
  if (v > 0) return "var(--gain)";
  if (v < 0) return "var(--loss)";
  return "var(--text-primary)";
}

function actionTone(action: string): string {
  if (action === "BUY" || action === "ADD") return "var(--gain)";
  if (action === "AVOID" || action === "SELL") return "var(--loss)";
  if (action === "WATCH") return "var(--accent)";
  return "var(--text-secondary)";
}

function accuracyDot(a: number | null) {
  if (a === null) return { dot: "○", label: "pending", color: "var(--text-tertiary)" };
  if (a === 1) return { dot: "●", label: "hit", color: "var(--gain)" };
  return { dot: "●", label: "miss", color: "var(--loss)" };
}

export default async function DecisionsPage({
  searchParams,
}: {
  searchParams: Promise<{ market?: string; status?: string }>;
}) {
  const sp = await searchParams;
  const market = sp.market === "us" || sp.market === "br" ? sp.market : undefined;
  const status = sp.status; // 'closed' | 'open' | undefined

  const closed = status === "closed" ? true : status === "open" ? false : undefined;
  const rows = listVerdicts({ market, closed, limit: 300 });

  const closedCount = rows.filter((r) => r.outcome_return_pct !== null).length;
  const hits = rows.filter((r) => r.accuracy === 1).length;
  const misses = rows.filter((r) => r.accuracy === 0).length;

  return (
    <div className="px-8 py-6">
      <header className="mb-4 flex items-end justify-between">
        <div>
          <h1
            className="text-2xl font-semibold"
            style={{ color: "var(--text-primary)" }}
          >
            Decisions
          </h1>
          <p
            className="mt-1 text-sm"
            style={{ color: "var(--text-secondary)" }}
          >
            Verdict history with realized outcomes. {rows.length} rows · {closedCount} closed ·{" "}
            {hits} hits · {misses} misses
          </p>
        </div>
        <div className="flex gap-2 text-xs">
          <FilterChip label="All markets" href="/decisions" active={!market} />
          <FilterChip label="US" href="/decisions?market=us" active={market === "us"} />
          <FilterChip label="BR" href="/decisions?market=br" active={market === "br"} />
          <span className="px-1" style={{ color: "var(--border-subtle)" }}>|</span>
          <FilterChip label="All" href={market ? `/decisions?market=${market}` : "/decisions"} active={!status} />
          <FilterChip
            label="Closed"
            href={market ? `/decisions?market=${market}&status=closed` : "/decisions?status=closed"}
            active={status === "closed"}
          />
          <FilterChip
            label="Open"
            href={market ? `/decisions?market=${market}&status=open` : "/decisions?status=open"}
            active={status === "open"}
          />
        </div>
      </header>

      <div
        className="rounded border overflow-hidden"
        style={{ borderColor: "var(--border-subtle)" }}
      >
        <table className="w-full text-sm">
          <thead style={{ background: "var(--bg-canvas)" }}>
            <tr>
              <Th>Date</Th>
              <Th>Mkt</Th>
              <Th>Ticker</Th>
              <Th>Action</Th>
              <Th align="right">Score</Th>
              <Th align="right">Conf</Th>
              <Th align="right">Return</Th>
              <Th align="right">vs Bench</Th>
              <Th align="center">Outcome</Th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => {
              const acc = accuracyDot(r.accuracy);
              return (
                <tr
                  key={`${r.market}-${r.ticker}-${r.date}-${i}`}
                  style={{ borderTop: "1px solid var(--border-subtle)" }}
                >
                  <Td>{r.date}</Td>
                  <Td>
                    <span
                      className="text-xs uppercase"
                      style={{ color: "var(--text-tertiary)" }}
                    >
                      {r.market}
                    </span>
                  </Td>
                  <Td>
                    <Link
                      href={`/ticker/${r.ticker}`}
                      style={{ color: "var(--accent)", textDecoration: "underline" }}
                    >
                      {r.ticker}
                    </Link>
                  </Td>
                  <Td>
                    <span
                      className="font-medium"
                      style={{ color: actionTone(r.action) }}
                    >
                      {r.action}
                    </span>
                  </Td>
                  <Td align="right">{r.total_score?.toFixed(2) ?? "—"}</Td>
                  <Td align="right">{r.confidence_pct !== null ? `${r.confidence_pct}%` : "—"}</Td>
                  <Td align="right">
                    <span style={{ color: pctColor(r.outcome_return_pct) }}>
                      {fmtPct(r.outcome_return_pct)}
                    </span>
                  </Td>
                  <Td align="right">
                    <span style={{ color: pctColor(r.return_vs_benchmark_pct) }}>
                      {fmtPct(r.return_vs_benchmark_pct)}
                    </span>
                  </Td>
                  <Td align="center">
                    <span style={{ color: acc.color }} title={acc.label}>
                      {acc.dot} {acc.label}
                    </span>
                  </Td>
                </tr>
              );
            })}
            {rows.length === 0 && (
              <tr>
                <td
                  colSpan={9}
                  className="px-3 py-6 text-center"
                  style={{ color: "var(--text-tertiary)" }}
                >
                  No verdicts match the current filter.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Th({
  children,
  align = "left",
}: {
  children: React.ReactNode;
  align?: "left" | "right" | "center";
}) {
  return (
    <th
      className="px-3 py-2 text-xs uppercase tracking-wide"
      style={{ color: "var(--text-tertiary)", textAlign: align }}
    >
      {children}
    </th>
  );
}

function Td({
  children,
  align = "left",
}: {
  children: React.ReactNode;
  align?: "left" | "right" | "center";
}) {
  return (
    <td
      className="px-3 py-2"
      style={{ color: "var(--text-primary)", textAlign: align }}
    >
      {children}
    </td>
  );
}

function FilterChip({
  label,
  href,
  active,
}: {
  label: string;
  href: string;
  active: boolean;
}) {
  return (
    <Link
      href={href}
      className="px-3 py-1 rounded border"
      style={{
        background: active ? "var(--accent)" : "transparent",
        color: active ? "var(--bg-canvas)" : "var(--text-secondary)",
        borderColor: active ? "var(--accent)" : "var(--border-subtle)",
      }}
    >
      {label}
    </Link>
  );
}
