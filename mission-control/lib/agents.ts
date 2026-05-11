import fs from "fs";
import path from "path";
import { AGENTS_STATE_DIR, AGENTS_YAML } from "./paths";

export type AgentPersona = {
  name: string;
  employee_name: string;
  title: string;
  bio: string;
  department: string;
  reports_to: string;
  schedule: string;
  enabled: boolean;
};

// Tiny YAML parser for our flat agents.yaml — avoids adding a dep.
// Supports the structure we use: top-level `agents:` list with simple key:value pairs.
export function loadPersonas(): AgentPersona[] {
  let raw: string;
  try {
    raw = fs.readFileSync(AGENTS_YAML, "utf-8");
  } catch {
    return [];
  }
  const out: AgentPersona[] = [];
  let cur: Partial<AgentPersona> | null = null;
  let inMultiline = false;
  let multilineKey = "";
  let multilineValue = "";

  for (const rawLine of raw.split("\n")) {
    const line = rawLine.replace(/\r$/, "");
    if (line.match(/^\s*#/) || line.match(/^\s*$/)) continue;
    if (line.match(/^agents\s*:/)) continue;

    // List item start: "  - name: foo"
    const itemMatch = line.match(/^\s+-\s+name:\s*(.+)$/);
    if (itemMatch) {
      if (cur) out.push(finalize(cur));
      cur = { name: itemMatch[1].trim().replace(/^["']|["']$/g, "") };
      inMultiline = false;
      continue;
    }

    if (!cur) continue;

    // Detect indentation continuation of multiline string (gets folded).
    if (inMultiline) {
      const m = line.match(/^\s{4,}(.+)$/);
      if (m && !line.match(/^\s+\w[\w_]*:/)) {
        multilineValue += " " + m[1].trim();
        continue;
      }
      // Falls through — multiline ended.
      (cur as any)[multilineKey] = multilineValue.trim();
      inMultiline = false;
    }

    const kv = line.match(/^\s+([a-z_]+)\s*:\s*(.*)$/);
    if (!kv) continue;
    const [, key, valueRaw] = kv;
    const value = valueRaw.trim();

    if (value === "") {
      // Multiline scalar following — start collecting until indentation changes.
      inMultiline = true;
      multilineKey = key;
      multilineValue = "";
      continue;
    }

    // Strip quotes
    let cleaned = value.replace(/^["']|["']$/g, "");
    if (cleaned === "true") (cur as any)[key] = true;
    else if (cleaned === "false") (cur as any)[key] = false;
    else (cur as any)[key] = cleaned;
  }
  if (cur) {
    if (inMultiline) (cur as any)[multilineKey] = multilineValue.trim();
    out.push(finalize(cur));
  }
  return out.filter((a) => a.name);
}

function finalize(p: Partial<AgentPersona>): AgentPersona {
  return {
    name: p.name || "",
    employee_name: p.employee_name || p.name || "",
    title: p.title || "Agent",
    bio: (p.bio || "").trim(),
    department: p.department || "Operations",
    reports_to: p.reports_to || "founder",
    schedule: p.schedule || "manual",
    enabled: p.enabled !== false,
  };
}

export type AgentStatus = {
  name: string;
  last_status: string | null;
  last_run: string | null;
  consecutive_failures: number;
  run_count: number;
  failed_count: number;
  last_summary: string | null;
};

export function loadAgentStatus(): Record<string, AgentStatus> {
  const out: Record<string, AgentStatus> = {};
  try {
    const files = fs.readdirSync(AGENTS_STATE_DIR);
    for (const f of files) {
      if (!f.endsWith(".json") || f.startsWith("_")) continue;
      const name = f.replace(/\.json$/, "");
      try {
        const data = JSON.parse(fs.readFileSync(path.join(AGENTS_STATE_DIR, f), "utf-8"));
        out[name] = {
          name,
          last_status: data.last_status ?? null,
          last_run: data.last_run ?? null,
          consecutive_failures: data.consecutive_failures || 0,
          run_count: data.run_count || 0,
          failed_count: data.failed_count || 0,
          last_summary: data.last_summary ?? null,
        };
      } catch {
        /* skip malformed */
      }
    }
  } catch {
    /* dir missing */
  }
  return out;
}

export type Department = {
  name: string;
  members: (AgentPersona & { status?: AgentStatus })[];
};

export function listDepartments(): Department[] {
  const personas = loadPersonas();
  const status = loadAgentStatus();
  const map = new Map<string, Department>();
  for (const p of personas) {
    const d = map.get(p.department) || { name: p.department, members: [] };
    d.members.push({ ...p, status: status[p.name] });
    map.set(p.department, d);
  }
  return [...map.values()].sort((a, b) => a.name.localeCompare(b.name));
}
