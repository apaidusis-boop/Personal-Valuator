# Pilot Deep Dive — Leitura para ti (2026-05-10)

> Leitura curada do que aprendemos no pilot. Para a tabela auto-gen,
> ver [[_MASTER]]. Para os 5 dossiers individuais, ver `[[ITSA4]]`,
> `[[BBDC4]]`, `[[PRIO3]]`, `[[JPM]]`, `[[JNJ]]`.

## TLDR (3 minutos de leitura)

1. **Pipeline funciona em 100% dos 5 tickers do pilot**, com 4 layouts de RI
   distintos (BR/US, Mz Group / Bradesco próprio / JPM corporate / JNJ
   classic). Tempo médio: **~43s por ticker** com cache fresh.

2. **Descobrimos 45 filings novos cross-ticker** que não estavam na nossa
   DB (CVM/SEC monitor). 1 deles é **material** (PRIO3 mudança de Diretor
   de Operações, 5 maio).

3. **2 eventos calendário urgentes** detectados: ITSA4 divulga 1T26
   **AMANHÃ (11/05)**, FRE 29/05.

4. **Acesso desbloqueado a tudo o que era cego**: 22 audio/video sources
   (5 conference calls JPM transcribíveis), 341 PDFs de releases
   trimestrais históricos.

5. **Escala viável**: 23min/holdings (33), 71min/Tier-A (100),
   142min/universo (200) — tudo cabe em janelas overnight. Recomendação:
   **escalar para 33 holdings esta noite** se quiseres ver a tendência
   confirmada, depois universo.

---

## Por ticker — o que importa para a tese

### ITSA4 (Holding · Mz Group RI)

- **Descoberto novo**: 05/05 "Itaúsa integra novamente o ISE da B3"
  (governance positive, low impact)
- **Já em DB**: 14/04 ajuste contábil Aegea
- **CRÍTICO**: 11/05 (amanhã) divulga **Resultados 1T26**. RI tem o
  calendário oficial. Recomendo re-scrape automático no dia.
- **Apresentações**: Itaúsa Cast (podcast trimestral) ainda não
  consumido — markitdown lê audio.
- **Sinal de tese**: nenhuma surpresa material. Acompanhar 1T26.

### BBDC4 (Bank · Bradesco RI próprio, NÃO Mz Group)

- **Descoberto novo**: 27 entries no RI vs 15 na DB. Inclui:
  - **06/05 Bradesco 1T26 Press Release** (já saiu! DB ainda não tem)
  - 06/05 Resultados e Videoconferência 1T26
  - 25/03 Arquivamento Formulário 20-F 2025
  - 27/02 Reorganização Societária Bradsaúde / Odontoprev
- **CRÍTICO**: O **release 1T26 (06/05) já existe** mas a nossa DB tem
  só CVM filings genéricos. **Devemos puxar e analisar**.
- **Layout de tabela MD** complexo (provider Bradesco) — parser
  actualizado para suportar `DD-MM-YYYY` (Bradesco-style).
- **Sinal de tese**: 1T26 acabou de sair — verificar payout JCP +
  efficiency ratio + NPL. CONCRETIZAR esta semana.

### PRIO3 (Oil & Gas · Mz Group RI)

- **🚨 SINAL MATERIAL DETECTADO**: 05/05 **"Alteração na Diretoria
  de Operações"** — Francilmar Fernandes (Diretor de Ops) renunciou
  por motivos pessoais. Substituído por **Jean Carlos Calvi**
  (engenheiro interno, 10 anos PRIO, responsável por Polvo / Tubarão
  Martelo / Frade / Wahoo).
  - Interpretação: continuidade mantida (Calvi é veterano interno),
    mas mudança em executivo-chave de operações merece monitoring.
    Nada que mude tese hoje.
- **Outros novos**: 04/05 dados operacionais Abril (markitdown
  extraiu **tabelas de produção por cluster** que pdfplumber teria
  perdido), 13/01 aviso AGO.
- **Wahoo well status**: vários FRs sobre poços de Wahoo (1º/2º/3º
  poços) — não são novos vs DB mas confirmamos que RI é fonte
  primária mais rica em context.
