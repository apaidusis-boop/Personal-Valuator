import fs from "fs";
import path from "path";
import matter from "gray-matter";
import {
  CONSTITUTION,
  BIBLIOTHECA_DIR,
  DASHBOARDS_DIR,
  DOSSIERS_DIR,
  REPORTS_DIR,
  VAULT_DIR,
  AUTO_MEMORY_DIR,
} from "./paths";

export type VaultDoc = {
  path: string;
  relpath: string;
  title: string;
  modified: number;
  size: number;
  preview: string;
  data: Record<string, unknown>;
};

function safeRead(p: string): string | null {
  try {
    // Normalize CRLF/CR → LF so SSR text matches client hydration on Windows.
    return fs.readFileSync(p, "utf-8").replace(/\r\n?/g, "\n");
  } catch {
    return null;
  }
}

export function readMarkdown(p: string): VaultDoc | null {
  const raw = safeRead(p);
  if (raw == null) return null;
  let parsed;
  try {
    parsed = matter(raw);
  } catch {
    parsed = { content: raw, data: {} };
  }
  const stat = fs.statSync(p);
  const lines = parsed.content.split("\n").filter(Boolean);
  const title = lines[0]?.replace(/^#+\s*/, "") || path.basename(p, ".md");
  return {
    path: p,
    relpath: path.relative(VAULT_DIR, p).replace(/\\/g, "/"),
    title,
    modified: stat.mtimeMs,
    size: stat.size,
    preview: parsed.content.slice(0, 600),
    data: parsed.data,
  };
}

export function listMarkdownIn(dir: string, recursive = false, limit = 200): VaultDoc[] {
  const out: VaultDoc[] = [];
  function walk(d: string) {
    let entries: fs.Dirent[];
    try {
      entries = fs.readdirSync(d, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of entries) {
      const full = path.join(d, e.name);
      if (e.isDirectory() && recursive) walk(full);
      else if (e.isFile() && e.name.endsWith(".md")) {
        const doc = readMarkdown(full);
        if (doc) out.push(doc);
        if (out.length >= limit) return;
      }
    }
  }
  walk(dir);
  return out.sort((a, b) => b.modified - a.modified);
}

export function readConstitution(): string | null {
  return safeRead(CONSTITUTION);
}

/** Extract Phase entries from the constitution / changelog. */
export function listPhases(): { id: string; title: string; status: string; date: string }[] {
  const text = readConstitution() || "";
  // Look for lines like "## Phase EE — LocalClaw (2026-04-29) — IN PROGRESS"
  const re = /^##\s+(Phase\s+[A-Z]+\.?\d*[^\n]*)/gm;
  const out: { id: string; title: string; status: string; date: string }[] = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(text)) !== null) {
    const line = m[1];
    const idMatch = line.match(/Phase\s+([A-Z]+(?:\.\d+)?)/);
    const dateMatch = line.match(/(\d{4}-\d{2}-\d{2})/);
    const statusMatch = line.match(/(SHIPPED|IN PROGRESS|PLANNED|DEFERRED|DONE|COMPLETE|PROPOSED)/i);
    out.push({
      id: idMatch ? idMatch[1] : line,
      title: line.replace(/—.*$/, "").trim(),
      status: statusMatch ? statusMatch[1].toUpperCase() : "UNKNOWN",
      date: dateMatch ? dateMatch[1] : "",
    });
  }
  return out;
}

export function listResearchDigests(limit = 20): VaultDoc[] {
  const dir = path.join(BIBLIOTHECA_DIR);
  if (!fs.existsSync(dir)) return [];
  return listMarkdownIn(dir, false, limit).filter((d) =>
    d.relpath.includes("Research_Digest")
  );
}

export function listKnowledgeCards(limit = 30): VaultDoc[] {
  const dir = path.join(BIBLIOTHECA_DIR, "Knowledge");
  if (!fs.existsSync(dir)) return [];
  return listMarkdownIn(dir, false, limit);
}

export function listDossiers(limit = 50): VaultDoc[] {
  if (!fs.existsSync(DOSSIERS_DIR)) return [];
  return listMarkdownIn(DOSSIERS_DIR, false, limit);
}

// ---------------------------------------------------------------------------
// Council outputs (Night Shift / STORYT_3.0)
// ---------------------------------------------------------------------------

export type CouncilStance = "BUY" | "HOLD" | "AVOID" | "NEEDS_DATA" | "UNKNOWN";

export type CouncilSynthesis = {
  consensus_points: string[];
  dissent_points: string[];
  final_stance: CouncilStance;
  confidence: string;
  pre_publication_flags: string[];
  sizing_recommendation: string | null;
};

