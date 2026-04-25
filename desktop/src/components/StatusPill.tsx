/**
 * StatusPill.tsx — mirror of scripts/_components.py::status_pill.
 */

type Tone = 'neutral' | 'positive' | 'negative' | 'warning' | 'accent';

export function StatusPill({ children, tone = 'neutral' }: {
  children: React.ReactNode;
  tone?: Tone;
}) {
  return <span className={`status-pill status-pill--${tone}`}>{children}</span>;
}
