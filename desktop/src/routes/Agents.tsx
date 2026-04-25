import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { SectionHeader } from '@/components/SectionHeader';
import { StatusPill } from '@/components/StatusPill';

type Agent = {
  name: string;
  description: string;
  schedule: string;
  enabled: boolean;
};

type RunResult = {
  agent: string;
  status: string;
  summary: string;
  duration_sec: number;
  actions: string[];
  errors: string[];
};

export function Agents() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [err, setErr] = useState<string | null>(null);
  const [running, setRunning] = useState<string | null>(null);
  const [results, setResults] = useState<Record<string, RunResult>>({});

  useEffect(() => {
    api.agentsList()
      .then(setAgents)
      .catch(e => setErr(String(e)));
  }, []);

  async function run(name: string) {
    setRunning(name);
    try {
      const r = await api.agentRun(name, true); // dry_run by default
      setResults(prev => ({ ...prev, [name]: r }));
    } catch (e) {
      setResults(prev => ({
        ...prev,
        [name]: { agent: name, status: 'failed', summary: String(e),
                  duration_sec: 0, actions: [], errors: [String(e)] },
      }));
    } finally {
      setRunning(null);
    }
  }

  if (err) return <div className="state-message state-message--error">{err}</div>;

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Agents</h1>
          <div className="kpi-tile__label" style={{ marginTop: 4 }}>
            Synthetic company · {agents.length} registered
          </div>
        </div>
      </div>

      <SectionHeader title="Registry" caption="From config/agents.yaml" />

      <table className="helena">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Schedule</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {agents.map(a => {
            const r = results[a.name];
            return (
              <tr key={a.name}>
                <td><strong>{a.name}</strong></td>
                <td style={{ maxWidth: 360 }}>{a.description}</td>
                <td><code>{a.schedule}</code></td>
                <td>
                  {a.enabled ? (
                    <StatusPill tone="positive">Enabled</StatusPill>
                  ) : (
                    <StatusPill tone="neutral">Disabled</StatusPill>
                  )}
                  {r && (
                    <span style={{ marginLeft: 6 }}>
                      <StatusPill tone={r.status === 'ok' ? 'positive'
                        : r.status === 'no_action' ? 'neutral'
                        : 'negative'}>
                        {r.status}
                      </StatusPill>
                    </span>
                  )}
                </td>
                <td>
                  <button
                    onClick={() => run(a.name)}
                    disabled={running === a.name}
                  >
                    {running === a.name ? 'running…' : 'dry-run'}
                  </button>
                  {r && (
                    <div style={{ marginTop: 4, color: 'var(--muted)', fontSize: '0.72rem' }}>
                      {r.duration_sec.toFixed(2)}s · {r.summary}
                    </div>
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
