"""Scrapers de narrativa.

Cada scraper é independente, idempotente, e devolve uma lista de dicts no
formato `RawItem` (ver classifier.py). O scraper NÃO classifica — só captura
o conteúdo bruto e escreve em `narrative_items` com classified_at = NULL.

Ordem de prioridade:
    1. rss      — estruturado, baixo custo, alta cobertura (InfoMoney, Valor,
                  Reuters, Bloomberg, WSJ, Seeking Alpha)
    2. youtube  — alto sinal mas alto custo (transcript via yt-dlp + LLM)
    3. transcripts — earnings calls (Bamsec/Seeking Alpha) — futuro
"""
