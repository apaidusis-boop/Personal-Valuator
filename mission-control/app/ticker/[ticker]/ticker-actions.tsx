"use client";

import ActionButton, { runScript } from "@/components/action-button";

export default function TickerActions({ ticker }: { ticker: string }) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <ActionButton
        label="↻ refresh price"
        busyLabel="fetching…"
        doneLabel="✓ done"
        tone="ghost"
        onClick={() => runScript("refresh", { ticker })}
      />
      <ActionButton
        label="🔍 deepdive (no LLM)"
        busyLabel="analyzing…"
        doneLabel="✓ done"
        tone="primary"
        onClick={() => runScript("deepdive", { ticker, "no-llm": "1" })}
      />
      <ActionButton
        label="📜 deepdive + dossier"
        busyLabel="LLM 3-5min…"
        doneLabel="✓ saved to vault"
        tone="primary"
        onClick={() =>
          runScript("deepdive", { ticker, "save-obsidian": "1" })
        }
      />
      <ActionButton
        label="⚖ verdict"
        busyLabel="…"
        doneLabel="✓"
        tone="ghost"
        onClick={() => runScript("verdict", { ticker })}
      />
      <ActionButton
        label="🔭 panorama"
        busyLabel="…"
        doneLabel="✓"
        tone="ghost"
        onClick={() => runScript("panorama", { ticker })}
      />
    </div>
  );
}
