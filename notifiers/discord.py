"""discord — multi-channel push notifications via Discord webhooks.

OpenClaw pattern: each agent/perpetuum/topic gets its own channel. We use
**webhooks** (not bot tokens) for simplicity — no event loop, no permissions
config, just HTTP POST per channel.

Setup (1-time, manual):
  1. Discord → Server Settings → Integrations → Webhooks → New Webhook
     for each desired channel:
        #general
        #daily-digest
        #research
        #triggers
        #perpetuum-actions
        #captains-log
        #paper-trade
        #memory-promotions
  2. Copy each webhook URL.
  3. Add to .env (one line per channel):
        DISCORD_WEBHOOK_GENERAL=https://discord.com/api/webhooks/...
        DISCORD_WEBHOOK_DAILY_DIGEST=...
        DISCORD_WEBHOOK_RESEARCH=...
        DISCORD_WEBHOOK_TRIGGERS=...
        DISCORD_WEBHOOK_PERPETUUM_ACTIONS=...
        DISCORD_WEBHOOK_CAPTAINS_LOG=...
        DISCORD_WEBHOOK_PAPER_TRADE=...
        DISCORD_WEBHOOK_MEMORY_PROMOTIONS=...
  4. Test: python -m notifiers.discord general "Hello LocalClaw"

Without webhooks configured, send() returns {"ok": False, "skipped": True}
so callers can broadcast to all channels without exploding when only some
are wired.

Channels canonicalised here so callers use logical names ('triggers') not
URLs.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Logical channel name → env var mapping. Add new channels here.
CHANNEL_ENV: dict[str, str] = {
    "general": "DISCORD_WEBHOOK_GENERAL",
    "daily-digest": "DISCORD_WEBHOOK_DAILY_DIGEST",
    "research": "DISCORD_WEBHOOK_RESEARCH",
    "triggers": "DISCORD_WEBHOOK_TRIGGERS",
    "perpetuum-actions": "DISCORD_WEBHOOK_PERPETUUM_ACTIONS",
    "captains-log": "DISCORD_WEBHOOK_CAPTAINS_LOG",
    "paper-trade": "DISCORD_WEBHOOK_PAPER_TRADE",
    "memory-promotions": "DISCORD_WEBHOOK_MEMORY_PROMOTIONS",
}


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


def webhook_url(channel: str) -> str | None:
    env = _load_env()
    var = CHANNEL_ENV.get(channel)
    if not var:
        return None
    return env.get(var)


def configured_channels() -> list[str]:
    """Return list of channels with webhook URLs in .env."""
    return [ch for ch in CHANNEL_ENV if webhook_url(ch)]


def send(channel: str, content: str, *, username: str | None = None,
         avatar_url: str | None = None) -> dict:
    """Post `content` to a logical channel via webhook.

    Returns:
      {"ok": True, "channel": ...}  on success
      {"ok": False, "skipped": True, "reason": ...}  if channel not wired (no env var)
      {"ok": False, "error": ...}  on HTTP error
    """
    import requests
    url = webhook_url(channel)
    if not url:
        return {"ok": False, "skipped": True,
                "reason": f"no webhook for '{channel}' (set {CHANNEL_ENV.get(channel, '?')})",
                "channel": channel}

    payload: dict = {"content": content[:1990]}  # Discord 2000-char limit, safe margin
    if username:
        payload["username"] = username[:80]
    if avatar_url:
        payload["avatar_url"] = avatar_url

    try:
        r = requests.post(url, json=payload, timeout=15)
        ok = 200 <= r.status_code < 300
        return {"ok": ok, "status": r.status_code, "channel": channel,
                "error": None if ok else r.text[:300]}
    except Exception as e:
        return {"ok": False, "channel": channel, "error": f"{type(e).__name__}: {e}"}


def broadcast(channels: list[str], content: str, **kwargs) -> list[dict]:
    """Send same content to multiple channels. Skips ones not wired."""
    return [send(ch, content, **kwargs) for ch in channels]


def _main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("--help", "-h"):
        print("Usage:")
        print("  python -m notifiers.discord <channel> '<msg>'")
        print("  python -m notifiers.discord --list")
        print("  python -m notifiers.discord --setup")
        print(f"\nKnown channels: {', '.join(CHANNEL_ENV.keys())}")
        return 1
    if args[0] == "--list":
        wired = configured_channels()
        for ch, var in CHANNEL_ENV.items():
            mark = "✅" if ch in wired else "·"
            print(f"  {mark} {ch:<22} {var}")
        return 0
    if args[0] == "--setup":
        print("""
Setup Discord Webhooks (1-time):
1. Discord server → Server Settings → Integrations → Webhooks → New Webhook
   for each desired channel.
2. Copy webhook URL.
3. Add to .env:
""")
        for ch, var in CHANNEL_ENV.items():
            print(f"  {var}=https://discord.com/api/webhooks/...")
        print("\n4. Test: python -m notifiers.discord general 'hello'")
        return 0

    if len(args) < 2:
        print("Need: <channel> <msg>")
        return 1
    channel, msg = args[0], " ".join(args[1:])
    r = send(channel, msg)
    print(r)
    return 0 if r.get("ok") else 2


if __name__ == "__main__":
    sys.exit(_main())
