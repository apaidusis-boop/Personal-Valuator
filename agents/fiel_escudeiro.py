"""Fiel Escudeiro — assistente pessoal com acesso total ao repo + vault.

Substitui o cérebro Qwen do antigo Antonio Carlos por Claude CLI headless.
Cada chat_id mapeia a uma session Claude persistida (resumível). O Claude
spawnado tem cwd=II_ROOT, ou seja: vê todo o repo, todas as DBs SQLite, todo
o vault Obsidian, e pode executar `ii <command>` directamente.

Memória: SQLite `data/fiel_escudeiro.db`, tabela `chat_sessions(chat_id, session_id)`.
Primeira mensagem dum chat_id cria session + injecta system prompt; mensagens
seguintes fazem `claude --resume <session_id>`.
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import subprocess
import sys
import uuid
from pathlib import Path

II_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = II_ROOT / "data" / "fiel_escudeiro.db"

SYSTEM_PROMPT = """És o **Fiel Escudeiro**, assistente pessoal do user neste projecto investment-intelligence.

Identidade:
- Nunca te apresentes como Claude. És o Fiel Escudeiro.
- PT-BR (português europeu OK também — sem rigidez). Terse. Sem emojis a não ser que o user use primeiro.

Acesso:
- Tens read/write a todo o repo (CLAUDE.md tem o catálogo de scripts) e ao vault Obsidian em `obsidian_vault/`.
- DBs SQLite em `data/` (br_investments.db, us_investments.db, e dezenas de outras — listadas no CLAUDE.md).
- Podes correr `ii <command>` directamente via Bash; o catálogo está em CLAUDE.md.

Comportamento:
- Pergunta simples (consultar SQL, ler nota, correr `ii panorama X`) → executa e devolve resultado directo.
- Pedido de mudança no código → descreve em 1-2 frases o que vais fazer, faz, depois resume o que mudou e onde (file:line).
- Operações destrutivas (rm, drop table, git push --force, sobrescrever ficheiros não-versionados, recriar venv) → pedir confirmação textual antes.
- Não inventar tickers ou métricas. Se não tens dados, dizes "não tenho" — ler `feedback_inhouse_first.md` na memória.

Segurança:
- **NUNCA** mostrar conteúdo de `.env`, chaves de API, tokens, ou qualquer secret no output. Se o user pedir, recusa e explica.
- Se um ficheiro tem padrão de chave (`*_API_KEY`, `*_TOKEN`, `password`, etc.), ler para ti mas **redact** ao mostrar.