export type CouncilEntry = {
  ticker: string;
  market: "br" | "us" | string;
  modo: string | null;
  sector: string | null;
  is_holding: boolean;
  date: string;                  // YYYY-MM-DD from STORY frontmatter or json
  stance: CouncilStance;
  confidence: string;
  philosophy_primary: string | null;
  philosophy_secondary: string | null;
  margin_of_safety: number | null;
  elapsed_sec: number | null;
  dissent_count: number;
  flag_count: number;
  story_path: string;
  council_path: string | null;
  council_md_path: string | null;
  synthesis: CouncilSynthesis | null;
  seats: string[];
};

function readJSON<T = unknown>(p: string): T | null {
  try {
    return JSON.parse(fs.readFileSync(p, "utf-8")) as T;
  } catch {
    return null;
  }
}

function extractSeats(raw: unknown): string[] {
  if (!Array.isArray(raw)) return [];
  return raw
    .map((s) => {
      if (typeof s === "string") return s;
      if (s && typeof s === "object") {
        const o = s as Record<string, unknown>;
        return String(o.employee_name || o.name || o.title || o.agent_slug || "");
      }
      return "";
    })
    .filter(Boolean);
}

function normaliseStance(s: unknown): CouncilStance {
  const v = String(s || "").toUpperCase().trim();
  if (v === "BUY" || v === "HOLD" || v === "AVOID" || v === "NEEDS_DATA") return v;
  return "UNKNOWN";
}

/**
 * Pair STORY.md + COUNCIL.json under DOSSIERS_DIR for the latest run of each ticker.
 * Returns the most-recently-modified STORY.md per ticker (live file, not archive).
 */
export function listCouncilOutputs(limit = 200): CouncilEntry[] {
  if (!fs.existsSync(DOSSIERS_DIR)) return [];
  let files: string[];
  try {
    files = fs.readdirSync(DOSSIERS_DIR);
  } catch {
    return [];
  }
  const out: CouncilEntry[] = [];
  for (const f of files) {
    const m = f.match(/^(.+)_STORY\.md$/);
    if (!m) continue;
    const ticker = m[1];
    const storyPath = path.join(DOSSIERS_DIR, f);
    const story = readMarkdown(storyPath);
    if (!story) continue;
    const fm = story.data as Record<string, unknown>;

    const councilJsonPath = path.join(DOSSIERS_DIR, `${ticker}_COUNCIL.json`);
    const councilMdPath = path.join(DOSSIERS_DIR, `${ticker}_COUNCIL.md`);
    const councilJson = fs.existsSync(councilJsonPath)
      ? readJSON<Record<string, unknown>>(councilJsonPath)
      : null;
    const synthesis: CouncilSynthesis | null = councilJson
      ? {
          consensus_points: ((councilJson.synthesis as Record<string, unknown>)?.consensus_points as string[]) || [],
          dissent_points: ((councilJson.synthesis as Record<string, unknown>)?.dissent_points as string[]) || [],
          final_stance: normaliseStance((councilJson.synthesis as Record<string, unknown>)?.final_stance),
          confidence: String((councilJson.synthesis as Record<string, unknown>)?.confidence || "—"),
          pre_publication_flags: ((councilJson.synthesis as Record<string, unknown>)?.pre_publication_flags as string[]) || [],
          sizing_recommendation: ((councilJson.synthesis as Record<string, unknown>)?.sizing_recommendation as string) || null,
        }
      : null;

    const stance = synthesis?.final_stance ?? normaliseStance(fm.council_stance);
    const confidence = synthesis?.confidence ?? String(fm.council_confidence || "—");

    out.push({
      ticker,
      market: String(fm.market || councilJson?.market || ""),
      modo: fm.modo ? String(fm.modo) : null,
      sector: (councilJson?.sector as string) ?? null,
      is_holding: Boolean(councilJson?.is_holding ?? false),
      date: String(fm.date || councilJson?.date || ""),
      stance,
      confidence,
      philosophy_primary: fm.philosophy_primary ? String(fm.philosophy_primary) : null,
      philosophy_secondary: fm.philosophy_secondary ? String(fm.philosophy_secondary) : null,
      margin_of_safety:
        typeof fm.margin_of_safety === "number" ? (fm.margin_of_safety as number) : null,
      elapsed_sec:
        typeof fm.narrative_elapsed_sec === "number"
          ? (fm.narrative_elapsed_sec as number)
          : typeof councilJson?.elapsed_sec === "number"
            ? (councilJson.elapsed_sec as number)
            : null,
      dissent_count: synthesis?.dissent_points.length ?? 0,
      flag_count: synthesis?.pre_publication_flags.length ?? 0,
      story_path: storyPath,
      council_path: fs.existsSync(councilJsonPath) ? councilJsonPath : null,
      council_md_path: fs.existsSync(councilMdPath) ? councilMdPath : null,
      synthesis,
      seats: extractSeats(councilJson?.seats),
    });
    if (out.length >= limit) break;
  }
  // newest first by date string then ticker
  return out.sort((a, b) => (b.date.localeCompare(a.date) || a.ticker.localeCompare(b.ticker)));
}

