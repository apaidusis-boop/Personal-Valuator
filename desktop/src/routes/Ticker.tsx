import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '@/lib/api';
import { KPITile } from '@/components/KPITile';
import { SectionHeader } from '@/components/SectionHeader';

type Summary = {
  ticker: string;
  market: 'br' | 'us';
  company: { name: string; sector: string; currency: string };
  last_price?: { date: string; close: number; volume: number };
  latest_score?: { run_date: string; score: number; passes_screen: number };
};

export function Ticker() {
  const { symbol } = useParams<{ symbol: string }>();
  const navigate = useNavigate();
  const [input, setInput] = useState(symbol ?? 'ACN');
  const [data, setData] = useState<Summary | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const sym = symbol ?? input;

  useEffect(() => {
    if (!sym) return;
    setLoading(true);
    setErr(null);
    api.ticker(sym)
      .then(d => setData(d as Summary))
      .catch(e => setErr(String(e)))
      .finally(() => setLoading(false));
  }, [sym]);

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Ticker</h1>
          <div className="kpi-tile__label" style={{ marginTop: 4 }}>
            Single-ticker drill-down
          </div>
        </div>
      </div>

      <form
        onSubmit={e => {
          e.preventDefault();
          navigate(`/ticker/${input.toUpperCase()}`);
        }}
        style={{ display: 'flex', gap: 8, marginBottom: 24 }}
      >
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="ACN, ITSA4, …"
          style={{
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-button)',
            color: 'var(--text)',
            padding: '8px 12px',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.88rem',
            minWidth: 200,
          }}
        />
        <button type="submit" className="btn--primary">Load</button>
      </form>

      {loading && <div className="state-message">Loading {sym}…</div>}
      {err && <div className="state-message state-message--error">{err}</div>}

      {data && !loading && (
        <>
          <div className="kpi-grid">
            <KPITile label="Ticker" value={data.ticker} tone="accent" />
            <KPITile label="Market" value={data.market.toUpperCase()} tone="neutral" />
            <KPITile
              label="Last close"
              value={
                data.last_price
                  ? `${data.company.currency} ${data.last_price.close.toFixed(2)}`
                  : '—'
              }
              footnote={data.last_price?.date}
              tone="positive"
            />
            <KPITile
              label="Screen score"
              value={
                data.latest_score
                  ? data.latest_score.score.toFixed(2)
                  : '—'
              }
              tone={
                data.latest_score?.passes_screen === 1 ? 'positive'
                  : data.latest_score?.passes_screen === 0 ? 'negative' : 'neutral'
              }
              footnote={data.latest_score?.run_date}
            />
          </div>

          <SectionHeader title="Company" />
          <table className="helena">
            <tbody>
              <tr><td style={{ color: 'var(--muted)', width: 140 }}>Name</td><td>{data.company.name}</td></tr>
              <tr><td style={{ color: 'var(--muted)' }}>Sector</td><td>{data.company.sector ?? '—'}</td></tr>
              <tr><td style={{ color: 'var(--muted)' }}>Currency</td><td>{data.company.currency}</td></tr>
            </tbody>
          </table>
        </>
      )}
    </>
  );
}
