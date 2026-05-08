"""Voice CLI — record, transcribe (Whisper local), parse (Qwen), save to vault.

Commands:
  python scripts/voice_cli.py analyze BBDC4   # Ticker-scoped voice note
  python scripts/voice_cli.py note            # Free-form note (auto-detects ticker)
  python scripts/voice_cli.py brief           # TTS reading of morning brief
  python scripts/voice_cli.py test            # Verify mic + whisper + TTS
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.voice_input import record_and_transcribe
from agents.voice_output import speak, speak_summary

VOICE_NOTES_DIR = ROOT / "obsidian_vault" / "voice_notes"
VOICE_NOTES_DIR.mkdir(parents=True, exist_ok=True)


def _save_to_vault(ticker: str | None, raw_text: str, intent: dict) -> Path:
    today = datetime.now().strftime("%Y-%m-%d")
    ts = datetime.now().strftime("%H%M%S")
    label = ticker.upper() if ticker else "note"
    note_path = VOICE_NOTES_DIR / f"{today}_{label}_{ts}.md"

    lines = [
        f"# Voice Note — {label} — {today}",
        "",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Intent:** `{intent.get('intent', 'general_note')}`",
        "",
        "## Transcription",
        "",
        raw_text,
        "",
        "## Structured",
        "",
    ]

    cf = intent.get("conviction_from")
    ct = intent.get("conviction_to")
    if cf or ct:
        lines.append(f"- **Conviction:** {cf} → {ct}" if cf and ct else f"- **Conviction:** {ct}")

    td = intent.get("trigger_direction")
    if td:
        curr = intent.get("trigger_currency", "")
        price = intent.get("trigger_price", "?")
        lines.append(f"- **Trigger:** {td} at {curr} {price}".strip())

    risk = intent.get("risk_level")
    if risk:
        lines.append(f"- **Risk flag:** {risk.upper()}")

    summary = intent.get("summary")
    if summary:
        lines.append(f"- **Summary:** {summary}")

    if ticker:
        lines.extend(["", f"[[{ticker.upper()}]]"])

    note_path.write_text("\n".join(lines), encoding="utf-8")
    return note_path


def _build_confirmation(ticker: str | None, intent: dict) -> str:
    parts: list[str] = []

    if ticker:
        parts.append(f"{ticker.upper()} note saved.")
    else:
        t = intent.get("ticker")
        parts.append(f"{t} note saved." if t else "Note saved.")

    cf, ct = intent.get("conviction_from"), intent.get("conviction_to")
    if cf and ct:
        parts.append(f"Conviction updated from {cf} to {ct}.")
    elif ct:
        parts.append(f"Conviction set to {ct}.")

    td = intent.get("trigger_direction")
    if td:
        price = intent.get("trigger_price", "?")
        curr = intent.get("trigger_currency", "")
        parts.append(f"New trigger: {td} at {curr} {price}.".strip())

    risk = intent.get("risk_level")
    if risk:
        parts.append(f"Risk flag: {risk}.")

    summary = intent.get("summary")
    if summary and summary not in " ".join(parts):
        parts.append(summary)

    return " ".join(parts)


def cmd_analyze(ticker: str) -> None:
    print(f"\n🎙  Voice analysis: {ticker.upper()}")
    raw, intent = record_and_transcribe(ticker=ticker.upper())
    if not raw:
        print("❌ No audio captured.")
        return

    note_path = _save_to_vault(ticker, raw, intent)
    print(f"\n✅ Saved: obsidian_vault/voice_notes/{note_path.name}")

    msg = _build_confirmation(ticker, intent)
    print(f"💬 {msg}")
    speak(msg)


def cmd_note() -> None:
    print("\n🎙  Free note — speak freely (mention tickers by name or symbol)")
    raw, intent = record_and_transcribe(ticker=None)
    if not raw:
        print("❌ No audio captured.")
        return

    note_path = _save_to_vault(intent.get("ticker"), raw, intent)
    print(f"\n✅ Saved: obsidian_vault/voice_notes/{note_path.name}")
    msg = _build_confirmation(None, intent)
    print(f"💬 {msg}")
    speak(msg)


def cmd_brief() -> None:
    """Run morning_briefing.py and read a summary aloud."""
    brief = ROOT / "scripts" / "morning_briefing.py"
    if not brief.exists():
        brief = ROOT / "scripts" / "portfolio_report.py"

    print(f"📰 Running {brief.name}...")
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(brief)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    if output:
        print(output[:2000])
        speak_summary(output)
    else:
        speak("No briefing output available.")


def cmd_test() -> None:
    print("=== Voice System Check ===\n")

    ok_sd = False
    try:
        import sounddevice as sd
        devs = sd.query_devices()
        inp = [d for d in devs if d["max_input_channels"] > 0]
        print(f"✅ sounddevice — {len(inp)} input device(s)")
        ok_sd = True
    except ImportError:
        print("❌ sounddevice missing — pip install sounddevice")

    ok_w = False
    try:
        import faster_whisper
        print("✅ faster-whisper — available (GPU-accelerated)")
        ok_w = True
    except ImportError:
        try:
            import whisper
            print("✅ whisper (openai) — available (faster-whisper preferred for GPU)")
            ok_w = True
        except ImportError:
            print("❌ No whisper — pip install faster-whisper")

    ok_tts = False
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        print(f"✅ pyttsx3 TTS — {len(voices)} voice(s)")
        engine.stop()
        ok_tts = True
    except ImportError:
        print("❌ pyttsx3 missing — pip install pyttsx3")
    except Exception as e:
        print(f"⚠️  pyttsx3 error — {e}")

    from agents._llm import OLLAMA_URL
    import requests
    try:
        r = requests.get(OLLAMA_URL.replace("/api/generate", "/api/tags"), timeout=3)
        models = [m["name"] for m in r.json().get("models", [])]
        qwen = [m for m in models if "qwen" in m.lower()]
        print(f"✅ Ollama — {len(qwen)} Qwen model(s) available")
    except Exception:
        print("⚠️  Ollama not reachable — intent parsing will fail")

    print()
    if ok_sd and ok_w and ok_tts:
        print("All systems ready.")
        speak("Voice system test complete. All systems nominal.")
    else:
        print("Some components missing — see above.")


def main() -> None:
    p = argparse.ArgumentParser(
        description="Voice CLI for investment-intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  ii voice analyze BBDC4\n"
            "  ii voice note\n"
            "  ii voice brief\n"
            "  ii voice test\n"
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    an = sub.add_parser("analyze", help="Ticker-scoped voice note")
    an.add_argument("ticker", type=str.upper, help="e.g. BBDC4 or JNJ")

    sub.add_parser("note", help="Free-form note (ticker auto-detected from speech)")
    sub.add_parser("brief", help="Read morning brief via TTS")
    sub.add_parser("test", help="Test mic + whisper + TTS + Ollama")

    args = p.parse_args()
    {"analyze": lambda: cmd_analyze(args.ticker),
     "note": cmd_note,
     "brief": cmd_brief,
     "test": cmd_test}[args.cmd]()


if __name__ == "__main__":
    main()
