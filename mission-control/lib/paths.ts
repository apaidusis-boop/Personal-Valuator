import path from "path";
import fs from "fs";

// mission-control/ lives inside investment-intelligence/.
// We anchor II_ROOT relative to *this file* (which is in mission-control/lib/)
// rather than process.cwd() — because Next.js dev servers, Tauri shells,
// scheduled tasks, etc. can launch with arbitrary cwds, and a wrong II_ROOT
// causes the venv-detection in spawn callers to silently fall back to the
// system `python`. On this machine that resolves to the Microsoft Store stub
// (App Execution Alias) which fails with 0xC0000142 STATUS_DLL_INIT_FAILED
// when spawned by a long-running Node process. Anchoring on __dirname makes
// the path deterministic regardless of how the server was started.
const _hereDirname = (() => {
  // Next dev compiles this to CommonJS where __dirname is available.
  // In ESM contexts we'd need fileURLToPath(import.meta.url); the existing
  // build is CJS so __dirname works.
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const d = (typeof __dirname !== "undefined" ? __dirname : "") as string;
  return d || path.resolve(process.cwd(), "lib");
})();

// Walk up until we find a directory that contains both `mission-control/`
// and `.venv/`. That's the investment-intelligence root.
function _findIIRoot(startDir: string): string {
  let cur = startDir;
  for (let i = 0; i < 8; i++) {
    const hasMC = fs.existsSync(path.join(cur, "mission-control"));
    const hasVenv = fs.existsSync(path.join(cur, ".venv", "Scripts", "python.exe"));
    if (hasMC && hasVenv) return cur;
    const parent = path.dirname(cur);
    if (parent === cur) break;
    cur = parent;
  }
  // Last resort: cwd-based heuristic (legacy behaviour).
  return path.resolve(process.cwd(), "..");
}

export const II_ROOT = _findIIRoot(_hereDirname);

export const DB_BR = path.join(II_ROOT, "data", "br_investments.db");
export const DB_US = path.join(II_ROOT, "data", "us_investments.db");
export const DB_CHIEF = path.join(II_ROOT, "data", "chief_memory.db");
export const AGENTS_STATE_DIR = path.join(II_ROOT, "data", "agents");
export const AGENTS_YAML = path.join(II_ROOT, "config", "agents.yaml");
export const VAULT_DIR = path.join(II_ROOT, "obsidian_vault");
export const REPORTS_DIR = path.join(II_ROOT, "reports");
export const CONSTITUTION = path.join(VAULT_DIR, "CONSTITUTION.md");
export const BIBLIOTHECA_DIR = path.join(VAULT_DIR, "Bibliotheca");
export const DASHBOARDS_DIR = path.join(VAULT_DIR, "dashboards");
export const DOSSIERS_DIR = path.join(VAULT_DIR, "dossiers");

// Claude Code auto-memory directory (outside the project)
export const AUTO_MEMORY_DIR = path.join(
  process.env.USERPROFILE || process.env.HOME || "",
  ".claude",
  "projects",
  "C--Users-paidu-investment-intelligence",
  "memory"
);
