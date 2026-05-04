"use client";

import ActionButton, { runScript } from "./action-button";

export default function HomeToolbar() {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <ActionButton
        label="↻ refresh briefing"
        busyLabel="briefing…"
        doneLabel="✓ briefed"
        tone="primary"
        onClick={() => runScript("brief")}
      />
      <ActionButton
        label="↻ topics rescore"
        busyLabel="scoring…"
        doneLabel="✓ scored"
        tone="ghost"
        onClick={() => runScript("topics")}
      />
      <ActionButton
        label="↻ refresh prices (holdings)"
        busyLabel="fetching…"
        doneLabel="✓ refreshed"
        tone="ghost"
        onClick={() => runScript("refresh", { all: "1" })}
      />
      <ActionButton
        label="ii setup"
        busyLabel="checking…"
        doneLabel="see chat"
        tone="ghost"
        refreshAfter={false}
        onClick={() => runScript("setup")}
      />
    </div>
  );
}
