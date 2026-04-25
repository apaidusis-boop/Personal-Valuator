/**
 * plotly_theme.ts — port of scripts/_theme.py::PLOTLY_TEMPLATE (`ii_dark`).
 *
 * Apply per-figure:
 *   import { iiDark } from '@/lib/plotly_theme'
 *   <Plot data={...} layout={iiDark.layout} config={iiDark.config} />
 *
 * Keep this in sync with scripts/_theme.py if tokens change.
 */

export const COLORS = {
  bg:         '#0f1115',
  surface:    '#161a22',
  surface_2:  '#1d2330',
  border:     '#222833',
  text:       '#e6e8eb',
  muted:      '#7a8290',
  accent:     '#4f8df9',
  positive:   '#4ade80',
  negative:   '#f87171',
  warning:    '#fbbf24',
  amethyst:   '#a78bfa',
} as const;

export const CATEGORICAL = [
  COLORS.accent,
  COLORS.positive,
  COLORS.negative,
  COLORS.warning,
  COLORS.amethyst,
] as const;

export const iiDarkLayout = {
  paper_bgcolor: COLORS.surface,
  plot_bgcolor:  COLORS.surface,
  font: {
    family: 'system-ui, -apple-system, sans-serif',
    color:  COLORS.text,
    size:   13,
  },
  title: {
    font: { color: COLORS.text, size: 15, family: 'system-ui' },
    x: 0.0,
    xanchor: 'left',
    pad: { l: 0, t: 4 },
  },
  xaxis: {
    gridcolor: COLORS.border,
    linecolor: COLORS.border,
    tickfont:  { color: COLORS.muted },
    title:     { font: { color: COLORS.muted } },
    zeroline:  false,
  },
  yaxis: {
    gridcolor: COLORS.border,
    linecolor: COLORS.border,
    tickfont:  { color: COLORS.muted },
    title:     { font: { color: COLORS.muted } },
    zeroline:  false,
  },
  legend: {
    font:        { color: COLORS.muted, size: 11 },
    bgcolor:     'rgba(0,0,0,0)',
    borderwidth: 0,
    orientation: 'h',
    y: 1.05,
    x: 0,
  },
  margin: { l: 8, r: 8, t: 36, b: 8 },
  colorway: CATEGORICAL,
  hoverlabel: {
    bgcolor:     COLORS.surface_2,
    bordercolor: COLORS.border,
    font:        { color: COLORS.text, family: 'system-ui' },
  },
} as const;

export const iiDarkConfig = {
  displayModeBar: false,
  responsive: true,
} as const;

export const iiDark = {
  layout: iiDarkLayout,
  config: iiDarkConfig,
};
