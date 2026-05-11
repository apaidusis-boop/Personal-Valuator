---
type: roadmap
scope: commercial
created: 2026-05-11
status: active
---

# 🗺️ Roadmap — Dois Mundos (Pessoal & Comercial)

> Origem: user 2026-05-11 — *"duas Constitutions (Pessoal & Comercial), equal but separate; separar os dois mundos dentro do Obsidian; vê como seria melhor implementado"*. Cobre (a) a separação estrutural e (b) o build-out do Mundo Comercial.
> **Não é uma "Phase X"** (letras em conflito no projecto) — são blocos B1…Bn. Master roadmap: [[ROADMAP]]. Constituições: [[CONSTITUTION]] (núcleo) · [[CONSTITUTION_Pessoal]] · [[CONSTITUTION_Comercial]].

## Princípios da separação
1. **A filosofia é a mesma; a governança separa.** Buffett/Graham, DRIP, in-house first, honestidade, os 10 hábitos ([[Bibliotheca/Disciplina_de_Investidor]]) — idênticos nos dois mundos. O que muda: obrigações para com terceiros, licenciamento de dados, custo marginal por request, multi-user, e o que NUNCA pode ser shipado a um cliente.
2. **Código é partilhado.** Um engine novo (scoring, fetcher, agent) entra no repo normal. Só *docs + regras + (futuro) tenancy* se bifurcam. **Não duplicar lógica de código por causa disto.**
3. **Simplicity first / Think before coding.** Não construir infra comercial enquanto não houver decisão de a construir. O `blueprint` é planeamento, não implementação.

## Blocos

### ✅ B1 — Constitution split *(feito 2026-05-11)*
- `CONSTITUTION.md` → núcleo partilhado + nova secção "🌍 Dois Mundos" + Decision Log entry.
- `CONSTITUTION_Pessoal.md` criado (carteira real sagrada, blacklist viva, superfícies CLI/Escritório, midnight work, output = verdade comprimida, não micro-aprovar).
- `CONSTITUTION_Comercial.md` criado (`status: blueprint`; not financial advice, in-house-first vira modelo de negócio, "teatro" = tier de entrega, disciplina embutida = moat, paper-trade gate = feature de confiança, never ship auto-trading).
- **Done quando**: as três páginas existem e linkam-se mutuamente; memória actualizada. ✓

### ✅ B2 — `Comercial/` scaffold *(feito 2026-05-11)*
- Pasta `obsidian_vault/Comercial/` + `_Index.md` + este `00_Roadmap.md`.
- `Personal_Investment_OS_Blueprint.md` movido `Bibliotheca/` → `Comercial/` via `git mv` (wikilinks resolvem por basename → sobrevivem).
- **Done quando**: pasta existe, `_Index` linka tudo, blueprint acessível pelo novo caminho. ✓

### ✅ B3 — Preencher o Mundo Comercial (docs) *(feito 2026-05-11)*
- [[Comercial/Competitive_Landscape]] — o gap é *disciplina*, não *dados*; wedge + vantagens injustas + ameaças.
- [[Comercial/Pricing]] — dois baldes de custo (SQL/Ollama ≈ 0 vs Claude API > 0) → Free/Plus/Pro; in-house-first = motor de margem; âncoras de mercado.
- [[Comercial/Compliance]] — postura "ferramenta educacional, não conselheiro": disclaimers, sem execução, sem promessas de retorno; BR (CVM, evitar "recomendação") + US (publisher's exemption); licenciamento de dados; LGPD/GDPR. ⚠️ "advogado antes do B6".
- [[Comercial/GTM]] — ICP (investidor PF disciplinado, longo prazo, BR+US); posicionamento "o teu Constitution pessoal de investidor"; canais (content-led → comunidade → boca-a-boca); sequência de launch; métricas (ativação/retenção/o "aha").
- **Done quando**: os 4 docs têm conteúdo real, linkados no `_Index`. ✓
- **Effort gasto**: ~1 sessão de escrita. Zero código.

### B4 — Tier "relatório" (a feature que justifica o "teatro")
- ✅ **Spec** — [[Comercial/Product_Specs/report_tier.spec]] *(feito 2026-05-11)*: 2 tipos (initiating coverage ~8-12p · earnings update ~6-8p), de onde vem cada dado (tudo já existe — zero novo fetching), motor recomendado **HTML→PDF reusando `design.lint`**, anti-patterns, hooks de compliance/pricing, success metrics. Esqueleto: [[Bibliotheca/Disciplina_de_Investidor]] §7 + memória `anthropic_fsi_plugins.md`.
- ⏳ **Reference material** — recolher exemplos reais de relatórios (sell-side US + casas BR) para calibrar o formato; guardar em `docs/references/` + nota índice no vault.
- ⏳ **Build** — protótipo gerado a partir de uma holding real + finalizar toolchain PDF.
- **Bloqueado por** (o *build*, não a spec): 3 picks de disciplina de [[Bibliotheca/Disciplina_de_Investidor]] (freshness gate · earnings-update template · thesis scorecard) + validação dos verdicts (~Ago/2026; mesmo gate da Phase GG). Decisão "vale a pena já?" fica para essa altura.
- **Effort do build**: ~2-3d quando destravado.

### B5 — (opcional, decidir depois) Simetria total: pasta `Pessoal/`
- Hoje: raiz do vault = Mundo Pessoal *por default*; só `Comercial/` é explícito. Mover 184 ticker notes + wiki + dossiers + briefings + reconfigurar `obsidian_bridge.py` / `daily_run` tem custo **alto**; o valor é cosmético.
- Reabrir só se: (a) o Mundo Comercial crescer ao ponto de a assimetria confundir, ou (b) tooling precisar de namespacing duro.
- **Done quando**: decisão registada. **Default actual: não.**

### B6 — (futuro, só com "go" comercial) Infra multi-tenant
- SQLite → Postgres; auth; isolamento de tenant; rate-limit por plano; billing.
- **Pré-requisito duro**: decisão explícita de comercializar **+** ≥90d de verdicts validados (não vender um sistema que ainda não se provou — anti confirmation-bias retrofit, mesmo princípio da Phase GG).
- Não detalhar agora — "Think before coding".

## Relação com os 5 picks de disciplina
Os 5 picks de [[Bibliotheca/Disciplina_de_Investidor]] (freshness gate · model-sanity flags · thesis scorecard + falsificabilidade · template earnings-update · catalyst outcome archive) são **código partilhado** — servem o Mundo Pessoal como régua dos agentes e o Mundo Comercial como substância do produto. Implementá-los não depende deste roadmap; este roadmap depende deles (B4 reusa o template earnings-update).

## Manutenção
- Este doc actualiza-se quando um bloco entra/sai. Estado de blocos vive aqui; o master [[ROADMAP]] tem só uma linha-ponteiro.
- Quando houver conflito com o `CONSTITUTION.md`, **a Constituição ganha** (fonte de verdade temporal).
