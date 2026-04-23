"""vault_ask — busca semântica sobre obsidian_vault/ via LLM local.

Pipeline:
  1. Index vault (embed cada .md via nomic-embed-text) — cached em memory/
  2. Query → embed → cosine top-K docs
  3. Send top-K chunks + query para Qwen 14B → resposta ~200 tokens
  4. Imprime resposta + cita os docs usados

Zero tokens Claude. Usa Ollama localhost.

Uso:
    python scripts/vault_ask.py "tickers com tese de turnaround ou transição AI"
    python scripts/vault_ask.py "que holdings estão em deterioração Piotroski?"
    python scripts/vault_ask.py "quais notas mencionam dividend cut?" --k 10
    python scripts/vault_ask.py --reindex              # força re-index
    python scripts/vault_ask.py --status               # status do index
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

VAULT = ROOT / "obsidian_vault"


def _memory_dir() -> Path:
    home = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or "")
    slug = "C--Users-paidu-investment-intelligence"
    c = home / ".claude" / "projects" / slug / "memory"
    if c.exists():
        return c
    (ROOT / "memory").mkdir(exist_ok=True)
    return ROOT / "memory"


INDEX_PATH = _memory_dir() / "vault_index.json"

EMBED_MODEL = "nomic-embed-text"
ANSWER_MODEL = "qwen2.5:14b-instruct-q4_K_M"  # 14B suficiente para síntese


def _hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8", errors="replace")).hexdigest()


def _list_vault_docs() -> list[Path]:
    if not VAULT.exists():
        return []
    # exclude hidden + archive
    return [p for p in VAULT.rglob("*.md") if "/.obsidian/" not in str(p) and "/_archive/" not in str(p)]


def _embed_one(text: str) -> list[float]:
    import requests
    # Try new API first, then legacy
    for endpoint, payload in (
        ("http://localhost:11434/api/embed",
         {"model": EMBED_MODEL, "input": text[:8000]}),
        ("http://localhost:11434/api/embeddings",
         {"model": EMBED_MODEL, "prompt": text[:8000]}),
    ):
        try:
            r = requests.post(endpoint, json=payload, timeout=60)
            if r.status_code == 404:
                continue
            r.raise_for_status()
            data = r.json()
            if "embeddings" in data:
                return data["embeddings"][0]
            if "embedding" in data:
                return data["embedding"]
        except requests.HTTPError:
            continue
    raise RuntimeError("Ollama embeddings endpoint não disponível")


def _cosine(a: list[float], b: list[float]) -> float:
    sa = sum(x * x for x in a) ** 0.5
    sb = sum(x * x for x in b) ** 0.5
    if sa == 0 or sb == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (sa * sb)


def _load_index() -> dict:
    if INDEX_PATH.exists():
        try:
            return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"model": EMBED_MODEL, "docs": {}}


def _save_index(idx: dict) -> None:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")


def index_vault(force: bool = False, verbose: bool = True) -> dict:
    """Embed docs que mudaram ou não estão no index. Devolve stats."""
    idx = _load_index()
    if idx.get("model") != EMBED_MODEL:
        # model change → reindex all
        force = True
        idx = {"model": EMBED_MODEL, "docs": {}}

    docs = _list_vault_docs()
    embedded = 0
    skipped = 0
    errors = 0
    for p in docs:
        rel = str(p.relative_to(VAULT)).replace("\\", "/")
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            errors += 1
            continue
        h = _hash(text)
        entry = idx["docs"].get(rel)
        if entry and entry.get("hash") == h and not force:
            skipped += 1
            continue
        try:
            emb = _embed_one(text)
        except Exception as e:  # noqa: BLE001
            if verbose:
                print(f"  embed fail {rel}: {e}")
            errors += 1
            continue
        idx["docs"][rel] = {
            "hash": h,
            "embedding": emb,
            "chars": len(text),
        }
        embedded += 1
        if verbose and embedded % 25 == 0:
            print(f"  embedded {embedded}...")

    _save_index(idx)
    if verbose:
        print(f"index done: {embedded} embedded, {skipped} unchanged, {errors} errors, total {len(idx['docs'])} docs")
    return {"embedded": embedded, "skipped": skipped, "errors": errors, "total": len(idx["docs"])}


def _retrieve(query: str, k: int) -> list[tuple[str, float, str]]:
    """[(rel_path, score, doc_text_truncated)] top-K."""
    idx = _load_index()
    if not idx["docs"]:
        return []
    q_emb = _embed_one(query)
    scored = []
    for rel, entry in idx["docs"].items():
        emb = entry.get("embedding")
        if not emb:
            continue
        scored.append((rel, _cosine(q_emb, emb)))
    scored.sort(key=lambda x: -x[1])
    top = scored[:k]
    out = []
    for rel, score in top:
        p = VAULT / rel
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            continue
        # trunca para não estourar contexto LLM
        out.append((rel, score, text[:2500]))
    return out


SYSTEM_PROMPT = """És um assistente que responde perguntas sobre um vault de
investimentos (Obsidian) em português. Recebes a pergunta e os excertos mais
relevantes do vault. Responde de forma concisa (máximo ~180 palavras),
citando **ticker** ou **ficheiro** sempre que extraíres um facto.

