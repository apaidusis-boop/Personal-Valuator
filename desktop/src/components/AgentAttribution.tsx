/**
 * AgentAttribution.tsx — mirror of scripts/_components.py::agent_attribution.
 *
 * Implementa os 3 transparency moments (Why · What · Who paid)
 * documentados em Design_System.md.
 */
export function AgentAttribution({ agent, tier, why }: {
  agent: string;
  tier: string;
  why: string;
}) {
  return (
    <div style={{
      color: 'var(--muted)',
      fontSize: '0.72rem',
      fontFamily: 'var(--font-mono)',
      letterSpacing: '0.02em',
      padding: '6px 0',
      borderTop: '1px solid var(--border)',
      marginTop: '8px',
    }}>
      by <span style={{ color: 'var(--accent)' }}>{agent}</span>
      {' · '}
      <span style={{ color: 'var(--text)' }}>{tier}</span>
      {' · '}
      {why}
    </div>
  );
}
