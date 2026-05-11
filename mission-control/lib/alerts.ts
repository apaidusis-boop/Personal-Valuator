// Lightweight alerts store backed by data/alerts.json (no DB schema change).
// Keeps the feature reversible — if user wants to migrate to SQLite later,
// it's a clean port of the same shape.

import fs from "node:fs";
import path from "node:path";
import { II_ROOT } from "./paths";

export type AlertKind = "price" | "fair_value_entry" | "manual";
export type AlertDirection = "above" | "below";
export type AlertStatus = "active" | "triggered" | "dismissed";

export type Alert = {
  id: string;
  ticker: string;
  market: "br" | "us";
  kind: AlertKind;
  direction: AlertDirection;
  threshold: number;
  current_price: number | null;
  source: string;       // "manual" | "fair_value:graham_number" | "fair_value:buffett_ceiling"
  note: string | null;
  status: AlertStatus;
  created_at: string;   // ISO
  updated_at: string;   // ISO
};

const ALERTS_FILE = path.join(II_ROOT, "data", "alerts.json");

function readAll(): Alert[] {
  try {
    if (!fs.existsSync(ALERTS_FILE)) return [];
    const raw = fs.readFileSync(ALERTS_FILE, "utf-8");
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed as Alert[];
  } catch {
    return [];
  }
}

function writeAll(alerts: Alert[]) {
  fs.mkdirSync(path.dirname(ALERTS_FILE), { recursive: true });
  fs.writeFileSync(ALERTS_FILE, JSON.stringify(alerts, null, 2), "utf-8");
}

export function listAlerts(status?: AlertStatus): Alert[] {
  const all = readAll();
  if (!status) return all.sort((a, b) => b.created_at.localeCompare(a.created_at));
  return all
    .filter((a) => a.status === status)
    .sort((a, b) => b.created_at.localeCompare(a.created_at));
}

export function createAlert(input: {
  ticker: string;
  market: "br" | "us";
  kind: AlertKind;
  direction: AlertDirection;
  threshold: number;
  current_price?: number | null;
  source?: string;
  note?: string | null;
}): Alert {
  const all = readAll();
  const now = new Date().toISOString();
  const id = `${input.ticker}-${input.kind}-${input.direction}-${Date.now()}`;
  const alert: Alert = {
    id,
    ticker: input.ticker.toUpperCase(),
    market: input.market,
    kind: input.kind,
    direction: input.direction,
    threshold: input.threshold,
    current_price: input.current_price ?? null,
    source: input.source || "manual",
    note: input.note ?? null,
    status: "active",
    created_at: now,
    updated_at: now,
  };
  all.push(alert);
  writeAll(all);
  return alert;
}

export function updateAlertStatus(id: string, status: AlertStatus): Alert | null {
  const all = readAll();
  const idx = all.findIndex((a) => a.id === id);
  if (idx < 0) return null;
  all[idx].status = status;
  all[idx].updated_at = new Date().toISOString();
  writeAll(all);
  return all[idx];
}

export function deleteAlert(id: string): boolean {
  const all = readAll();
  const filtered = all.filter((a) => a.id !== id);
  if (filtered.length === all.length) return false;
  writeAll(filtered);
  return true;
}
