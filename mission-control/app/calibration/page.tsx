import type { Metadata } from "next";
import { getCalibrationData } from "@/lib/db";
import CalibrationCharts from "./calibration-charts";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Calibration · Mission Control" };

function fmtPct(v: number | null, digits = 1) {
  if (v === null || v === undefined || Number.isNaN(v)) return "—";
  return `${v.toFixed(digits)}%`;
}

export default async function CalibrationPage() {
  const us = getCalibrationData("us");
  const br = getCalibrationData("br");

  return (
    <div className="px-8 py-6">
      <header className="mb-6">
        <h1 className="text-2xl font-semibold" style={{ color: "var(--text-primary)" }}>
          Calibration
        </h1>
        <p className="mt-1 text-sm" style={{ color: "var(--text-secondary)" }}>
          Phase FF closed-loop validation. <strong>Hit-rate</strong> = directional accuracy
          of the verdict (BUY/AVOID checked against return sign; HOLD checked against
          ±5% band). <strong>n=closed</strong> means the outcome window has elapsed and
          the realized return is recorded.
        </p>
      </header>

      <div className="grid grid-cols-2 gap-6 mb-6">
        {[us, br].map((d) => (
          <div
            key={d.market}
            className="rounded border p-4"
            style={{
              background: "var(--bg-card)",
              borderColor: "var(--border-subtle)",
            }}
          >
            <h2
              className="text-base font-semibold uppercase tracking-wide mb-3"
              style={{ color: "var(--text-primary)" }}
            >
              {d.market}
            </h2>
            <div className="flex gap-6 text-sm" style={{ color: "var(--text-secondary)" }}>
              <span>
                Total verdicts: <strong style={{ color: "var(--text-primary)" }}>{d.n_total}</strong>
              </span>
              <span>
                Closed: <strong style={{ color: "var(--text-primary)" }}>{d.n_closed}</strong>
              </span>
              <span>
                Pending: <strong style={{ color: "var(--text-primary)" }}>{d.n_total - d.n_closed}</strong>
              </span>
            </div>
          </div>
        ))}
      </div>

      <CalibrationCharts us={us} br={br} />

      <section className="mt-8 grid grid-cols-2 gap-6">
        {[us, br].map((d) => (
          <div key={`tbl-${d.market}`}>
            <h3
              className="text-sm font-semibold uppercase tracking-wide mb-2"
              style={{ color: "var(--text-secondary)" }}
            >
              {d.market} — Calibration buckets
            </h3>
            <div
              className="rounded border overflow-hidden"
              style={{ borderColor: "var(--border-subtle)" }}
            >
              <table className="w-full text-sm">
                <thead style={{ background: "var(--bg-canvas)" }}>
                  <tr>
                    <th className="text-left px-3 py-2" style={{ color: "var(--text-tertiary)" }}>Bin</th>
                    <th className="text-right px-3 py-2" style={{ color: "var(--text-tertiary)" }}>n</th>
                    <th className="text-right px-3 py-2" style={{ color: "var(--text-tertiary)" }}>Hit %</th>
                    <th className="text-right px-3 py-2" style={{ color: "var(--text-tertiary)" }}>Med. ret</th>
                    <th className="text-right px-3 py-2" style={{ color: "var(--text-tertiary)" }}>vs Bench</th>
                  </tr>
                </thead>
                <tbody>
                  {d.calibration.map((b) => (
                    <tr
                      key={b.bin_label}
                      style={{ borderTop: "1px solid var(--border-subtle)" }}
                    >
                      <td className="px-3 py-2" style={{ color: "var(--text-primary)" }}>
                        {b.bin_label}
                      </td>
                      <td className="px-3 py-2 text-right" style={{ color: "var(--text-primary)" }}>
                        {b.n}
                      </td>
                      <td className="px-3 py-2 text-right" style={{ color: "var(--text-primary)" }}>
                        {fmtPct(b.hit_rate_pct)}
                      </td>
                      <td className="px-3 py-2 text-right" style={{ color: "var(--text-primary)" }}>
                        {fmtPct(b.median_return_pct)}
                      </td>
                      <td className="px-3 py-2 text-right" style={{ color: "var(--text-primary)" }}>
                        {fmtPct(b.median_vs_bench_pct)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </section>

      <section className="mt-8">
        <h3
          className="text-sm font-semibold uppercase tracking-wide mb-2"
          style={{ color: "var(--text-secondary)" }}
        >
          Per-engine attribution
        </h3>
        <div className="grid grid-cols-2 gap-6">
          {[us, br].map((d) => (
            <div key={`eng-${d.market}`}>
              <p
                className="text-xs uppercase mb-2"
                style={{ color: "var(--text-tertiary)" }}
              >
                {d.market} ({d.engine_attribution.length} engine×verdict cells)
              </p>
              <div
                className="rounded border overflow-hidden"
                style={{ borderColor: "var(--border-subtle)" }}
              >
                <table className="w-full text-sm">
                  <thead style={{ background: "var(--bg-canvas)" }}>
                    <tr>
                      <th className="text-left px-3 py-2" style={{ color: "var(--text-tertiary)" }}>Engine</th>
                      <th className="text-left px-3 py-2" style={{ color: "var(--text-tertiary)" }}>Verdict</th>
                      <th className="text-right px-3 py-2" style={{ color: "var(--text-tertiary)" }}>n</th>
                      <th className="text-right px-3 py-2" style={{ color: "var(--text-tertiary)" }}>Hit %</th>
                    </tr>
                  </thead>
                  <tbody>
                    {d.engine_attribution.map((r, i) => (
                      <tr
                        key={`${r.engine}-${r.verdict}-${i}`}
                        style={{ borderTop: "1px solid var(--border-subtle)" }}
                      >
                        <td className="px-3 py-2" style={{ color: "var(--text-primary)" }}>
                          {r.engine}
                        </td>
                        <td className="px-3 py-2" style={{ color: "var(--text-primary)" }}>
                          {r.verdict}
                        </td>
                        <td className="px-3 py-2 text-right" style={{ color: "var(--text-primary)" }}>
                          {r.n}
                        </td>
                        <td
                          className="px-3 py-2 text-right font-medium"
                          style={{
                            color:
                              r.hit_rate_pct >= 60
                                ? "var(--gain)"
                                : r.hit_rate_pct < 30
                                ? "var(--loss)"
                                : "var(--text-primary)",
                          }}
                        >
                          {fmtPct(r.hit_rate_pct)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
