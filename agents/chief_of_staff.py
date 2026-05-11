"""Antonio Carlos — Chief of Staff agent.

Tool-calling loop on Ollama (Qwen 2.5 32B) with persistent per-chat conversation
memory. Replaces the rigid intent classifier in `_nl_dispatch.py` for anything
beyond trivial single-shot questions. The trivial path is preserved as a fast
fallback (sub-second answers for "preço de X", "minha posição em Y").

Architecture:
  user msg → load history → loop {
    Ollama chat with tools → if tool_calls: execute and feed back; else: done
  } → save assistant turn → return text

Memory:
  SQLite at data/chief_memory.db, table `messages(chat_id, ts, role, content)`.
  Last MAX_HISTORY messages per chat_id loaded into context. Older auto-pruned.

Identity:
  Persona "Antonio Carlos" — Chief of Staff. Speaks PT-BR, factual, terse.
  Refuses to invent numbers; if a tool returns no data, says so.
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents._tools import execute_tool, tool_schemas


OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "qwen2.5:32b-instruct-q4_K_M"
DB_PATH = ROOT / "data" / "chief_memory.db"
WORKSPACE_DIR = ROOT / "obsidian_vault" / "workspace"
WORKSPACE_FILES = ("IDENTITY.md", "SOUL.md", "AGENTS.md", "USER.md", "TOOLS.md")
MAX_HISTORY = 20
MAX_TOOL_ROUNDS = 6
TOOL_TIMEOUT_SEC = 240


SYSTEM_PROMPT_BASE = """Tu és o Antonio Carlos, Chief of Staff de um sistema pessoal de investimentos do founder.

A tua identidade, voz, SOP e profile do founder estão nos blocos workspace
abaixo (=== IDENTITY.md ===, === SOUL.md ===, === AGENTS.md ===, === USER.md ===,
=== TOOLS.md ===). Lê-os como tua extensão — não os repitas, age sobre eles.

CONTEXTO TÉCNICO (operacional, não-mutável em runtime):
- Duas DBs: BR (B3, BRL) e US (NYSE/NASDAQ, USD). Tickers BR não levam .SA na DB.
- 15 perpetuums em agents/perpetuum/. Verdict, synthetic_ic, variant_perception são ferramentas profundas (mais lentas).
- Memória conversacional em data/chief_memory.db (per-chat, 20 turns rolling).

REGRAS DE USO DE TOOLS:
1. SEMPRE chama uma tool antes de responder com números. Não chutes EPS, P/E, preço, posição.
2. Para perguntas simples (preço, posição) → 1 tool, resposta directa.
3. Para perguntas complexas (rebalance, comparação, "o que fazer") → encadeia tools.
4. NUNCA chames `web_research` se outra tool serve — quota Tavily é limitada.
5. NUNCA chames `add_note` sem o user pedir explicitamente "anota", "lembra-te", "guarda".
6. Se uma tool falha (`error` no resultado), explica ao founder e oferece alternativa.

QUANDO PARAR DE CHAMAR TOOLS:
- Tens dados suficientes para responder.
- Já fizeste 5+ tool calls (limite prático).
- Uma tool retornou erro irrecuperável.

