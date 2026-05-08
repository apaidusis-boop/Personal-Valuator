"use client";

import { useEffect, useMemo, useState } from "react";
import { ExternalLink, FileText, Filter } from "lucide-react";
import { openTickerSheet } from "@/lib/ticker-sheet";

type Filing = {
  ticker: string;
  market: "br" | "us";
  event_date: string;
  source: string; // cvm | sec
  kind: string;
  summary: string;
  url: string | null;
  is_holding: boolean;
};

function fmtBRDate(iso: string): string {
  const d = new Date(iso + "T00:00:00");
  return `${String(d.getDate()).padStart(2, "0")}/${String(
    d.getMonth() + 1
  ).padStart(2, "0")}/${d.getFullYear()}`;
}

function relativeDay(iso: string): string {
  const t = new Date();
  t.setHours(0, 0, 0, 0);
  const d = new Date(iso + "T00:00:00");
  const n = Math.round((t.getTime() - d.getTime()) / 86400000);
  if (n === 0) return "hoje";
  if (n === 1) return "ontem";
  if (n < 7) return `há ${n}d`;
  if (n < 30) return `há ${Math.floor(n / 7)}sem`;
  return fmtBRDate(iso);
}

function kindBadge(source: string, kind: string) {
  const colorMap: Record<string, { bg: string; fg: string }> = {
    "8-K": { bg: "var(--val-blue-soft, var(--bg-overlay))", fg: "var(--val-blue, var(--accent-primary))" },
    "10-K": { bg: "var(--val-gold-soft, var(--bg-overlay))", fg: "var(--val-gold, var(--accent-primary))" },
    "10-Q": { bg: "var(--val-gold-soft, var(--bg-overlay))", fg: "var(--val-gold, var(--accent-primary))" },
    "6-K": { bg: "var(--bg-overlay)", fg: "var(--text-secondary)" },
    "fato_relevante": { bg: "var(--jpm-loss-soft, var(--bg-overlay))", fg: "var(--verdict-avoid, var(--loss))" },
    "comunicado": { bg: "var(--bg-overlay)", fg: "var(--text-secondary)" },
  };
  const colors = colorMap[kind] || { bg: "var(--bg-overlay)", fg: "var(--text-secondary)" };
  return (
    <span
      className="text-[10px] uppercase font-data px-1.5 py-0.5 rounded"
      style={{
        background: colors.bg,
        color: colors.fg,
        letterSpacing: "0.04em",
        fontWeight: 600,
      }}
    >
      {kind}
    </span>
  );
}

