import type { Metadata } from "next";
import { listAllPositions, UnifiedPosition } from "@/lib/db";
import { formatCurrency, formatDate } from "@/lib/format";
import PortfolioRowClick from "./row-click";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Carteira · Mission Control" };

// ── helpers ──────────────────────────────────────────────────────────────────

function pnlColor(v: number | null): string {
  if (v === null) return "var(--text-tertiary)";
  if (v > 0) return "var(--gain)";
  if (v < 0) return "var(--loss)";
  return "var(--neutral)";
}

function fmtQty(n: number | null) {
  if (n === null) return "—";
  return n.toLocaleString("pt-BR", { maximumFractionDigits: 4 });
}

function fmtUnit(n: number | null, currency: "BRL" | "USD" = "BRL") {
  if (n === null) return "—";
  return formatCurrency(n, currency, 2);
}

type GroupMeta = {
  label: string;
  positions: UnifiedPosition[];
  total_cost: number;
  total_value: number;
  total_pnl: number;
  pnl_pct: number;
  weight_pct: number;
  is_rf: boolean;
  currency: "BRL" | "USD";
};

function buildGroups(positions: UnifiedPosition[]): GroupMeta[] {
  const map = new Map<string, UnifiedPosition[]>();
  for (const p of positions) {
    const g = p.group_label;
    if (!map.has(g)) map.set(g, []);
    map.get(g)!.push(p);
  }
  const RF_CLASSES = new Set(["tesouro", "debenture", "cra", "lca", "fundo"]);
  const brTotal = positions
    .filter((p) => p.market === "br")
    .reduce((s, p) => s + p.current_value, 0);
  const usTotal = positions
    .filter((p) => p.market === "us")
    .reduce((s, p) => s + p.current_value, 0);

  const groups: GroupMeta[] = [];
  for (const [label, rows] of map) {
    const tc = rows.reduce((s, r) => s + r.cost_basis, 0);
    const tv = rows.reduce((s, r) => s + r.current_value, 0);
    const tp = tv - tc;
    const currency = rows[0].market === "us" ? "USD" : "BRL";
    const denom = currency === "USD" ? usTotal : brTotal;
    groups.push({
      label,
      positions: rows,
      total_cost: tc,
      total_value: tv,
      total_pnl: tp,
      pnl_pct: tc > 0 ? (tp / tc) * 100 : 0,
      weight_pct: denom > 0 ? (tv / denom) * 100 : 0,
      is_rf: RF_CLASSES.has(rows[0].asset_class),
      currency,
    });
  }
  return groups;
}

const GROUP_COLORS: Record<string, string> = {
  "Ações": "#2D6CDF",
  "US Equities": "#1B4DB5",
  "FIIs": "#4CAF50",
  "ETFs": "#26A69A",
  "Tesouro Direto": "#C9A15B",
  "Debêntures": "#A07840",
  "CRAs": "#806030",
  "LCAs": "#604820",
  "Fundos": "#9C27B0",
};

// ── sub-components ────────────────────────────────────────────────────────────

