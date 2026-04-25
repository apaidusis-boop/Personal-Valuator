import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api, type ActionRow } from '@/lib/api';
import { KPITile } from '@/components/KPITile';
import { SectionHeader } from '@/components/SectionHeader';
import { StatusPill } from '@/components/StatusPill';

const HINT_TONE: Record<string, 'positive' | 'negative' | 'warning' | 'accent' | 'neutral'> = {
  ADD: 'positive',
  BUY: 'positive',
  TRIM: 'warning',
  SELL: 'negative',
  WATCH: 'accent',
  HOLD: 'neutral',
};

function fmtKey(k: string) {
  return k.replace(/_/g, ' ');
}

function fmtSnapshot(s: Record<string, unknown> | null | undefined): string {
  if (!s) return '';
  return Object.entries(s)
    .filter(([k]) => !['ticker', 'date'].includes(k))
    .slice(0, 4)
    .map(([k, v]) => {
      if (typeof v === 'number') {
        return `${fmtKey(k)} ${v.toFixed(2)}`;
      }
      return `${fmtKey(k)} ${v}`;
    })
    .join(' · ');
}

export function Actions() {
  const [open, setOpen] = useState<ActionRow[]>([]);
  const [recent, setRecent] = useState<ActionRow[]>([]);
  const [busy, setBusy] = useState<number | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [noteDraft, setNoteDraft] = useState<Record<number, string>>({});

  function load() {
    setErr(null);
    Promise.all([api.actionsOpen(), api.actionsRecent(20)])
      .then(([o, r]) => {
        setOpen(o);
        setRecent(r.filter(a => a.status !== 'open'));
      })
      .catch(e => setErr(String(e)));
  }
  useEffect(load, []);

  async function decide(action: ActionRow, kind: 'resolve' | 'ignore') {
    const note = noteDraft[action.id]?.trim() || undefined;
    setBusy(action.id);
    try {
      if (kind === 'resolve') await api.actionResolve(action.market, action.id, note);
      else await api.actionIgnore(action.market, action.id, note);
      load();
      setNoteDraft(d => { const c = { ...d }; delete c[action.id]; return c; });
    } catch (e) {
      setErr(String(e));
    } finally {
      setBusy(null);
    }
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Actions queue</h1>
          <div className="kpi-tile__label" style={{ marginTop: 4 }}>
            Perpetuum proposals + watchlist alerts
          </div>
        </div>
      </div>

      <div className="kpi-grid">
        <KPITile
          label="Open"
          value={String(open.length)}
          tone={open.length > 0 ? 'warning' : 'positive'}
          footnote={open.length > 0 ? 'Decisão pendente' : 'Tudo limpo'}
        />
        <KPITile
          label="Recent decisions"
          value={String(recent.length)}
          tone="neutral"
          footnote="Last 20"
        />
      </div>

      {err && <div className="state-message state-message--error">{err}</div>}

      <SectionHeader title="Open" caption="Por ordem de chegada (mais recente primeiro)" />
      {open.length === 0 ? (
        <div className="state-message">Sem actions pendentes.</div>
      ) : (
        <div className="actions-list">
          {open.map(a => (
            <div key={`${a.market}-${a.id}`} className="action-card">
              <div className="action-card__head">
                <div className="action-card__lead">
                  <Link to={`/ticker/${a.ticker}`} className="action-card__ticker">{a.ticker}</Link>
                  <StatusPill tone={HINT_TONE[a.action_hint] ?? 'neutral'}>
                    {a.action_hint}
                  </StatusPill>
                  <span className="action-card__market">{a.market.toUpperCase()}</span>
                  <span className="action-card__kind">{fmtKey(a.kind)}</span>
                </div>
                <div className="action-card__meta">
                  #{a.id} · {a.opened_at?.slice(0, 10)}
                </div>
              </div>
              {a.notes && <div className="action-card__notes">{a.notes}</div>}
              {a.snapshot && (
                <div className="action-card__snapshot">{fmtSnapshot(a.snapshot)}</div>
              )}
              <div className="action-card__controls">
                <input
                  type="text"
                  placeholder="nota (opcional)"
                  value={noteDraft[a.id] ?? ''}
                  onChange={e => setNoteDraft(d => ({ ...d, [a.id]: e.target.value }))}
                  className="action-card__note-input"
                />
                <button
                  className="btn--primary"
                  disabled={busy === a.id}
                  onClick={() => decide(a, 'resolve')}
                >
                  {busy === a.id ? '…' : 'Resolve'}
                </button>
                <button
                  disabled={busy === a.id}
                  onClick={() => decide(a, 'ignore')}
                >
                  Ignore
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <SectionHeader title="Recent decisions" caption={`${recent.length} resolved/ignored`} />
      {recent.length === 0 ? (
        <div className="state-message">Sem histórico ainda.</div>
      ) : (
        <table className="helena">
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Mkt</th>
              <th>Kind</th>
              <th>Hint</th>
              <th>Status</th>
              <th>Resolved</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {recent.map(a => (
              <tr key={`${a.market}-${a.id}`}>
                <td><Link to={`/ticker/${a.ticker}`}>{a.ticker}</Link></td>
                <td>{a.market.toUpperCase()}</td>
                <td>{fmtKey(a.kind)}</td>
                <td>{a.action_hint}</td>
                <td>
                  <StatusPill tone={a.status === 'resolved' ? 'positive' : 'neutral'}>
                    {a.status}
                  </StatusPill>
                </td>
                <td>{a.resolved_at?.slice(0, 10) ?? '—'}</td>
                <td style={{ color: 'var(--muted)', maxWidth: 280 }}>{a.notes ?? '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}
