/**
 * api.ts — fetch wrapper for the Helena backend (FastAPI sidecar).
 *
 * Sidecar listens on 127.0.0.1:8765 in both dev and prod (Tauri spawns it).
 */

const BASE = 'http://127.0.0.1:8765/api';

async function get<T>(path: string): Promise<T> {
  const r = await fetch(`${BASE}${path}`);
  if (!r.ok) throw new Error(`${r.status} ${r.statusText} on GET ${path}`);
  return r.json() as Promise<T>;
}

async function post<T>(path: string, body?: unknown): Promise<T> {
  const r = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!r.ok) throw new Error(`${r.status} ${r.statusText} on POST ${path}`);
  return r.json() as Promise<T>;
}

export type Position = {
  ticker: string;
  market: 'br' | 'us';
  name?: string;
  sector?: string;
  currency?: string;
  quantity: number;
  entry_price: number;
  price?: number;
  price_date?: string;
  mv_native: number;
  cost_native: number;
  pnl_pct?: number;
  screen_score?: number;
  screen_pass?: number;
};

export type SectorRow = { sector: string; mv_brl: number };

export type Snapshot = {
  date: string;
  ticker: string;
  mv_brl: number;
  mv_native: number;
  market: 'br' | 'us';
};

export type Meta = {
  fx_usdbrl: number;
  holdings_active: number;
  last_price_date: string | null;
};

export type ActionRow = {
  id: number;
  ticker: string;
  market: 'br' | 'us';
  kind: string;
  trigger_id: string;
  action_hint: string;
  status: 'open' | 'resolved' | 'ignored';
  opened_at: string;
  resolved_at?: string | null;
  notes?: string | null;
  snapshot?: Record<string, unknown> | null;
};

export type SignalRow = {
  id: number;
  signal_date: string;
  ticker: string;
  market: 'br' | 'us';
  method_id: string;
  book_slug: string;
  direction: 'LONG' | 'SHORT' | string;
  horizon: string;
  expected_move_pct: number;
  entry_price: number;
  thesis: string;
  status: 'open' | 'closed';
  notes?: string | null;
};

export type VerdictHistoryRow = {
  date: string;
  action: string;
  total_score: number;
  confidence_pct: number;
  quality_score: number;
  valuation_score: number;
  momentum_score: number;
  narrative_score: number;
  price_at_verdict: number;
  recorded_at: string;
  market: 'br' | 'us';
};

export const api = {
  health:    () => get<{ status: string; service: string; version: string }>('/health'),
  meta:      () => get<Meta>('/meta'),
  positions: () => get<Position[]>('/positions'),
  sectors:   () => get<SectorRow[]>('/sectors'),
  snapshot:  (days = 180) => get<Snapshot[]>(`/snapshot?days=${days}`),

  ticker:    (sym: string) => get(`/ticker/${sym}`),
  prices:    (sym: string, days = 365) => get(`/prices/${sym}?days=${days}`),
  verdict:   (sym: string) => get(`/verdict/${sym}`),
  verdictHistory: (sym: string, limit = 20) =>
    get<VerdictHistoryRow[]>(`/verdicts/${sym}/history?limit=${limit}`),

  agentsList: () => get<{ name: string; description: string; schedule: string; enabled: boolean }[]>('/agents/list'),
  agentRun:   (name: string, dryRun = false) =>
    post<{ agent: string; status: string; summary: string; duration_sec: number; actions: string[]; errors: string[] }>(
      `/agents/run/${name}${dryRun ? '?dry_run=true' : ''}`,
    ),

  actionsOpen:    () => get<ActionRow[]>('/actions/open'),
  actionsRecent:  (limit = 30) => get<ActionRow[]>(`/actions/recent?limit=${limit}`),
  actionResolve:  (market: string, id: number, note?: string) =>
    post<{ id: number; market: string; status: string; resolved_at: string }>(
      `/actions/${market}/${id}/resolve`, note ? { note } : undefined,
    ),
  actionIgnore:   (market: string, id: number, note?: string) =>
    post<{ id: number; market: string; status: string; resolved_at: string }>(
      `/actions/${market}/${id}/ignore`, note ? { note } : undefined,
    ),

  signalsOpen:     (limit = 50) => get<SignalRow[]>(`/signals/open?limit=${limit}`),
  signalsSummary:  () => get<{ total_open: number; total_closed: number; by_direction: Record<string, number>; by_method_top10: Record<string, number> }>('/signals/summary'),
  signalsByTicker: (sym: string) => get<SignalRow[]>(`/signals/by-ticker/${sym}`),
};
