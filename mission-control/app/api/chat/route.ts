import { NextRequest, NextResponse } from "next/server";
import { spawn } from "node:child_process";
import path from "node:path";
import { II_ROOT } from "@/lib/paths";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Resolve the project's venv Python. Fall back to system `python` ONLY if the
// venv is genuinely missing (fresh checkout) — and never silently: the caller
// surfaces a clear error if the venv is gone. We avoid the bare `python` on
// Windows because the default PATH puts the Microsoft Store App Execution
// Alias first, and that alias fails with 0xC0000142 STATUS_DLL_INIT_FAILED
// when spawned by a long-running Node parent.
function pythonExe(): { path: string; from_venv: boolean } {
  const venv = path.join(II_ROOT, ".venv", "Scripts", "python.exe");
  if (require("node:fs").existsSync(venv)) return { path: venv, from_venv: true };
  return { path: "python", from_venv: false };
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
    // Strip Store Python aliases from PATH so any indirect `python` lookup
    // (subprocess libs, popen calls inside Python) doesn't hit them.
    const filteredPath = (process.env.PATH || "")
      .split(path.delimiter)
      .filter((p) => !/WindowsApps/i.test(p))
      .join(path.delimiter);
    const proc = spawn(py.path, [
      "-X", "utf8",
      "-m", "agents.chief_of_staff",
      "--chat-id", chat_id,
      message,
    ], {
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
          { error: "timeout (240s)", stderr: stderr.slice(-1000) },
          { status: 504 }
        )
      );
    }, 240_000);

    proc.stdout.on("data", (d) => (stdout += d.toString()));
    proc.stderr.on("data", (d) => (stderr += d.toString()));
    proc.on("close", (code) => {
      clearTimeout(timer);
      // The CLI prints "[antonio-carlos] <prompt>" then a blank line then the answer.
      // Strip that header to get just the reply.
      const lines = stdout.split("\n");
      const headerIdx = lines.findIndex((l) => l.startsWith("[antonio-carlos]"));
      const answer = headerIdx >= 0
        ? lines.slice(headerIdx + 1).join("\n").trim()
        : stdout.trim();
      if (code === 0 || answer) {
        resolve(NextResponse.json({ reply: answer || "(sem resposta)", chat_id }));
      } else {
        resolve(
          NextResponse.json(
            { error: `python exited ${code}`, stderr: stderr.slice(-2000) },
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
