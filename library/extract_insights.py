"""Extract structured insights from book chunks via Ollama (in-house, zero Claude tokens).

Strategy:
  1. Load chunks from library/chunks/<book>/
  2. Sample representative chunks (stride-based: skip intro/acknowledgements)
  3. For each chunk: ask Qwen to extract:
     - methodology mentions (formulas, frameworks, rules)
     - actionable heuristics
     - tickers / asset classes / regime conditions referenced
     - one concise takeaway
  4. Aggregate per-book into library/insights/<book_slug>.json
  5. Generate proposal YAML methods in library/methods/drafts/ for review

Output is STRUCTURED so library/matcher.py can potentially use it later.

Uso:
    python library/extract_insights.py --book <slug>             # 1 livro
    python library/extract_insights.py --book <slug> --max 30    # cap chunks
    python library/extract_insights.py --all                     # tudo (slow)
    python library/extract_insights.py --list                    # list books
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHUNKS_DIR = ROOT / "library" / "chunks"
INSIGHTS_DIR = ROOT / "library" / "insights"
DRAFTS_DIR = ROOT / "library" / "methods" / "drafts"

# Qwen 14B é rápido e suficiente para extraction structured.
# Qwen 32B se qualidade precisar (mais lento, mais memory).
OLLAMA_MODEL = "qwen2.5:14b-instruct-q4_K_M"


EXTRACT_PROMPT = """You are an expert investment analyst reading a book chunk.
Extract from the chunk, strictly as JSON (NO markdown wrapper):

{
  "has_substance": true|false,
  "is_filler": true|false,
  "methods": [
    {"name": "string", "description": "1-2 sentence", "rules_or_formula": "string"}
  ],
  "heuristics": ["actionable rule of thumb 1", "..."],
  "key_concepts": ["concept 1", "concept 2"],
  "tickers_or_assets": ["TICKER/asset class mentions"],
  "regime_conditions": ["any macro regime mentioned"],
  "one_line_takeaway": "the single most important sentence to remember"
}

Rules:
- If chunk is intro, acknowledgements, table-of-contents, or bibliography: "is_filler": true, and return empty arrays.
- "methods": ONLY concrete investment methodologies with rules/formulas. Not vague advice.
- Stay faithful to the text; do not invent tickers not present.
- Reply JSON ONLY, no prose before/after.

CHUNK:
\"\"\"
{chunk}
\"\"\""""


def call_ollama(chunk: str, timeout: int = 120) -> dict | None:
    prompt = EXTRACT_PROMPT.replace("{chunk}", chunk[:6000])
    from agents._llm import ollama_call
    raw = ollama_call(
        prompt,
        model=OLLAMA_MODEL,
        max_tokens=800,
        temperature=0.2,
        timeout=timeout,
    )
    if raw.startswith("[LLM FAILED"):
        return {"_error": raw}
    # Try to find first {...} block
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        # Best-effort repair of common issues
        text = m.group(0)
        text = re.sub(r",\s*}", "}", text)
        text = re.sub(r",\s*]", "]", text)
        try:
            return json.loads(text)
        except Exception:
            return None


