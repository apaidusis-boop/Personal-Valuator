"""Zé Mensageiro — Telegram Desk.

Faz long-poll ao Telegram Bot API (getUpdates) a cada 2 minutos.
Processa comandos enviados pelo founder:

  /status                          → dashboard health (meta_agent output)
  /status <agent>                  → state de um agent específico
  /run <agent>                     → trigger manual de um agent
  /approve <action_id>             → marca watchlist_action como resolved (executed)
  /ignore <action_id>              → marca como ignored
  /panorama <ticker>               → corre ii panorama e envia resumo
  /brief                           → trigger morning_briefing manual
  /help                            → lista comandos
  /who                             → lista funcionários (personas)

Persistente offset em state (.custom.last_update_id) para não re-processar
comandos. Singleton por natureza (cron garante 1 instance).

Requer .env com:
  TELEGRAM_BOT_TOKEN=<token>
  TELEGRAM_CHAT_ID=<teu chat id>  (authorizes SÓ este chat)

Ver wiki/playbooks/Telegram_setup.md para setup inicial.
"""
from __future__ import annotations

import json
import os
import subprocess
import sqlite3
import sys
from pathlib import Path
from datetime import datetime, timezone

import requests

from ._base import AgentContext, AgentResult, BaseAgent
from ._personas import load_all, format_signature, get as get_persona
from ._state import AgentState


