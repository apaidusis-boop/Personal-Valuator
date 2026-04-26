---
type: design_prototypes_index
phase: U.1
created: 2026-04-26
owner: huashu_design + helena_linha
tags: [design, prototypes, home, huashu, helena]
---

# Protótipos Home v1 — 3 direções

> Geração: huashu-design skill em modo *design direction advisor*.
> Prerequisite: Helena Mega audit (23 violações no estado actual, maioria DS006 hex literals fora dos tokens).
> Anti-slop checklist passou em todos os 3.

## Como usar este index

1. **Abre os 3 ficheiros HTML** lado a lado no browser (drag-drop ou `start .html`):
   - `proto_home_v1_a.html` — Tufte / Pentagram
   - `proto_home_v1_b.html` — Vignelli / Unimark
   - `proto_home_v1_c.html` — Hara / MUJI
2. **Compara**: cada um resolve o mesmo problema (Home com sidebar de carteiras + chart 5y + holdings table + status bar) com **conteúdo idêntico** (mock).
3. **Escolhe um**, ou pede mistura ("layout do A com paleta do C").
4. Próximo passo: **ui-ux-pro-max-skill** fixa os tokens definitivos da escolha.

---

## A — Tufte / Pentagram (Information Architecture)

### Filosofia
Edward Tufte's data-ink principle. Cada pixel justifica a sua presença. **Sparklines integradas em cada row da tabela** (signature Tufte genuíno). Tabelas como estrutura primária. Mono dominante (JetBrains Mono); IBM Plex Sans só para micro-labels uppercase. Fundo near-black `#0a0a0a`. Cor é semântica e nunca decorativa.

### Quando este ganha
- Trabalhas sempre com chart + tabela densa simultaneamente
- Valorizas **densidade analítica** sobre estética
- Queres ver 5y de história num único *row* da tabela (sparkline)
- Adoras Bloomberg Terminal pela sua função, não pela cor amarelo-âmbar

### Quando este falha
- Convidas alguém a olhar para o ecrã — pode parecer intimidador (todos os números, tudo mono)
- Para *deep reading* sobre uma posição específica, falta espaço narrativo

### Referências honestas
- Tufte, *The Visual Display of Quantitative Information* (1983)
- Pentagram financial reports (Citigroup 2010s)
- Refinitiv Eikon "MOSAIC"

---

## B — Massimo Vignelli / Unimark (Minimalismo Suíço-Italiano)

### Filosofia
"Form follows meaning." Vignelli's design system principles — **3 typefaces apenas, cada um com role explícito**:
- *Bodoni Moda italic* = display ("Carteiras" em 56px italic)
- *Helvetica Neue* = UI (labels, nav, table headers)
- *IBM Plex Mono* = data

**Light theme** `#fafaf7` (paper-warm — Vignelli usou paper background em quase tudo). 1 accent vermelho Vignelli `#cc2936`. Grid 12-col visível como linha vertical subtil. Voz portuguesa formal ("Recomendadas pelos analistas", "Composição da carteira", "Cotação", "Ativo").

### Quando este ganha
- Queres um sistema **disciplinado** com regras claras (3 fontes, 1 cor, grid)
- Aprecias o **contraste cultural**: relatório financeiro 1970s aplicado a dados 2026
- Estás cansado de dashboards dark-mode-default
- O Bodoni italic page-title é uma **assinatura de identidade** que não vais ver noutro produto

### Quando este falha
- Bodoni italic 56px pode parecer "decoração" se mal usado (depende de auto-disciplina futura)
- Light theme em sala escura cansa olhos (depende do teu workflow)

### Referências honestas
- Vignelli, *The Vignelli Canon* (2010, free PDF)
- NYC Subway diagram (1972)
- Knoll, American Airlines, Bloomingdale's identities (Unimark, anos 1970)
- Müller-Brockmann grid systems

---

## C — Kenya Hara / MUJI (Filosofia Oriental, Banca Privada)

### Filosofia
"NÃO É DASHBOARD. É um documento." A página abre com uma **lede sentence completa** — não label/value pairs. *"A carteira encerra a semana em R$ 287.432, com +1,24% em sete pregões, distribuída por 33 posições entre Brasil e Estados Unidos."*

