---
type: constitution
scope: personal
parent: "[[CONSTITUTION]]"
created: 2026-05-11
---

# 📜 Constituição — Mundo Pessoal

> **Herda tudo de [[CONSTITUTION]]** (núcleo partilhado: os 7 não-negociáveis + os 10 hábitos de [[Bibliotheca/Disciplina_de_Investidor]]). Aqui ficam **só** as regras que existem por isto ser a *minha carteira* — não um produto. Mesma filosofia do [[CONSTITUTION_Comercial|Mundo Comercial]]; governança diferente.

## Identidade
Este mundo = **o meu dinheiro real**. Investidor pessoa física, BR (B3) + US (NYSE/NASDAQ). Estratégia core: DRIP + Buffett/Graham, horizonte de anos. Sem clientes, sem SLA, sem obrigações para com terceiros. As decisões são minhas e tomadas com clareza visual (Obsidian / dashboards / HTML), não em CLI.

## Não-negociáveis do Mundo Pessoal

1. **A carteira real é sagrada** — `portfolio_positions` reflecte posições reais; nunca pedir quantidades ao user, consultar a DB. Não simular trades como se fossem reais. Não tocar em `data/` de forma destrutiva.

2. **Blacklist viva** (estende o nº6 do núcleo):
   - **TEN** — 4 sinais cycle peak Abr/2026 → NUNCA adicionar.
   - **GREK** — dividendos semianuais voláteis → reclassificado tactical; NÃO aplicar lógica DRIP / não reforçar por DRIP.
   - **RBRX11** — substituído por **KNHF11** no full swap de 2026-05-08 (Pátria-RBR) → não re-sugerir RBRX11.
   - **PVBI11** — Tier C mas tese contrarian deliberada (prédio FL vazio) → NÃO sugerir venda.
   - Fonte canónica: as memórias `ten_distress_signal.md`, `grek_irregular_dividends.md`, `rbrx11_patria_acquisition.md`, `pvbi11_turnaround_thesis.md` + esta lista.

3. **Intenção por posição** — DRIP vs Growth vs Compounder difere por ticker (XP = growth, BN = post-split 2023, …); não aplicar lógica DRIP a growth picks. Ver `user_investment_intents.md`.

4. **Superfícies: CLI = sala do chefe; Obsidian / dashboards / reports HTML = Escritório** — output bruto e sem cerimónia na CLI; output polido (o Design System, handle `design.lint`) no Escritório. Eu leio e decido no Escritório. (No Mundo Comercial o "Escritório" é o que o cliente vê — e ganha um *tier relatório* a mais.)

5. **Trabalho autónomo autorizado** — overnight / workday / midnight: enrichment + cleanup + tarefas idempotentes OK. Proibido: writes destrutivos em `data/`, force-push, Tavily acima de quota. Sempre smoke-test 1-ticker + `nvidia-smi` antes de detachar (pós-incidente 2026-05-09).

6. **Output = verdade comprimida** — meia página + 1 gráfico se for isso que basta. Volume não é rigor. Não escrever relatório de iniciação para responder "compro/mantenho/vendo X?". (Esta regra **inverte-se** no Mundo Comercial — lá o relatório longo é um tier de entrega que o cliente quer.)

7. **Direcção, não micro-aprovação** — "Avança com X" = acção total: escrita em `data/` / vault OK, resultados no Escritório para eu ler depois. Anti-padrão proibido: "carece da tua aprovação" para cada passo. Delegar a sub-agentes quando faz sentido.

## O que este mundo NÃO faz
- Não tem utilizadores além de mim — logo, sem auth, sem multi-tenant, sem billing, sem tiers de pricing.
- Não tem disclaimers "not financial advice" (sou eu a aconselhar-me a mim).
- Não optimiza para impressionar — optimiza para eu decidir bem e rápido.
- Não constrói infra comercial "por via das dúvidas" — isso vive no [[CONSTITUTION_Comercial|outro mundo]] e só avança com decisão explícita.

## Cross-links
- Núcleo partilhado: [[CONSTITUTION]] · disciplina: [[Bibliotheca/Disciplina_de_Investidor]]
- Mundo Comercial: [[CONSTITUTION_Comercial]] · [[Comercial/_Index]]
- Roadmap da separação: [[Comercial/00_Roadmap]] · master roadmap: [[ROADMAP]]
- Contrato do projecto (código): `CLAUDE.md` na raiz do repo
