"use client";

import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

type Slice = {
  name: string;
  value: number;
  pct: number;
  color: string;
};

export function DiversificationPie({
  data,
  total,
  currency = "BRL",
}: {
  data: Slice[];
  total: number;
  currency?: "BRL" | "USD";
}) {
  const fmt = (v: number) =>
    v.toLocaleString(currency === "BRL" ? "pt-BR" : "en-US", {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
      notation: total >= 1_000_000 ? "compact" : "standard",
    });

  return (
    <div className="flex items-center gap-4">
      <div className="w-[140px] h-[140px] shrink-0">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={40}
              outerRadius={65}
              dataKey="value"
              stroke="none"
              isAnimationActive={false}
            >
              {data.map((slice, i) => (
                <Cell key={i} fill={slice.color} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="flex-1 space-y-1.5 min-w-0">
        {data.map((slice) => (
          <div key={slice.name} className="flex items-center gap-2 text-xs">
            <span
              className="w-2.5 h-2.5 rounded-full shrink-0"
              style={{ background: slice.color }}
            />
            <span
              className="truncate"
              style={{ color: "var(--text-tertiary)" }}
            >
              {slice.name}
            </span>
            <span
              className="font-data ml-auto shrink-0"
              style={{ color: "var(--text-primary)" }}
            >
              {slice.pct.toFixed(1)}%
            </span>
          </div>
        ))}
        <div
          className="pt-2 mt-2"
          style={{ borderTop: "1px solid var(--border-subtle)" }}
        >
          <p
            className="text-base font-display font-bold"
            style={{ color: "var(--text-primary)" }}
          >
            {fmt(total)}
          </p>
          <p className="text-[10px]" style={{ color: "var(--text-tertiary)" }}>
            Total BR
          </p>
        </div>
      </div>
    </div>
  );
}
