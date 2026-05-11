"use client";

// Fiel Escudeiro chat widget — JPM-clean rebuild.
// - Floating circular button bottom-right (JPM blue, chat glyph).
// - Slide-up card panel: header / scroll / suggestions / composer.
// - Wires to /api/chat (Fiel Escudeiro Claude CLI, stdin-fixed 2026-05-06).
// - Markdown rendered via inline mini-renderer that uses JPM tokens.
// - localStorage history (cap 50), Cmd/Ctrl+K to toggle, ESC closes.

import { useState, useRef, useEffect, useMemo } from "react";
import { MessageSquare, X, Send, Trash2, ChevronRight } from "lucide-react";

type Msg = { role: "user" | "assistant" | "error"; text: string; ts: number };

const STORAGE_KEY = "fiel-escudeiro-chat-v2";
const LEGACY_KEYS = ["fiel-escudeiro-chat-v1", "antonio-carlos-chat-v2"];

function loadMessages(): Msg[] {
  if (typeof window === "undefined") return [];
  try {
    const fresh = localStorage.getItem(STORAGE_KEY);
    if (fresh) return JSON.parse(fresh);
    for (const k of LEGACY_KEYS) {
      const legacy = localStorage.getItem(k);
      if (legacy) {
        localStorage.setItem(STORAGE_KEY, legacy);
        localStorage.removeItem(k);
        return JSON.parse(legacy);
      }
    }
    return [];
  } catch {
    return [];
  }
}

function saveMessages(msgs: Msg[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(msgs.slice(-50)));
  } catch {/* ignore */}
}

