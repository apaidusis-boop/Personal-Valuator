import type { Metadata } from "next";
import { listPerpetuumStatus, listRecentPerpetuumRuns } from "@/lib/db";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Perpetuums · Mission Control" };

function tierTone(tier: string | null): string {
  if (tier === "T1") return "var(--text-secondary)";   // Observer
  if (tier === "T2") return "var(--accent)";            // Proposer
  if (tier === "T3" || tier === "T4" || tier === "T5") return "var(--gain)";
  return "var(--text-tertiary)";
}

function scoreTone(s: number | null): string {
  if (s === null) return "var(--text-tertiary)";
  if (s >= 80) return "var(--gain)";
  if (s >= 60) return "var(--text-primary)";
  if (s >= 40) return "var(--accent)";
  return "var(--loss)";
}

function fmtDuration(sec: number | null): string {
  if (sec === null) return "—";
  if (sec < 1) return `${Math.round(sec * 1000)}ms`;
  if (sec < 60) return `${sec.toFixed(1)}s`;
  return `${Math.floor(sec / 60)}m ${Math.round(sec % 60)}s`;
}

function lastRunFreshness(date: string | null): { tone: string; label: string } {
  if (!date) return { tone: "var(--loss)", label: "never" };
  const d = new Date(date);
  const days = (Date.now() - d.getTime()) / 86400000;
  if (days < 1) return { tone: "var(--gain)", label: "today" };
  if (days < 2) return { tone: "var(--gain)", label: "yesterday" };
  if (days < 7) return { tone: "var(--accent)", label: `${Math.round(days)}d ago` };
  return { tone: "var(--loss)", label: `${Math.round(days)}d ago` };
}