Cream warm `#f4eee5`. Source Serif 4 (variable font, optical-size 60 no headline). Inter para micro-labels. Mono SÓ em números, em tamanho menor que o texto. 1 accent terracotta `#b85c38` em 3 sítios apenas. **Voz PT-BR completa**: "Início" em vez de "Home", "Pergunta" em vez de "Ask", "Frente ao IBOV", "Cinco anos", "Composição".

### Quando este ganha
- Lês a página de manhã com café — não estás a "monitorizar trades"
- Queres uma **identidade brasileira/portuguesa autêntica**, não uma tradução de SaaS gringo
- Aprecias quando a UI **respeita a tua inteligência** (não há over-explaining)
- Esta é a página que mostras ao teu pai sem precisar de explicar

### Quando este falha
- Quando precisas de varrer 12 carteiras × 3 KPIs em 5 segundos (densidade fica curta)
- Para active trading / decisões rápidas (a calma desliga reflexos)

### Referências honestas
- Hara, *Designing Design* (2007), *White* (2010)
- MUJI brand identity (Hara art director, 2002–presente)
- Itaú Private Bank quarterly letters
- Pictet & Cie. asset management reports

---

## Recomendação honesta

> **Não há resposta única — a escolha define o produto.**

A minha leitura, dado o que sei do utilizador (PT-BR fluente, valoriza profundidade de análise sobre velocidade, leitor de cartas Suno e JPM Research, perspectiva DRIP/Buffett-Graham que assume horizonte longo):

**Opção dominante: C (Hara / MUJI)** — porque a tua filosofia DRIP é literalmente "long-horizon contemplation". A UI deve **espelhar como tu pensas sobre os teus investimentos**, não estar em conflito.

**Opção alternativa: B (Vignelli)** — se quiseres signature visual mais *marcada*, mais "este produto é meu", o italic Bodoni é uma assinatura forte. É menos calmo que C, mas mais memorável.

**Razão para A (Tufte)**: só se realmente quiseres uma ferramenta de varrimento operacional onde *cada visita à Home leva ≤30 segundos*. Para sessions curtas e densas, A é imbatível. Mas pelo que vi do uso real (vault de 200+ notas, escrita reflexiva nas teses), tu **não usas a Home como ferramenta operacional rápida** — usas-la como ponto de entrada para estudo.

---

## Próximos passos

Depois de tu escolheres:

1. **`ui-ux-pro-max-skill`** — pego nos tokens da direcção escolhida e construo o `Design_System v2.0` definitivo (paleta confirmada, 3 fontes confirmadas, spacing scale, type scale, chart conventions).
2. **Helena Mega curate** — actualiza as 9 regras DS001-DS009 com os novos tokens, faz audit-lint passar a 0.
3. **Implementação Streamlit** — traduzo a HTML escolhida para `dashboard_app.py` reusando `_components.py`. **Eu não invento nada de cabeça** — o protótipo é a fonte da verdade.
4. **Ticker page editorial** — repete o exercício para a página de ticker (modo FT/WSJ).

---

## Anti-slop verdict (resumo)

| Critério | A · Tufte | B · Vignelli | C · Hara |
|---|:---:|:---:|:---:|
| Sem emojis | ✓ | ✓ | ✓ |
| Sem mistura PT/EN | ✓ | ✓ | ✓ |
| Sem cards `border-left:2px accent` | ✓ | ✓ | ✓ |
| Sem hero number gigante | ✓ (stat bar) | ✓ (Bodoni serve outro role) | ✓ (lede em vez disso) |
| Voz consistente | mono editorial | sistema 1970s | carta privada |
| Identidade clara (não SaaS template) | Tufte signature (sparklines) | Vignelli signature (italic Bodoni + grid) | Hara signature (cream + lede sentence) |
| Paleta justificada | 5 tokens canónicos | +1 (Vignelli red) | +2 (cream + clay) |
| Anti-slop checklist passa | ✓ | ✓ | ✓ |