const SLASH_COMMANDS: { name: string; description: string; expand: string }[] = [
  { name: "/allocate", description: "ver proposta de alocação", expand: "Mostra a allocation actual e top weights." },
  { name: "/hedge", description: "estado do hedge tactical", expand: "O hedge tactical está activo? Qual instrument e size?" },
  { name: "/strategy", description: "engines de um ticker", expand: "Como é que cada engine vê o ticker {arg}? Score, verdict, rationale." },
  { name: "/why", description: "porque este verdict", expand: "Porque é que {arg} tem este verdict no Council? Quais drivers, quais dissents?" },
  { name: "/position", description: "minha posição em ticker", expand: "Qual minha posição actual em {arg}? PnL, YoC, custo, market value." },
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

// ─── Component ────────────────────────────────────────────────────────

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => { setMessages(loadMessages()); }, []);

  useEffect(() => {
    saveMessages(messages);
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, busy]);

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  // Cmd+K toggles, ESC closes
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((v) => !v);
      }
      if (e.key === "Escape" && open) setOpen(false);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open]);

  // Auto-grow textarea
  useEffect(() => {
    const el = inputRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 160) + "px";
  }, [input]);

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
    if (!confirm("Limpar histórico local? Isto não apaga a memória do servidor.")) return;
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
      {/* ── Floating launcher (closed state) ──────────────────────── */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          aria-label="Abrir Fiel Escudeiro"
          title="Fiel Escudeiro · ⌘K"
          className="fixed bottom-6 right-6 z-40 transition-all"
          style={{
            width: 56,
            height: 56,
            borderRadius: 999,
            background: "var(--accent-primary)",
            color: "white",
            border: 0,
            boxShadow: "var(--shadow-lg)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "var(--jpm-blue-hover)";
            e.currentTarget.style.transform = "translateY(-2px)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "var(--accent-primary)";
            e.currentTarget.style.transform = "translateY(0)";
          }}
        >
          <MessageSquare size={22} strokeWidth={2.2} />
          {messages.length > 0 && (
            <span
              aria-hidden
              style={{
                position: "absolute",
                top: 6,
                right: 6,
                width: 10,
                height: 10,
                borderRadius: 999,
                background: "var(--verdict-buy)",
                border: "2px solid var(--accent-primary)",
              }}
            />
          )}
        </button>
      )}

      {/* ── Open panel ────────────────────────────────────────────── */}
      {open && (
        <div
          className="fixed z-40"
          style={{
            bottom: 24,
            right: 24,
            width: 440,
            maxWidth: "calc(100vw - 32px)",
            height: 620,
            maxHeight: "calc(100vh - 48px)",
            display: "flex",
            flexDirection: "column",
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
            borderRadius: 14,
            boxShadow: "var(--shadow-lg)",
            overflow: "hidden",
          }}
        >
          {/* Header */}
          <header
            className="flex items-center gap-3"
            style={{
              padding: "14px 16px",
              borderBottom: "1px solid var(--border-subtle)",
              background: "var(--bg-elevated)",
            }}
          >
            <span
              aria-hidden
              style={{
                width: 36,
                height: 36,
                borderRadius: 999,
                background: "var(--accent-primary)",
                color: "white",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontWeight: 700,
                fontSize: 14,
                letterSpacing: 0.5,
              }}
            >
              FE
            </span>
            <div style={{ flex: 1, minWidth: 0 }}>
              <p
                className="font-display"
                style={{
                  fontSize: 14,
                  fontWeight: 600,
                  color: "var(--text-primary)",
                  margin: 0,
                  lineHeight: 1.2,
                }}
              >
                Fiel Escudeiro
              </p>
              <p
                className="type-byline"
                style={{ marginTop: 2, color: "var(--text-tertiary)" }}
              >
                <span
                  aria-hidden
                  style={{
                    display: "inline-block",
                    width: 6,
                    height: 6,
                    borderRadius: 999,
                    background: "var(--verdict-buy)",
                    marginRight: 6,
                  }}
                />
                AI · acesso ao repo · ⌘K
              </p>
            </div>
            <button
              onClick={clearChat}
              aria-label="Limpar histórico"
              title="Limpar histórico"
              style={{
                background: "transparent",
                border: 0,
                color: "var(--text-tertiary)",
                cursor: "pointer",
                padding: 6,
                borderRadius: 6,
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "var(--bg-overlay)";
                e.currentTarget.style.color = "var(--verdict-avoid)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "transparent";
                e.currentTarget.style.color = "var(--text-tertiary)";
              }}
            >
              <Trash2 size={15} />
            </button>
            <button
              onClick={() => setOpen(false)}
              aria-label="Fechar"
              style={{
                background: "transparent",
                border: 0,
                color: "var(--text-tertiary)",
                cursor: "pointer",
                padding: 6,
                borderRadius: 6,
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "var(--bg-overlay)";
                e.currentTarget.style.color = "var(--text-primary)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "transparent";
                e.currentTarget.style.color = "var(--text-tertiary)";
              }}
            >
              <X size={16} />
            </button>
          </header>

          {/* Scroll area */}
          <div
            ref={scrollRef}
            style={{
              flex: 1,
              overflowY: "auto",
              padding: "16px",
              background: "var(--bg-canvas)",
            }}
          >
            {messages.length === 0 && (
              <Welcome onPick={pickSlash} />
            )}
            {messages.map((m, i) => (
              <Bubble key={i} msg={m} />
            ))}
            {busy && <ThinkingIndicator />}
          </div>

          {/* Slash suggestions */}
          {slashSuggestions.length > 0 && (
            <div
              style={{
                borderTop: "1px solid var(--border-subtle)",
                padding: "8px 12px",
                background: "var(--bg-overlay)",
                display: "flex",
                gap: 6,
                overflowX: "auto",
              }}
            >
              {slashSuggestions.map((s) => (
                <button
                  key={s.name}
                  onClick={() => pickSlash(s.name)}
                  className="font-data"
                  style={{
                    background: "var(--bg-elevated)",
                    color: "var(--accent-primary)",
                    border: "1px solid var(--border-subtle)",
                    padding: "4px 10px",
                    borderRadius: 999,
                    fontSize: 11,
                    fontWeight: 600,
                    whiteSpace: "nowrap",
                    cursor: "pointer",
                  }}
                  title={s.description}
                >
                  {s.name}
                </button>
              ))}
            </div>
          )}

          {/* Composer */}
          <footer
            style={{
              borderTop: "1px solid var(--border-subtle)",
              padding: "10px 12px",
              background: "var(--bg-elevated)",
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems: "flex-end",
                gap: 8,
                background: "var(--bg-overlay)",
                border: "1px solid var(--border-subtle)",
                borderRadius: 12,
                padding: "8px 10px",
              }}
            >
              <textarea
                ref={inputRef}
                rows={1}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={keyHandler}
                placeholder={busy ? "aguarda…" : "Pergunta · /comando · Enter envia"}
                disabled={busy}
                style={{
                  flex: 1,
                  background: "transparent",
                  color: "var(--text-primary)",
                  fontSize: 14,
                  outline: "none",
                  resize: "none",
                  border: 0,
                  fontFamily: "var(--font-sans)",
                  lineHeight: 1.5,
                  maxHeight: 160,
                }}
              />
              <button
                onClick={send}
                disabled={busy || !input.trim()}
                aria-label="Enviar"
                style={{
                  width: 32,
                  height: 32,
                  borderRadius: 999,
                  background: input.trim() && !busy ? "var(--accent-primary)" : "var(--text-disabled)",
                  color: "white",
                  border: 0,
                  cursor: input.trim() && !busy ? "pointer" : "not-allowed",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                  transition: "background 120ms ease-out",
                }}
              >
                <Send size={14} />
              </button>
            </div>
            <p
              className="type-byline"
              style={{
                marginTop: 6,
                color: "var(--text-tertiary)",
                paddingLeft: 4,
              }}
            >
              Shift+Enter = nova linha · {messages.length} mensagens
            </p>
          </footer>
        </div>
      )}
    </>
  );
}

