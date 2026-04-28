"""PDF → structured insights via Ollama Qwen 14B local.

Reutiliza pattern do `yt_reextract`: Ollama HTTP API em localhost:11434.
Zero tokens Claude. Usa canonical `agents._llm.ollama_call` (CH005-compliant).

Uso:
    from fetchers.subscriptions._pdf_extract import extract_pdf_text, extract_insights

    text = extract_pdf_text(Path("report.pdf"))
    insights = extract_insights(text, ticker_universe=["ITUB4", "VALE3"])
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from agents._llm import ollama_call

OLLAMA_MODEL = "qwen2.5:14b-instruct-q4_K_M"


def extract_pdf_text(pdf_path: Path, max_chars: int = 50_000) -> str:
    """Extrai texto plano de PDF. Usa pypdf (dep leve).

    Cap a 50k chars para caber na context window do Qwen 14B (~32k tokens).
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        raise RuntimeError(
            "pypdf não instalado. `pip install pypdf` (ou via requirements.txt)."
        )
    reader = PdfReader(str(pdf_path))
    chunks = []
    total = 0
    for page in reader.pages:
        t = page.extract_text() or ""
        chunks.append(t)
        total += len(t)
        if total >= max_chars:
            break
    return "\n\n".join(chunks)[:max_chars]


SYSTEM_PROMPT = """És um assistente analítico que extrai insights estruturados de relatórios de analistas financeiros (em PT ou EN).

Para cada relatório, identifica:
1. Tickers mencionados (B3 .SA ou NYSE/NASDAQ).
2. Para cada ticker ou tema: extrai claims em formato estruturado.

Devolve JSON válido com o schema:
{
  "summary": "2-3 frases em PT resumindo tese principal",
  "language": "pt" | "en",
  "tags": ["sector:banks", "br-equity", ...],
  "insights": [
    {
      "ticker": "ITUB4" | null,
      "kind": "thesis" | "catalyst" | "risk" | "numerical" | "rating" | "price_target" | "sector_view",
      "claim": "texto breve do claim",
      "stance": "bull" | "bear" | "neutral" | null,
      "price_target": 35.50 | null,
      "confidence": 0.0-1.0,
      "evidence_quote": "trecho curto do relatório"
    }
  ]
}

Regras:
- Max 10 insights. Prioriza alto impacto.
- `ticker: null` se insight é sectorial/macro sem ticker específico.
- `confidence` reflete quão explícito o claim está no texto.
- Cuidado com claims de corretora promocional ("compre agora!") — mark confidence baixa.
- Nunca inventar números. Se não está no texto, omitir.

Output APENAS JSON, sem markdown fences."""


def extract_insights(
    text: str,
    ticker_universe: list[str] | None = None,
    model: str = OLLAMA_MODEL,
) -> dict:
    """Chama Ollama para extrair insights estruturados.

    Devolve dict com schema acima. Em erro, devolve {"error": "...", "raw": "..."}
    """
    universe_hint = ""
    if ticker_universe:
        sample = ", ".join(ticker_universe[:50])
        universe_hint = f"\n\nUniverso de tickers do user (prioriza matches): {sample}"
    prompt = f"{SYSTEM_PROMPT}{universe_hint}\n\n---RELATÓRIO---\n{text}\n---FIM---"
    raw = ollama_call(
        prompt,
        model=model,
        temperature=0.2,
        json_mode=True,
        timeout=600,
        extra_options={"num_ctx": 16384},
    )
    if raw.startswith("[LLM FAILED"):
        return {"error": raw}
    # format=json garante JSON válido mas não perfeito; tenta parse
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # tentar extrair JSON do meio do texto
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
        return {"error": "json parse failed", "raw": raw[:500]}


def extract_html_text(html: str, max_chars: int = 50_000) -> str:
    """Parse HTML → texto plano. Prefere BeautifulSoup se disponível."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        # fallback cru
        text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:max_chars]
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style", "nav", "footer", "aside"]):
        s.decompose()
    # prefer <article> se existir
    article = soup.find("article") or soup.find("main") or soup.body
    text = article.get_text(separator="\n", strip=True) if article else ""
    return text[:max_chars]