NUNCA NARRES O QUE VAIS FAZER:
- Errado: "Agora vou chamar X..." e parar a resposta sem chamar.
- Certo: chamas X (tool call) OU dás a resposta final completa.
- Resposta truncada é pior que resposta curta com tool calls em falta.
"""


def _load_workspace() -> str:
    """Read workspace markdown files (IDENTITY/SOUL/AGENTS/USER/TOOLS) and concat.

    Hot-reloads on every invocation — edits to vault files take effect immediately
    without restarting any daemon. Missing files are silently skipped (graceful
    fallback to SYSTEM_PROMPT_BASE only).
    """
    parts: list[str] = []
    for fname in WORKSPACE_FILES:
        p = WORKSPACE_DIR / fname
        if not p.exists():
            continue
        try:
            content = p.read_text(encoding="utf-8").strip()
        except Exception:
            continue
        if content:
            parts.append(f"\n\n=== {fname} ===\n\n{content}")
    return "".join(parts)


def build_system_prompt() -> str:
    """SYSTEM_PROMPT_BASE + workspace markdown injection. Public for tests/inspection."""
    return SYSTEM_PROMPT_BASE + _load_workspace()


# Backwards-compatibility alias — some callers still import SYSTEM_PROMPT.
# Resolves at module-load time; for hot-reload use build_system_prompt() per turn.
SYSTEM_PROMPT = build_system_prompt()


# ─── Memory ───────────────────────────────────────────────────────────────

def _ensure_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id   TEXT NOT NULL,
                ts        TEXT NOT NULL,
                role      TEXT NOT NULL,
                content   TEXT NOT NULL,
                tool_name TEXT
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_chat_ts ON messages(chat_id, ts)")
        c.commit()


def _load_history(chat_id: str, limit: int = MAX_HISTORY) -> list[dict]:
    _ensure_db()
    with sqlite3.connect(DB_PATH) as c:
        rows = c.execute(
            "SELECT role, content, tool_name FROM messages "
            "WHERE chat_id=? ORDER BY id DESC LIMIT ?",
            (chat_id, limit),
        ).fetchall()
    rows.reverse()
    out: list[dict] = []
    for role, content, tool_name in rows:
        msg: dict = {"role": role, "content": content}
        if role == "tool" and tool_name:
            msg["name"] = tool_name
        out.append(msg)
    return out


def _save_message(chat_id: str, role: str, content: str, tool_name: str | None = None):
    _ensure_db()
    with sqlite3.connect(DB_PATH) as c:
        c.execute(
            "INSERT INTO messages (chat_id, ts, role, content, tool_name) VALUES (?,?,?,?,?)",
            (chat_id, datetime.now(timezone.utc).isoformat(timespec="seconds"),
             role, content, tool_name),
        )
        c.commit()


def reset_chat(chat_id: str) -> int:
    """Wipe history for a chat. Returns rows deleted."""
    _ensure_db()
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM messages WHERE chat_id=?", (chat_id,))
        c.commit()
        return cur.rowcount


# ─── Ollama chat with tools ───────────────────────────────────────────────

def _chat(messages: list[dict], model: str = DEFAULT_MODEL,
          tools: list[dict] | None = None, temperature: float = 0.3,
          max_tokens: int = 3000) -> dict:
    """Single Ollama chat completion. Returns the message dict."""
    payload: dict = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    if tools:
        payload["tools"] = tools
    try:
        r = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=TOOL_TIMEOUT_SEC)
        r.raise_for_status()
        return r.json().get("message", {}) or {}
    except Exception as e:
        return {"role": "assistant", "content": f"[chat erro: {type(e).__name__}: {e}]"}


# ─── Slash directives ─────────────────────────────────────────────────────
#
# OpenClaw pattern: lightweight prefix tokens that modify a turn (or persist to
# session if directive-only). Stripped before model sees the text.

_DIRECTIVE_RE = re.compile(r"^/(think|verbose|fast|model|reset|limpar)(?:\s+(\S.*))?$")


def _parse_directives(text: str) -> tuple[dict, str]:
    """Strip leading slash directives; return (overrides_dict, remaining_text).

    Recognises: /think <low|med|high>, /verbose, /fast, /model <id>, /reset, /limpar.
    Multiple directives can be chained on separate leading lines.
    """
    overrides: dict = {}
    lines = text.splitlines()
    consumed = 0
    for line in lines:
        m = _DIRECTIVE_RE.match(line.strip())
        if not m:
            break
        verb, arg = m.group(1), (m.group(2) or "").strip()
        if verb in ("reset", "limpar"):
            overrides["reset"] = True
        elif verb == "verbose":
            overrides["verbose"] = True
        elif verb == "fast":
            overrides["fast"] = True
            overrides["temperature"] = 0.1
        elif verb == "think":
            level = arg.lower() if arg else "med"
            overrides["thinking"] = level
            # higher thinking = more tokens to plan
            overrides["max_tokens"] = {"low": 1500, "med": 3000, "high": 6000}.get(level, 3000)
        elif verb == "model":
            if arg:
                overrides["model"] = arg
        consumed += 1
    remaining = "\n".join(lines[consumed:]).strip()
    return overrides, remaining


# ─── Main entry point ─────────────────────────────────────────────────────

def handle(text: str, chat_id: str = "default", *, verbose: bool = False) -> str:
    """Process a free-form user message; return final assistant reply text."""
    text = (text or "").strip()
    if not text:
        return "Mensagem vazia."

    # Parse leading slash directives (OpenClaw-style: /think, /verbose, /fast, /model, /reset).
    overrides, text = _parse_directives(text)
    if overrides.get("reset"):
        n = reset_chat(chat_id)
        return f"Memória limpa ({n} mensagens removidas)."
    if overrides.get("verbose"):
        verbose = True
    model_override = overrides.get("model") or DEFAULT_MODEL
    max_tokens = overrides.get("max_tokens", 3000)
    temperature = overrides.get("temperature", 0.3)

    if not text:  # directive-only message — acknowledge and persist preferences
        ack = []
        if "thinking" in overrides:
            ack.append(f"thinking={overrides['thinking']}")
        if "model" in overrides:
            ack.append(f"model={overrides['model']}")
        if overrides.get("fast"):
            ack.append("fast mode")
        if overrides.get("verbose"):
            ack.append("verbose tracing")
        return "OK. " + ", ".join(ack) if ack else "OK."

    history = _load_history(chat_id)
    _save_message(chat_id, "user", text)

    # Hot-reload workspace markdowns on every turn — vault edits take effect immediately.
    messages: list[dict] = [{"role": "system", "content": build_system_prompt()}]
    messages.extend(history)
    messages.append({"role": "user", "content": text})

    tools = tool_schemas()
    final_text = ""
    tool_trace: list[str] = []

    for turn in range(MAX_TOOL_ROUNDS):
        msg = _chat(messages, tools=tools, model=model_override,
                    temperature=temperature, max_tokens=max_tokens)
        tool_calls = msg.get("tool_calls") or []
        content = msg.get("content", "") or ""

        if not tool_calls:
            final_text = content.strip() or "(sem resposta)"
            break

        messages.append({"role": "assistant", "content": content, "tool_calls": tool_calls})

        for tc in tool_calls:
            fn = tc.get("function", {})
            name = fn.get("name", "")
            args = fn.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}

            if verbose:
                tool_trace.append(f"→ {name}({json.dumps(args, ensure_ascii=False)[:80]})")

            result = execute_tool(name, args)
            result_str = json.dumps(result, ensure_ascii=False, default=str)[:4000]

            messages.append({
                "role": "tool",
                "name": name,
                "content": result_str,
            })
            _save_message(chat_id, "tool", result_str, tool_name=name)
    else:
        final_text = ("Atingi o limite de tool calls sem chegar a uma resposta. "
                      "Tenta reformular a pergunta ou pede passos mais pequenos.")

    _save_message(chat_id, "assistant", final_text)

    if verbose and tool_trace:
        return final_text + "\n\n_trace:_\n" + "\n".join(tool_trace)
    return final_text


# ─── BaseAgent wrapper (for registry / personas) ──────────────────────────

from agents._base import AgentContext, AgentResult, BaseAgent


class ChiefOfStaffAgent(BaseAgent):
    """Thin BaseAgent shell so Antonio Carlos shows up in /who, /status, agents.yaml.
    Real work happens in `handle()` which is called directly from the Telegram
    controller — this class is not scheduled, it's request-driven."""
    name = "antonio_carlos"
    description = "Chief of Staff — orquestra tools por chat livre"
    default_schedule = "manual"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        return AgentResult(
            agent=self.name, status="no_action",
            summary="Antonio Carlos é request-driven (Telegram), não scheduled.",
            started_at="", finished_at="", duration_sec=0,
        )


# ─── CLI smoke test ───────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Antonio Carlos — Chief of Staff CLI")
    p.add_argument("text", nargs="*", help="Pergunta livre em PT-BR")
    p.add_argument("--chat-id", default="cli-test")
    p.add_argument("--verbose", action="store_true", help="show tool trace")
    p.add_argument("--reset", action="store_true", help="reset chat memory and exit")
    args = p.parse_args()

    if args.reset:
        n = reset_chat(args.chat_id)
        print(f"Memória {args.chat_id}: {n} mensagens removidas.")
        sys.exit(0)

    q = " ".join(args.text) or "qual a minha posição em ITSA4 e vale a pena reforçar?"
    print(f"\n[antonio-carlos] {q}\n")
    print(handle(q, chat_id=args.chat_id, verbose=args.verbose))
