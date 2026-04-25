import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { api, type VerdictHistoryRow, type SignalRow } from '@/lib/api';
import { KPITile } from '@/components/KPITile';
import { SectionHeader } from '@/components/SectionHeader';
import { StatusPill } from '@/components/StatusPill';

type Summary = {
  ticker: string;
  market: 'br' | 'us';
  company: { name: string; sector: string; currency: string };
  last_price?: { date: string; close: number; volume: number };
  latest_score?: { run_date: string; score: number; passes_screen: number };
};

type Verdict =
  | { ticker: string; error: string }
  | {
      ticker: string;
      action: string;
      total_score: number;
      confidence_pct: number;
      quality_score: number;
      valuation_score: number;
      momentum_score: number;
      narrative_score: number;
      reasons?: string[];
    };

const ACTION_TONE: Record<string, 'positive' | 'negative' | 'warning' | 'accent' | 'neutral'> = {
  BUY: 'positive', ADD: 'positive',
  WATCH: 'accent', HOLD: 'warning',
  TRIM: 'warning', SELL: 'negative', AVOID: 'negative', SKIP: 'neutral',
};

function isVerdict(v: Verdict | null): v is Exclude<Verdict, { error: string }> {
  return !!v && !('error' in v);
}

export function Ticker() {
  const { symbol } = useParams<{ symbol: string }>();
  const navigate = useNavigate();
  const [input, setInput] = useState(symbol ?? 'ACN');
  const [data, setData] = useState<Summary | null>(null);
  const [verdict, setVerdict] = useState<Verdict | null>(null);
  const [history, setHistory] = useState<VerdictHistoryRow[]>([]);
  const [signals, setSignals] = useState<SignalRow[]>([]);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [computing, setComputing] = useState(false);

  const sym = symbol ?? input;

  useEffect(() => {
    if (!sym) return;
    setLoading(true);
    setErr(null);
    setVerdict(null);
    Promise.all([
      api.ticker(sym).then(d => setData(d as Summary)),
      api.verdictHistory(sym, 10).then(setHistory).catch(() => setHistory([])),
      api.signalsByTicker(sym).then(setSignals).catch(() => setSignals([])),
    ])
      .catch(e => setErr(String(e)))
      .finally(() => setLoading(false));
  }, [sym]);

  async function compute() {
    if (!sym) return;
    setComputing(true);
    try {
      const v = await api.verdict(sym);
      setVerdict(v as Verdict);
    } catch (e) {
      setVerdict({ ticker: sym, error: String(e) });
    } finally {
      setComputing(false);
    }
  }

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
        onSubmit={e => { e.preventDefault(); navigate(`/ticker/${input.toUpperCase()}`); }}
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
              value={data.latest_score ? data.latest_score.score.toFixed(2) : '—'}
              tone={
                data.latest_score?.passes_screen === 1 ? 'positive'
                  : data.latest_score?.passes_screen === 0 ? 'negative' : 'neutral'
              }
              footnote={data.latest_score?.run_date}
            />
          </div>

          <SectionHeader title="Verdict" caption="Computed on-demand by the engine" />
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
            <button className="btn--primary" onClick={compute} disabled={computing}>
              {computing ? 'Computing…' : 'Compute verdict'}
            </button>
            {isVerdict(verdict) && (
              <>
                <StatusPill tone={ACTION_TONE[verdict.action] ?? 'neutral'}>
                  {verdict.action}
                </StatusPill>
                <span className="tabular" style={{ color: 'var(--muted)' }}>
                  score {verdict.total_score.toFixed(2)}/10 · conf {verdict.confidence_pct}%
                </span>
              </>
            )}
            {verdict && 'error' in verdict && (
              <span style={{ color: 'var(--negative)', fontSize: '0.84rem' }}>{verdict.error}</span>
            )}
          </div>

          {isVerdict(verdict) && (
            <>
              <div className="kpi-grid" style={{ marginBottom: 8 }}>
                <KPITile label="Quality" value={`${verdict.quality_score.toFixed(1)}/10`} tone="positive" />
                <KPITile label="Valuation" value={`${verdict.valuation_score.toFixed(1)}/10`} tone="accent" />
                <KPITile label="Momentum" value={`${verdict.momentum_score.toFixed(1)}/10`} tone="warning" />
                <KPITile label="Narrative" value={`${verdict.narrative_score.toFixed(1)}/10`} tone="neutral" />
              </div>
              {verdict.reasons && verdict.reasons.length > 0 && (
                <ul style={{ color: 'var(--muted)', fontSize: '0.84rem', lineHeight: 1.6 }}>
                  {verdict.reasons.map((r, i) => <li key={i}>{r}</li>)}
                </ul>
              )}
            </>
          )}

          {history.length > 0 && (
            <>
              <SectionHeader title="Verdict history" caption={`${history.length} entries`} />
              <table className="helena">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Action</th>
                    <th className="num">Score</th>
                    <th className="num">Conf %</th>
                    <th className="num">Q</th>
                    <th className="num">V</th>
                    <th className="num">M</th>
                    <th className="num">N</th>
                    <th className="num">Price</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((h, i) => (
                    <tr key={i}>
                      <td>{h.date}</td>
                      <td><StatusPill tone={ACTION_TONE[h.action] ?? 'neutral'}>{h.action}</StatusPill></td>
                      <td className="num">{h.total_score.toFixed(2)}</td>
                      <td className="num">{h.confidence_pct}</td>
                      <td className="num">{h.quality_score.toFixed(1)}</td>
                      <td className="num">{h.valuation_score.toFixed(1)}</td>
                      <td className="num">{h.momentum_score.toFixed(1)}</td>
                      <td className="num">{h.narrative_score.toFixed(1)}</td>
                      <td className="num">{h.price_at_verdict?.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}

          {signals.length > 0 && (
            <>
              <SectionHeader title="Paper signals" caption={`${signals.length} for ${sym}`} />
              <table className="helena">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Method</th>
                    <th>Dir</th>
                    <th className="num">Move %</th>
                    <th className="num">Entry</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {signals.slice(0, 15).map(s => (
                    <tr key={s.id}>
                      <td>{s.signal_date}</td>
                      <td style={{ color: 'var(--muted)', maxWidth: 200 }}>{s.method_id}</td>
                      <td>
                        <StatusPill tone={s.direction === 'LONG' ? 'positive' : s.direction === 'SHORT' ? 'negative' : 'neutral'}>
                          {s.direction}
                        </StatusPill>
                      </td>
                      <td className="num">{s.expected_move_pct >= 0 ? '+' : ''}{s.expected_move_pct.toFixed(0)}%</td>
                      <td className="num">{s.entry_price?.toFixed(2)}</td>
                      <td>
                        <StatusPill tone={s.status === 'open' ? 'warning' : 'neutral'}>{s.status}</StatusPill>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}

          <SectionHeader title="Company" />
          <table className="helena">
            <tbody>
              <tr><td style={{ color: 'var(--muted)', width: 140 }}>Name</td><td>{data.company.name}</td></tr>
              <tr><td style={{ color: 'var(--muted)' }}>Sector</td><td>{data.company.sector ?? '—'}</td></tr>
              <tr><td style={{ color: 'var(--muted)' }}>Currency</td><td>{data.company.currency}</td></tr>
            </tbody>
          </table>
          <div style={{ marginTop: 12 }}>
            <Link to="/portfolio" style={{ color: 'var(--accent)', fontSize: '0.84rem' }}>← back to portfolio</Link>
          </div>
        </>
      )}
    </>
  );
}
