"use client";

import { useState, useRef, useEffect, useMemo } from "react";

type Msg = { role: "user" | "assistant" | "error"; text: string; ts: number };

const STORAGE_KEY = "antonio-carlos-chat-v2";

function loadMessages(): Msg[] {
  if (typeof window === "undefined") return [];
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
}

function saveMessages(msgs: Msg[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(msgs.slice(-50)));
  } catch {
    /* ignore */
  }
}

const SLASH_COMMANDS: { name: string; description: string; expand: string }[] = [
  { name: "/allocate", description: "ver proposta de alocação", expand: "Mostra a allocation actual e top weights." },
  { name: "/hedge", description: "estado do hedge tactical", expand: "O hedge tactical está activo? Qual instrument e size?" },
  { name: "/strategy", description: "engines de um ticker — ex: /strategy ACN", expand: "Como é que cada engine vê o ticker {arg}? Score, verdict, rationale." },
  { name: "/why", description: "porque este ticker está em XYZ — ex: /why JNJ", expand: "Porque é que {arg} tem este verdict no Council? Quais drivers, quais dissents?" },
  { name: "/position", description: "minha posição em — ex: /position ITSA4", expand: "Qual minha posição actual em {arg}? PnL, YoC, custo, market value." },
  { name: "/regime", description: "regime macro actual", expand: "Em que regime macro estamos (BR e US)? Sectores favorecidos, defesa em curso?" },
];

