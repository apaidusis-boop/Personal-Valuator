/**
 * KPITile.tsx — mirror of scripts/_components.py::kpi_tile.
 *
 * Card métrico com left-accent border. Substituto de st.metric.
 */
import './KPITile.css';

type Tone = 'neutral' | 'positive' | 'negative' | 'warning' | 'accent';

type Props = {
  label: string;
  value: string;
  delta?: string;
  footnote?: string;
  tone?: Tone;
};

const TONE_CSS: Record<Tone, string> = {
  neutral:  'var(--muted)',
  positive: 'var(--positive)',
  negative: 'var(--negative)',
  warning:  'var(--warning)',
  accent:   'var(--accent)',
};

export function KPITile({ label, value, delta, footnote, tone = 'accent' }: Props) {
  const accent = TONE_CSS[tone];
  const deltaTone =
    delta?.startsWith('+') ? 'positive' :
    delta?.startsWith('-') ? 'negative' : null;

  return (
    <div className="kpi-tile" style={{ borderLeftColor: accent }}>
      <div className="kpi-tile__label">{label}</div>
      <div className="kpi-tile__value">{value}</div>
      {delta && (
        <div className={`kpi-tile__delta ${deltaTone ? `kpi-tile__delta--${deltaTone}` : ''}`}>
          {delta}
        </div>
      )}
      {footnote && <div className="kpi-tile__footnote">{footnote}</div>}
    </div>
  );
}