export type CouncilStoryFull = {
  entry: CouncilEntry;
  body: string;          // markdown body (frontmatter stripped)
  council_md: string | null;
};

export function readCouncilStory(ticker: string): CouncilStoryFull | null {
  const tk = ticker.toUpperCase();
  const storyPath = path.join(DOSSIERS_DIR, `${tk}_STORY.md`);
  if (!fs.existsSync(storyPath)) return null;
  const raw = safeRead(storyPath);
  if (raw == null) return null;
  let parsed;
  try {
    parsed = matter(raw);
  } catch {
    parsed = { content: raw, data: {} };
  }
  // Find the entry by re-using listCouncilOutputs (cheap; one disk read per file).
  // For a focused viewer we instead build the entry inline to avoid scanning all dossiers.
  const councilJsonPath = path.join(DOSSIERS_DIR, `${tk}_COUNCIL.json`);
  const councilMdPath = path.join(DOSSIERS_DIR, `${tk}_COUNCIL.md`);
  const councilJson = fs.existsSync(councilJsonPath)
    ? readJSON<Record<string, unknown>>(councilJsonPath)
    : null;
  const synthesis: CouncilSynthesis | null = councilJson
    ? {
        consensus_points: ((councilJson.synthesis as Record<string, unknown>)?.consensus_points as string[]) || [],
        dissent_points: ((councilJson.synthesis as Record<string, unknown>)?.dissent_points as string[]) || [],
        final_stance: normaliseStance((councilJson.synthesis as Record<string, unknown>)?.final_stance),
        confidence: String((councilJson.synthesis as Record<string, unknown>)?.confidence || "—"),
        pre_publication_flags: ((councilJson.synthesis as Record<string, unknown>)?.pre_publication_flags as string[]) || [],
        sizing_recommendation: ((councilJson.synthesis as Record<string, unknown>)?.sizing_recommendation as string) || null,
      }
    : null;
  const fm = parsed.data as Record<string, unknown>;
  const entry: CouncilEntry = {
    ticker: tk,
    market: String(fm.market || councilJson?.market || ""),
    modo: fm.modo ? String(fm.modo) : null,
    sector: (councilJson?.sector as string) ?? null,
    is_holding: Boolean(councilJson?.is_holding ?? false),
    date: String(fm.date || councilJson?.date || ""),
    stance: synthesis?.final_stance ?? normaliseStance(fm.council_stance),
    confidence: synthesis?.confidence ?? String(fm.council_confidence || "—"),
    philosophy_primary: fm.philosophy_primary ? String(fm.philosophy_primary) : null,
    philosophy_secondary: fm.philosophy_secondary ? String(fm.philosophy_secondary) : null,
    margin_of_safety:
      typeof fm.margin_of_safety === "number" ? (fm.margin_of_safety as number) : null,
    elapsed_sec:
      typeof fm.narrative_elapsed_sec === "number"
        ? (fm.narrative_elapsed_sec as number)
        : typeof councilJson?.elapsed_sec === "number"
          ? (councilJson.elapsed_sec as number)
          : null,
    dissent_count: synthesis?.dissent_points.length ?? 0,
    flag_count: synthesis?.pre_publication_flags.length ?? 0,
    story_path: storyPath,
    council_path: fs.existsSync(councilJsonPath) ? councilJsonPath : null,
    council_md_path: fs.existsSync(councilMdPath) ? councilMdPath : null,
    synthesis,
    seats: extractSeats(councilJson?.seats),
  };
  const councilMdBody = fs.existsSync(councilMdPath) ? safeRead(councilMdPath) : null;
  return { entry, body: parsed.content, council_md: councilMdBody };
}