Regras:
1. Responde APENAS com base nos excertos — não inventes dados.
2. Se os excertos não têm a resposta, diz 'não encontrei nos documentos'.
3. Formato: bullets curtos com ticker/file em negrito.
4. Não paráfrases muito — mantém os números exactos dos excertos.
"""


def _answer(query: str, hits: list[tuple[str, float, str]]) -> str:
    import requests
    if not hits:
        return "(vault vazio ou index não inicializado)"
    context = "\n\n---\n\n".join(f"[{rel} | score={score:.2f}]\n{text}" for rel, score, text in hits)
    user = f"PERGUNTA: {query}\n\nEXCERTOS:\n{context}"
    r = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": ANSWER_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user},
            ],
            "options": {"temperature": 0.2, "num_ctx": 16384},
            "stream": False,
        },
        timeout=300,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]


def ask(query: str, k: int = 6, show_sources: bool = True) -> None:
    hits = _retrieve(query, k)
    ans = _answer(query, hits)
    print(ans)
    if show_sources and hits:
        print("\n---")
        print("Fontes consultadas:")
        for rel, score, _ in hits:
            print(f"  {score:.3f}  {rel}")


def status() -> None:
    idx = _load_index()
    n = len(idx.get("docs", {}))
    print(f"Index model: {idx.get('model','?')}")
    print(f"Documents indexed: {n}")
    if INDEX_PATH.exists():
        print(f"Index file: {INDEX_PATH} ({INDEX_PATH.stat().st_size/1024:.1f} KB)")
    vault_docs = _list_vault_docs()
    print(f"Vault .md files: {len(vault_docs)}")
    missing = [p for p in vault_docs if str(p.relative_to(VAULT)).replace("\\", "/") not in idx.get("docs", {})]
    print(f"Missing from index: {len(missing)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query", nargs="?", help="Pergunta (free-form PT)")
    ap.add_argument("--k", type=int, default=6, help="Top-K docs a recuperar")
    ap.add_argument("--reindex", action="store_true", help="Força re-embed de tudo")
    ap.add_argument("--status", action="store_true", help="Status do index")
    ap.add_argument("--no-sources", action="store_true")
    args = ap.parse_args()

    if args.status:
        status()
        return 0
    if args.reindex:
        print("Re-indexing vault (força)...")
        index_vault(force=True)
        return 0

    if not args.query:
        ap.print_help()
        return 1

    # Ensure index is up to date (incremental)
    idx = _load_index()
    if len(idx.get("docs", {})) == 0:
        print("Index vazio — a construir (demora ~1-2min p/ 200 docs)...")
        index_vault(force=False)
    else:
        # incremental: só docs novos/alterados
        vault_docs = _list_vault_docs()
        known = set(idx["docs"].keys())
        current = {str(p.relative_to(VAULT)).replace("\\", "/") for p in vault_docs}
        new_or_gone = (current - known) | (known - current)
        # We don't check for content-change here to keep ask() fast; reindex for that.
        if new_or_gone:
            print(f"Vault mudou ({len(new_or_gone)} ficheiros) — incremental update...")
            index_vault(force=False, verbose=False)

    ask(args.query, k=args.k, show_sources=not args.no_sources)
    return 0


if __name__ == "__main__":
    sys.exit(main())
