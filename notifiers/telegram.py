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


def send(text: str, silent: bool = False) -> dict:
    """Envia mensagem. Markdown V2 suportado. Devolve dict da API."""
    import requests
    token, chat_id = _config()
    if not token or not chat_id:
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID não configurados em .env"}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, json={
        "chat_id": chat_id,
        "text": text[:4000],
        "parse_mode": "Markdown",
        "disable_notification": silent,
        "disable_web_page_preview": True,
    }, timeout=15)
    try:
        return r.json()
    except Exception:
        return {"ok": False, "error": f"http {r.status_code}: {r.text[:200]}"}


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
