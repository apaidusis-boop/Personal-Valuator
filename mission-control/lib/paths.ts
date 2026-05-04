import path from "path";

// mission-control/ lives inside investment-intelligence/.
// All data sources are at ../<dir> relative to the Next.js root.
export const II_ROOT = path.resolve(process.cwd(), "..");

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