- **Sinal de tese**: ROE 9.7% baixo, score 0.25 (não passa screen actual).
  **Posição actual em PROFIT** (entry 39.85 vs close 63.27 = **+58.8%**).
  Manter monitoring; se mudança de Diretor de Ops impactar próximas
  produções, reavaliar.

### JPM (US Bank · Multi-page IR)

- **12 press releases novos descobertos** (Bernstein conference 27/05,
  Annual Meeting 19/05, Preferred Dividends, Common Stock Dividend,
  1Q26 Earnings Call hosted, Conference Calls Q1+Q2+Q3+Q4).
- **312 PDFs históricos acessíveis** (5+ anos de earnings, supplements,
  transcripts, presentations, proxies).
- **16 conference call audios** disponíveis para transcrição via
  markitdown (1Q26, 4Q25, 3Q25, 2Q25, 1Q25).
- **CRÍTICO upcoming**: 19/05 Annual Meeting, 27/05 Bernstein
  Strategic Decisions Conference (potencial guidance update),
  14/07 (presumido 2Q26 earnings).
- **Sinal de tese**: ROE 16.5%, P/E 14.5 — passa Buffett screen mas
  nosso score 0.4 não passa. Re-screen necessário?

### JNJ (US Healthcare/Aristocrat · Single-page IR)

- **1 novo entry**: "Investor news" de 7/05 (link "Johnson & Johnson
  launches Generation Fine, a New Movement Encouraging Pa..." —
  marketing campaign, low signal)
- **Apresentações**: 10 disponíveis (10-Q forms, IR fact sheet 2025)
- **Audio/video**: 3 (provavelmente earnings call playbacks)
- **Sinal de tese**: pouco signal novo. JNJ é estável. Próximo
  earnings provavelmente Julho. Re-scrape próximo do release 2Q26.

---

## Comparação técnica: ANTES vs DEPOIS (multi-dimension)

| Dimensão | Ontem (CVM/SEC monitor only) | Hoje (Pipeline MCP-5) | Δ |
|---|---|---|---|
| **Filings cobertos** | só CVM/SEC oficial (latência 24-72h) | RI live (latência 0-2h) + agregação multi-source | ⬆⬆ |
| **Filings novos descobertos no pilot** | 0 (apanhar via cron normal) | **45 cross-ticker antecipadamente** | ⬆⬆⬆ |
| **Calendário próximos eventos** | Não tínhamos por ticker | **5 detectados** (ITSA4 1T26 amanhã!) | ⬆⬆ |
| **PDFs históricos acessíveis** | Só os que CVM monitor baixou | **341 (release+10K+supplements+transcripts)** | ⬆⬆⬆ |
| **Audio/video** | Cego | **22 (incluindo 5 JPM conference calls)** | ⬆⬆⬆ |
| **Markdown estruturado** | pdfplumber (texto plano, perde tabelas) | markitdown (tabelas/headers preservados) | ⬆ |
| **Sites JS-rendered** | Cego (requests retorna HTML vazio) | **Playwright headless (renderiza tudo)** | ⬆⬆ |
| **Multi-format** (.pptx, audio, etc) | Só PDF | PDF/DOCX/XLSX/PPTX/MP3/HTML/imagens | ⬆⬆ |
| **RI providers cobertos** | n/a | **4 testados** (Mz Group BR / Bradesco own / JPM corp / JNJ classic) | ✅ |
| **Tempo por ticker (cold)** | n/a (não tínhamos) | **~43s avg** | n/a |
| **Cache 24h reuso** | n/a | Sim (Playwright cache em `data/portal_cache/`) | ✅ |
| **Idempotência** | n/a | Sim (re-runs são no-op em cache hot) | ✅ |
| **Reusabilidade** | n/a | Sim (`scripts/pilot_deep_dive.py` extensível) | ✅ |

---

## Limitações honestas (NÃO inflar)