Princípios coding (de CLAUDE.md):
- Think before coding (declarar assumptions explicitamente).
- Simplicity first (50 linhas > 200).
- Surgical changes (não fazer drive-by refactor).
- Goal-driven (critério verificável antes de declarar done).
"""


def _ensure_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_sessions (
                chat_id      TEXT PRIMARY KEY,
                session_id   TEXT NOT NULL,
                created_at   TEXT NOT NULL DEFAULT (datetime('now')),
                last_used_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )


def _get_or_create_session(chat_id: str) -> tuple[str, bool]:
    """Return (session_uuid, is_new). is_new=True on the first message of this chat."""
    _ensure_db()
    with sqlite3.connect(DB_PATH) as c:
        row = c.execute(
            "SELECT session_id FROM chat_sessions WHERE chat_id=?", (chat_id,)
        ).fetchone()
        if row:
            c.execute(
                "UPDATE chat_sessions SET last_used_at=datetime('now') WHERE chat_id=?",
                (chat_id,),
            )
            return row[0], False
        new_uuid = str(uuid.uuid4())
        c.execute(
            "INSERT INTO chat_sessions (chat_id, session_id) VALUES (?, ?)",
            (chat_id, new_uuid),
        )
        return new_uuid, True


def _reset_chat(chat_id: str) -> int:
    _ensure_db()
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM chat_sessions WHERE chat_id=?", (chat_id,))
        return cur.rowcount


def _claude_exe() -> str:
    """Resolve the claude CLI shim. On Windows, npm installs claude.cmd which
    must be invoked via the .cmd path explicitly when spawned (PowerShell-friendly
    PATH lookup doesn't always work from subprocess)."""
    direct = os.environ.get("CLAUDE_CLI")
    if direct and Path(direct).exists():
        return direct
    if os.name == "nt":
        candidate = Path(os.environ.get("APPDATA", "")) / "npm" / "claude.cmd"
        if candidate.exists():
            return str(candidate)
    return "claude"


def _build_argv(rest: list[str]) -> tuple[list[str], bool]:
    """Build the argv for subprocess.run, plus the shell flag.

    On Windows, npm-installed `.cmd` shims cannot be spawned with shell=False
    in Python 3.7+ (CreateProcess refuses .cmd files). We invoke them via
    cmd.exe /c explicitly so the call works without enabling the broader
    shell=True (which has its own escaping headaches with arbitrary user text)."""
    exe = _claude_exe()
    if os.name == "nt" and exe.lower().endswith((".cmd", ".bat")):
        comspec = os.environ.get("COMSPEC", "C:\\Windows\\System32\\cmd.exe")
        return [comspec, "/d", "/s", "/c", exe, *rest], False
    return [exe, *rest], False


def _permission_mode() -> str:
    """Resolve permission mode from env. Default is `acceptEdits` (safe-ish).
    Set FIEL_ESCUDEIRO_PERMISSION_MODE=bypassPermissions to enable Bash etc.

    bypassPermissions is what the user needs for the assistant to actually
    run scripts (`ii panorama X`, SQL queries, tests). It is equivalent to
    --dangerously-skip-permissions and is opt-in via env var to avoid
    silently granting that capability."""
    mode = os.environ.get("FIEL_ESCUDEIRO_PERMISSION_MODE", "acceptEdits").strip()
    valid = {"default", "acceptEdits", "auto", "bypassPermissions", "plan", "dontAsk"}
    return mode if mode in valid else "acceptEdits"


def _max_budget() -> str | None:
    """Per-message $ cap, configurable via env. Default $3 — generous for Sonnet
    multi-turn but cuts off runaway loops."""
    raw = os.environ.get("FIEL_ESCUDEIRO_MAX_BUDGET_USD", "3.00").strip()
    try:
        v = float(raw)
        return f"{v:.2f}" if v > 0 else None
    except ValueError:
        return "3.00"


def handle(message: str, chat_id: str = "default", *, retried: bool = False) -> str:
    session_id, is_new = _get_or_create_session(chat_id)
    rest: list[str] = [
        "-p",
        "--output-format", "text",
        "--permission-mode", _permission_mode(),
    ]
    budget = _max_budget()
    if budget is not None:
        rest.extend(["--max-budget-usd", budget])
    # Pass the user's message via stdin (NOT as a positional arg). On Windows,
    # the npm-installed claude.cmd is invoked through `cmd.exe /c ...`, and
    # multi-line `--system-prompt` arguments break cmd's argument tokeniser
    # (the newlines collapse and the trailing positional gets eaten as part
    # of the system-prompt value, producing the cryptic "Input must be
    # provided either through stdin or as a prompt argument" error).
    # Stdin is unaffected by cmd's command-line parser.
    if is_new:
        rest.extend(["--session-id", session_id])
        rest.extend(["--append-system-prompt", SYSTEM_PROMPT])
    else:
        rest.extend(["--resume", session_id])
    args, use_shell = _build_argv(rest)

    try:
        proc = subprocess.run(
            args,
            cwd=str(II_ROOT),
            input=message,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
            shell=use_shell,
        )
    except subprocess.TimeoutExpired:
        return "[fiel-escudeiro] timeout (10 min). Tenta dividir a pergunta em passos menores."
    except FileNotFoundError as e:
        return f"[fiel-escudeiro] claude CLI não encontrado: {e}. Verifica PATH ou seta CLAUDE_CLI=<path>."

    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        # If the resume failed (e.g. session id rotated by an external process),
        # nuke the mapping and retry once as a fresh session.
        if not is_new and not retried and ("session" in stderr.lower() or "resume" in stderr.lower()):
            _reset_chat(chat_id)
            return handle(message, chat_id, retried=True)
        return f"[fiel-escudeiro] erro (exit {proc.returncode})\n{stderr[:1500]}"

    out = (proc.stdout or "").strip()
    return out or "(sem resposta)"


def main() -> None:
    p = argparse.ArgumentParser(description="Fiel Escudeiro — assistente Claude-powered")
    p.add_argument("text", nargs="*", help="Pergunta livre em PT-BR")
    p.add_argument("--chat-id", default="cli-test", help="Chat session bucket (mantém memória separada)")
    p.add_argument("--reset", action="store_true", help="Apaga sessão deste chat-id e sai")
    args = p.parse_args()

    if args.reset:
        n = _reset_chat(args.chat_id)
        print(f"Sessão {args.chat_id}: {n} entrada(s) removida(s).")
        sys.exit(0)

    q = " ".join(args.text).strip()
    if not q:
        print("(vazio — passa a pergunta como argumento)", file=sys.stderr)
        sys.exit(2)

    print(f"[fiel-escudeiro] {q}\n")
    print(handle(q, chat_id=args.chat_id))


if __name__ == "__main__":
    main()
