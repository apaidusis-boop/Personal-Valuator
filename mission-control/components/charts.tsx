"use client";

import { useEffect, useState } from "react";
import {
  LineChart, Line, AreaChart, Area, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from "recharts";

// ─── Per-ticker price chart ────────────────────────────────────────────────

export function PriceChart({ ticker, days = 365, height = 220 }: {
  ticker: string;
  days?: number;
  height?: number;
}) {
  const [data, setData] = useState<{ date: string; close: number }[]>([]);
  const [meta, setMeta] = useState<{ name?: string; market?: string }>({});
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    fetch(`/api/prices/${ticker}?days=${days}`)
      .then((r) => r.json())
      .then((j) => {
        if (!alive) return;
        if (j.error) setErr(j.error);
        else {
          setData(j.series || []);
          setMeta({ name: j.name, market: j.market });
        }
      })
      .catch((e) => alive && setErr(String(e)))
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, [ticker, days]);

  if (loading) return <div className="h-[200px] grid place-items-center text-zinc-600 text-xs">loading {ticker}…</div>;
  if (err) return <div className="text-red-400 text-xs font-mono">{err}</div>;
  if (data.length === 0) return <div className="text-zinc-500 text-xs italic">sem dados de preço</div>;

  const cur = meta.market === "br" ? "R$" : "US$";
  const first = data[0]?.close || 1;
  const last = data[data.length - 1]?.close || 1;
  const pct = ((last / first - 1) * 100).toFixed(1);
  const positive = last >= first;

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <div className="text-xs font-mono text-zinc-400">
          <span className="text-cyan-300">{ticker}</span>
          {meta.name && <span className="ml-2 text-zinc-500">{meta.name}</span>}
        </div>
        <div className={"text-xs font-mono tabular " + (positive ? "text-green-400" : "text-red-400")}>
          {cur}{last.toFixed(2)} · {positive ? "+" : ""}{pct}% / {days}d
        </div>
      </div>
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
          <CartesianGrid stroke="#1f1f3d" strokeDasharray="3 3" />
          <XAxis dataKey="date" stroke="#6b6b8c" fontSize={10}
            tick={{ fontFamily: "monospace" }}
            tickFormatter={(v: string) => v.slice(5)}
            interval="preserveStartEnd"
          />
          <YAxis stroke="#6b6b8c" fontSize={10}
            tick={{ fontFamily: "monospace" }}
            domain={["auto", "auto"]}
            tickFormatter={(v: number) => v.toFixed(0)}
          />
          <Tooltip
            contentStyle={{ background: "#11112a", border: "1px solid #1f1f3d", fontSize: 11 }}
            labelStyle={{ color: "#a855f7", fontFamily: "monospace" }}
            formatter={(v: any) => [`${cur}${Number(v).toFixed(2)}`, "close"]}
          />
          <Line type="monotone" dataKey="close"
            stroke={positive ? "#4ade80" : "#f87171"}
            strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

// ─── Portfolio P&L chart ───────────────────────────────────────────────────

export function PortfolioChart({ height = 250 }: { height?: number }) {
  const [data, setData] = useState<{
    br: { date: string; mv: number; cost: number }[];
    us: { date: string; mv: number; cost: number }[];
    source?: string;
  }>({ br: [], us: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    fetch("/api/portfolio/timeseries")
      .then((r) => r.json())
      .then((j) => alive && setData(j))
      .catch(() => {})
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, []);

  if (loading) return <div className="h-[230px] grid place-items-center text-zinc-600 text-xs">loading portfolio…</div>;

  // Pick the longer series; if both exist render both as separate sub-charts
  const hasBR = data.br.length > 1;
  const hasUS = data.us.length > 1;
  if (!hasBR && !hasUS) {
    return <div className="text-zinc-500 text-xs italic">sem timeseries — corre <code>ii snapshot --backfill 90</code></div>;
  }

  return (
    <div className="space-y-3">
      {hasBR && <PFSubChart label="BR · BRL" data={data.br} stroke="#4ade80" height={height} />}
      {hasUS && <PFSubChart label="US · USD" data={data.us} stroke="#4dd4ff" height={height} />}
      {data.source && <div className="text-[9px] font-mono text-zinc-600">source: {data.source}</div>}
    </div>
  );
}

function PFSubChart({ label, data, stroke, height }: {
  label: string;
  data: { date: string; mv: number; cost: number }[];
  stroke: string;
  height: number;
}) {
  const last = data[data.length - 1];
  const cost = last?.cost || 0;
  const mv = last?.mv || 0;
  const pnl = cost ? ((mv / cost - 1) * 100).toFixed(1) : "—";
  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs font-mono text-zinc-400">{label}</span>
        <span className="text-xs font-mono tabular" style={{ color: mv >= cost ? "#4ade80" : "#f87171" }}>
          mv {mv.toFixed(0)} · {pnl}% vs cost
        </span>
      </div>
      <ResponsiveContainer width="100%" height={height}>
        <AreaChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
          <CartesianGrid stroke="#1f1f3d" strokeDasharray="3 3" />
          <XAxis dataKey="date" stroke="#6b6b8c" fontSize={10}
            tickFormatter={(v: string) => v.slice(5)}
            interval="preserveStartEnd"
          />
          <YAxis stroke="#6b6b8c" fontSize={10} tickFormatter={(v: number) => `${(v / 1000).toFixed(0)}k`} />
          <Tooltip
            contentStyle={{ background: "#11112a", border: "1px solid #1f1f3d", fontSize: 11 }}
            formatter={(v: any, n: any) => [Number(v).toFixed(0), String(n)]}
          />
          <Legend wrapperStyle={{ fontSize: 10, fontFamily: "monospace" }} />
          <Area type="monotone" dataKey="cost" name="cost" stroke="#6b6b8c" fill="#6b6b8c20" strokeDasharray="4 4" />
          <Area type="monotone" dataKey="mv" name="mv" stroke={stroke} fill={`${stroke}30`} strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