1. **Novelty BBDC4 sobre-conta** — 27 detectados como novos, mas
   alguns (~12) são duplicados que diferem só em prefix/punctuation
   ("Outros Comunicados Não Considerados Fatos Relevantes |
   Fechamento" vs "Comunicado ao Mercado - Fechamento"). Heuristic
   de fuzzy matching tokens precisa polir mais para confiar 100%.

2. **"Investor news" como título JNJ** — parser apanha headline da
   page mas o título correcto está num H3 abaixo da date. Heuristic
   US precisa de mais um pass para layouts não-H2 standard.

3. **Não wired automaticamente** — os 45 filings descobertos NÃO
   foram persistidos na `events` table. Continuam só no dossier .md.
   Se queres que entrem na DB para feed CLI/perpetuums, é uma
   sessão extra.

4. **312 presentations JPM** — verdadeiro mas overwhelming. Capped
   no display (top 12). Para usar, precisaríamos filtrar por ano /
   keyword no consumo, não só por count.

5. **Apenas 5 tickers testados** — extrapolar para 200 vai descobrir
   provavelmente 5-10 layouts adicionais (REITs, FIIs, smaller cap
   BR). Pipeline robusto **mas** não bullet-proof.

6. **Não testámos auth** — tudo público. Suno/XP/Bloomberg
   autenticados continuam por outro caminho (já implementado antes).

7. **Anti-bot** — JPM e JNJ não bloquearam. Mas TipRanks, MarketBeat,
   Seeking Alpha tipicamente bloqueiam. Para esses precisaríamos
   stealth mode no Playwright (não testado).

---

## Recomendação para escalar

### Próxima noite (HIGH CONFIDENCE)
- **Correr `pilot_deep_dive.py` em todas as 33 holdings** (BR+US).
  Estimado: ~25min com cache cold.
- **Output**: dossiers em `Pilot_Deep_Dive_<DATE>/`, master report
  consolidado.
- **Pré-requisito**: ter URLs de RI mapeados para todas as 33. Posso
  fazer um seed de URLs default agora se quiseres deixar pronto.

### 2-3 noites depois (MEDIUM CONFIDENCE)
- **Universo completo (200+ tickers)**: ~2.5h overnight. Precisa de
  resolver URL de RI para cada (~30min de prep + lookup table).
- **Wire para `events` table**: mais 1-2h de dev para inserir filings
  novos detectados como rows tipadas (kind=ri_filing, source=ri).

### Decisão tua quando voltares
1. Aceitas o pilot como prova de conceito? (sim/não)
2. Vou agora preparar URLs default das 33 holdings?
3. Corremos o full-33 esta noite ou esperamos teu OK explícito?

---

## Onde está cada coisa

```
obsidian_vault/Pilot_Deep_Dive_2026-05-10/
├── _LEITURA_PARA_O_USER.md     ← este ficheiro (TLDR humano)
├── _MASTER.md                   ← tabela auto-gen + estatísticas
├── ITSA4.md                     ← dossier técnico per-ticker
├── BBDC4.md
├── PRIO3.md
├── JPM.md
└── JNJ.md

scripts/
└── pilot_deep_dive.py           ← código reusable (correr de novo: ii ou direct)

data/
├── portal_cache/                ← MD/HTML/PNG cache 24h (Playwright)
└── cvm_pdfs/_pilot/             ← PDFs descarregados durante o pilot

logs/
└── pilot_deep_dive_2026-05-10.log  ← log estruturado JSON
```

## Como aceder no Obsidian

Abre o vault em `obsidian_vault/`. Navega para
`Pilot_Deep_Dive_2026-05-10/`. Começa por `_LEITURA_PARA_O_USER.md`,
clica nos `[[ITSA4]]` etc para os dossiers individuais.

## Como rodar de novo

```powershell
# Pilot de 5 tickers (default)
.venv\Scripts\python.exe scripts/pilot_deep_dive.py

# Cache fresh (real timing, slower)
.venv\Scripts\python.exe scripts/pilot_deep_dive.py --force-fresh

# Outros tickers
.venv\Scripts\python.exe scripts/pilot_deep_dive.py --tickers ITSA4 BBDC4

# Skip download de PDFs
.venv\Scripts\python.exe scripts/pilot_deep_dive.py --no-download
```

---

_Escrito por Claude (Opus 4.7) — 2026-05-10 18:35_
_Tempo total da sessão: ~2.5h (incluindo Phase MCP-5 setup + pilot dev + iteration)_
