"""TTS output via Windows SAPI (pyttsx3). Zero API cost, fully local."""
from __future__ import annotations

import re


def _clean_markdown(text: str) -> str:
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    text = re.sub(r"[├─└│╔╗╚╝║╠╣]", "", text)
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`(.+?)`", r"\1", text)
    # strip emoji/symbols that TTS reads weirdly
    text = re.sub(r"[✅❌⚠️🔴🟡🟢📊💰⚡🎯📅🎤💬⏳📝🎙️✔✗→←↑↓]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def speak(text: str, rate: int = 160) -> None:
    """Speak text using Windows SAPI. Falls back to print if unavailable."""
    try:
        import pyttsx3
    except ImportError:
        print(f"[TTS] {text}")
        print("[TTS] pip install pyttsx3  to enable voice output")
        return

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", rate)
        for v in engine.getProperty("voices"):
            if "zira" in v.name.lower() or "female" in v.name.lower():
                engine.setProperty("voice", v.id)
                break
        engine.say(_clean_markdown(text))
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[TTS] {text}")
        print(f"[TTS] Error: {e}")


def speak_summary(text: str, max_chars: int = 600) -> None:
    """Speak a capped summary (avoids reading long reports in full)."""
    clean = _clean_markdown(text)
    if len(clean) > max_chars:
        clean = clean[:max_chars].rsplit(" ", 1)[0] + "."
    speak(clean)