/** Group council outputs by date and stance — used for the index header. */
export function summariseCouncil(entries: CouncilEntry[]): {
  date: string;
  total: number;
  buy: number;
  hold: number;
  avoid: number;
  needs_data: number;
} {
  if (entries.length === 0) {
    return { date: "—", total: 0, buy: 0, hold: 0, avoid: 0, needs_data: 0 };
  }
  // Latest date present in any entry — use that as the headline.
  const latestDate = entries.reduce((m, e) => (e.date > m ? e.date : m), entries[0].date);
  const latest = entries.filter((e) => e.date === latestDate);
  return {
    date: latestDate,
    total: latest.length,
    buy: latest.filter((e) => e.stance === "BUY").length,
    hold: latest.filter((e) => e.stance === "HOLD").length,
    avoid: latest.filter((e) => e.stance === "AVOID").length,
    needs_data: latest.filter((e) => e.stance === "NEEDS_DATA").length,
  };
}

export function listDailyMemory(limit = 30): { date: string; path: string; words: number }[] {
  // Scans for daily memory files in vault — pattern <YYYY-MM-DD>.md or similar
  const candidates = [
    path.join(VAULT_DIR, "Daily"),
    path.join(VAULT_DIR, "daily"),
    path.join(VAULT_DIR, "memory"),
  ];
  const out: { date: string; path: string; words: number }[] = [];
  for (const dir of candidates) {
    if (!fs.existsSync(dir)) continue;
    let entries: string[];
    try {
      entries = fs.readdirSync(dir);
    } catch {
      continue;
    }
    for (const f of entries) {
      const m = f.match(/^(\d{4}-\d{2}-\d{2})\.md$/);
      if (!m) continue;
      const full = path.join(dir, f);
      try {
        const text = fs.readFileSync(full, "utf-8");
        out.push({ date: m[1], path: full, words: text.split(/\s+/).length });
      } catch {
        /* skip */
      }
    }
  }
  return out.sort((a, b) => b.date.localeCompare(a.date)).slice(0, limit);
}

export function readBriefing(): string | null {
  const p = path.join(DASHBOARDS_DIR, "Briefing.md");
  return safeRead(p);
}

export function readBriefingMeta(): { content: string | null; mtime: string | null } {
  const p = path.join(DASHBOARDS_DIR, "Briefing.md");
  const content = safeRead(p);
  let mtime: string | null = null;
  try {
    const st = fs.statSync(p);
    mtime = st.mtime.toISOString();
  } catch {
    /* missing */
  }
  return { content, mtime };
}

export type Topic = {
  id: string;
  name: string;
  summary: string;
  tags: string[];
  tickers: string[];
  score: number;
  tier: "make_now" | "rising" | "watch" | "background";
  weeks_tracked: number;
  mentions_recent: number;
  holdings_hit: string[];
  open_triggers: number;
  last_mention_iso: string | null;
  components: {
    freshness: number;
    frequency: number;
    breadth: number;
    trigger: number;
  };
};