export default function FilingsView() {
  const [filings, setFilings] = useState<Filing[]>([]);
  const [loading, setLoading] = useState(true);
  const [holdingsOnly, setHoldingsOnly] = useState(false);
  const [days, setDays] = useState(30);

  useEffect(() => {
    setLoading(true);
    fetch(
      `/api/calendar?days=0&filings_days=${days}${holdingsOnly ? "&holdings_only=1" : ""}`
    )
      .then((r) => r.json())
      .then((j) => setFilings(j.filings || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [days, holdingsOnly]);

  const cvm = useMemo(
    () => filings.filter((f) => f.source === "cvm"),
    [filings]
  );
  const sec = useMemo(
    () => filings.filter((f) => f.source === "sec"),
    [filings]
  );

  return (
    <div className="px-6 py-5 max-w-[1440px] mx-auto">
      <header className="mb-5">
        <h1
          className="font-display"
          style={{
            fontSize: 26,
            fontWeight: 600,
            color: "var(--text-primary)",
            letterSpacing: "-0.005em",
          }}
        >
          Filings
        </h1>
        <p className="type-body" style={{ marginTop: 4, color: "var(--text-tertiary)" }}>
          CVM (Brasil) + SEC EDGAR (EUA) · últimos {days} dias
        </p>
      </header>

      {/* Filter bar */}
      <div className="card p-3 mb-4 flex items-center gap-3 flex-wrap">
        <div className="flex items-center gap-2 text-xs" style={{ color: "var(--text-tertiary)" }}>
          <Filter size={12} />
          <span className="uppercase tracking-wider" style={{ fontWeight: 600 }}>
            Filtros
          </span>
        </div>
        <button
          type="button"
          onClick={() => setHoldingsOnly((v) => !v)}
          className="text-[11px] px-2.5 py-1 rounded transition-colors uppercase tracking-wider"
          style={{
            background: holdingsOnly ? "var(--accent-primary)" : "transparent",
            color: holdingsOnly ? "white" : "var(--text-tertiary)",
            border: `1px solid ${holdingsOnly ? "var(--accent-primary)" : "var(--border-subtle)"}`,
            fontWeight: 600,
          }}
        >
          {holdingsOnly ? "✓ holdings only" : "todas as empresas"}
        </button>
        <div className="flex items-center gap-px">
          {[7, 14, 30, 90].map((n) => (
            <button
              key={n}
              type="button"
              onClick={() => setDays(n)}
              className="text-[11px] px-2.5 py-1 transition-colors"
              style={{
                color: days === n ? "var(--accent-primary)" : "var(--text-tertiary)",
                borderBottom: days === n ? "1px solid var(--accent-primary)" : "1px solid transparent",
                fontWeight: days === n ? 600 : 500,
              }}
            >
              {n}d
            </button>
          ))}
        </div>
        <span className="text-[11px] ml-auto" style={{ color: "var(--text-tertiary)" }}>
          CVM {cvm.length} · SEC {sec.length}
        </span>
      </div>

      {loading ? (
        <p className="text-xs italic" style={{ color: "var(--text-tertiary)" }}>
          carregando filings…
        </p>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <FilingsColumn title="CVM · Brasil" rows={cvm} accent="var(--mkt-br, var(--accent-primary))" />
          <FilingsColumn title="SEC EDGAR · EUA" rows={sec} accent="var(--mkt-us, var(--accent-primary))" />
        </div>
      )}
    </div>
  );
}

function FilingsColumn({
  title,
  rows,
  accent,
}: {
  title: string;
  rows: Filing[];
  accent: string;
}) {
  return (
    <section
      className="card overflow-hidden"
      style={{ borderTop: `2px solid ${accent}` }}
    >
      <div
        className="px-4 py-2 flex items-center justify-between"
        style={{
          background: "var(--bg-elevated)",
          borderBottom: "1px solid var(--border-subtle)",
        }}
      >
        <h2
          className="text-[11px] uppercase tracking-wider flex items-center gap-2"
          style={{ color: "var(--text-secondary)", fontWeight: 600 }}
        >
          <FileText size={12} />
          {title}
        </h2>
        <span
          className="font-data text-[11px]"
          style={{ color: "var(--text-tertiary)" }}
        >
          {rows.length}
        </span>
      </div>
      {rows.length === 0 ? (
        <p className="px-4 py-6 text-xs italic" style={{ color: "var(--text-tertiary)" }}>
          sem filings na janela seleccionada
        </p>
      ) : (
        <ul style={{ display: "flex", flexDirection: "column" }}>
          {rows.map((f, i) => (
            <li
              key={`${f.ticker}-${f.event_date}-${i}`}
              className="px-4 py-3 transition-colors"
              style={{
                borderBottom: i < rows.length - 1 ? "1px solid var(--border-subtle)" : "none",
              }}
            >
              <div className="flex items-center justify-between gap-3 mb-1.5 flex-wrap">
                <div className="flex items-center gap-2 flex-wrap">
                  <button
                    type="button"
                    onClick={() => openTickerSheet(f.ticker)}
                    className="font-data hover:underline"
                    style={{
                      color: "var(--text-primary)",
                      fontWeight: 600,
                      fontSize: 13,
                    }}
                  >
                    {f.ticker}
                  </button>
                  {f.is_holding && (
                    <span
                      className="text-[10px] px-1.5 py-0.5 rounded font-data"
                      style={{
                        background: "var(--val-gold-soft, var(--bg-overlay))",
                        color: "var(--val-gold, var(--accent-primary))",
                        fontWeight: 600,
                      }}
                    >
                      H
                    </span>
                  )}
                  {kindBadge(f.source, f.kind)}
                </div>
                <div className="flex items-center gap-2 text-[11px]" style={{ color: "var(--text-tertiary)" }}>
                  <span className="font-data">{relativeDay(f.event_date)}</span>
                  {f.url && (
                    <a
                      href={f.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-1 hover:underline"
                      style={{ color: "var(--accent-primary)" }}
                    >
                      <ExternalLink size={10} />
                      fonte
                    </a>
                  )}
                </div>
              </div>
              <p
                className="text-[12px]"
                style={{ color: "var(--text-secondary)", lineHeight: 1.45 }}
              >
                {f.summary || "—"}
              </p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
