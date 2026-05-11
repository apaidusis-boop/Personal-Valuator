"use client";

import { Search } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { openTickerSheet } from "@/lib/ticker-sheet";

type Hit = {
  ticker: string;
  name: string | null;
  sector: string | null;
  market: "br" | "us";
  is_holding: 0 | 1;
};

export default function GlobalSearch() {
  const [q, setQ] = useState("");
  const [hits, setHits] = useState<Hit[]>([]);
  const [open, setOpen] = useState(false);
  const [activeIdx, setActiveIdx] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  // Cmd/Ctrl-K focus
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        inputRef.current?.focus();
        setOpen(true);
      }
      if (e.key === "Escape") {
        setOpen(false);
        inputRef.current?.blur();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  // Debounced fetch
  useEffect(() => {
    if (!q.trim()) {
      setHits([]);
      return;
    }
    let alive = true;
    const id = setTimeout(() => {
      fetch(`/api/search?q=${encodeURIComponent(q.trim())}`)
        .then((r) => r.json())
        .then((j) => alive && setHits(j.hits || []))
        .catch(() => {});
    }, 120);
    return () => {
      alive = false;
      clearTimeout(id);
    };
  }, [q]);

  function pick(h: Hit) {
    setOpen(false);
    setQ("");
    openTickerSheet(h.ticker);
  }

  function gotoPage(h: Hit) {
    setOpen(false);
    setQ("");
    router.push(`/ticker/${encodeURIComponent(h.ticker)}`);
  }

  return (
    <div className="relative w-[360px]">
      <div
        className="flex items-center gap-2 rounded px-3 py-2"
        style={{ background: "var(--bg-elevated)" }}
      >
        <Search size={15} style={{ color: "var(--text-label)" }} />
        <input
          ref={inputRef}
          type="text"
          value={q}
          onChange={(e) => {
            setQ(e.target.value);
            setOpen(true);
            setActiveIdx(0);
          }}
          onFocus={() => setOpen(true)}
          onBlur={() => setTimeout(() => setOpen(false), 150)}
          onKeyDown={(e) => {
            if (e.key === "ArrowDown") {
              e.preventDefault();
              setActiveIdx((i) => Math.min(i + 1, hits.length - 1));
            } else if (e.key === "ArrowUp") {
              e.preventDefault();
              setActiveIdx((i) => Math.max(i - 1, 0));
            } else if (e.key === "Enter") {
              e.preventDefault();
              const h = hits[activeIdx];
              if (h) {
                if (e.shiftKey) gotoPage(h);
                else pick(h);
              }
            }
          }}
          placeholder="Buscar empresas, setores, relatórios e mais…"
          className="bg-transparent text-sm outline-none flex-1"
          style={{ color: "var(--text-primary)" }}
        />
        <kbd
          className="text-[10px] px-1.5 py-0.5 rounded"
          style={{
            color: "var(--text-tertiary)",
            background: "var(--bg-canvas)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          ⌘K
        </kbd>
      </div>

      {open && q.trim() && (
        <div
          className="absolute left-0 right-0 mt-1 rounded shadow-lg z-50 overflow-hidden"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
            maxHeight: 360,
            overflowY: "auto",
          }}
        >
          {hits.length === 0 ? (
            <div
              className="px-3 py-3 text-xs italic"
              style={{ color: "var(--text-tertiary)" }}
            >
              Sem matches para "{q}".
            </div>
          ) : (
            <>
              {hits.map((h, i) => (
                <button
                  key={`${h.market}-${h.ticker}`}
                  type="button"
                  onMouseDown={(e) => {
                    e.preventDefault();
                    pick(h);
                  }}
                  onMouseEnter={() => setActiveIdx(i)}
                  className="w-full text-left flex items-center gap-3 px-3 py-2 transition-colors"
                  style={{
                    background:
                      i === activeIdx ? "var(--bg-overlay)" : "transparent",
                    borderBottom:
                      i < hits.length - 1
                        ? "1px solid var(--border-subtle)"
                        : "none",
                  }}
                >
                  <span
                    className="text-[10px] uppercase font-data"
                    style={{
                      color:
                        h.market === "br"
                          ? "var(--mkt-br, var(--accent-primary))"
                          : "var(--mkt-us, var(--accent-primary))",
                      width: 22,
                      letterSpacing: "0.05em",
                    }}
                  >
                    {h.market}
                  </span>
                  <span
                    className="font-data"
                    style={{
                      color: "var(--text-primary)",
                      fontWeight: 600,
                      fontSize: 12,
                      width: 64,
                    }}
                  >
                    {h.ticker}
                  </span>
                  <span
                    style={{
                      color: "var(--text-secondary)",
                      fontSize: 12,
                      flex: 1,
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {h.name || "—"}
                  </span>
                  {h.sector && (
                    <span
                      className="text-[10px]"
                      style={{ color: "var(--text-tertiary)" }}
                    >
                      {h.sector}
                    </span>
                  )}
                  {h.is_holding === 1 && (
                    <span
                      className="text-[10px] px-1.5 py-0.5 rounded font-data"
                      style={{
                        background: "var(--val-gold-soft, var(--bg-overlay))",
                        color: "var(--val-gold, var(--accent-primary))",
                      }}
                    >
                      H
                    </span>
                  )}
                </button>
              ))}
              <div
                className="px-3 py-2 text-[10px] flex items-center justify-between"
                style={{
                  color: "var(--text-tertiary)",
                  borderTop: "1px solid var(--border-subtle)",
                  background: "var(--bg-canvas)",
                }}
              >
                <span>↵ abre side-sheet · ⇧↵ abre página</span>
                <span>{hits.length} match{hits.length === 1 ? "" : "es"}</span>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
