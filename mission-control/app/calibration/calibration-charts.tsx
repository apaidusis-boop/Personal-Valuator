"use client";

import {
  BarChart,
  Bar,
  CartesianGrid,
  Cell,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { CalibrationSummary } from "@/lib/db";

function NarrowAxis({ orientation }: { orientation: "x" | "y" }) {
  const props =
    orientation === "x"
      ? { tick: { fontSize: 11, fill: "var(--text-tertiary)" }, dataKey: "bin_label" as const }
      : { tick: { fontSize: 11, fill: "var(--text-tertiary)" }, domain: [0, 100] as [number, number] };
  return orientation === "x" ? <XAxis {...props} /> : <YAxis {...props} unit="%" />;
}

export default function CalibrationCharts({
  us,
  br,
}: {
  us: CalibrationSummary;
  br: CalibrationSummary;
}) {
  return (
    <section className="grid grid-cols-2 gap-6">
      {[us, br].map((d) => (
        <div
          key={`chart-${d.market}`}
          className="rounded border p-4"
          style={{
            background: "var(--bg-card)",
            borderColor: "var(--border-subtle)",
          }}
        >
          <h3
            className="text-sm font-semibold uppercase tracking-wide mb-3"
            style={{ color: "var(--text-secondary)" }}
          >
            {d.market} — Calibration curve
          </h3>
          <div style={{ width: "100%", height: 240 }}>
            <ResponsiveContainer>
              <BarChart
                data={d.calibration.map((b) => ({
                  bin_label: b.bin_label,
                  hit_rate: b.hit_rate_pct ?? 0,
                  n: b.n,
                }))}
                margin={{ top: 10, right: 16, bottom: 4, left: -10 }}
              >
                <CartesianGrid stroke="var(--border-subtle)" strokeDasharray="3 3" />
                <NarrowAxis orientation="x" />
                <NarrowAxis orientation="y" />
                <Tooltip
                  contentStyle={{
                    background: "var(--bg-canvas)",
                    border: "1px solid var(--border-subtle)",
                    fontSize: 12,
                  }}
                />
                <Bar dataKey="hit_rate" name="Hit %">
                  {d.calibration.map((b, i) => (
                    <Cell
                      key={`${b.bin_label}-${i}`}
                      fill={
                        b.n === 0
                          ? "var(--text-tertiary)"
                          : (b.hit_rate_pct ?? 0) >= 60
                          ? "var(--gain)"
                          : (b.hit_rate_pct ?? 0) < 30
                          ? "var(--loss)"
                          : "var(--accent)"
                      }
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <h3
            className="text-sm font-semibold uppercase tracking-wide mt-4 mb-3"
            style={{ color: "var(--text-secondary)" }}
          >
            {d.market} — Engine BUY hit %
          </h3>
          <div style={{ width: "100%", height: 200 }}>
            <ResponsiveContainer>
              <BarChart
                data={d.engine_attribution
                  .filter((e) => e.verdict === "BUY")
                  .map((e) => ({
                    engine: e.engine,
                    hit_rate_pct: e.hit_rate_pct,
                    n: e.n,
                  }))}
                margin={{ top: 10, right: 16, bottom: 4, left: -10 }}
              >
                <CartesianGrid stroke="var(--border-subtle)" strokeDasharray="3 3" />
                <XAxis dataKey="engine" tick={{ fontSize: 11, fill: "var(--text-tertiary)" }} />
                <YAxis
                  tick={{ fontSize: 11, fill: "var(--text-tertiary)" }}
                  domain={[0, 100]}
                  unit="%"
                />
                <Tooltip
                  contentStyle={{
                    background: "var(--bg-canvas)",
                    border: "1px solid var(--border-subtle)",
                    fontSize: 12,
                  }}
                />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                <Bar dataKey="hit_rate_pct" name="Hit % (BUY only)" fill="var(--gain)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      ))}
    </section>
  );
}
