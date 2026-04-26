---
layer: 2
authority: scripts
regenerable: true
exceptions: ["*_DOSSIE.md", "*_NOTES.md"]
---

# Layer 2 — Projecção (auto-gerada)

Notas por ticker geradas a partir do SQLite (`fundamentals`, `prices`, `scores`, `quarterly_history`).

**Não editar manualmente os ficheiros base** (`X.md`, `X_RI.md`).

**Excepções (L3, sagrados):**
- `*_DOSSIE.md` — research aprofundada manual
- `*_NOTES.md` — observações soltas humanas (criar à mão)

Geradores:
- `scripts/obsidian_bridge.py`
- `agents/holding_wiki_synthesizer.py`
- `library/ri/cvm_parser*.py`
