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

async function post<T>(path: string): Promise<T> {
  const r = await fetch(`${BASE}${path}`, { method: 'POST' });
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

export const api = {
  health:    () => get<{ status: string; service: string; version: string }>('/health'),
  meta:      () => get<Meta>('/meta'),
  positions: () => get<Position[]>('/positions'),
  sectors:   () => get<SectorRow[]>('/sectors'),
  snapshot:  (days = 180) => get<Snapshot[]>(`/snapshot?days=${days}`),

  ticker:    (sym: string) => get(`/ticker/${sym}`),
  prices:    (sym: string, days = 365) => get(`/prices/${sym}?days=${days}`),
  verdict:   (sym: string) => get(`/verdict/${sym}`),

  agentsList: () => get<{ name: string; description: string; schedule: string; enabled: boolean }[]>('/agents/list'),
  agentRun:   (name: string, dryRun = false) =>
    post<{ agent: string; status: string; summary: string; duration_sec: number; actions: string[]; errors: string[] }>(
      `/agents/run/${name}${dryRun ? '?dry_run=true' : ''}`,
    ),
};
