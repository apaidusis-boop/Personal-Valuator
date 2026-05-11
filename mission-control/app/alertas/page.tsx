import type { Metadata } from "next";
import Link from "next/link";
import { Bell, Calendar, FileText, Newspaper, TrendingUp, Zap } from "lucide-react";

import {
  listOpenActions,
  upcomingDividends,
  upcomingFilings,
  listRecentEvents,
  recentVerdictDeltas,
  listFairValue,
} from "@/lib/db";
import { formatDate } from "@/lib/format";
import TaskRowActions from "../tasks/row-actions";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Alertas · Mission Control" };

export default function AlertasPage() {
  const actions = listOpenActions(60);
  const divs = upcomingDividends(45);
  const filings = upcomingFilings(90);
  const events = listRecentEvents(30);
  const deltas = recentVerdictDeltas(7);
  const fairValues = listFairValue();
  const topUpside = fairValues
    .filter((f) => f.upside_pct >= 5)
    .slice(0, 12);
  const topOverpriced = fairValues
    .filter((f) => f.upside_pct <= -10)
    .slice(-12)
    .reverse();

  const brActions = actions.filter((a) => a.market === "br");
  const usActions = actions.filter((a) => a.market === "us");

  return (
    <div className="p-5 space-y-5">
      {/* Header --------------------------------------------------- */}
      <div>
        <h1
          className="font-display text-xl font-bold"
          style={{ color: "var(--text-primary)" }}
        >
          Alertas
        </h1>
        <p
          className="text-xs mt-0.5"
          style={{ color: "var(--text-tertiary)" }}
        >
          {actions.length} triggers · {events.length} fatos recentes ·{" "}
          {divs.length} ex-dividendos · {filings.length} filings · {deltas.length} verdict deltas
        </p>
      </div>

      {/* Verdict deltas — auto-recomputed após filings -------------- */}
      {deltas.length > 0 && (
        <div
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
            <div className="flex items-center gap-2">
              <Zap size={15} style={{ color: "var(--val-gold)" }} />
              <h3
                className="text-sm font-semibold"
                style={{ color: "var(--text-primary)" }}
              >
                Verdict deltas (últimos 7 dias)
              </h3>
            </div>
            <span
              className="text-[10px] uppercase tracking-wider"
              style={{ color: "var(--text-tertiary)" }}
            >
              auto-recompute on filing
            </span>
          </div>
          <table className="w-full">
            <thead>
              <tr
                className="text-[10px]"
                style={{
                  color: "var(--text-label)",
                  background: "rgba(11,19,36,0.5)",
                  borderBottom: "1px solid var(--border-subtle)",
                }}
              >
                <th className="text-left px-4 py-2.5 font-semibold">Ticker</th>
                <th className="text-left px-3 py-2.5 font-semibold">Antes</th>
                <th className="text-left px-3 py-2.5 font-semibold">Depois</th>
                <th className="text-right px-3 py-2.5 font-semibold">Score</th>
                <th className="text-left px-3 py-2.5 font-semibold">Trigger</th>
                <th className="text-right px-4 py-2.5 font-semibold">Data</th>
              </tr>
            </thead>
            <tbody>
              {deltas.map((d) => {
                const changed = d.prior_action && d.prior_action !== d.new_action;
                return (
                  <tr
                    key={`${d.market}-${d.ticker}-${d.date}-${d.triggered_by}`}
                    style={{ borderBottom: "1px solid rgba(45,55,72,0.4)" }}
                  >
                    <td className="px-4 py-2.5">
                      <Link
                        href={`/ticker/${d.ticker}`}
                        className="text-sm font-data font-bold hover:underline"
                        style={{ color: "var(--text-primary)" }}
                      >
                        {d.ticker}
                      </Link>
                    </td>
                    <td className="px-3 py-2.5 text-xs" style={{ color: "var(--text-tertiary)" }}>
                      {d.prior_action || "—"}
                    </td>
                    <td className="px-3 py-2.5 text-xs font-bold" style={{
                      color: changed ? "var(--val-gold)" : "var(--text-secondary)",
                    }}>
                      {changed ? "→ " : ""}{d.new_action}
                    </td>
                    <td className="px-3 py-2.5 text-xs font-data text-right" style={{ color: "var(--text-secondary)" }}>
                      {d.new_score != null ? d.new_score.toFixed(1) : "—"}
                    </td>
                    <td className="px-3 py-2.5 text-xs" style={{ color: "var(--text-tertiary)" }}>
                      {d.triggered_url ? (
                        <a
                          href={d.triggered_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="hover:underline"
                          style={{ color: "var(--text-secondary)" }}
                        >
                          {d.triggered_by}
                        </a>
                      ) : (
                        d.triggered_by
                      )}
                    </td>
                    <td className="px-4 py-2.5 text-xs font-data text-right" style={{ color: "var(--text-tertiary)" }}>
                      {formatDate(d.date, "short")}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Open actions ---------------------------------------------- */}
      <div
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
          <div className="flex items-center gap-2">
            <Bell size={15} style={{ color: "var(--val-gold)" }} />
            <h3
              className="text-sm font-semibold"
              style={{ color: "var(--text-primary)" }}
            >
              Triggers abertos
            </h3>
          </div>
          <span
            className="text-[10px] uppercase tracking-wider"
            style={{ color: "var(--text-tertiary)" }}
          >
            {brActions.length} BR · {usActions.length} US
          </span>
        </div>

        {actions.length > 0 ? (
          <table className="w-full">
            <thead>
              <tr
                className="text-[10px]"
                style={{
                  color: "var(--text-label)",
                  background: "rgba(11,19,36,0.5)",
                  borderBottom: "1px solid var(--border-subtle)",
                }}
              >
                <th className="text-left px-4 py-2.5 font-semibold">Ticker</th>
                <th className="text-left px-3 py-2.5 font-semibold">Mercado</th>
                <th className="text-left px-3 py-2.5 font-semibold">Tipo</th>
                <th className="text-left px-3 py-2.5 font-semibold">Descrição</th>
                <th className="text-right px-3 py-2.5 font-semibold">Aberto</th>
                <th className="text-right px-4 py-2.5 font-semibold">Ações</th>
              </tr>
            </thead>
            <tbody>
              {actions.map((a) => (
                <tr
                  key={`${a.market}-${a.id}`}
                  className="hover:bg-[var(--bg-overlay)]/40 transition-colors"
                  style={{
                    borderBottom: "1px solid rgba(45,55,72,0.4)",
                  }}
                >
                  <td className="px-4 py-3">
                    <Link
                      href={`/ticker/${a.ticker}`}
                      className="text-sm font-data font-bold hover:underline"
                      style={{ color: "var(--text-primary)" }}
                    >
                      {a.ticker}
                    </Link>
                  </td>
                  <td className="px-3 py-3">
                    <span className={`pill pill-${a.market === "br" ? "mkt-br" : "mkt-us"}`}>
                      {a.market.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-3 py-3 text-xs" style={{ color: "var(--text-secondary)" }}>
                    {a.kind}
                  </td>
                  <td
                    className="px-3 py-3 text-xs max-w-[420px] truncate"
                    style={{ color: "var(--text-tertiary)" }}
                    title={a.description}
                  >
                    {a.description}
                  </td>
                  <td
                    className="px-3 py-3 text-xs font-data text-right"
                    style={{ color: "var(--text-tertiary)" }}
                  >
                    {formatDate(a.created_at, "relative")}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <TaskRowActions
                      id={a.id}
                      market={a.market}
                      ticker={a.ticker}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p
            className="px-4 py-8 text-xs italic text-center"
            style={{ color: "var(--text-tertiary)" }}
          >
            Nenhum trigger aberto. Watchlist limpa.
          </p>
        )}
      </div>

      {/* Fatos recentes (events) -------------------------------- */}
      <div
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
          <div className="flex items-center gap-2">
            <Newspaper size={15} style={{ color: "var(--val-gold)" }} />
            <h3
              className="text-sm font-semibold"
              style={{ color: "var(--text-primary)" }}
            >
              Fatos relevantes & filings
            </h3>
          </div>
          <span
            className="text-[10px] uppercase tracking-wider"
            style={{ color: "var(--text-tertiary)" }}
          >
            CVM · SEC
          </span>
        </div>
        {events.length > 0 ? (
          <table className="w-full">
            <thead>
              <tr
                className="text-[10px]"
                style={{
                  color: "var(--text-label)",
                  background: "rgba(11,19,36,0.5)",
                  borderBottom: "1px solid var(--border-subtle)",
                }}
              >
                <th className="text-left px-4 py-2.5 font-semibold">Ticker</th>
                <th className="text-left px-3 py-2.5 font-semibold">Fonte</th>
                <th className="text-left px-3 py-2.5 font-semibold">Tipo</th>
                <th className="text-left px-3 py-2.5 font-semibold">Resumo</th>
                <th className="text-right px-4 py-2.5 font-semibold">Data</th>
              </tr>
            </thead>
            <tbody>
              {events.map((e) => (
                <tr
                  key={`${e.market}-${e.id}`}
                  className="hover:bg-[var(--bg-overlay)]/40 transition-colors"
                  style={{ borderBottom: "1px solid rgba(45,55,72,0.4)" }}
                >
                  <td className="px-4 py-2.5">
                    <Link
                      href={`/ticker/${e.ticker}`}
                      className="text-sm font-data font-bold hover:underline"
                      style={{ color: "var(--text-primary)" }}
                    >
                      {e.ticker}
                    </Link>
                  </td>
                  <td className="px-3 py-2.5">
                    <span
                      className="pill"
                      style={{
                        color:
                          e.source === "cvm"
                            ? "var(--mkt-br)"
                            : "var(--mkt-us)",
                      }}
                    >
                      {String(e.source).toUpperCase()}
                    </span>
                  </td>
                  <td
                    className="px-3 py-2.5 text-xs"
                    style={{ color: "var(--text-secondary)" }}
                  >
                    {e.kind}
                  </td>
                  <td
                    className="px-3 py-2.5 text-xs max-w-[520px]"
                    style={{ color: "var(--text-tertiary)" }}
                    title={e.summary || ""}
                  >
                    {e.url ? (
                      <a
                        href={e.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="hover:underline"
                        style={{ color: "var(--text-secondary)" }}
                      >
                        {(e.summary || "—")
                          .replace(/�+/g, "·")
                          .slice(0, 140)}
                        {(e.summary || "").length > 140 ? "…" : ""}
                      </a>
                    ) : (
                      (e.summary || "—").replace(/�+/g, "·").slice(0, 140)
                    )}
                  </td>
                  <td
                    className="px-4 py-2.5 text-xs font-data text-right"
                    style={{ color: "var(--text-tertiary)" }}
                  >
                    {formatDate(e.event_date, "short")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p
            className="px-4 py-8 text-xs italic text-center"
            style={{ color: "var(--text-tertiary)" }}
          >
            Nenhum filing registado nas duas DBs.
          </p>
        )}
      </div>

      {/* Upcoming dividends --------------------------------------- */}
      <div
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
          <div className="flex items-center gap-2">
            <Calendar size={15} style={{ color: "var(--val-gold)" }} />
            <h3
              className="text-sm font-semibold"
              style={{ color: "var(--text-primary)" }}
            >
              Próximos ex-dividendos
            </h3>
          </div>
          <span
            className="text-[10px] uppercase tracking-wider"
            style={{ color: "var(--text-tertiary)" }}
          >
            45 dias
          </span>
        </div>
        {divs.length > 0 ? (
          <table className="w-full">
            <thead>
              <tr
                className="text-[10px]"
                style={{
                  color: "var(--text-label)",
                  background: "rgba(11,19,36,0.5)",
                  borderBottom: "1px solid var(--border-subtle)",
                }}
              >
                <th className="text-left px-4 py-2.5 font-semibold">Ticker</th>
                <th className="text-left px-3 py-2.5 font-semibold">Mercado</th>
                <th className="text-left px-3 py-2.5 font-semibold">Ex-data</th>
                <th className="text-left px-3 py-2.5 font-semibold">Pagamento</th>
                <th className="text-right px-4 py-2.5 font-semibold">Valor / ação</th>
              </tr>
            </thead>
            <tbody>
              {divs.map((d, i) => (
                <tr
                  key={`${d.market}-${d.ticker}-${d.ex_date}-${i}`}
                  style={{
                    borderBottom: "1px solid rgba(45,55,72,0.4)",
                  }}
                >
                  <td className="px-4 py-2.5">
                    <Link
                      href={`/ticker/${d.ticker}`}
                      className="text-sm font-data font-bold hover:underline"
                      style={{ color: "var(--text-primary)" }}
                    >
                      {d.ticker}
                    </Link>
                  </td>
                  <td className="px-3 py-2.5">
                    <span className={`pill pill-${d.market === "br" ? "mkt-br" : "mkt-us"}`}>
                      {d.market.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-3 py-2.5 text-xs font-data" style={{ color: "var(--text-secondary)" }}>
                    {formatDate(d.ex_date, "medium")}
                  </td>
                  <td className="px-3 py-2.5 text-xs font-data" style={{ color: "var(--text-tertiary)" }}>
                    {d.pay_date ? formatDate(d.pay_date, "medium") : "—"}
                  </td>
                  <td
                    className="px-4 py-2.5 text-sm font-data text-right"
                    style={{ color: "var(--text-primary)" }}
                  >
                    {d.amount > 0
                      ? `${d.market === "br" ? "R$" : "$"}${d.amount.toFixed(d.market === "br" ? 4 : 3)}`
                      : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p
            className="px-4 py-8 text-xs italic text-center"
            style={{ color: "var(--text-tertiary)" }}
          >
            Nenhum dividendo programado em 45 dias.
          </p>
        )}
      </div>

      {/* Upcoming filings — projected from earnings_calendar -------- */}
      <div
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
          <div className="flex items-center gap-2">
            <FileText size={15} style={{ color: "var(--val-gold)" }} />
            <h3
              className="text-sm font-semibold"
              style={{ color: "var(--text-primary)" }}
            >
              Próximos filings
            </h3>
          </div>
          <span
            className="text-[10px] uppercase tracking-wider"
            style={{ color: "var(--text-tertiary)" }}
          >
            90 dias · earnings + projeção
          </span>
        </div>
        {filings.length > 0 ? (
          <table className="w-full">
            <thead>
              <tr
                className="text-[10px]"
                style={{
                  color: "var(--text-label)",
                  background: "rgba(11,19,36,0.5)",
                  borderBottom: "1px solid var(--border-subtle)",
                }}
              >
                <th className="text-left px-4 py-2.5 font-semibold">Ticker</th>
                <th className="text-left px-3 py-2.5 font-semibold">Mercado</th>
                <th className="text-left px-3 py-2.5 font-semibold">Tipo previsto</th>
                <th className="text-left px-3 py-2.5 font-semibold">Empresa</th>
                <th className="text-right px-4 py-2.5 font-semibold">Earnings date</th>
              </tr>
            </thead>
            <tbody>
              {filings.map((f) => (
                <tr
                  key={`${f.market}-${f.ticker}-${f.earnings_date}`}
                  className="hover:bg-[var(--bg-overlay)]/40 transition-colors"
                  style={{ borderBottom: "1px solid rgba(45,55,72,0.4)" }}
                >
                  <td className="px-4 py-2.5">
                    <Link
                      href={`/ticker/${f.ticker}`}
                      className="text-sm font-data font-bold hover:underline"
                      style={{ color: f.is_holding ? "var(--text-primary)" : "var(--text-secondary)" }}
                    >
                      {f.is_holding ? "★ " : ""}{f.ticker}
                    </Link>
                  </td>
                  <td className="px-3 py-2.5">
                    <span className={`pill pill-${f.market === "br" ? "mkt-br" : "mkt-us"}`}>
                      {f.market.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-3 py-2.5 text-xs font-mono" style={{ color: "var(--text-secondary)" }}>
                    {f.projected_kind}
                  </td>
                  <td className="px-3 py-2.5 text-xs" style={{ color: "var(--text-tertiary)" }}>
                    {f.name || "—"}
                  </td>
                  <td className="px-4 py-2.5 text-xs font-data text-right" style={{ color: "var(--text-primary)" }}>
                    {formatDate(f.earnings_date, "medium")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p
            className="px-4 py-8 text-xs italic text-center"
            style={{ color: "var(--text-tertiary)" }}
          >
            Nenhum filing previsto em 90 dias.
          </p>
        )}
      </div>

      {/* Fair value — top upside / overpriced ---------------------- */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {[
          { title: "Upside (preço justo > atual)", rows: topUpside, badge: "BUY zone" },
          { title: "Overpriced (preço > justo)", rows: topOverpriced, badge: "AVOID zone" },
        ].map((box) => (
          <div
            key={box.title}
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
              <div className="flex items-center gap-2">
                <TrendingUp size={15} style={{ color: "var(--val-gold)" }} />
                <h3 className="text-sm font-semibold" style={{ color: "var(--text-primary)" }}>
                  {box.title}
                </h3>
              </div>
              <span className="text-[10px] uppercase tracking-wider" style={{ color: "var(--text-tertiary)" }}>
                {box.badge}
              </span>
            </div>
            {box.rows.length > 0 ? (
              <table className="w-full">
                <thead>
                  <tr
                    className="text-[10px]"
                    style={{
                      color: "var(--text-label)",
                      background: "rgba(11,19,36,0.5)",
                      borderBottom: "1px solid var(--border-subtle)",
                    }}
                  >
                    <th className="text-left px-3 py-2 font-semibold">Ticker</th>
                    <th className="text-left px-3 py-2 font-semibold">Método</th>
                    <th className="text-right px-3 py-2 font-semibold">Justo</th>
                    <th className="text-right px-3 py-2 font-semibold">Atual</th>
                    <th className="text-right px-3 py-2 font-semibold">Upside</th>
                  </tr>
                </thead>
                <tbody>
                  {box.rows.map((f) => (
                    <tr
                      key={`${f.market}-${f.ticker}-${f.method}`}
                      style={{ borderBottom: "1px solid rgba(45,55,72,0.3)" }}
                    >
                      <td className="px-3 py-2">
                        <Link
                          href={`/ticker/${f.ticker}`}
                          className="text-xs font-data font-bold hover:underline"
                          style={{ color: "var(--text-primary)" }}
                        >
                          {f.ticker}
                        </Link>
                      </td>
                      <td className="px-3 py-2 text-[10px] font-mono" style={{ color: "var(--text-tertiary)" }}>
                        {f.method}
                      </td>
                      <td className="px-3 py-2 text-xs font-data text-right" style={{ color: "var(--text-secondary)" }}>
                        {f.market === "br" ? "R$" : "$"}{f.fair_price.toFixed(2)}
                      </td>
                      <td className="px-3 py-2 text-xs font-data text-right" style={{ color: "var(--text-tertiary)" }}>
                        {f.market === "br" ? "R$" : "$"}{f.current_price.toFixed(2)}
                      </td>
                      <td className="px-3 py-2 text-xs font-data font-bold text-right" style={{
                        color: f.upside_pct > 0 ? "var(--val-positive)" : "var(--val-negative)",
                      }}>
                        {f.upside_pct > 0 ? "+" : ""}{f.upside_pct.toFixed(1)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p
                className="px-4 py-8 text-xs italic text-center"
                style={{ color: "var(--text-tertiary)" }}
              >
                Sem dados.
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
