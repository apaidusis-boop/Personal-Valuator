"use client";

import ActionButton, { patchAction, runScript } from "@/components/action-button";

export default function TaskRowActions({
  id,
  market,
  ticker,
}: {
  id: number;
  market: string;
  ticker: string;
}) {
  return (
    <div className="flex items-center gap-1">
      <ActionButton
        size="xs"
        tone="ok"
        label="✓ approve"
        busyLabel="…"
        doneLabel="approved"
        onClick={() => patchAction(id, "resolved", market)}
      />
      <ActionButton
        size="xs"
        tone="ghost"
        label="✗ ignore"
        busyLabel="…"
        doneLabel="ignored"
        onClick={() => patchAction(id, "ignored", market)}
      />
      <ActionButton
        size="xs"
        tone="primary"
        label={`deepdive ${ticker}`}
        busyLabel="running…"
        doneLabel="✓ done"
        refreshAfter={false}
        onClick={() =>
          runScript("deepdive", { ticker, "no-llm": "1", "save-obsidian": "1" })
        }
      />
    </div>
  );
}
