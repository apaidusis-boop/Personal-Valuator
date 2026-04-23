"""YouTube ingestion pipeline (Phase Q).

Router → Extractor → Evidência. Zero tokens Claude: Whisper+Ollama locais.
Áudio e transcripts nunca são escritos em disco. Só factos estruturados
com `evidence_quote` validada entram na BD.
"""