export default async function PerpetuumsPage() {
  const status = listPerpetuumStatus();
  const recent = listRecentPerpetuumRuns(40);

  const totalSubjects = status.reduce((acc, p) => acc + (p.subjects_count || 0), 0);
  const totalAlerts = status.reduce((acc, p) => acc + (p.alerts_count || 0), 0);
  const totalActions = status.reduce((acc, p) => acc + p.open_actions, 0);
  const totalErrors = status.reduce((acc, p) => acc + (p.errors_count || 0), 0);

  return (
    <div className="px-8 py-6">
      <header className="mb-6">
        <h1 className="text-2xl font-semibold" style={{ color: "var(--text-primary)" }}>
          Perpetuums
        </h1>
        <p className="mt-1 text-sm" style={{ color: "var(--text-secondary)" }}>
          Phase X engine — {status.length} perpetuums. Tier <strong>T1</strong> Observer ·{" "}
          <strong>T2</strong> Proposer · <strong>T3+</strong> Executor (per Phase FF Bloco 3.2
          proposal in <code>config/action_safety.yaml</code>).
        </p>
      </header>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <KPI label="Subjects scored (last run)" value={totalSubjects.toString()} />
        <KPI
          label="Alerts surfaced"
          value={totalAlerts.toString()}
          tone={totalAlerts > 0 ? "var(--accent)" : "var(--text-primary)"}
        />
        <KPI
          label="Open actions"
          value={totalActions.toString()}
          tone={totalActions > 0 ? "var(--accent)" : "var(--text-primary)"}
        />
        <KPI
          label="Errors"
          value={totalErrors.toString()}
          tone={totalErrors > 0 ? "var(--loss)" : "var(--gain)"}
        />
      </div>

      <section className="mb-8">
        <h2
          className="text-sm font-semibold uppercase tracking-wide mb-2"
          style={{ color: "var(--text-secondary)" }}
        >
          Status per perpetuum
        </h2>
        <div
          className="rounded border overflow-hidden"
          style={{ borderColor: "var(--border-subtle)" }}
        >
          <table className="w-full text-sm">
            <thead style={{ background: "var(--bg-canvas)" }}>
              <tr>
                <Th>Name</Th>
                <Th align="center">Tier</Th>
                <Th align="center">Last run</Th>
                <Th align="right">Duration</Th>
                <Th align="right">Subjects</Th>
                <Th align="right">Avg score</Th>
                <Th align="right">Low (&lt;60)</Th>
                <Th align="right">Alerts</Th>
                <Th align="right">Open actions</Th>
                <Th align="right">Errors</Th>
              </tr>
            </thead>
            <tbody>
              {status.map((p) => {
                const fresh = lastRunFreshness(p.last_run);
                return (
                  <tr
                    key={p.name}
                    style={{ borderTop: "1px solid var(--border-subtle)" }}
                  >
                    <Td>
                      <code style={{ color: "var(--text-primary)" }}>{p.name}</code>
                    </Td>
                    <Td align="center">
                      <span
                        className="px-2 py-0.5 rounded text-xs font-semibold"
                        style={{
                          color: tierTone(p.tier),
                          border: `1px solid ${tierTone(p.tier)}`,
                        }}
                      >
                        {p.tier ?? "—"}
                      </span>
                    </Td>
                    <Td align="center">
                      <span style={{ color: fresh.tone }}>{fresh.label}</span>
                    </Td>
                    <Td align="right">{fmtDuration(p.duration_sec)}</Td>
                    <Td align="right">{p.subjects_count ?? "—"}</Td>
                    <Td align="right">
                      <span style={{ color: scoreTone(p.median_score) }}>
                        {p.median_score?.toFixed(1) ?? "—"}
                      </span>
                    </Td>
                    <Td align="right">
                      <span
                        style={{
                          color: p.low_subjects > 0 ? "var(--accent)" : "var(--text-tertiary)",
                        }}
                      >
                        {p.low_subjects}
                      </span>
                    </Td>
                    <Td align="right">
                      <span
                        style={{
                          color:
                            (p.alerts_count || 0) > 0
                              ? "var(--accent)"
                              : "var(--text-tertiary)",
                        }}
                      >
                        {p.alerts_count ?? 0}
                      </span>
                    </Td>
                    <Td align="right">
                      <span
                        style={{
                          color:
                            p.open_actions > 0 ? "var(--accent)" : "var(--text-tertiary)",
                        }}
                      >
                        {p.open_actions}
                      </span>
                    </Td>
                    <Td align="right">
                      <span
                        style={{
                          color:
                            (p.errors_count || 0) > 0 ? "var(--loss)" : "var(--text-tertiary)",
                        }}
                      >
                        {p.errors_count ?? 0}
                      </span>
                    </Td>
                  </tr>
                );
              })}
              {status.length === 0 && (
                <tr>
                  <td
                    colSpan={10}
                    className="px-3 py-6 text-center"
                    style={{ color: "var(--text-tertiary)" }}
                  >
                    No perpetuum runs recorded yet. Trigger via{" "}
                    <code>python agents/perpetuum_master.py</code>.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section>
        <h2
          className="text-sm font-semibold uppercase tracking-wide mb-2"
          style={{ color: "var(--text-secondary)" }}
        >
          Recent runs ({recent.length})
        </h2>
        <div
          className="rounded border overflow-hidden"
          style={{ borderColor: "var(--border-subtle)" }}
        >
          <table className="w-full text-sm">
            <thead style={{ background: "var(--bg-canvas)" }}>
              <tr>
                <Th>Started</Th>
                <Th>Perpetuum</Th>
                <Th align="right">Duration</Th>
                <Th align="right">Subjects</Th>
                <Th align="right">Alerts</Th>
                <Th align="right">Errors</Th>
                <Th>Summary</Th>
              </tr>
            </thead>
            <tbody>
              {recent.map((r, i) => (
                <tr
                  key={`${r.perpetuum_name}-${r.started_at}-${i}`}
                  style={{ borderTop: "1px solid var(--border-subtle)" }}
                >
                  <Td>
                    <span
                      className="text-xs"
                      style={{ color: "var(--text-tertiary)" }}
                    >
                      {r.started_at?.slice(0, 16).replace("T", " ")}
                    </span>
                  </Td>
                  <Td>
                    <code style={{ color: "var(--text-primary)" }}>
                      {r.perpetuum_name}
                    </code>
                  </Td>
                  <Td align="right">{fmtDuration(r.duration_sec)}</Td>
                  <Td align="right">{r.subjects_count ?? "—"}</Td>
                  <Td align="right">
                    <span
                      style={{
                        color:
                          (r.alerts_count || 0) > 0
                            ? "var(--accent)"
                            : "var(--text-tertiary)",
                      }}
                    >
                      {r.alerts_count ?? 0}
                    </span>
                  </Td>
                  <Td align="right">
                    <span
                      style={{
                        color:
                          (r.errors_count || 0) > 0
                            ? "var(--loss)"
                            : "var(--text-tertiary)",
                      }}
                    >
                      {r.errors_count ?? 0}
                    </span>
                  </Td>
                  <Td>
                    <span
                      className="text-xs"
                      style={{ color: "var(--text-secondary)" }}
                    >
                      {r.summary?.slice(0, 90)}
                    </span>
                  </Td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function KPI({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone?: string;
}) {
  return (
    <div
      className="rounded border p-4"
      style={{
        background: "var(--bg-card)",
        borderColor: "var(--border-subtle)",
      }}
    >
      <div
        className="text-xs uppercase tracking-wide"
        style={{ color: "var(--text-tertiary)" }}
      >
        {label}
      </div>
      <div
        className="text-2xl font-semibold mt-1"
        style={{ color: tone || "var(--text-primary)" }}
      >
        {value}
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
