import { NextRequest, NextResponse } from "next/server";
import { spawn } from "node:child_process";
import path from "node:path";
import fs from "node:fs";
import { II_ROOT } from "@/lib/paths";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Resolve the Python that runs Fiel Escudeiro. We use `.venv311` (Python 3.11
// non-Store) instead of `.venv` because the latter is based on the Microsoft
// Store Python — spawning that from the long-running Node dev server fails
// with STATUS_DLL_INIT_FAILED (0xC0000142) due to AppContainer redirector.
function pythonExe(): { path: string; ok: boolean } {
  const venv311 = path.join(II_ROOT, ".venv311", "Scripts", "python.exe");
  if (fs.existsSync(venv311)) return { path: venv311, ok: true };
  // Fallback: try plain `.venv` (likely to fail with 0xC0000142, but at least
  // surfaces a discoverable error rather than silently breaking).
  const venv = path.join(II_ROOT, ".venv", "Scripts", "python.exe");
  if (fs.existsSync(venv)) return { path: venv, ok: true };
  return { path: "", ok: false };
}

export async function POST(req: NextRequest) {
  let body: { message?: string; chat_id?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "invalid json" }, { status: 400 });
  }
  const message = (body.message || "").trim();
  const chat_id = (body.chat_id || "mission-control").trim();
  if (!message) return NextResponse.json({ error: "empty message" }, { status: 400 });

  return new Promise<Response>((resolve) => {
    const py = pythonExe();
    if (!py.ok) {
      resolve(
        NextResponse.json(
          {
            error: `Fiel Escudeiro venv não encontrada. Esperava: ${path.join(II_ROOT, ".venv311", "Scripts", "python.exe")}. ` +
              `Cria com: py -3.11 -m venv .venv311`,
          },
          { status: 500 }
        )
      );
      return;
    }

    // Keep PATH minimal-but-functional. System32 must be there for DLL loads;
    // WindowsApps stripped to avoid Store Python aliases hijacking subprocess
    // calls inside the Python process.
    const systemRoot = process.env.SystemRoot || "C:\\Windows";
    const baseSystemPaths = [
      path.join(systemRoot, "System32"),
      systemRoot,
      path.join(systemRoot, "System32", "Wbem"),
    ];
    const filteredPath = (process.env.PATH || "")
      .split(path.delimiter)
      .filter((p) => p && !/WindowsApps/i.test(p))
      .join(path.delimiter);
    const safePath = [...baseSystemPaths, filteredPath].join(path.delimiter);

    // Drop Python-pointing env vars from another venv (corrupts DLL search).
    const cleanEnv: Record<string, string> = {};
    for (const [k, v] of Object.entries(process.env)) {
      if (v === undefined) continue;
      if (k === "PYTHONHOME" || k === "PYTHONPATH" || k === "VIRTUAL_ENV") continue;
      cleanEnv[k] = v;
    }

    const proc = spawn(
      py.path,
      [
        "-X", "utf8",
        "-m", "agents.fiel_escudeiro",
        "--chat-id", chat_id,
        message,
      ],
      {
        cwd: II_ROOT,
        env: {
          ...cleanEnv,
          PATH: safePath,
          PYTHONIOENCODING: "utf-8",
          PYTHONUTF8: "1",
          // Authorized by user (see chat 2026-05-06): Fiel Escudeiro runs Claude CLI
          // with bypassPermissions so it can execute `ii <command>`, query SQLite,
          // run tests. System prompt asks for confirmation on destructive ops.
          FIEL_ESCUDEIRO_PERMISSION_MODE:
            process.env.FIEL_ESCUDEIRO_PERMISSION_MODE || "bypassPermissions",
          FIEL_ESCUDEIRO_MAX_BUDGET_USD:
            process.env.FIEL_ESCUDEIRO_MAX_BUDGET_USD || "3.00",
        } as unknown as NodeJS.ProcessEnv,
      }
    );

    let stdout = "";
    let stderr = "";
    // Claude can take a while on multi-step tool use. 10 min cap matches the
    // Python-side subprocess timeout in agents/fiel_escudeiro.py.
    const TIMEOUT_MS = 600_000;
    const timer = setTimeout(() => {
      proc.kill();
      resolve(
        NextResponse.json(
          { error: "timeout (10 min)", stderr: stderr.slice(-1000) },
          { status: 504 }
        )
      );
    }, TIMEOUT_MS);

    proc.stdout.on("data", (d) => (stdout += d.toString()));
    proc.stderr.on("data", (d) => (stderr += d.toString()));
    proc.on("close", (code) => {
      clearTimeout(timer);
      // CLI prints "[fiel-escudeiro] <prompt>" then a blank line then the answer.
      const lines = stdout.split("\n");
      const headerIdx = lines.findIndex((l) => l.startsWith("[fiel-escudeiro]"));
      const answer =
        headerIdx >= 0
          ? lines.slice(headerIdx + 1).join("\n").trim()
          : stdout.trim();
      if (code === 0 && answer) {
        resolve(NextResponse.json({ reply: answer, chat_id }));
      } else {
        resolve(
          NextResponse.json(
            {
              error: `escudeiro exited ${code}`,
              stderr: stderr.slice(-2000),
              stdout_tail: stdout.slice(-500),
            },
            { status: 500 }
          )
        );
      }
    });
    proc.on("error", (e) => {
      clearTimeout(timer);
      resolve(
        NextResponse.json({ error: `spawn failed: ${e.message}` }, { status: 500 })
      );
    });
  });
}
