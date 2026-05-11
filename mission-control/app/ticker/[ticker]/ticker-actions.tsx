"use client";

import { useState } from "react";
import { Loader2, Terminal, X, Copy, Check } from "lucide-react";

type RunResult = {
  ok: boolean;
  exit_code?: number;
  stdout?: string;
  stderr?: string;
  error?: string;
  script: string;
  args?: string[];
  durationMs: number;
};

async function runScriptFull(
  script: string,
  qs: Record<string, string>
): Promise<RunResult> {
  const url = `/api/run/${script}?${new URLSearchParams(qs).toString()}`;
  const t0 = performance.now();
  try {
    const res = await fetch(url, { method: "POST" });
    const data = await res.json();
    return {
      ok: res.ok,
      exit_code: data.exit_code,
      stdout: data.stdout,
      stderr: data.stderr,
      error: data.error,
      script,
      args: data.args,
      durationMs: Math.round(performance.now() - t0),
    };
  } catch (e: unknown) {
    return {
      ok: false,
      error: e instanceof Error ? e.message : String(e),
      script,
      durationMs: Math.round(performance.now() - t0),
    };
  }
}

export default function TickerActions({ ticker }: { ticker: string }) {
  const [running, setRunning] = useState<string | null>(null);
  const [result, setResult] = useState<RunResult | null>(null);
  const [copied, setCopied] = useState(false);

  async function fire(label: string, script: string, qs: Record<string, string>) {
    if (running) return;
    setRunning(label);
    setResult(null);
    const r = await runScriptFull(script, qs);
    setResult(r);
    setRunning(null);
  }

  const buttons: {
    label: string;
    busyLabel: string;
    tone: "primary" | "ghost";
    script: string;
    qs: Record<string, string>;
  }[] = [
    {
      label: "↻ refresh price",
      busyLabel: "fetching",
      tone: "ghost",
      script: "refresh",
      qs: { ticker },
    },
    {
      label: "🔍 deepdive (no LLM)",
      busyLabel: "analyzing",
      tone: "primary",
      script: "deepdive",
      qs: { ticker, "no-llm": "1" },
    },
    {
      label: "📜 deepdive + dossier",
      busyLabel: "LLM 3-5min",
      tone: "primary",
      script: "deepdive",
      qs: { ticker, "save-obsidian": "1" },
    },
    {
      label: "⚖ verdict",
      busyLabel: "running",
      tone: "ghost",
      script: "verdict",
      qs: { ticker },
    },
    {
      label: "🔭 panorama",
      busyLabel: "running",
      tone: "ghost",
      script: "panorama",
      qs: { ticker },
    },
  ];

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        {buttons.map((b) => {
          const isThis = running === b.label;
          return (
            <button
              key={b.label}
              type="button"
              onClick={() => fire(b.label, b.script, b.qs)}
              disabled={running !== null}
              className="font-mono border px-3 py-1 text-xs disabled:opacity-50 transition-colors flex items-center gap-1.5"
              style={{
                borderRadius: "var(--radius)",
                borderColor:
                  b.tone === "primary"
                    ? "var(--accent-primary)"
                    : "var(--border-subtle)",
                color:
                  b.tone === "primary"
                    ? "var(--accent-primary)"
                    : "var(--text-secondary)",
                background: isThis ? "var(--bg-overlay)" : "transparent",
              }}
            >
              {isThis && <Loader2 size={11} className="animate-spin" />}
              {isThis ? b.busyLabel : b.label}
            </button>
          );
        })}
      </div>

      {result && (
        <div
          className="rounded overflow-hidden"
          style={{
            background: "var(--bg-elevated)",
            border: `1px solid ${result.ok ? "var(--border-subtle)" : "var(--verdict-avoid, var(--loss))"}`,
            borderTop: `2px solid ${result.ok ? "var(--gain, #16a34a)" : "var(--loss)"}`,
          }}
        >
          <div
            className="flex items-center justify-between gap-3 px-3 py-2 text-[11px]"
            style={{
              background: "var(--bg-canvas)",
              borderBottom: "1px solid var(--border-subtle)",
              color: "var(--text-tertiary)",
            }}
          >
            <div className="flex items-center gap-2 flex-wrap">
              <Terminal size={11} />
              <span style={{ color: "var(--text-secondary)", fontWeight: 600 }}>
                {result.script}
              </span>
              {result.args && (
                <span
                  className="font-data"
                  style={{ color: "var(--text-tertiary)" }}
                >
                  {result.args.join(" ")}
                </span>
              )}
              <span style={{ color: "var(--border-subtle)" }}>·</span>
              <span
                className="font-data"
                style={{
                  color: result.ok ? "var(--gain, #16a34a)" : "var(--loss)",
                  fontWeight: 600,
                }}
              >
                {result.ok ? "OK" : `EXIT ${result.exit_code ?? "?"}`}
              </span>
              <span
                className="font-data"
                style={{ color: "var(--text-tertiary)" }}
              >
                {(result.durationMs / 1000).toFixed(1)}s
              </span>
            </div>
            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={() => {
                  const text =
                    (result.stdout || "") +
                    (result.stderr ? "\n--- STDERR ---\n" + result.stderr : "");
                  navigator.clipboard.writeText(text).then(() => {
                    setCopied(true);
                    setTimeout(() => setCopied(false), 1500);
                  });
                }}
                className="p-1 rounded transition-colors"
                style={{ color: "var(--text-tertiary)" }}
                aria-label="Copy output"
              >
                {copied ? <Check size={11} /> : <Copy size={11} />}
              </button>
              <button
                type="button"
                onClick={() => setResult(null)}
                className="p-1 rounded transition-colors"
                style={{ color: "var(--text-tertiary)" }}
                aria-label="Close"
              >
                <X size={11} />
              </button>
            </div>
          </div>
          <pre
            className="font-mono text-[11px] px-3 py-2 overflow-x-auto"
            style={{
              maxHeight: 360,
              overflowY: "auto",
              color: "var(--text-secondary)",
              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
              lineHeight: 1.5,
              margin: 0,
            }}
          >
            {result.stdout && result.stdout.trim() ? (
              result.stdout
            ) : result.error ? (
              <span style={{ color: "var(--loss)" }}>{result.error}</span>
            ) : result.stderr ? (
              <span style={{ color: "var(--loss)" }}>{result.stderr}</span>
            ) : (
              <span
                style={{ color: "var(--text-tertiary)", fontStyle: "italic" }}
              >
                (sem output)
              </span>
            )}
          </pre>
          {result.stdout && result.stderr && (
            <details
              className="px-3 py-2 text-[11px]"
              style={{ borderTop: "1px solid var(--border-subtle)" }}
            >
              <summary
                className="cursor-pointer"
                style={{ color: "var(--text-tertiary)" }}
              >
                stderr ({result.stderr.length} chars)
              </summary>
              <pre
                className="font-mono mt-2"
                style={{
                  color: "var(--loss)",
                  whiteSpace: "pre-wrap",
                  wordBreak: "break-word",
                  maxHeight: 200,
                  overflowY: "auto",
                  lineHeight: 1.5,
                  margin: 0,
                }}
              >
                {result.stderr}
              </pre>
            </details>
          )}
        </div>
      )}
    </div>
  );
}
