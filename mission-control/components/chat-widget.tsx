"use client";

import { useState, useRef, useEffect } from "react";

type Msg = { role: "user" | "assistant" | "error"; text: string; ts: number };

const STORAGE_KEY = "antonio-carlos-chat-v1";

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

  async function send() {
    const text = input.trim();
    if (!text || busy) return;
    const userMsg: Msg = { role: "user", text, ts: Date.now() };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setBusy(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ message: text, chat_id: "mission-control" }),
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

  function keyHandler(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  return (
    <>
      {/* Trigger button */}
      <button
        onClick={() => setOpen((v) => !v)}
        className={
          "fixed bottom-5 right-5 z-50 grid place-items-center w-14 h-14 rounded-full " +
          "bg-gradient-to-br from-purple-600 to-cyan-500 shadow-[0_0_20px_rgba(168,85,247,0.5)] " +
          "hover:scale-105 transition-transform text-2xl"
        }
        aria-label="Antonio Carlos"
      >
        {open ? "×" : "🐙"}
      </button>

      {/* Panel */}
      {open && (
        <div className="fixed bottom-24 right-5 z-50 w-[28rem] max-w-[calc(100vw-2rem)] h-[32rem] flex flex-col card-purple rounded-xl shadow-2xl overflow-hidden">
          <header className="flex items-center justify-between px-4 py-3 border-b border-purple-800/40 bg-purple-950/40">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400 dot-live animate-pulse"></span>
              <span className="font-mono text-sm text-purple-200">Antonio Carlos</span>
              <span className="text-[10px] text-zinc-500 font-mono">Chief of Staff</span>
            </div>
            <button
              onClick={clearChat}
              className="text-[10px] font-mono text-zinc-500 hover:text-red-400"
              title="Clear local history"
            >
              CLEAR
            </button>
          </header>

          <div ref={scrollRef} className="flex-1 overflow-y-auto p-3 space-y-3 text-sm">
            {messages.length === 0 && (
              <div className="text-xs text-zinc-500 italic px-2 py-4 text-center">
                Pergunta livre em PT-BR.<br />
                Ex: <em>&ldquo;qual minha posição em ITSA4?&rdquo;</em><br />
                <em>&ldquo;tô com 5k em caixa, onde adicionar?&rdquo;</em>
              </div>
            )}
            {messages.map((m, i) => (
              <Bubble key={i} msg={m} />
            ))}
            {busy && (
              <div className="text-xs text-zinc-500 italic px-2 py-1 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
                Antonio Carlos a pensar (Qwen 2.5 32B)…
              </div>
            )}
          </div>

          <footer className="border-t border-purple-800/40 p-2 bg-zinc-950/60">
            <textarea
              ref={inputRef}
              rows={2}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={keyHandler}
              placeholder={busy ? "aguarda…" : "pergunta em PT (Enter envia)"}
              disabled={busy}
              className="w-full bg-transparent text-sm text-zinc-100 outline-none resize-none placeholder-zinc-600 px-2 py-1"
            />
            <div className="flex items-center justify-between mt-1 px-2">
              <span className="text-[9px] font-mono text-zinc-600">
                Shift+Enter = new line · {messages.length} msgs
              </span>
              <button
                onClick={send}
                disabled={busy || !input.trim()}
                className="px-3 py-1 text-xs font-mono rounded border border-purple-700/50 bg-purple-900/30 hover:bg-purple-900/50 disabled:opacity-40"
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
        <div className="bg-cyan-900/40 border border-cyan-700/40 rounded-lg px-3 py-2 max-w-[85%] text-zinc-100 whitespace-pre-wrap">
          {msg.text}
        </div>
      </div>
    );
  }
  if (msg.role === "error") {
    return (
      <div className="bg-red-900/30 border border-red-700/40 rounded-lg px-3 py-2 text-red-300 text-xs whitespace-pre-wrap font-mono">
        {msg.text}
      </div>
    );
  }
  return (
    <div className="flex justify-start">
      <div className="bg-purple-900/30 border border-purple-700/30 rounded-lg px-3 py-2 max-w-[88%] text-zinc-100 whitespace-pre-wrap leading-relaxed">
        {msg.text}
      </div>
    </div>
  );
}