function expandCommand(text: string): string {
  const trimmed = text.trim();
  if (!trimmed.startsWith("/")) return text;
  const [cmd, ...rest] = trimmed.split(/\s+/);
  const arg = rest.join(" ").trim();
  const match = SLASH_COMMANDS.find((c) => c.name === cmd);
  if (!match) return text;
  return match.expand.replace("{arg}", arg || "(specify)");
}

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    setMessages(loadMessages());
  }, []);

  useEffect(() => {
    saveMessages(messages);
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  // Cmd+K / Ctrl+K opens chat
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((v) => !v);
      }
      if (e.key === "Escape" && open) {
        setOpen(false);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open]);

  const slashSuggestions = useMemo(() => {
    const t = input.trim();
    if (!t.startsWith("/")) return [];
    const prefix = t.split(/\s+/)[0];
    return SLASH_COMMANDS.filter((c) => c.name.startsWith(prefix)).slice(0, 5);
  }, [input]);

  async function send() {
    const raw = input.trim();
    if (!raw || busy) return;
    const expanded = expandCommand(raw);
    const userMsg: Msg = { role: "user", text: raw, ts: Date.now() };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setBusy(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ message: expanded, chat_id: "mission-control" }),
      });
      const data = await res.json();
      if (res.ok) {
        setMessages((m) => [
          ...m,
          { role: "assistant", text: data.reply || "(empty)", ts: Date.now() },
        ]);
      } else {
        setMessages((m) => [
          ...m,
          {
            role: "error",
            text: `Erro: ${data.error || res.statusText}\n${data.stderr || ""}`.slice(0, 800),
            ts: Date.now(),
          },
        ]);
      }
    } catch (e: unknown) {
      const err = e instanceof Error ? e.message : String(e);
      setMessages((m) => [...m, { role: "error", text: `Network: ${err}`, ts: Date.now() }]);
    } finally {
      setBusy(false);
    }
  }

  function clearChat() {
    setMessages([]);
    saveMessages([]);
  }

  function pickSlash(name: string) {
    setInput(name + " ");
    inputRef.current?.focus();
  }

  function keyHandler(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
    if (e.key === "Tab" && slashSuggestions.length > 0 && input.startsWith("/")) {
      e.preventDefault();
      pickSlash(slashSuggestions[0].name);
    }
  }

  return (
    <>
      {/* Trigger button */}
      <button
        onClick={() => setOpen((v) => !v)}
        className={
          "fixed bottom-5 right-5 z-50 grid place-items-center w-12 h-12 rounded-full " +
          "transition-all duration-200 hover:scale-105 type-h2 " +
          (open
            ? "bg-[var(--bg-overlay)] border border-[var(--border-strong)] text-[var(--text-secondary)]"
            : "")
        }
        style={
          !open
            ? {
                background:
                  "linear-gradient(135deg, var(--accent-primary), var(--accent-glow))",
                boxShadow: "0 0 24px rgba(139,92,246,0.4)",
              }
            : undefined
        }
        aria-label="Antonio Carlos"
        title="Antonio Carlos · cmd+k"
      >
        <span aria-hidden>{open ? "×" : "◈"}</span>
      </button>

      {/* Panel */}
      {open && (
        <div className="fixed bottom-20 right-5 z-50 w-[28rem] max-w-[calc(100vw-2rem)] h-[34rem] flex flex-col rounded-lg overflow-hidden border border-[var(--border-strong)] shadow-2xl"
          style={{ background: "var(--bg-elevated)" }}
        >
          <header className="flex items-center justify-between px-4 py-3 border-b border-[var(--border-subtle)]">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-[var(--accent-glow)] dot-live animate-pulse" aria-hidden />
              <span className="type-body text-[var(--text-primary)] font-medium">
                Antonio Carlos
              </span>
              <span className="type-mono-sm text-[var(--text-tertiary)]">
                · chief of staff
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="type-mono-sm text-[var(--text-disabled)] hidden sm:inline">
                ⌘K
              </span>
              <button
                onClick={clearChat}
                className="type-mono-sm text-[var(--text-tertiary)] hover:text-[var(--verdict-avoid)] transition-colors"
                title="Clear local history"
              >
                clear
              </button>
            </div>
          </header>

          <div
            ref={scrollRef}
            className="flex-1 overflow-y-auto p-3 space-y-3"
          >
            {messages.length === 0 && (
              <div className="space-y-3 px-2 py-2">
                <p className="type-body-sm text-[var(--text-secondary)] italic">
                  Pergunta livre em PT-BR ou usa um shortcut:
                </p>
                <ul className="space-y-1">
                  {SLASH_COMMANDS.map((c) => (
                    <li key={c.name}>
                      <button
                        onClick={() => pickSlash(c.name)}
                        className="w-full text-left px-2 py-1.5 rounded hover:bg-[var(--bg-overlay)] transition-colors"
                      >
                        <span className="type-mono text-[var(--accent-glow)]">
                          {c.name}
                        </span>
                        <span className="type-body-sm text-[var(--text-tertiary)] ml-2">
                          {c.description}
                        </span>
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {messages.map((m, i) => (
              <Bubble key={i} msg={m} />
            ))}
            {busy && (
              <div className="type-body-sm text-[var(--text-tertiary)] italic px-2 py-1 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-[var(--accent-glow)] animate-pulse" aria-hidden />
                a pensar (qwen 2.5 32B)…
              </div>
            )}
          </div>

          {/* Slash suggestions strip */}
          {slashSuggestions.length > 0 && (
            <div className="border-t border-[var(--border-subtle)] px-2 py-1.5 flex items-center gap-1 overflow-x-auto"
              style={{ background: "var(--bg-overlay)" }}
            >
              {slashSuggestions.map((s) => (
                <button
                  key={s.name}
                  onClick={() => pickSlash(s.name)}
                  className="pill pill-glow whitespace-nowrap shrink-0 hover:bg-[rgba(6,182,212,0.12)]"
                  title={s.description}
                >
                  {s.name}
                </button>
              ))}
            </div>
          )}

          <footer
            className="border-t border-[var(--border-subtle)] p-2"
            style={{ background: "var(--bg-deep)" }}
          >
            <textarea
              ref={inputRef}
              rows={2}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={keyHandler}
              placeholder={busy ? "aguarda…" : "pergunta · ou /comando · enter envia"}
              disabled={busy}
              className="w-full bg-transparent type-body-sm text-[var(--text-primary)] outline-none resize-none placeholder-[var(--text-disabled)] px-2 py-1"
            />
            <div className="flex items-center justify-between mt-1 px-2">
              <span className="type-mono-sm text-[var(--text-disabled)]">
                shift+enter = new line · {messages.length} msgs
              </span>
              <button
                onClick={send}
                disabled={busy || !input.trim()}
                className="pill pill-purple disabled:opacity-40 disabled:cursor-not-allowed hover:bg-[rgba(139,92,246,0.18)]"
              >
                send →
              </button>
            </div>
          </footer>
        </div>
      )}
    </>
  );
}

function Bubble({ msg }: { msg: Msg }) {
  if (msg.role === "user") {
    return (
      <div className="flex justify-end">
        <div
          className="rounded-lg px-3 py-2 max-w-[85%] type-body-sm whitespace-pre-wrap"
          style={{
            background: "rgba(6,182,212,0.08)",
            border: "1px solid rgba(6,182,212,0.2)",
            color: "var(--text-primary)",
          }}
        >
          {msg.text}
        </div>
      </div>
    );
  }
  if (msg.role === "error") {
    return (
      <div
        className="rounded-lg px-3 py-2 type-mono-sm whitespace-pre-wrap"
        style={{
          background: "rgba(239,68,68,0.06)",
          border: "1px solid rgba(239,68,68,0.25)",
          color: "var(--verdict-avoid)",
        }}
      >
        {msg.text}
      </div>
    );
  }
  return (
    <div className="flex justify-start">
      <div
        className="rounded-lg px-3 py-2 max-w-[88%] type-body-sm whitespace-pre-wrap leading-relaxed"
        style={{
          background: "rgba(139,92,246,0.06)",
          border: "1px solid rgba(139,92,246,0.18)",
          color: "var(--text-primary)",
        }}
      >
        {msg.text}
      </div>
    </div>
  );
}