// ─── Welcome state ───────────────────────────────────────────────────

function Welcome({ onPick }: { onPick: (name: string) => void }) {
  return (
    <div>
      <p
        className="font-display"
        style={{
          fontSize: 16,
          fontWeight: 600,
          color: "var(--text-primary)",
          margin: 0,
          marginBottom: 4,
        }}
      >
        Olá. O que precisas?
      </p>
      <p
        className="type-body-sm"
        style={{ color: "var(--text-tertiary)", marginBottom: 14, marginTop: 0 }}
      >
        Pergunta livre em PT-BR ou usa um shortcut. Eu corro {"`ii <command>`"},
        consulto o SQLite e leio o vault.
      </p>
      <div className="grid grid-cols-2 gap-2">
        {SLASH_COMMANDS.map((c) => (
          <button
            key={c.name}
            onClick={() => onPick(c.name)}
            style={{
              textAlign: "left",
              background: "var(--bg-elevated)",
              border: "1px solid var(--border-subtle)",
              padding: "10px 12px",
              borderRadius: 8,
              cursor: "pointer",
              display: "flex",
              flexDirection: "column",
              gap: 2,
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = "var(--accent-primary)";
              e.currentTarget.style.background = "var(--jpm-blue-soft)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = "var(--border-subtle)";
              e.currentTarget.style.background = "var(--bg-elevated)";
            }}
          >
            <span
              className="font-data"
              style={{ color: "var(--accent-primary)", fontSize: 12, fontWeight: 600 }}
            >
              {c.name}
            </span>
            <span
              className="type-byline"
              style={{ color: "var(--text-tertiary)", lineHeight: 1.35 }}
            >
              {c.description}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

// ─── Thinking indicator ──────────────────────────────────────────────

function ThinkingIndicator() {
  return (
    <div
      className="flex items-center gap-2"
      style={{
        padding: "10px 12px",
        marginTop: 10,
        background: "var(--bg-elevated)",
        border: "1px solid var(--border-subtle)",
        borderRadius: 10,
        maxWidth: "70%",
      }}
    >
      <span className="thinking-dot" style={{ animationDelay: "0ms" }} />
      <span className="thinking-dot" style={{ animationDelay: "180ms" }} />
      <span className="thinking-dot" style={{ animationDelay: "360ms" }} />
      <span
        className="type-byline ml-2"
        style={{ color: "var(--text-tertiary)" }}
      >
        Claude a pensar…
      </span>
      <style jsx>{`
        .thinking-dot {
          width: 6px;
          height: 6px;
          border-radius: 999px;
          background: var(--accent-primary);
          display: inline-block;
          /* Apple-style breathing pulse — opacity-only, ease-out-expo.
             Replaces bounce+translateY which is documented AI-tell
             (impeccable detect: bounce-easing rule). */
          animation: thinking-pulse 1.4s infinite cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes thinking-pulse {
          0%, 100% { opacity: 0.3; }
          50% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}

// ─── Bubble ──────────────────────────────────────────────────────────

function Bubble({ msg }: { msg: Msg }) {
  if (msg.role === "user") {
    return (
      <div className="flex justify-end" style={{ marginBottom: 10 }}>
        <div
          style={{
            background: "var(--accent-primary)",
            color: "white",
            padding: "8px 12px",
            borderRadius: 14,
            borderTopRightRadius: 4,
            maxWidth: "85%",
            fontSize: 14,
            lineHeight: 1.5,
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
          }}
        >
          {msg.text}
        </div>
      </div>
    );
  }
  if (msg.role === "error") {
    return (
      <div style={{ marginBottom: 10 }}>
        <div
          className="type-mono-sm"
          style={{
            background: "var(--jpm-loss-soft)",
            color: "var(--verdict-avoid)",
            padding: "8px 12px",
            borderRadius: 10,
            border: "1px solid var(--verdict-avoid)",
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
          }}
        >
          {msg.text}
        </div>
      </div>
    );
  }
  return (
    <div className="flex" style={{ marginBottom: 10, gap: 8 }}>
      <span
        aria-hidden
        style={{
          width: 28,
          height: 28,
          borderRadius: 999,
          background: "var(--accent-primary)",
          color: "white",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontWeight: 700,
          fontSize: 11,
          flexShrink: 0,
          marginTop: 2,
        }}
      >
        FE
      </span>
      <div
        style={{
          background: "var(--bg-elevated)",
          color: "var(--text-primary)",
          padding: "8px 12px",
          borderRadius: 14,
          borderTopLeftRadius: 4,
          border: "1px solid var(--border-subtle)",
          maxWidth: "85%",
          fontSize: 14,
          lineHeight: 1.55,
          flex: 1,
          minWidth: 0,
        }}
      >
        <ChatMarkdown source={msg.text} />
      </div>
    </div>
  );
}

// ─── Tiny markdown renderer (JPM-themed, inline) ─────────────────────
// Supports headings (##, ###), paragraphs, bullet lists, bold, italic,
// inline code, code blocks, links. No tables (unused in chat).

function ChatMarkdown({ source }: { source: string }) {
  const blocks = parseChatBlocks(source);
  return (
    <>
      {blocks.map((b, i) => {
        if (b.kind === "h2") {
          return (
            <h4
              key={i}
              style={{
                fontWeight: 600,
                fontSize: 13,
                color: "var(--text-primary)",
                margin: "10px 0 4px",
              }}
            >
              {renderInline(b.text)}
            </h4>
          );
        }
        if (b.kind === "h3") {
          return (
            <h5
              key={i}
              className="type-h3"
              style={{ marginTop: 10, marginBottom: 4 }}
            >
              {renderInline(b.text)}
            </h5>
          );
        }
        if (b.kind === "ul") {
          return (
            <ul
              key={i}
              style={{
                paddingLeft: 18,
                margin: "6px 0",
                listStyle: "disc",
              }}
            >
              {b.items.map((it, j) => (
                <li key={j} style={{ marginBottom: 2, lineHeight: 1.5 }}>
                  {renderInline(it)}
                </li>
              ))}
            </ul>
          );
        }
        if (b.kind === "code") {
          return (
            <pre
              key={i}
              style={{
                background: "var(--bg-overlay)",
                border: "1px solid var(--border-subtle)",
                padding: "8px 10px",
                borderRadius: 6,
                fontFamily: "var(--font-mono)",
                fontSize: 12,
                overflowX: "auto",
                margin: "6px 0",
              }}
            >
              {b.text}
            </pre>
          );
        }
        return (
          <p key={i} style={{ margin: "4px 0", lineHeight: 1.55 }}>
            {renderInline(b.text)}
          </p>
        );
      })}
    </>
  );
}

type ChatBlock =
  | { kind: "p"; text: string }
  | { kind: "h2"; text: string }
  | { kind: "h3"; text: string }
  | { kind: "ul"; items: string[] }
  | { kind: "code"; text: string };

function parseChatBlocks(md: string): ChatBlock[] {
  const lines = md.split(/\r?\n/);
  const out: ChatBlock[] = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }
    if (/^##\s+/.test(line)) {
      out.push({ kind: "h2", text: line.replace(/^##\s+/, "") });
      i++;
      continue;
    }
    if (/^###\s+/.test(line)) {
      out.push({ kind: "h3", text: line.replace(/^###\s+/, "") });
      i++;
      continue;
    }
    if (/^```/.test(line)) {
      const buf: string[] = [];
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) {
        buf.push(lines[i]);
        i++;
      }
      i++;
      out.push({ kind: "code", text: buf.join("\n") });
      continue;
    }
    if (/^\s*[-*]\s+/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*[-*]\s+/, ""));
        i++;
      }
      out.push({ kind: "ul", items });
      continue;
    }
    const buf: string[] = [line];
    i++;
    while (i < lines.length && lines[i].trim() && !/^(##|###|```|\s*[-*]\s+)/.test(lines[i])) {
      buf.push(lines[i]);
      i++;
    }
    out.push({ kind: "p", text: buf.join(" ") });
  }
  return out;
}

function renderInline(text: string): React.ReactNode[] {
  // Order matters: code → bold → italic → links
  const out: React.ReactNode[] = [];
  let key = 0;
  let i = 0;
  let buf = "";
  const flush = () => {
    if (buf) { out.push(<span key={key++}>{buf}</span>); buf = ""; }
  };
  while (i < text.length) {
    const c = text[i];
    if (c === "`") {
      const close = text.indexOf("`", i + 1);
      if (close > i) {
        flush();
        out.push(
          <code
            key={key++}
            style={{
              background: "var(--bg-overlay)",
              padding: "1px 5px",
              borderRadius: 4,
              fontFamily: "var(--font-mono)",
              fontSize: 12,
              color: "var(--accent-primary)",
            }}
          >
            {text.slice(i + 1, close)}
          </code>
        );
        i = close + 1;
        continue;
      }
    }
    if (c === "*" && text[i + 1] === "*") {
      const close = text.indexOf("**", i + 2);
      if (close > i + 2) {
        flush();
        out.push(<strong key={key++}>{text.slice(i + 2, close)}</strong>);
        i = close + 2;
        continue;
      }
    }
    if (c === "*" && text[i + 1] !== "*") {
      const close = text.indexOf("*", i + 1);
      if (close > i + 1 && !text.slice(i + 1, close).includes("\n")) {
        flush();
        out.push(<em key={key++}>{text.slice(i + 1, close)}</em>);
        i = close + 1;
        continue;
      }
    }
    if (c === "[") {
      const closeB = text.indexOf("]", i + 1);
      if (closeB > i && text[closeB + 1] === "(") {
        const closeP = text.indexOf(")", closeB + 2);
        if (closeP > closeB) {
          flush();
          out.push(
            <a
              key={key++}
              href={text.slice(closeB + 2, closeP)}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                color: "var(--accent-primary)",
                textDecoration: "underline",
                textDecorationStyle: "dotted",
              }}
            >
              {text.slice(i + 1, closeB)}
            </a>
          );
          i = closeP + 1;
          continue;
        }
      }
    }
    buf += c;
    i++;
  }
  flush();
  return out;
}
