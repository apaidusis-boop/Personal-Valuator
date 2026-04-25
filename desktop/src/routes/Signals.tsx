import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api, type SignalRow } from '@/lib/api';
import { KPITile } from '@/components/KPITile';
import { SectionHeader } from '@/components/SectionHeader';
import { StatusPill } from '@/components/StatusPill';

type Summary = {
  total_open: number;
  total_closed: number;
  by_direction: Record<string, number>;
  by_method_top10: Record<string, number>;
};

const dirTone = (d: string) =>
  d === 'LONG' ? 'positive' : d === 'SHORT' ? 'negative' : 'neutral';

export function Signals() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [signals, setSignals] = useState<SignalRow[]>([]);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([api.signalsSummary(), api.signalsOpen(50)])
      .then(([s, sigs]) => {
        setSummary(s);
        setSignals(sigs);
      })
      .catch(e => setErr(String(e)));
  }, []);

  if (err) return <div className="state-message state-message--error">{err}</div>;

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Paper signals</h1>
          <div className="kpi-tile__label" style={{ marginTop: 4 }}>
            Book methods × portfolio (paper-only, never real capital)
          </div>
        </div>
      </div>

      <div className="kpi-grid">
        <KPITile
          label="Total open"
          value={String(summary?.total_open ?? '—')}
          tone="warning"
        />
        <KPITile
          label="Closed (history)"
          value={String(summary?.total_closed ?? '—')}
          tone="neutral"
        />
        <KPITile
          label="Long open"
          value={String(summary?.by_direction.LONG ?? 0)}
          tone="positive"
        />
        <KPITile
          label="Short open"
          value={String(summary?.by_direction.SHORT ?? 0)}
          tone="negative"
        />
      </div>

      <SectionHeader title="Top methods (open)" caption="By signal count" />
      <div className="sector-list" style={{ marginBottom: 24 }}>
        {summary && Object.entries(summary.by_method_top10).map(([method, n]) => {
          const max = Math.max(...Object.values(summary.by_method_top10));
          return (
            <div key={method} className="sector-row">
              <div className="sector-row__name" style={{ width: 200 }}>{method}</div>
              <div className="sector-row__bar">
                <div className="sector-row__bar-fill" style={{ width: `${(n / max) * 100}%` }} />
              </div>
              <div className="sector-row__value">{n}</div>
            </div>
          );
        })}
      </div>

      <SectionHeader title="Open signals" caption={`Most recent ${signals.length}`} />
      <table className="helena">
        <thead>
          <tr>
            <th>Date</th>
            <th>Ticker</th>
            <th>Mkt</th>
            <th>Method</th>
            <th>Dir</th>
            <th>Horizon</th>
            <th className="num">Move %</th>
            <th className="num">Entry</th>
            <th>Thesis</th>
          </tr>
        </thead>
        <tbody>
          {signals.map(s => (
            <tr key={`${s.market}-${s.id}`}>
              <td>{s.signal_date}</td>
              <td><Link to={`/ticker/${s.ticker}`}>{s.ticker}</Link></td>
              <td>{s.market.toUpperCase()}</td>
              <td style={{ maxWidth: 180, color: 'var(--muted)' }}>{s.method_id}</td>
              <td><StatusPill tone={dirTone(s.direction)}>{s.direction}</StatusPill></td>
              <td>{s.horizon}</td>
              <td className="num">{s.expected_move_pct >= 0 ? '+' : ''}{s.expected_move_pct.toFixed(0)}%</td>
              <td className="num">{s.entry_price?.toFixed(2)}</td>
              <td style={{ maxWidth: 280, color: 'var(--muted)', fontSize: '0.78rem' }}>{s.thesis}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