def sample_chunks(book_slug: str, max_chunks: int = 50, stride: int | None = None) -> list[Path]:
    """Sample chunks with a stride to cover the whole book without reading all chunks.

    stride=None → compute automatically so max_chunks is hit.
    Skip first 3 and last 2 chunks (intro/bibliography).
    """
    book_dir = CHUNKS_DIR / book_slug
    if not book_dir.exists():
        return []
    all_files = sorted(book_dir.glob("*.txt"))
    if len(all_files) <= 5:
        return all_files

    # trim ends
    usable = all_files[3:-2] if len(all_files) > 10 else all_files

    if stride is None:
        stride = max(1, len(usable) // max_chunks)
    sampled = usable[::stride][:max_chunks]
    return sampled


def extract_book(book_slug: str, max_chunks: int = 40, model: str = OLLAMA_MODEL) -> dict:
    global OLLAMA_MODEL
    OLLAMA_MODEL = model

    chunks_paths = sample_chunks(book_slug, max_chunks=max_chunks)
    if not chunks_paths:
        return {"error": f"no chunks for {book_slug}"}

    INSIGHTS_DIR.mkdir(exist_ok=True, parents=True)
    DRAFTS_DIR.mkdir(exist_ok=True, parents=True)

    print(f"[extract] book={book_slug}  chunks_sampled={len(chunks_paths)}  model={OLLAMA_MODEL}")
    results = []
    t0 = time.time()
    for i, cp in enumerate(chunks_paths, 1):
        chunk_text = cp.read_text(encoding="utf-8", errors="ignore")
        res = call_ollama(chunk_text)
        if res is None:
            res = {"_error": "no_json_parsed"}
        res["_chunk_file"] = cp.name
        results.append(res)
        elapsed = time.time() - t0
        avg = elapsed / i
        eta = (len(chunks_paths) - i) * avg
        if i % 5 == 0 or i == len(chunks_paths):
            methods_so_far = sum(len(r.get("methods") or []) for r in results if "_error" not in r)
            print(f"  [{i:>3}/{len(chunks_paths)}]  methods_so_far={methods_so_far}  avg={avg:.1f}s  eta={eta/60:.1f}min")

    # Aggregate
    aggregate = {
        "book": book_slug,
        "chunks_sampled": len(chunks_paths),
        "model_used": OLLAMA_MODEL,
        "methods_all": [],
        "heuristics_all": [],
        "key_concepts": set(),
        "tickers_assets": set(),
        "regime_conditions": set(),
        "takeaways": [],
        "errors": 0,
    }

    for r in results:
        if "_error" in r:
            aggregate["errors"] += 1
            continue
        if r.get("is_filler") or not r.get("has_substance"):
            continue
        for m in (r.get("methods") or []):
            if isinstance(m, dict) and m.get("name"):
                aggregate["methods_all"].append(m)
        aggregate["heuristics_all"].extend(r.get("heuristics") or [])
        aggregate["key_concepts"].update(r.get("key_concepts") or [])
        aggregate["tickers_assets"].update(r.get("tickers_or_assets") or [])
        aggregate["regime_conditions"].update(r.get("regime_conditions") or [])
        if r.get("one_line_takeaway"):
            aggregate["takeaways"].append(r["one_line_takeaway"])

    # Serialize sets
    for k in ("key_concepts", "tickers_assets", "regime_conditions"):
        aggregate[k] = sorted(aggregate[k])

    # Dedup methods by name
    seen = set()
    uniq = []
    for m in aggregate["methods_all"]:
        key = m["name"].lower()[:60]
        if key not in seen:
            seen.add(key)
            uniq.append(m)
    aggregate["methods_unique"] = uniq
    aggregate["methods_count"] = len(uniq)

    out = INSIGHTS_DIR / f"{book_slug}.json"
    out.write_text(json.dumps(aggregate, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"[extract] saved: {out.relative_to(ROOT)}")
    print(f"  methods_unique={len(uniq)}  heuristics={len(aggregate['heuristics_all'])}  concepts={len(aggregate['key_concepts'])}  errors={aggregate['errors']}")

    return aggregate


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", help="slug to process")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--max", type=int, default=40)
    ap.add_argument("--model", default=OLLAMA_MODEL)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list or (not args.book and not args.all):
        print("Available books:")
        for d in sorted(CHUNKS_DIR.iterdir()):
            if d.is_dir():
                meta = d / "meta.json"
                if meta.exists():
                    m = json.loads(meta.read_text(encoding="utf-8"))
                    print(f"  {d.name:<50}  chunks={m['chunks_count']}")
        return

    books = []
    if args.all:
        books = [d.name for d in sorted(CHUNKS_DIR.iterdir()) if d.is_dir()]
    else:
        books = [args.book]

    for b in books:
        extract_book(b, max_chunks=args.max, model=args.model)
        print()


if __name__ == "__main__":
    main()