export function readTopicScores(): { computed_at: string; topics: Topic[] } | null {
  const p = path.join(VAULT_DIR, "..", "data", "topic_scores.json");
  try {
    const raw = fs.readFileSync(p, "utf-8");
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export type AutoMemoryEntry = {
  name: string;
  path: string;
  type: string;        // user / feedback / project / reference
  description: string;
  modified: number;
  words: number;
  preview: string;
  body: string;
};

export function listAutoMemory(limit = 100): AutoMemoryEntry[] {
  if (!fs.existsSync(AUTO_MEMORY_DIR)) return [];
  let files: string[];
  try {
    files = fs.readdirSync(AUTO_MEMORY_DIR);
  } catch {
    return [];
  }
  const out: AutoMemoryEntry[] = [];
  for (const f of files) {
    if (!f.endsWith(".md")) continue;
    if (f === "MEMORY.md") continue; // index file, separate
    const full = path.join(AUTO_MEMORY_DIR, f);
    try {
      const raw = fs.readFileSync(full, "utf-8");
      const parsed = matter(raw);
      const stat = fs.statSync(full);
      const data = parsed.data || {};
      out.push({
        name: f.replace(/\.md$/, ""),
        path: full,
        type: String((data as Record<string, unknown>).type || "note"),
        description: String((data as Record<string, unknown>).description || ""),
        modified: stat.mtimeMs,
        words: parsed.content.split(/\s+/).filter(Boolean).length,
        preview: parsed.content.slice(0, 300).trim(),
        body: parsed.content,
      });
      if (out.length >= limit) break;
    } catch {
      /* skip */
    }
  }
  return out.sort((a, b) => b.modified - a.modified);
}

export function readAutoMemoryIndex(): string {
  const p = path.join(AUTO_MEMORY_DIR, "MEMORY.md");
  return safeRead(p) || "";
}

export type DailyEntry = {
  date: string;          // YYYY-MM-DD
  path: string;
  source: string;        // origin label (digest / phase / vault-daily)
  title: string;
  words: number;
  preview: string;
  body: string;
};

export function listDailyEntries(limit = 60): DailyEntry[] {
  const out: DailyEntry[] = [];

  // Source 1: Bibliotheca/Research_Digest_<DATE>.md
  if (fs.existsSync(BIBLIOTHECA_DIR)) {
    let files: string[];
    try {
      files = fs.readdirSync(BIBLIOTHECA_DIR);
    } catch {
      files = [];
    }
    for (const f of files) {
      const m = f.match(/^Research_Digest_(\d{4}-\d{2}-\d{2})\.md$/);
      if (!m) continue;
      const full = path.join(BIBLIOTHECA_DIR, f);
      try {
        const raw = fs.readFileSync(full, "utf-8");
        const parsed = matter(raw);
        out.push({
          date: m[1],
          path: full,
          source: "research_digest",
          title: `Research Digest ${m[1]}`,
          words: parsed.content.split(/\s+/).filter(Boolean).length,
          preview: parsed.content.slice(0, 400),
          body: parsed.content,
        });
      } catch {
        /* skip */
      }
    }
  }

  // Source 2: vault/Daily/<YYYY-MM-DD>.md if exists
  for (const dir of [path.join(VAULT_DIR, "Daily"), path.join(VAULT_DIR, "daily")]) {
    if (!fs.existsSync(dir)) continue;
    let files: string[] = [];
    try { files = fs.readdirSync(dir); } catch {}
    for (const f of files) {
      const m = f.match(/^(\d{4}-\d{2}-\d{2})\.md$/);
      if (!m) continue;
      const full = path.join(dir, f);
      try {
        const raw = fs.readFileSync(full, "utf-8");
        const parsed = matter(raw);
        out.push({
          date: m[1],
          path: full,
          source: "vault_daily",
          title: `Daily ${m[1]}`,
          words: parsed.content.split(/\s+/).filter(Boolean).length,
          preview: parsed.content.slice(0, 400),
          body: parsed.content,
        });
      } catch {}
    }
  }

  return out.sort((a, b) => b.date.localeCompare(a.date)).slice(0, limit);
}

export function listDeepdiveJSON(limit = 30): { ticker: string; ts: string; path: string }[] {
  const dir = path.join(REPORTS_DIR, "deepdive");
  if (!fs.existsSync(dir)) return [];
  let files: string[];
  try {
    files = fs.readdirSync(dir);
  } catch {
    return [];
  }
  const out: { ticker: string; ts: string; path: string }[] = [];
  for (const f of files) {
    const m = f.match(/^(.+)_deepdive_(\d{8}_\d{4})\.json$/);
    if (!m) continue;
    out.push({ ticker: m[1], ts: m[2], path: path.join(dir, f) });
  }
  return out.sort((a, b) => b.ts.localeCompare(a.ts)).slice(0, limit);
}

// ============================================================
// Allocation proposals (overnight backfill output)
// ============================================================
export type AllocationData = {
  market: "br" | "us";
  date: string;
  target_weights: Record<string, number>;
  bucket_weights: Record<string, number>;
  conflicts: Array<{ ticker: string; verdicts: Record<string, string>; resolution?: string }>;
  macro_overlay: any;
  hedge_overlay: any;
  notes: string[];
  per_engine: Record<string, any[]>;
};

export function loadLatestAllocation(market: "br" | "us"): AllocationData | null {
  if (!fs.existsSync(BIBLIOTHECA_DIR)) return null;
  let files: string[];
  try {
    files = fs.readdirSync(BIBLIOTHECA_DIR);
  } catch {
    return null;
  }
  const prefix = `Allocation_${market.toUpperCase()}_`;
  const matches = files
    .filter((f) => f.startsWith(prefix) && f.endsWith(".json"))
    .sort()
    .reverse();
  if (!matches.length) return null;
  const file = path.join(BIBLIOTHECA_DIR, matches[0]);
  let raw: string;
  try {
    raw = fs.readFileSync(file, "utf-8");
  } catch {
    return null;
  }
  let data: any;
  try {
    data = JSON.parse(raw);
  } catch {
    return null;
  }
  const dm = matches[0].match(/_(\d{4}-\d{2}-\d{2})\.json$/);
  return {
    market,
    date: dm ? dm[1] : "",
    target_weights: data.target_weights || {},
    bucket_weights: data.bucket_weights || {},
    conflicts: data.conflicts || [],
    macro_overlay: data.macro_overlay || {},
    hedge_overlay: data.hedge_overlay || {},
    notes: data.notes || [],
    per_engine: data.per_engine || {},
  };
}
