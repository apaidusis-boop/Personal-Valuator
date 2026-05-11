"""Voice capture + Whisper transcription + Qwen intent parsing. Fully local.

Deps: sounddevice, numpy, faster-whisper (preferred) or whisper (fallback).
No cloud API used — respects inhouse-first rule.
"""
from __future__ import annotations

import os
import sys
import tempfile
import threading
import wave
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents._llm import ollama_call_json

SAMPLE_RATE = 16_000
CHANNELS = 1

_INTENT_SYSTEM = """You are a financial investment assistant. Extract structured intent from a voice note.
Return ONLY valid JSON. No explanation, no markdown.

Schema:
{
  "intent": "<one of: thesis_update | conviction_change | trigger_add | risk_flag | general_note>",
  "ticker": "<TICKER symbol in uppercase, or null>",
  "conviction_from": <integer 1-10 or null>,
  "conviction_to": <integer 1-10 or null>,
  "trigger_direction": "<BUY or SELL or null>",
  "trigger_price": <float or null>,
  "trigger_currency": "<BRL or USD or null>",
  "risk_level": "<yellow or red or null>",
  "summary": "<one concise sentence summarising the note>",
  "text": "<cleaned version of the transcription>"
}"""


def record_until_enter(max_seconds: int = 60) -> bytes | None:
    """Record from default microphone until Enter is pressed (or timeout).

    Returns raw int16 PCM bytes, or None if sounddevice unavailable.
    """
    try:
        import numpy as np
        import sounddevice as sd
    except ImportError:
        print("❌ sounddevice/numpy not found. Run: pip install sounddevice numpy")
        return None

    frames: list = []
    stop_event = threading.Event()

    def _wait_for_enter():
        input()
        stop_event.set()

    t = threading.Thread(target=_wait_for_enter, daemon=True)
    t.start()

    print("🎤 Recording... Press Enter to stop.")
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16") as stream:
            elapsed = 0.0
            chunk = SAMPLE_RATE // 4  # 250ms chunks
            while not stop_event.is_set() and elapsed < max_seconds:
                data, _ = stream.read(chunk)
                frames.append(data.copy())
                elapsed += chunk / SAMPLE_RATE
    except Exception as e:
        print(f"❌ Recording error: {e}")
        return None

    if not frames:
        return None

    import numpy as np
    return np.concatenate(frames, axis=0).tobytes()


def _write_wav(pcm: bytes, path: str) -> None:
    with wave.open(path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm)


def transcribe(audio_path: str) -> str:
    """Transcribe WAV file. Prefers faster-whisper (GPU), falls back to whisper."""
    # faster-whisper: GPU-accelerated via ctranslate2 (preferred on RTX 5090)
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("base", device="auto", compute_type="auto")
        segments, info = model.transcribe(audio_path, beam_size=5)
        text = " ".join(s.text.strip() for s in segments).strip()
        if text:
            print(f"   [faster-whisper, lang={info.language}, {info.duration:.1f}s]")
        return text
    except ImportError:
        pass
    except Exception as e:
        print(f"   [faster-whisper error: {e}]")

    # openai-whisper fallback
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result.get("text", "").strip()
    except ImportError:
        pass

    print("❌ No whisper package. Run: pip install faster-whisper")
    return ""


def parse_intent(text: str, ticker: str | None = None) -> dict[str, Any]:
    """Parse transcribed text into structured intent via Qwen (local)."""
    ctx = f"Ticker context: {ticker}\n\n" if ticker else ""
    result = ollama_call_json(
        f"{ctx}Voice note:\n{text}",
        system=_INTENT_SYSTEM,
        max_tokens=400,
        temperature=0.1,
    )
    if not isinstance(result, dict):
        return {"intent": "general_note", "ticker": ticker, "summary": text[:120], "text": text}
    # inject ticker hint if LLM missed it
    if ticker and not result.get("ticker"):
        result["ticker"] = ticker
    return result


def record_and_transcribe(ticker: str | None = None) -> tuple[str, dict[str, Any]]:
    """End-to-end: record → WAV → transcribe → parse intent.

    Returns (raw_text, intent_dict). Both empty on failure.
    """
    pcm = record_until_enter()
    if not pcm:
        return "", {}

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp_path = f.name
    _write_wav(pcm, tmp_path)

    try:
        print("⏳ Transcribing...")
        text = transcribe(tmp_path)
    finally:
        os.unlink(tmp_path)

    if not text:
        print("⚠️  Transcription empty — check microphone or speak more clearly.")
        return "", {}

    print(f"📝 Transcribed: {text}")
    print("⏳ Parsing intent (Qwen)...")
    intent = parse_intent(text, ticker=ticker)
    return text, intent
