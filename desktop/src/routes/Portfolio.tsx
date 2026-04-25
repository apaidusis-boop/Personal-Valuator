import { useEffect, useState } from 'react';
import { api, type Position, type SectorRow, type Meta } from '@/lib/api';
import { KPITile } from '@/components/KPITile';
import { SectionHeader } from '@/components/SectionHeader';
import { StatusPill } from '@/components/StatusPill';

const fmtBRL = (v: number) =>
  v.toLocaleString('pt-PT', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });

const fmtPct = (v: number | null | undefined) =>
  v == null ? '—' : `${v >= 0 ? '+' : ''}${v.toFixed(2)}%`;

const fmtQty = (v: number) =>
  Number.isInteger(v) ? v.toString() : v.toFixed(2);

export function Portfolio() {
  const [meta, setMeta] = useState<Meta | null>(null);
  const [positions, setPositions] = useState<Position[]>([]);
  const [sectors, setSectors] = useState<SectorRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([api.meta(), api.positions(), api.sectors()])
      .then(([m, p, s]) => {
        setMeta(m);
        setPositions(p);
        setSectors(s);
      })
      .catch(e => setErr(String(e)))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="state-message">Loading…</div>;
  if (err)
    return (
      <div className="state-message state-message--error">
        Backend unreachable: {err}
        <br />
        <small>Run: <code>uvicorn desktop.backend.main:app --port 8765</code></small>
      </div>
    );

  // Compute totals client-side
  const fx = meta?.fx_usdbrl ?? 5.0;
  const brMV = positions.filter(p => p.market === 'br').reduce((s, p) => s + (p.mv_native || 0), 0);
  const usMV = positions.filter(p => p.market === 'us').reduce((s, p) => s + (p.mv_native || 0), 0);
  const totalBRL = brMV + usMV * fx;

  const sortedPositions = [...positions].sort((a, b) => {
    const aMV = a.market === 'br' ? a.mv_native : a.mv_native * fx;
    const bMV = b.market === 'br' ? b.mv_native : b.mv_native * fx;
    return bMV - aMV;
  });

  const maxSector = sectors[0]?.mv_brl || 1;

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Portfolio</h1>
          <div className="kpi-tile__label" style={{ marginTop: 4 }}>
            BR + US consolidated · BRL
          </div>
        </div>
        <div className="page-header__meta">
          fx {fx.toFixed(4)} · last px {meta?.last_price_date ?? '—'}
        </div>
      </div>

      <div className="kpi-grid">
        <KPITile
          label="Total"
          value={fmtBRL(totalBRL)}
          tone="accent"
          footnote={`${positions.length} active positions`}
        />
        <KPITile
          label="Holdings"
          value={String(meta?.holdings_active ?? positions.length)}
          tone="neutral"
        />
        <KPITile
          label="BR"
          value={fmtBRL(brMV)}
          delta={`${((brMV / totalBRL) * 100).toFixed(1)}% of total`}
          tone="positive"
        />
        <KPITile
          label="US (in BRL)"
          value={fmtBRL(usMV * fx)}
          delta={`${((usMV * fx / totalBRL) * 100).toFixed(1)}% of total`}
          tone="positive"
        />
      </div>

      <SectionHeader title="Sector exposure" caption="MV in BRL · top 10" />
      <div className="sector-list">
        {sectors.slice(0, 10).map(s => (
          <div key={s.sector} className="sector-row">
            <div className="sector-row__name">{s.sector}</div>
            <div className="sector-row__bar">
              <div
                className="sector-row__bar-fill"
                style={{ width: `${(s.mv_brl / maxSector) * 100}%` }}
              />
            </div>
            <div className="sector-row__value">{fmtBRL(s.mv_brl)}</div>
          </div>
        ))}
      </div>

      <SectionHeader title="Holdings" caption="Sorted by market value" />
      <table className="helena holdings-table">
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Mkt</th>
            <th>Sector</th>
            <th className="num">Qty</th>
            <th className="num">Entry</th>
            <th className="num">Now</th>
            <th className="num">MV (native)</th>
            <th className="num">P&L %</th>
            <th>Screen</th>
          </tr>
        </thead>
        <tbody>
          {sortedPositions.map(p => {
            const pnlClass = p.pnl_pct == null ? '' :
              p.pnl_pct >= 0 ? 'pnl--positive' : 'pnl--negative';
            return (
              <tr key={`${p.ticker}-${p.market}`}>
                <td><strong>{p.ticker}</strong></td>
                <td>{p.market.toUpperCase()}</td>
                <td>{p.sector ?? '—'}</td>
                <td className="num">{fmtQty(p.quantity)}</td>
                <td className="num">{p.entry_price?.toFixed(2) ?? '—'}</td>
                <td className="num">{p.price?.toFixed(2) ?? '—'}</td>
                <td className="num">{p.mv_native.toLocaleString('pt-PT', { maximumFractionDigits: 0 })}</td>
                <td className={`num ${pnlClass}`}>{fmtPct(p.pnl_pct)}</td>
                <td>
                  {p.screen_pass === 1 ? (
                    <StatusPill tone="positive">Pass</StatusPill>
                  ) : p.screen_pass === 0 ? (
                    <StatusPill tone="negative">Fail</StatusPill>
                  ) : (
                    <StatusPill tone="neutral">—</StatusPill>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
}
