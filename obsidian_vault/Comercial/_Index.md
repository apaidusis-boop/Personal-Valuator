---
type: index
scope: commercial
created: 2026-05-11
---

# 🏢 Mundo Comercial — Index

> Workspace do **Mundo Comercial** do projecto (ver [[CONSTITUTION_Comercial]]). Mesma filosofia do [[CONSTITUTION_Pessoal|Mundo Pessoal]] — governança separada. **Estado: blueprint** — nada construído ainda. O resto do vault (tickers/, wiki/, dossiers/, briefings/, …) é, por default, o Mundo Pessoal; só esta pasta é o mundo comercial explícito.

## Documentos (existem)
- [[CONSTITUTION_Comercial]] — a constituição deste mundo (herda [[CONSTITUTION]])
- [[Comercial/00_Roadmap|00 — Roadmap: Dois Mundos + build-out comercial]] (blocos B1…B6)
- [[Comercial/Competitive_Landscape]] — TipRanks/Finviz/SimplyWallSt/SeekingAlpha/Suno/XP/Fool: o gap é *disciplina*, não *dados* *(B3 — 2026-05-11)*
- [[Comercial/Pricing]] — dois baldes de custo (SQL/Ollama ≈ 0 vs Claude API > 0) → tiers Free/Plus/Pro; in-house-first = motor de margem *(B3 — 2026-05-11)*
- [[Comercial/Compliance]] — postura "ferramenta educacional, não conselheiro": disclaimers, sem execução, sem promessas; BR (CVM) + US (publisher's exemption); licenciamento de dados; LGPD/GDPR *(B3 — 2026-05-11)*
- [[Comercial/GTM]] — ICP (investidor PF disciplinado de longo prazo), posicionamento ("o teu Constitution pessoal"), canais (content-led primeiro), sequência de launch *(B3 — 2026-05-11)*
- [[Comercial/Personal_Investment_OS_Blueprint|Investment OS Blueprint]] — MVP, telas, IA em camadas (SQL → RAG → Claude), stack, modelo SaaS *(movido de `Bibliotheca/` em 2026-05-11)*
- [[Bibliotheca/Disciplina_de_Investidor]] — os 10 hábitos de investidor + secção "Eficiência & comercialização" *(vive na Bibliotheca por ser partilhado entre os dois mundos)*

## Specs (existem)
- [[Comercial/Product_Specs/report_tier.spec|report_tier.spec]] — tier "relatório" institucional (initiating-coverage ~8-12p / earnings-update ~6-8p) gerado a partir do output denso do núcleo, *sem nova análise*; motor recomendado HTML→PDF reusando `design.lint`. **Spec pronta; build bloqueado** por 3 picks de disciplina (freshness gate, earnings-update template, thesis scorecard) + validação dos verdicts (~Ago/2026). *(B4 — 2026-05-11)*

## Reference material (a recolher — ver [[Comercial/References]] quando existir)
- Exemplos reais de relatórios sell-side / casas de research (JPM/GS/MS · Suno/XP/BTG) para calibrar o formato do report tier — initiating coverage + earnings update. Guardar PDFs em `docs/references/` (mesma pasta dos relatórios Suno/XP já lá) + nota índice no vault.

## A criar (próximo — bloco B4 *build* em [[Comercial/00_Roadmap]])
- protótipo de relatório gerado a partir de uma holding real (entregável de *build* do B4, não da spec).
- `Product_Specs/` continua a ser a pasta para specs por feature (reusa o padrão de `obsidian_vault/specs/`).

## Como navegar
- Decisão da minha carteira → [[CONSTITUTION_Pessoal]].
- O que um cliente vê / recebe / paga → [[CONSTITUTION_Comercial]] + esta pasta.
- O que afecta os dois (ex: novo engine de scoring) → [[CONSTITUTION]] (núcleo) + mencionado nas duas filhas.
