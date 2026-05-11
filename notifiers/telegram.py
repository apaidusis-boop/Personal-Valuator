"""telegram — push notifications via Bot API.

Requer em .env (na root do projecto):
  TELEGRAM_BOT_TOKEN=<bot token from @BotFather>
  TELEGRAM_CHAT_ID=<your chat id — get via @userinfobot>

Uso programático:
    from notifiers.telegram import send
    send("🔔 ACN trigger fired at $170")

CLI:
    python -m notifiers.telegram "Teste alert"
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_env() -> dict:
    env = dict(os.environ)
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return env


def _config() -> tuple[str | None, str | None]:
    env = _load_env()
    return env.get("TELEGRAM_BOT_TOKEN"), env.get("TELEGRAM_CHAT_ID")


def send(text: str, silent: bool = False, *,
         inline_buttons: list[list[dict]] | None = None) -> dict:
    """Envia mensagem. Markdown V2 suportado. Devolve dict da API.

    inline_buttons: optional list-of-rows of buttons. Each button = dict:
        {"text": "✅ Approve", "callback_data": "act:approve:42"}
        {"text": "Open Obsidian", "url": "obsidian://..."}
    Callback handlers vivem em agents/telegram_controller.py (handles
    callback_query updates).
    """
    import requests
    token, chat_id = _config()
    if not token or not chat_id:
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID não configurados em .env"}
    payload = {
        "chat_id": chat_id,
        "text": text[:4000],
        "parse_mode": "Markdown",
        "disable_notification": silent,
        "disable_web_page_preview": True,
    }
    if inline_buttons:
        payload["reply_markup"] = {"inline_keyboard": inline_buttons}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, json=payload, timeout=15)
    try:
        return r.json()
    except Exception:
        return {"ok": False, "error": f"http {r.status_code}: {r.text[:200]}"}


def answer_callback(callback_query_id: str, text: str = "", show_alert: bool = False) -> dict:
    """Acknowledge a callback_query (so the spinner clears in Telegram client)."""
    import requests
    token, _ = _config()
    if not token:
        return {"ok": False}
    url = f"https://api.telegram.org/bot{token}/answerCallbackQuery"
    r = requests.post(url, json={
        "callback_query_id": callback_query_id,
        "text": text[:200],
        "show_alert": show_alert,
    }, timeout=10)
    try:
        return r.json()
    except Exception:
        return {"ok": False}


def edit_message(chat_id: str | int, message_id: int, text: str,
                 inline_buttons: list[list[dict]] | None = None) -> dict:
    """Edit an existing message (used after callback to update buttons → status)."""
    import requests
    token, _ = _config()
    if not token:
        return {"ok": False}
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text[:4000],
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    if inline_buttons is not None:
        payload["reply_markup"] = {"inline_keyboard": inline_buttons}
    url = f"https://api.telegram.org/bot{token}/editMessageText"
    r = requests.post(url, json=payload, timeout=10)
    try:
        return r.json()
    except Exception:
        return {"ok": False}


def send_document(path: str, caption: str = "") -> dict:
    """Envia ficheiro (ex: briefing.md)."""
    import requests
    token, chat_id = _config()
    if not token or not chat_id:
        return {"ok": False, "error": "not configured"}
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(path, "rb") as f:
        files = {"document": (Path(path).name, f)}
        r = requests.post(url, data={
            "chat_id": chat_id,
            "caption": caption[:1000],
        }, files=files, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"ok": False}


def _main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python -m notifiers.telegram '<msg>'  OR  --setup (instruções)")
        return 1
    if sys.argv[1] == "--setup":
        print("""
Setup Telegram Bot (1-time):
1. Abrir Telegram → procurar @BotFather → /newbot → seguir instruções
   → copiar TOKEN (ex: 123456:ABC-DEF...)
2. Procurar @userinfobot → /start → copiar teu CHAT ID (número)
3. Criar .env na root do projecto com:
      TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
      TELEGRAM_CHAT_ID=000000000
4. Testar: python -m notifiers.telegram "ola"
""")
        return 0
    r = send(" ".join(sys.argv[1:]))
    print(r)
    return 0 if r.get("ok") else 2


if __name__ == "__main__":
    sys.exit(_main())
