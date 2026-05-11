import { NextRequest, NextResponse } from "next/server";
import { spawn } from "node:child_process";
import path from "node:path";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Phase LL.3 Sprint 2 — consensus targets endpoint.
 *
 * Spawns `python -m scoring.consensus_target <TICKER> --json` and returns
 * parsed dict with our_fair, house targets, blended median/mean/weighted,
 * dispersion, upside_blended_pct.
 *
 * Falls back to {error} if the subprocess fails or no data.
 */

const ROOT = path.join(process.cwd(), "..");
const VENV_PY = path.join(ROOT, ".venv", "Scripts", "python.exe");

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ ticker: string }> }
) {
  const { ticker } = await params;
  const tk = ticker.toUpperCase();

  return new Promise<NextResponse>((resolve) => {
    const proc = spawn(
      VENV_PY,
      ["-m", "scoring.consensus_target", tk, "--json"],
      { cwd: ROOT, env: { ...process.env, PYTHONIOENCODING: "utf-8" } }
    );
    let stdout = "";
    let stderr = "";
    const TIMEOUT_MS = 15000;
    const timer = setTimeout(() => {
      proc.kill();
      resolve(
        NextResponse.json(
          { error: "consensus_target timeout" },
          { status: 504 }
        )
      );
    }, TIMEOUT_MS);

    proc.stdout.on("data", (d) => (stdout += d.toString()));
    proc.stderr.on("data", (d) => (stderr += d.toString()));
    proc.on("close", (code) => {
      clearTimeout(timer);
      if (code !== 0) {
        resolve(
          NextResponse.json(
            { error: `exit ${code}`, stderr: stderr.slice(0, 500) },
            { status: 500 }
          )
        );
        return;
      }
      try {
        const data = JSON.parse(stdout);
        resolve(NextResponse.json(data));
      } catch (e) {
        resolve(
          NextResponse.json(
            { error: "parse failed", stdout_head: stdout.slice(0, 500) },
            { status: 500 }
          )
        );
      }
    });
  });
}