class TelegramControllerAgent(BaseAgent):
    name = "telegram_controller"
    description = "Telegram Desk — recebe comandos do founder e despacha"
    default_schedule = "every:2m"

    BOT_API = "https://api.telegram.org/bot{token}/{method}"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root

        # Load env
        env = self._load_env(root)
        token = env.get("TELEGRAM_BOT_TOKEN")
        authorized_chat = env.get("TELEGRAM_CHAT_ID")
        if not token:
            return AgentResult(
                agent=self.name, status="skipped",
                summary="TELEGRAM_BOT_TOKEN não configurado (.env)",
                started_at="", finished_at="", duration_sec=0,
            )

        state = AgentState(self.name, root=root)
        offset = state.get("last_update_id", 0)
        max_cmds = ctx.config.get("max_commands_per_run", 20)

        try:
            resp = requests.get(
                self.BOT_API.format(token=token, method="getUpdates"),
                params={"offset": offset + 1, "timeout": 10, "limit": max_cmds},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            return AgentResult(
                agent=self.name, status="failed",
                summary=f"Telegram getUpdates failed: {type(e).__name__}",
                started_at="", finished_at="", duration_sec=0,
                errors=[str(e)],
            )

        updates = data.get("result", [])
        if not updates:
            return AgentResult(
                agent=self.name, status="no_action",
                summary="Sem comandos novos.",
                started_at="", finished_at="", duration_sec=0,
            )

        actions: list[str] = []
        processed = 0

        for upd in updates:
            offset = max(offset, upd["update_id"])

            # Inline-button callback (JJ-AOW MVP)
            if "callback_query" in upd:
                self._handle_callback(token, root, upd["callback_query"], authorized_chat)
                actions.append(f"callback({upd['callback_query'].get('data','?')[:30]})")
                processed += 1
                continue

            msg = upd.get("message") or {}
            chat_id = str(msg.get("chat", {}).get("id", ""))
            text = (msg.get("text") or "").strip()

            if authorized_chat and chat_id != authorized_chat:
                self._reply(token, chat_id, "🚫 Chat não autorizado.")
                continue

            if not text.startswith("/"):
                # Antonio Carlos — Chief of Staff. Tool-calling agentic loop on
                # Ollama Qwen 2.5 32B, conversational memory per chat_id, ~15
                # tools wrapping the ii catalog. Replaces the rigid intent
                # classifier of _nl_dispatch (kept available as fallback if
                # Antonio Carlos itself fails to load).
                try:
                    from .chief_of_staff import handle as antonio_handle
                    reply = antonio_handle(text, chat_id=chat_id)
                except Exception as e:
                    try:
                        from ._nl_dispatch import handle as nl_handle
                        reply = (f"⚠️ Antonio Carlos offline ({type(e).__name__}); "
                                 f"fallback rápido:\n\n{nl_handle(text)}")
                    except Exception as e2:
                        reply = f"❌ NL dispatcher falhou: {type(e2).__name__}: {e2}"
                self._reply(token, chat_id, reply[:4000])
                actions.append(f"antonio({text[:30]})")
                processed += 1
                continue

            # Parse command
            parts = text.split(maxsplit=2)
            cmd = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []

            # /reset needs chat_id — handle inline before _dispatch
            if cmd == "/reset":
                try:
                    from .chief_of_staff import reset_chat
                    n = reset_chat(chat_id)
                    reply = f"🧹 Memória limpa ({n} mensagens removidas)."
                except Exception as e:
                    reply = f"❌ {type(e).__name__}: {e}"
            else:
                try:
                    reply = self._dispatch(root, cmd, args)
                except Exception as e:
                    reply = f"❌ Erro ao executar {cmd}: {type(e).__name__}: {e}"

            self._reply(token, chat_id, reply[:4000])
            actions.append(f"{cmd}({' '.join(args)})")
            processed += 1

        state.set("last_update_id", offset)
        state.save()

        return AgentResult(
            agent=self.name,
            status="ok" if processed else "no_action",
            summary=f"{format_signature(self.name)}: {processed} comandos processados.",
            started_at="", finished_at="", duration_sec=0,
            actions=actions,
            data={"processed": processed, "offset": offset},
        )

    # ─── Command dispatch ────────────────────────────────────────────────
    def _dispatch(self, root: Path, cmd: str, args: list[str]) -> str:
        if cmd == "/help":
            return (
                "📋 Comandos disponíveis:\n\n"
                "*Conversa livre* — escreve qualquer pergunta em PT, "
                "Antonio Carlos (Chief of Staff) responde e chama as tools certas.\n\n"
                "*Slash commands*:\n"
                "/status — health geral dos agents\n"
                "/status <agent> — detalhe de um agent\n"
                "/run <agent> — execução manual\n"
                "/brief — briefing matinal imediato\n"
                "/panorama <ticker> — verdict rápido\n"
                "/approve <action_id> — marca trigger como executado\n"
                "/ignore <action_id> — descarta trigger\n"
                "/reset — limpa memória conversacional do Antonio Carlos\n"
                "/who — lista funcionários da casa"
            )

        if cmd == "/reset":
            try:
                from .chief_of_staff import reset_chat
                # chat_id é o caller; passa-se via kwargs no caller
                return ("Use a frase 'esquece o que falamos' ou envie /reset "
                        "directamente do chat — a memória será limpa.")
            except Exception as e:
                return f"❌ {type(e).__name__}: {e}"

        if cmd == "/who":
            return self._list_personas()

        if cmd == "/status":
            if args:
                return self._status_agent(root, args[0])
            return self._status_summary(root)

        if cmd == "/run":
            if not args:
                return "Uso: /run <agent_name>"
            return self._run_agent(root, args[0])

        if cmd == "/brief":
            return self._run_agent(root, "morning_briefing")

        if cmd == "/panorama":
            if not args:
                return "Uso: /panorama <TICKER>"
            return self._panorama(root, args[0])

        if cmd == "/approve":
            if not args:
                return "Uso: /approve <action_id>"
            return self._resolve_action(root, int(args[0]), "resolved")

        if cmd == "/ignore":
            if not args:
                return "Uso: /ignore <action_id>"
            return self._resolve_action(root, int(args[0]), "ignored")

        return f"Comando desconhecido: {cmd}\nTenta /help"

    def _list_personas(self) -> str:
        personas = load_all()
        lines = ["👥 *Funcionários da casa:*", ""]
        by_dept: dict[str, list] = {}
        for p in personas.values():
            by_dept.setdefault(p.department, []).append(p)
        for dept, members in sorted(by_dept.items()):
            lines.append(f"*{dept}*")
            for p in members:
                lines.append(f"  • {p.employee_name} — {p.title} (`{p.agent_name}`)")
            lines.append("")
        return "\n".join(lines)

    def _status_summary(self, root: Path) -> str:
        data_dir = root / "data" / "agents"
        if not data_dir.exists():
            return "Sem state de agents."
        lines = ["📊 *Agent status*", ""]
        for f in sorted(data_dir.glob("*.json")):
            if f.name.startswith("_"):
                continue
            try:
                s = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            agent_name = s.get("agent") or f.stem
            p = get_persona(agent_name)
            name = p.employee_name if p else agent_name
            status = s.get("last_status") or "-"
            last = (s.get("last_run") or "")[:16]
            icon = {"ok": "✅", "no_action": "·", "failed": "❌"}.get(status, "?")
            lines.append(f"{icon} *{name}* — {status} @ {last}")
        return "\n".join(lines)

    def _status_agent(self, root: Path, agent_name: str) -> str:
        state_path = root / "data" / "agents" / f"{agent_name}.json"
        if not state_path.exists():
            return f"Sem state para {agent_name}"
        s = json.loads(state_path.read_text(encoding="utf-8"))
        p = get_persona(agent_name)
        name = p.employee_name if p else agent_name
        title = p.title if p else ""
        return (
            f"👤 *{name}* — {title}\n"
            f"`{agent_name}` · schedule {p.schedule if p else '?'}\n\n"
            f"Runs: {s.get('run_count', 0)}\n"
            f"Failed: {s.get('failed_count', 0)}\n"
            f"Consec. failures: {s.get('consecutive_failures', 0)}\n"
            f"Last run: {s.get('last_run') or 'never'}\n"
            f"Last status: {s.get('last_status') or '-'}\n"
            f"Last summary: {s.get('last_summary') or '-'}"
        )

    def _run_agent(self, root: Path, agent_name: str) -> str:
        py = sys.executable
        try:
            r = subprocess.run(
                [py, "-X", "utf8", str(root / "scripts" / "agents_cli.py"),
                 "run", agent_name],
                capture_output=True, text=True, timeout=600,
                cwd=str(root), encoding="utf-8", errors="replace",
            )
            out = (r.stdout or "").strip()[-1500:]
            return f"▶ *{agent_name}* output:\n```\n{out}\n```"
        except Exception as e:
            return f"❌ {type(e).__name__}: {e}"

    def _panorama(self, root: Path, ticker: str) -> str:
        py = sys.executable
        try:
            r = subprocess.run(
                [py, "-X", "utf8", str(root / "scripts" / "panorama.py"), ticker.upper()],
                capture_output=True, text=True, timeout=300,
                cwd=str(root), encoding="utf-8", errors="replace",
            )
            return f"📊 *Panorama {ticker.upper()}*\n\n{(r.stdout or '')[:3500]}"
        except Exception as e:
            return f"❌ {type(e).__name__}: {e}"

    def _resolve_action(self, root: Path, action_id: int, status: str) -> str:
        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            try:
                with sqlite3.connect(db) as c:
                    cur = c.execute(
                        "UPDATE watchlist_actions SET status=?, resolved_at=? "
                        "WHERE id=? AND status='open'",
                        (status, datetime.now(timezone.utc).isoformat(timespec="seconds"), action_id),
                    )
                    if cur.rowcount > 0:
                        c.commit()
                        return f"✅ Action {action_id} → {status}"
            except sqlite3.OperationalError:
                pass
        return f"⚠️ Action {action_id} não encontrada em nenhuma DB."

    # ─── Callback query (inline buttons, JJ-AOW MVP) ─────────────────────

    def _handle_callback(self, token: str, root: Path, cb: dict, authorized_chat: str) -> None:
        """Process inline button click. Format: 'act:<verb>:<action_id>'.

        Verbs: approve | ignore | defer | dossier
        - approve/ignore/defer → UPDATE watchlist_actions.status
        - dossier → reply with link to obsidian dossier (if exists)
        """
        cb_id = cb.get("id", "")
        cb_data = cb.get("data", "")
        chat_id = str(cb.get("from", {}).get("id", ""))
        msg = cb.get("message") or {}
        msg_id = msg.get("message_id")
        msg_chat_id = str(msg.get("chat", {}).get("id", ""))

        if authorized_chat and chat_id != authorized_chat:
            self._answer_cb(token, cb_id, "🚫 não autorizado", show_alert=True)
            return

        try:
            verb, action_id_str = cb_data.split(":")[1:3]
            action_id = int(action_id_str)
        except (ValueError, IndexError):
            self._answer_cb(token, cb_id, f"❌ callback malformed: {cb_data}", show_alert=True)
            return

        verb_to_status = {"approve": "resolved", "ignore": "ignored", "defer": "deferred"}
        if verb in verb_to_status:
            result = self._resolve_action(root, action_id, verb_to_status[verb])
            self._answer_cb(token, cb_id, f"{verb} → {result[:80]}")
            self._edit_status_msg(token, msg_chat_id, msg_id, msg.get("text", ""), verb, action_id)
        elif verb == "dossier":
            ticker = self._ticker_for_action(root, action_id)
            self._answer_cb(token, cb_id, f"📄 dossier para {ticker} (ver vault)")
        else:
            self._answer_cb(token, cb_id, f"❓ verbo desconhecido: {verb}", show_alert=True)

    def _answer_cb(self, token: str, cb_id: str, text: str, show_alert: bool = False) -> None:
        try:
            requests.post(
                self.BOT_API.format(token=token, method="answerCallbackQuery"),
                json={"callback_query_id": cb_id, "text": text[:200],
                      "show_alert": show_alert},
                timeout=10,
            )
        except Exception:
            pass

    def _edit_status_msg(self, token: str, chat_id: str, msg_id: int,
                          original_text: str, verb: str, action_id: int) -> None:
        """Update the original message to show outcome + remove buttons."""
        if not msg_id:
            return
        marker = {
            "approve": "✅ APROVADO",
            "ignore":  "❌ IGNORADO",
            "defer":   "🕒 ADIADO",
        }.get(verb, f"→ {verb}")
        new_text = f"{original_text}\n\n*{marker}* (action #{action_id} via inline button)"
        try:
            requests.post(
                self.BOT_API.format(token=token, method="editMessageText"),
                json={
                    "chat_id": chat_id,
                    "message_id": msg_id,
                    "text": new_text[:4000],
                    "parse_mode": "Markdown",
                    "reply_markup": {"inline_keyboard": []},  # remove buttons
                },
                timeout=10,
            )
        except Exception:
            pass

    def _ticker_for_action(self, root: Path, action_id: int) -> str:
        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            try:
                with sqlite3.connect(db) as c:
                    r = c.execute(
                        "SELECT ticker FROM watchlist_actions WHERE id=?",
                        (action_id,),
                    ).fetchone()
                    if r:
                        return r[0]
            except sqlite3.OperationalError:
                continue
        return "?"

    # ─── Helpers ─────────────────────────────────────────────────────────

    def _load_env(self, root: Path) -> dict:
        env = {}
        env_path = root / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"\'')
        # also check os.environ (cron-set)
        for k in ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]:
            if k in os.environ and not env.get(k):
                env[k] = os.environ[k]
        return env

    def _reply(self, token: str, chat_id: str, text: str) -> None:
        try:
            requests.post(
                self.BOT_API.format(token=token, method="sendMessage"),
                data={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                timeout=15,
            )
        except Exception:
            pass