function DistributionBar({ groups }: { groups: GroupMeta[] }) {
  return (
    <div className="space-y-2">
      <div className="flex h-2 rounded-sm overflow-hidden gap-px">
        {groups.map((g) => (
          <div
            key={g.label}
            style={{
              width: `${g.weight_pct.toFixed(2)}%`,
              background: GROUP_COLORS[g.label] ?? "var(--text-tertiary)",
            }}
            title={`${g.label}: ${g.weight_pct.toFixed(1)}%`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-4 gap-y-1">
        {groups.map((g) => (
          <span
            key={g.label}
            className="text-[10px] flex items-center gap-1.5"
            style={{ color: "var(--text-tertiary)" }}
          >
            <span
              className="inline-block w-2 h-2 rounded-full"
              style={{
                background: GROUP_COLORS[g.label] ?? "var(--text-tertiary)",
              }}
            />
            {g.label} {g.weight_pct.toFixed(1)}%
          </span>
        ))}
      </div>
    </div>
  );
}

function GroupCard({ g }: { g: GroupMeta }) {
  const accent = GROUP_COLORS[g.label] ?? "var(--val-gold)";
  return (
    <div
      className="rounded overflow-hidden"
      style={{
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderTop: `2px solid ${accent}`,
      }}
    >
      <div
        className="px-4 py-3 flex items-baseline justify-between flex-wrap gap-2"
        style={{ borderBottom: "1px solid var(--border-subtle)" }}
      >
        <div className="flex items-baseline gap-3">
          <h2
            className="text-sm font-semibold"
            style={{ color: "var(--text-primary)" }}
          >
            {g.label}
          </h2>
          <span
            className="text-[10px]"
            style={{ color: "var(--text-tertiary)" }}
          >
            {g.positions.length} posições · {g.weight_pct.toFixed(1)}% da carteira
          </span>
        </div>
        <div className="flex items-baseline gap-3 text-xs font-data">
          <span style={{ color: "var(--text-primary)" }}>
            {formatCurrency(g.total_value, g.currency, 0)}
          </span>
          <span style={{ color: pnlColor(g.total_pnl) }}>
            {g.total_pnl >= 0 ? "+" : ""}
            {formatCurrency(g.total_pnl, g.currency, 0)} (
            {g.total_pnl >= 0 ? "+" : ""}
            {g.pnl_pct.toFixed(1)}%)
          </span>
        </div>
      </div>
      {g.is_rf ? <RFTable g={g} /> : <EquityTable g={g} />}
    </div>
  );
}

function EquityTable({ g }: { g: GroupMeta }) {
  const cur = g.currency;
  return (
    <table className="w-full">
      <thead>
        <tr
          className="text-[10px]"
          style={{
            color: "var(--text-label)",
            background: "var(--bg-overlay)",
            borderBottom: "1px solid var(--border-subtle)",
          }}
        >
          <th className="text-left px-4 py-2 font-semibold">Ticker</th>
          <th className="text-left px-3 py-2 font-semibold">Nome</th>
          <th className="text-right px-3 py-2 font-semibold">Qtd</th>
          <th className="text-right px-3 py-2 font-semibold">PM</th>
          <th className="text-right px-3 py-2 font-semibold">Preço</th>
          <th className="text-right px-3 py-2 font-semibold">Custo</th>
          <th className="text-right px-3 py-2 font-semibold">Valor</th>
          <th className="text-right px-3 py-2 font-semibold">P&amp;L</th>
          <th className="text-right px-3 py-2 font-semibold">P&amp;L%</th>
          <th className="text-right px-4 py-2 font-semibold">Peso</th>
        </tr>
      </thead>
      <tbody>
        {g.positions.map((p) => (
          <tr
            key={p.id}
            className="transition-colors hover:bg-[var(--jpm-card-hover)]"
            style={{ borderBottom: "1px solid var(--border-subtle)" }}
          >
            <td className="px-4 py-2 text-sm font-data font-bold">
              <PortfolioRowClick ticker={p.ticker}>
                <span
                  className="hover:underline"
                  style={{ color: "var(--accent-primary)" }}
                >
                  {p.ticker ?? "—"}
                </span>
              </PortfolioRowClick>
            </td>
            <td
              className="px-3 py-2 text-xs truncate max-w-[200px]"
              style={{ color: "var(--text-secondary)" }}
              title={p.name}
            >
              {p.name}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data"
              style={{ color: "var(--text-primary)" }}
            >
              {fmtQty(p.quantity)}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data"
              style={{ color: "var(--text-tertiary)" }}
            >
              {fmtUnit(p.entry_unit, cur)}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data"
              style={{ color: "var(--text-primary)" }}
            >
              {fmtUnit(p.current_unit, cur)}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data"
              style={{ color: "var(--text-tertiary)" }}
            >
              {formatCurrency(p.cost_basis, cur, 0)}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data font-medium"
              style={{ color: "var(--text-primary)" }}
            >
              {formatCurrency(p.current_value, cur, 0)}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data"
              style={{ color: pnlColor(p.pnl_abs) }}
            >
              {p.pnl_abs >= 0 ? "+" : ""}
              {formatCurrency(p.pnl_abs, cur, 0)}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data"
              style={{ color: pnlColor(p.pnl_pct) }}
            >
              {p.pnl_pct !== null
                ? `${p.pnl_pct >= 0 ? "+" : ""}${p.pnl_pct.toFixed(1)}%`
                : "—"}
            </td>
            <td
              className="px-4 py-2 text-right text-xs font-data"
              style={{ color: "var(--text-tertiary)" }}
            >
              {p.weight_pct.toFixed(1)}%
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function RFTable({ g }: { g: GroupMeta }) {
  return (
    <table className="w-full">
      <thead>
        <tr
          className="text-[10px]"
          style={{
            color: "var(--text-label)",
            background: "var(--bg-overlay)",
            borderBottom: "1px solid var(--border-subtle)",
          }}
        >
          <th className="text-left px-4 py-2 font-semibold">Ativo</th>
          <th className="text-left px-3 py-2 font-semibold">Taxa</th>
          <th className="text-right px-3 py-2 font-semibold">Qtd</th>
          <th className="text-left px-3 py-2 font-semibold">Vencimento</th>
          <th className="text-right px-3 py-2 font-semibold">Investido</th>
          <th className="text-right px-3 py-2 font-semibold">Valor</th>
          <th className="text-right px-3 py-2 font-semibold">P&amp;L</th>
          <th className="text-right px-3 py-2 font-semibold">P&amp;L%</th>
          <th className="text-right px-4 py-2 font-semibold">Peso</th>
        </tr>
      </thead>
      <tbody>
        {g.positions.map((p) => (
          <tr
            key={p.id}
            className="transition-colors hover:bg-[var(--jpm-card-hover)]"
            style={{ borderBottom: "1px solid var(--border-subtle)" }}
          >
            <td
              className="px-4 py-2 text-sm font-medium truncate max-w-[260px]"
              style={{ color: "var(--text-primary)" }}
              title={p.name}
            >
              {p.name}
            </td>
            <td
              className="px-3 py-2 text-xs"
              style={{ color: "var(--val-gold)" }}
            >
              {p.rate ?? "—"}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data"
              style={{ color: "var(--text-tertiary)" }}
            >
              {fmtQty(p.quantity)}
            </td>
            <td
              className="px-3 py-2 text-xs font-data"
              style={{ color: "var(--text-secondary)" }}
            >
              {p.maturity_date ? formatDate(p.maturity_date, "medium") : "—"}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data"
              style={{ color: "var(--text-tertiary)" }}
            >
              {formatCurrency(p.cost_basis, "BRL", 0)}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data font-medium"
              style={{ color: "var(--text-primary)" }}
            >
              {formatCurrency(p.current_value, "BRL", 0)}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data"
              style={{ color: pnlColor(p.pnl_abs) }}
            >
              {p.pnl_abs >= 0 ? "+" : ""}
              {formatCurrency(p.pnl_abs, "BRL", 0)}
            </td>
            <td
              className="px-3 py-2 text-right text-xs font-data"
              style={{ color: pnlColor(p.pnl_pct) }}
            >
              {p.pnl_pct !== null
                ? `${p.pnl_pct >= 0 ? "+" : ""}${p.pnl_pct.toFixed(1)}%`
                : "—"}
            </td>
            <td
              className="px-4 py-2 text-right text-xs font-data"
              style={{ color: "var(--text-tertiary)" }}
            >
              {p.weight_pct.toFixed(1)}%
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function GrandTotal({
  label,
  value,
  pnl,
  pnlPct,
  cost,
  currency,
}: {
  label: string;
  value: number;
  pnl: number;
  pnlPct: number;
  cost: number;
  currency: "BRL" | "USD";
}) {
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
      <p
        className="text-2xl font-display font-bold mb-1"
        style={{ color: "var(--text-primary)" }}
      >
        {formatCurrency(value, currency, 0)}
      </p>
      <p
        className="text-xs font-data"
        style={{ color: pnlColor(pnl) }}
      >
        {pnl >= 0 ? "+" : ""}
        {formatCurrency(pnl, currency, 0)} ({pnl >= 0 ? "+" : ""}
        {pnlPct.toFixed(1)}%) <span style={{ color: "var(--text-tertiary)" }}>vs custo {formatCurrency(cost, currency, 0)}</span>
      </p>
    </div>
  );
}

// ── page ──────────────────────────────────────────────────────────────────────

export default function PortfolioPage() {
  const positions = listAllPositions();
  const groups = buildGroups(positions);

  const brPositions = positions.filter((p) => p.market === "br");
  const usPositions = positions.filter((p) => p.market === "us");

  const brValue = brPositions.reduce((s, p) => s + p.current_value, 0);
  const brCost = brPositions.reduce((s, p) => s + p.cost_basis, 0);
  const brPnl = brValue - brCost;
  const brPnlPct = brCost > 0 ? (brPnl / brCost) * 100 : 0;

  const usValue = usPositions.reduce((s, p) => s + p.current_value, 0);
  const usCost = usPositions.reduce((s, p) => s + p.cost_basis, 0);
  const usPnl = usValue - usCost;
  const usPnlPct = usCost > 0 ? (usPnl / usCost) * 100 : 0;

  const brGroups = groups.filter((g) => g.currency === "BRL");
  const usGroups = groups.filter((g) => g.currency === "USD");

  return (
    <div className="p-5 space-y-5">
      {/* Header ----------------------------------------------- */}
      <div>
        <h1
          className="font-display text-xl font-bold"
          style={{ color: "var(--text-primary)" }}
        >
          Minha Carteira
        </h1>
        <p
          className="text-xs mt-0.5"
          style={{ color: "var(--text-tertiary)" }}
        >
          {positions.length} posições · {brGroups.length + usGroups.length} grupos · BRL e USD isolados
        </p>
      </div>

      {/* Grand totals (2 stat blocks) ------------------------- */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <GrandTotal
          label="BRASIL · BRL"
          value={brValue}
          pnl={brPnl}
          pnlPct={brPnlPct}
          cost={brCost}
          currency="BRL"
        />
        <GrandTotal
          label="EUA · USD"
          value={usValue}
          pnl={usPnl}
          pnlPct={usPnlPct}
          cost={usCost}
          currency="USD"
        />
      </div>

      {/* BR section ------------------------------------------- */}
      {brGroups.length > 0 && (
        <section className="space-y-4">
          <div
            className="p-4 rounded"
            style={{
              background: "var(--bg-elevated)",
              border: "1px solid var(--border-subtle)",
            }}
          >
            <h3
              className="text-[10px] font-semibold tracking-wider uppercase mb-3"
              style={{ color: "var(--text-label)" }}
            >
              Distribuição BR
            </h3>
            <DistributionBar groups={brGroups} />
          </div>
          {brGroups.map((g) => (
            <GroupCard key={g.label} g={g} />
          ))}
        </section>
      )}

      {/* US section ------------------------------------------- */}
      {usGroups.length > 0 && (
        <section className="space-y-4">
          <div
            className="p-4 rounded"
            style={{
              background: "var(--bg-elevated)",
              border: "1px solid var(--border-subtle)",
            }}
          >
            <h3
              className="text-[10px] font-semibold tracking-wider uppercase mb-3"
              style={{ color: "var(--text-label)" }}
            >
              Distribuição US
            </h3>
            <DistributionBar groups={usGroups} />
          </div>
          {usGroups.map((g) => (
            <GroupCard key={g.label} g={g} />
          ))}
        </section>
      )}
    </div>
  );
}
