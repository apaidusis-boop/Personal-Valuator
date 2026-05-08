"use client";

// Client-side bits for /alerts: suggestion accept/dismiss, alert row actions.
// Bundled as a namespace import so the server page can render
// AlertsClient.Suggestions / AlertsClient.List / AlertsClient.History.

import { useState } from "react";
import { Check, X, Trash2, Bell } from "lucide-react";

import type { Alert } from "@/lib/alerts";
import { openTickerSheet } from "@/lib/ticker-sheet";
import { formatCurrency, formatDate } from "@/lib/format";

type Suggestion = {
  ticker: string;
  market: "br" | "us";
  fair_price: number;
  current_price: number;
  upside_pct: number;
  method: string;
  computed_at: string;
  threshold: number;
  direction: "above" | "below";
  rationale: string;
};

// ─── Suggestions ───────────────────────────────────────────────────────

export function Suggestions({ suggestions }: { suggestions: Suggestion[] }) {
  const [dismissed, setDismissed] = useState<Set<string>>(new Set());
  const [accepting, setAccepting] = useState<string | null>(null);
  const [accepted, setAccepted] = useState<Set<string>>(new Set());

  async function accept(s: Suggestion) {
    setAccepting(s.ticker);
    try {
      const res = await fetch("/api/alerts", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          ticker: s.ticker,
          market: s.market,
          kind: "fair_value_entry",
          direction: s.direction,
          threshold: s.threshold,
          current_price: s.current_price,
          source: `fair_value:${s.method}`,
          note: s.rationale,
        }),
      });
      if (res.ok) {
        setAccepted((p) => new Set(p).add(s.ticker));
      } else {
        alert(`Erro a criar alert: ${(await res.json())?.error || res.statusText}`);
      }
    } catch (e: any) {
      alert(`Erro: ${e?.message || e}`);
    } finally {
      setAccepting(null);
    }
  }

  function dismiss(ticker: string) {
    setDismissed((p) => new Set(p).add(ticker));
  }

  const visible = suggestions.filter(
    (s) => !dismissed.has(s.ticker) && !accepted.has(s.ticker)
  );

  if (visible.length === 0) {
    return (
      <div className="card p-8 text-center">
        <p className="type-body-sm italic" style={{ color: "var(--text-tertiary)" }}>
          Todas as sugestões foram tratadas.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
      {visible.map((s) => (
        <div key={s.ticker} className="card p-4">
          <div className="flex items-start justify-between gap-3 mb-2">
            <div>
              <button
                onClick={() => openTickerSheet(s.ticker)}
                style={{
                  background: "transparent",
                  border: 0,
                  padding: 0,
                  cursor: "pointer",
                  color: "var(--accent-primary)",
                  fontFamily: "var(--font-mono)",
                  fontSize: 15,
                  fontWeight: 600,
                  letterSpacing: "0.02em",
                }}
              >
                {s.ticker}
              </button>
              <p className="type-byline" style={{ marginTop: 2 }}>
                {s.market.toUpperCase()} · {s.method}
              </p>
            </div>
            <span
              style={{
                background: "var(--jpm-amber-soft)",
                color: "var(--verdict-hold)",
                padding: "3px 10px",
                borderRadius: 999,
                fontSize: 11,
                fontWeight: 600,
              }}
            >
              suggested
            </span>
          </div>

          <div
            className="grid grid-cols-3"
            style={{
              gap: 0,
              border: "1px solid var(--border-subtle)",
              borderRadius: 6,
              overflow: "hidden",
              marginBottom: 10,
            }}
          >
            <SuggestStat
              label="Current"
              value={formatCurrency(s.current_price, s.market === "br" ? "BRL" : "USD", 2)}
            />
            <SuggestStat
              label="Fair price"
              value={formatCurrency(s.fair_price, s.market === "br" ? "BRL" : "USD", 2)}
              accent="var(--accent-primary)"
              divide
            />
            <SuggestStat
              label="Upside"
              value={`${s.upside_pct >= 0 ? "+" : ""}${s.upside_pct.toFixed(1)}%`}
              accent={s.upside_pct >= 0 ? "var(--verdict-buy)" : "var(--verdict-avoid)"}
              divide
            />
          </div>

          <p
            className="type-body-sm"
            style={{ color: "var(--text-secondary)", marginBottom: 10 }}
          >
            {s.rationale}
          </p>

          <div className="flex items-center gap-2">
            <button
              onClick={() => accept(s)}
              disabled={accepting === s.ticker}
              style={{
                background: "var(--accent-primary)",
                color: "white",
                border: 0,
                padding: "6px 14px",
                borderRadius: 6,
                fontSize: 13,
                fontWeight: 500,
                cursor: accepting === s.ticker ? "wait" : "pointer",
                display: "inline-flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <Check size={13} /> Set alert
            </button>
            <button
              onClick={() => dismiss(s.ticker)}
              style={{
                background: "transparent",
                color: "var(--text-tertiary)",
                border: "1px solid var(--border-subtle)",
                padding: "6px 14px",
                borderRadius: 6,
                fontSize: 13,
                fontWeight: 500,
                cursor: "pointer",
                display: "inline-flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <X size={13} /> Ignore
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

function SuggestStat({
  label,
  value,
  accent,
  divide,
}: {
  label: string;
  value: string;
  accent?: string;
  divide?: boolean;
}) {
  return (
    <div
      style={{
        padding: "8px 12px",
        background: "var(--bg-overlay)",
        borderLeft: divide ? "1px solid var(--border-subtle)" : "0",
      }}
    >
      <p className="type-caption" style={{ marginBottom: 2 }}>
        {label}
      </p>
      <p
        className="font-data tabular"
        style={{
          fontSize: 13,
          fontWeight: 600,
          color: accent || "var(--text-primary)",
          margin: 0,
        }}
      >
        {value}
      </p>
    </div>
  );
}

// ─── Active list ───────────────────────────────────────────────────────

export function List({ alerts }: { alerts: Alert[] }) {
  const [items, setItems] = useState<Alert[]>(alerts);

  async function dismiss(id: string) {
    if (!confirm("Marcar como dismissed?")) return;
    const res = await fetch(`/api/alerts/${id}`, {
      method: "PATCH",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ status: "dismissed" }),
    });
    if (res.ok) setItems((p) => p.filter((a) => a.id !== id));
    else alert("Erro a dismissed");
  }

  async function remove(id: string) {
    if (!confirm("Apagar definitivamente?")) return;
    const res = await fetch(`/api/alerts/${id}`, { method: "DELETE" });
    if (res.ok) setItems((p) => p.filter((a) => a.id !== id));
    else alert("Erro a apagar");
  }

  if (items.length === 0) {
    return (
      <div className="card p-8 text-center">
        <p className="type-body-sm italic" style={{ color: "var(--text-tertiary)" }}>
          Sem alerts activos.
        </p>
      </div>
    );
  }

  return (
    <div className="card overflow-hidden">
      <table className="data-table">
        <thead>
          <tr>
            <th style={{ width: 110 }}>Ticker</th>
            <th style={{ width: 80 }}>Mkt</th>
            <th style={{ width: 80 }}>Kind</th>
            <th style={{ width: 90 }}>Direction</th>
            <th className="num">Threshold</th>
            <th>Source</th>
            <th style={{ width: 110 }}>Created</th>
            <th style={{ width: 130 }}></th>
          </tr>
        </thead>
        <tbody>
          {items.map((a) => (
            <tr key={a.id} style={{ cursor: "default" }}>
              <td>
                <button
                  onClick={() => openTickerSheet(a.ticker)}
                  style={{
                    background: "transparent",
                    border: 0,
                    padding: 0,
                    cursor: "pointer",
                    color: "var(--accent-primary)",
                    fontFamily: "var(--font-mono)",
                    fontSize: 13,
                    fontWeight: 600,
                  }}
                >
                  {a.ticker}
                </button>
              </td>
              <td
                style={{
                  color: a.market === "br" ? "var(--mkt-br)" : "var(--mkt-us)",
                  fontWeight: 600,
                  fontSize: 11,
                }}
              >
                {a.market.toUpperCase()}
              </td>
              <td className="type-byline">{a.kind}</td>
              <td className="type-byline" style={{ color: "var(--text-primary)" }}>
                {a.direction === "above" ? "above ↑" : "below ↓"}
              </td>
              <td className="num">
                {formatCurrency(a.threshold, a.market === "br" ? "BRL" : "USD", 2)}
              </td>
              <td className="type-byline" style={{ color: "var(--text-tertiary)" }}>
                {a.source}
                {a.note && (
                  <span
                    style={{ display: "block", color: "var(--text-secondary)", marginTop: 2 }}
                  >
                    {a.note}
                  </span>
                )}
              </td>
              <td className="type-byline">{formatDate(a.created_at, "relative")}</td>
              <td>
                <div className="flex items-center gap-2 justify-end">
                  <button
                    onClick={() => dismiss(a.id)}
                    title="Dismiss"
                    style={{
                      background: "transparent",
                      border: "1px solid var(--border-subtle)",
                      padding: "4px 8px",
                      borderRadius: 6,
                      cursor: "pointer",
                      color: "var(--text-tertiary)",
                    }}
                  >
                    <X size={12} />
                  </button>
                  <button
                    onClick={() => remove(a.id)}
                    title="Delete"
                    style={{
                      background: "transparent",
                      border: "1px solid var(--border-subtle)",
                      padding: "4px 8px",
                      borderRadius: 6,
                      cursor: "pointer",
                      color: "var(--verdict-avoid)",
                    }}
                  >
                    <Trash2 size={12} />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ─── History (triggered + dismissed) ───────────────────────────────────

export function History({ alerts }: { alerts: Alert[] }) {
  if (alerts.length === 0) return null;
  return (
    <div className="card overflow-hidden">
      <table className="data-table">
        <thead>
          <tr>
            <th style={{ width: 110 }}>Ticker</th>
            <th style={{ width: 110 }}>Status</th>
            <th>Source</th>
            <th className="num">Threshold</th>
            <th style={{ width: 110 }}>Updated</th>
          </tr>
        </thead>
        <tbody>
          {alerts.slice(0, 30).map((a) => (
            <tr key={a.id} style={{ cursor: "default" }}>
              <td>
                <button
                  onClick={() => openTickerSheet(a.ticker)}
                  style={{
                    background: "transparent",
                    border: 0,
                    padding: 0,
                    cursor: "pointer",
                    color: "var(--accent-primary)",
                    fontFamily: "var(--font-mono)",
                    fontSize: 13,
                    fontWeight: 600,
                  }}
                >
                  {a.ticker}
                </button>
              </td>
              <td>
                <span
                  className="pill pill-solid"
                  style={{
                    background:
                      a.status === "triggered"
                        ? "var(--jpm-blue-soft)"
                        : "var(--bg-overlay)",
                    color:
                      a.status === "triggered"
                        ? "var(--accent-primary)"
                        : "var(--text-tertiary)",
                  }}
                >
                  {a.status}
                </span>
              </td>
              <td className="type-byline">{a.source}</td>
              <td className="num">
                {formatCurrency(a.threshold, a.market === "br" ? "BRL" : "USD", 2)}
              </td>
              <td className="type-byline">{formatDate(a.updated_at, "relative")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

