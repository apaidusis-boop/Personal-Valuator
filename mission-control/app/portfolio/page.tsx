import { listAllPositions, UnifiedPosition } from "@/lib/db";
import { formatCurrency, formatPercent, formatDate } from "@/lib/format";
import { PageHeader } from "@/components/ui";

export const dynamic = "force-dynamic";

// ── helpers ──────────────────────────────────────────────────────────────────

function pnlClass(v: number | null) {
  if (v === null) return "text-[var(--text-tertiary)]";
  if (v > 0) return "text-[var(--gain)]";
  if (v < 0) return "text-[var(--loss)]";
  return "text-[var(--neutral)]";
}

function fmtQty(n: number | null) {
  if (n === null) return "—";
  return n.toLocaleString("pt-BR", { maximumFractionDigits: 4 });
}

function fmtUnit(n: number | null, currency: "BRL" | "USD" = "BRL") {
  if (n === null) return "—";
  return formatCurrency(n, currency, 2);
}

function fmtPnl(abs: number, pct: number | null) {
  const absStr = formatCurrency(abs, "BRL", 0);
  const sign = abs >= 0 ? "+" : "";
  const pctStr = pct !== null ? ` (${abs >= 0 ? "+" : ""}${pct.toFixed(1)}%)` : "";
  return `${sign}${absStr}${pctStr}`;
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

// ── sub-components ────────────────────────────────────────────────────────────

function DistributionBar({ groups }: { groups: GroupMeta[] }) {
  const COLORS: Record<string, string> = {
    "Ações": "var(--accent-primary)",
    "US Equities": "var(--accent-secondary, #6B7CF6)",
    "FIIs": "var(--verdict-buy)",
    "ETFs": "var(--accent-glow)",
    "Tesouro Direto": "#C09A52",
    "Debêntures": "#A07840",
    "CRAs": "#806030",
    "LCAs": "#604820",
    "Fundos": "#503820",
  };

  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-sm overflow-hidden gap-px">
        {groups.map((g) => (
          <div
            key={g.label}
            style={{
              width: `${g.weight_pct.toFixed(2)}%`,
              background: COLORS[g.label] ?? "var(--text-secondary)",
            }}
            title={`${g.label}: ${g.weight_pct.toFixed(1)}%`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-4 gap-y-1">
        {groups.map((g) => (
          <span key={g.label} className="type-mono-sm text-[var(--text-secondary)] flex items-center gap-1.5">
            <span
              className="inline-block w-2 h-2 rounded-full"
              style={{ background: COLORS[g.label] ?? "var(--text-secondary)" }}
            />
            {g.label} {g.weight_pct.toFixed(1)}%
          </span>
        ))}
      </div>
    </div>
  );
}

function GroupHeader({ g }: { g: GroupMeta }) {
  return (
    <div className="flex items-baseline justify-between py-2 border-b border-[var(--rule)] mt-8">
      <h2 className="type-h2 text-[var(--text-primary)] uppercase tracking-wider text-xs font-semibold">
        {g.label}
      </h2>
      <div className="flex items-baseline gap-4 type-mono-sm text-[var(--text-secondary)]">
        <span>{formatCurrency(g.total_value, g.currency, 0)}</span>
        <span className={pnlClass(g.total_pnl)}>
          {g.total_pnl >= 0 ? "+" : ""}
          {formatCurrency(g.total_pnl, g.currency, 0)}
          {" "}({g.total_pnl >= 0 ? "+" : ""}{g.pnl_pct.toFixed(1)}%)
        </span>
        <span className="text-[var(--text-tertiary)]">{g.weight_pct.toFixed(1)}% da carteira</span>
      </div>
    </div>
  );
}

function EquityTable({ g }: { g: GroupMeta }) {
  const cur = g.currency;
  return (
    <table className="w-full type-mono-sm mt-1">
      <thead>
        <tr className="text-[var(--text-tertiary)] border-b border-[var(--border-subtle)]">
          <th className="text-left py-1.5 pr-3 font-normal w-20">Ticker</th>
          <th className="text-left py-1.5 pr-3 font-normal">Nome</th>
          <th className="text-right py-1.5 px-2 font-normal">Qtd</th>
          <th className="text-right py-1.5 px-2 font-normal">PM</th>
          <th className="text-right py-1.5 px-2 font-normal">Preço</th>
          <th className="text-right py-1.5 px-2 font-normal">Custo</th>
          <th className="text-right py-1.5 px-2 font-normal">Valor</th>
          <th className="text-right py-1.5 px-2 font-normal">P&amp;L</th>
          <th className="text-right py-1.5 pl-2 font-normal">P&amp;L%</th>
          <th className="text-right py-1.5 pl-2 font-normal">Peso</th>
        </tr>
      </thead>
      <tbody className="divide-y divide-[var(--border-subtle)]">
        {g.positions.map((p) => (
          <tr key={p.id} className="hover:bg-[var(--bg-raised)] transition-colors">
            <td className="py-1.5 pr-3 text-[var(--accent-primary)] font-medium">
              {p.ticker ?? "—"}
            </td>
            <td className="py-1.5 pr-3 text-[var(--text-secondary)] truncate max-w-[180px]">
              {p.name}
            </td>
            <td className="py-1.5 px-2 text-right tabular">{fmtQty(p.quantity)}</td>
            <td className="py-1.5 px-2 text-right tabular text-[var(--text-secondary)]">
              {fmtUnit(p.entry_unit, cur)}
            </td>
            <td className="py-1.5 px-2 text-right tabular">
              {fmtUnit(p.current_unit, cur)}
            </td>
            <td className="py-1.5 px-2 text-right tabular text-[var(--text-secondary)]">
              {formatCurrency(p.cost_basis, cur, 0)}
            </td>
            <td className="py-1.5 px-2 text-right tabular font-medium">
              {formatCurrency(p.current_value, cur, 0)}
            </td>
            <td className={`py-1.5 px-2 text-right tabular ${pnlClass(p.pnl_abs)}`}>
              {p.pnl_abs >= 0 ? "+" : ""}{formatCurrency(p.pnl_abs, cur, 0)}
            </td>
            <td className={`py-1.5 pl-2 text-right tabular ${pnlClass(p.pnl_pct)}`}>
              {p.pnl_pct !== null
                ? `${p.pnl_pct >= 0 ? "+" : ""}${p.pnl_pct.toFixed(1)}%`
                : "—"}
            </td>
            <td className="py-1.5 pl-2 text-right tabular text-[var(--text-tertiary)]">
              {p.weight_pct.toFixed(1)}%
            </td>
          </tr>
        ))}
      </tbody>
      <tfoot>
        <tr className="border-t border-[var(--rule)] text-[var(--text-secondary)] font-medium">
          <td colSpan={5} className="py-2 pr-3 type-mono-sm text-[var(--text-tertiary)]">
            {g.positions.length} posições
          </td>
          <td className="py-2 px-2 text-right tabular type-mono-sm">
            {formatCurrency(g.total_cost, cur, 0)}
          </td>
          <td className="py-2 px-2 text-right tabular type-mono-sm">
            {formatCurrency(g.total_value, cur, 0)}
          </td>
          <td className={`py-2 px-2 text-right tabular type-mono-sm ${pnlClass(g.total_pnl)}`}>
            {g.total_pnl >= 0 ? "+" : ""}{formatCurrency(g.total_pnl, cur, 0)}
          </td>
          <td className={`py-2 pl-2 text-right tabular type-mono-sm ${pnlClass(g.pnl_pct)}`}>
            {g.total_pnl >= 0 ? "+" : ""}{g.pnl_pct.toFixed(1)}%
          </td>
          <td className="py-2 pl-2 text-right tabular type-mono-sm text-[var(--text-tertiary)]">
            {g.weight_pct.toFixed(1)}%
          </td>
        </tr>
      </tfoot>
    </table>
  );
}

function RFTable({ g }: { g: GroupMeta }) {
  return (
    <table className="w-full type-mono-sm mt-1">
      <thead>
        <tr className="text-[var(--text-tertiary)] border-b border-[var(--border-subtle)]">
          <th className="text-left py-1.5 pr-3 font-normal">Ativo</th>
          <th className="text-left py-1.5 pr-3 font-normal">Taxa</th>
          <th className="text-right py-1.5 px-2 font-normal">Qtd</th>
          <th className="text-left py-1.5 px-2 font-normal">Vencimento</th>
          <th className="text-right py-1.5 px-2 font-normal">Investido</th>
          <th className="text-right py-1.5 px-2 font-normal">Valor</th>
          <th className="text-right py-1.5 px-2 font-normal">P&amp;L</th>
          <th className="text-right py-1.5 pl-2 font-normal">P&amp;L%</th>
          <th className="text-right py-1.5 pl-2 font-normal">Peso</th>
        </tr>
      </thead>
      <tbody className="divide-y divide-[var(--border-subtle)]">
        {g.positions.map((p) => (
          <tr key={p.id} className="hover:bg-[var(--bg-raised)] transition-colors">
            <td className="py-1.5 pr-3 text-[var(--text-primary)] font-medium max-w-[220px] truncate">
              {p.name}
            </td>
            <td className="py-1.5 pr-3 text-[var(--text-tertiary)]">
              {p.rate ?? "—"}
            </td>
            <td className="py-1.5 px-2 text-right tabular text-[var(--text-secondary)]">
              {fmtQty(p.quantity)}
            </td>
            <td className="py-1.5 px-2 text-[var(--text-secondary)]">
              {p.maturity_date ? formatDate(p.maturity_date, "medium") : "—"}
            </td>
            <td className="py-1.5 px-2 text-right tabular text-[var(--text-secondary)]">
              {formatCurrency(p.cost_basis, "BRL", 0)}
            </td>
            <td className="py-1.5 px-2 text-right tabular font-medium">
              {formatCurrency(p.current_value, "BRL", 0)}
            </td>
            <td className={`py-1.5 px-2 text-right tabular ${pnlClass(p.pnl_abs)}`}>
              {p.pnl_abs >= 0 ? "+" : ""}{formatCurrency(p.pnl_abs, "BRL", 0)}
            </td>
            <td className={`py-1.5 pl-2 text-right tabular ${pnlClass(p.pnl_pct)}`}>
              {p.pnl_pct !== null
                ? `${p.pnl_pct >= 0 ? "+" : ""}${p.pnl_pct.toFixed(1)}%`
                : "—"}
            </td>
            <td className="py-1.5 pl-2 text-right tabular text-[var(--text-tertiary)]">
              {p.weight_pct.toFixed(1)}%
            </td>
          </tr>
        ))}
      </tbody>
      <tfoot>
        <tr className="border-t border-[var(--rule)] text-[var(--text-secondary)] font-medium">
          <td colSpan={4} className="py-2 pr-3 type-mono-sm text-[var(--text-tertiary)]">
            {g.positions.length} posições
          </td>
          <td className="py-2 px-2 text-right tabular type-mono-sm">
            {formatCurrency(g.total_cost, "BRL", 0)}
          </td>
          <td className="py-2 px-2 text-right tabular type-mono-sm">
            {formatCurrency(g.total_value, "BRL", 0)}
          </td>
          <td className={`py-2 px-2 text-right tabular type-mono-sm ${pnlClass(g.total_pnl)}`}>
            {g.total_pnl >= 0 ? "+" : ""}{formatCurrency(g.total_pnl, "BRL", 0)}
          </td>
          <td className={`py-2 pl-2 text-right tabular type-mono-sm ${pnlClass(g.pnl_pct)}`}>
            {g.total_pnl >= 0 ? "+" : ""}{g.pnl_pct.toFixed(1)}%
          </td>
          <td className="py-2 pl-2 text-right tabular type-mono-sm text-[var(--text-tertiary)]">
            {g.weight_pct.toFixed(1)}%
          </td>
        </tr>
      </tfoot>
    </table>
  );
}

// ── page ──────────────────────────────────────────────────────────────────────

export default function PortfolioPage() {
  const positions = listAllPositions();
  const groups = buildGroups(positions);

  const brPositions = positions.filter((p) => p.market === "br");
  const usPositions = positions.filter((p) => p.market === "us");

  const brValue = brPositions.reduce((s, p) => s + p.current_value, 0);
  const brCost  = brPositions.reduce((s, p) => s + p.cost_basis, 0);
  const brPnl   = brValue - brCost;
  const brPnlPct = brCost > 0 ? (brPnl / brCost) * 100 : 0;

  const usValue = usPositions.reduce((s, p) => s + p.current_value, 0);
  const usCost  = usPositions.reduce((s, p) => s + p.cost_basis, 0);
  const usPnl   = usValue - usCost;
  const usPnlPct = usCost > 0 ? (usPnl / usCost) * 100 : 0;

  const brGroups = groups.filter((g) => g.currency === "BRL");
  const usGroups = groups.filter((g) => g.currency === "USD");

  return (
    <div className="p-8 space-y-6 max-w-[1400px]">
      <PageHeader title="Carteira" subtitle="Posições consolidadas · todas as classes" />

      {/* ── Grand totals ──────────────────────────────────────────── */}
      <div className="grid grid-cols-2 gap-8 border-t-2 border-[var(--rule)] pt-5">
        {/* BR total */}
        <div>
          <p className="type-h3 mb-1">Brasil · BRL</p>
          <p className="type-display tabular text-[var(--text-primary)]">
            {formatCurrency(brValue, "BRL", 0)}
          </p>
          <p className={`type-mono-sm mt-1 ${pnlClass(brPnl)}`}>
            {brPnl >= 0 ? "+" : ""}{formatCurrency(brPnl, "BRL", 0)}
            {" "}({brPnlPct >= 0 ? "+" : ""}{brPnlPct.toFixed(1)}%) vs custo {formatCurrency(brCost, "BRL", 0)}
          </p>
        </div>
        {/* US total */}
        <div>
          <p className="type-h3 mb-1">EUA · USD</p>
          <p className="type-display tabular text-[var(--text-primary)]">
            {formatCurrency(usValue, "USD", 0)}
          </p>
          <p className={`type-mono-sm mt-1 ${pnlClass(usPnl)}`}>
            {usPnl >= 0 ? "+" : ""}{formatCurrency(usPnl, "USD", 0)}
            {" "}({usPnlPct >= 0 ? "+" : ""}{usPnlPct.toFixed(1)}%) vs custo {formatCurrency(usCost, "USD", 0)}
          </p>
        </div>
      </div>

      {/* ── BR distribution bar ───────────────────────────────────── */}
      {brGroups.length > 0 && (
        <div>
          <p className="type-h3 mb-2">Distribuição BR</p>
          <DistributionBar groups={brGroups} />
        </div>
      )}

      {/* ── BR groups ─────────────────────────────────────────────── */}
      {brGroups.map((g) => (
        <div key={g.label}>
          <GroupHeader g={g} />
          {g.is_rf ? <RFTable g={g} /> : <EquityTable g={g} />}
        </div>
      ))}

      {/* ── US distribution bar ───────────────────────────────────── */}
      {usGroups.length > 0 && (
        <div className="mt-12">
          <div className="border-t-2 border-[var(--rule)] pt-5 mb-4">
            <p className="type-h3 mb-2">Distribuição US</p>
            <DistributionBar groups={usGroups} />
          </div>
          {usGroups.map((g) => (
            <div key={g.label}>
              <GroupHeader g={g} />
              <EquityTable g={g} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
