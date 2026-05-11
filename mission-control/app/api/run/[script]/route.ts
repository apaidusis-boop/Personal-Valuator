import { NextRequest, NextResponse } from "next/server";
import { spawn } from "node:child_process";
import path from "node:path";
import fs from "node:fs";
import { II_ROOT } from "@/lib/paths";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Whitelist + exact arg recipe per script. NEVER spawn arbitrary input.
const RECIPES: Record<
  string,
  (q: URLSearchParams) => { args: string[]; timeout_ms: number }
> = {
  deepdive: (q) => {
    const ticker = (q.get("ticker") || "").toUpperCase().replace(/[^A-Z0-9.]/g, "");
    if (!ticker) throw new Error("ticker required");
    const args = ["scripts/deepdive.py", ticker];
    if (q.get("no-llm") === "1") args.push("--no-llm");
    if (q.get("save-obsidian") === "1") args.push("--save-obsidian");
    return { args, timeout_ms: q.get("no-llm") === "1" ? 120_000 : 480_000 };
  },
  refresh: (q) => {
    const ticker = (q.get("ticker") || "").toUpperCase().replace(/[^A-Z0-9.]/g, "");
    if (!ticker && q.get("all") !== "1") throw new Error("ticker or all=1 required");
    const args = ticker
      ? ["scripts/refresh_ticker.py", ticker]
      : ["scripts/refresh_ticker.py", "--all-holdings"];
    return { args, timeout_ms: 90_000 };
  },
  brief: () => ({
    args: ["scripts/morning_briefing.py"],
    timeout_ms: 240_000,
  }),
  topics: () => ({
    args: ["-m", "analytics.topic_scorer", "--vault"],
    timeout_ms: 90_000,
  }),
  panorama: (q) => {
    const ticker = (q.get("ticker") || "").toUpperCase().replace(/[^A-Z0-9.]/g, "");
    if (!ticker) throw new Error("ticker required");
    return { args: ["scripts/panorama.py", ticker], timeout_ms: 120_000 };
  },
  verdict: (q) => {
    const ticker = (q.get("ticker") || "").toUpperCase().replace(/[^A-Z0-9.]/g, "");
    if (!ticker) throw new Error("ticker required");
    return { args: ["scripts/verdict.py", ticker], timeout_ms: 60_000 };
  },
  setup: () => ({
    args: ["scripts/localclaw_setup.py"],
    timeout_ms: 30_000,
  }),
};

// Resolve the project's venv Python. We never silently fall back to the bare
// `python` on Windows because PATH usually has the Microsoft Store App
// Execution Alias first, which crashes with 0xC0000142 STATUS_DLL_INIT_FAILED
// when spawned by a long-running Node parent. See chat/route.ts for the same
// pattern.
function pythonExe(): { path: string; from_venv: boolean } {
  const venv = path.join(II_ROOT, ".venv", "Scripts", "python.exe");
  if (fs.existsSync(venv)) return { path: venv, from_venv: true };
  return { path: "python", from_venv: false };
}

export async function POST(
  req: NextRequest,
  { params }: { params: Promise<{ script: string }> }
) {
  const { script } = await params;
  const recipe = RECIPES[script];
  if (!recipe) {
    return NextResponse.json(
      { error: `unknown script "${script}". whitelisted: ${Object.keys(RECIPES).join(", ")}` },
      { status: 404 }
    );
  }

  let resolved;
  try {
    resolved = recipe(req.nextUrl.searchParams);
  } catch (e: unknown) {
    return NextResponse.json(
      { error: e instanceof Error ? e.message : String(e) },
      { status: 400 }
    );
  }

  return new Promise<Response>((resolve) => {
    const py = pythonExe();
    if (!py.from_venv) {
      resolve(
        NextResponse.json(
          {
            error: `venv missing at ${path.join(II_ROOT, ".venv", "Scripts", "python.exe")}. ` +
              `Run: cd ${II_ROOT} && python -m venv .venv && .venv\\Scripts\\pip install -r requirements.txt`,
          },
          { status: 500 }
        )
      );
      return;
    }
    const filteredPath = (process.env.PATH || "")
      .split(path.delimiter)
      .filter((p) => !/WindowsApps/i.test(p))
      .join(path.delimiter);
    const proc = spawn(py.path, ["-X", "utf8", ...resolved.args], {
      cwd: II_ROOT,
      env: {
        ...process.env,
        PATH: filteredPath,
        PYTHONIOENCODING: "utf-8",
        PYTHONUTF8: "1",
      },
    });
    let stdout = "";
    let stderr = "";
    const timer = setTimeout(() => {
      proc.kill();
      resolve(
        NextResponse.json(
          {
            error: `timeout (${resolved.timeout_ms}ms)`,
            stdout: stdout.slice(-3000),
            stderr: stderr.slice(-1000),
          },
          { status: 504 }
        )
      );
    }, resolved.timeout_ms);
    proc.stdout.on("data", (d) => (stdout += d.toString()));
    proc.stderr.on("data", (d) => (stderr += d.toString()));
    proc.on("close", (code) => {
      clearTimeout(timer);
      resolve(
        NextResponse.json(
          {
            ok: code === 0,
            exit_code: code,
            stdout: stdout.slice(-6000),
            stderr: stderr.slice(-1500),
            script,
            args: resolved.args,
          },
          { status: code === 0 ? 200 : 500 }
        )
      );
    });
    proc.on("error", (e) => {
      clearTimeout(timer);
      resolve(NextResponse.json({ error: e.message }, { status: 500 }));
    });
  });
}
