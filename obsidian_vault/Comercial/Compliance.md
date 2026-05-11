---
type: doc
scope: commercial
roadmap_block: B3
created: 2026-05-11
---

# ⚖️ Compliance — os limites legais (para não virar consultoria ilegal)

> Bloco B3 de [[Comercial/00_Roadmap]]. Constituição: [[CONSTITUTION_Comercial]] (nº1: not financial advice). A pergunta: **que guardrails é que tornam isto uma ferramenta legal, e não uma assessoria de investimentos não-registada?**
> ⚠️ Isto é a *postura de design*, decidida agora. **Não substitui um advogado** — é um item "falar com jurídico antes do bloco B6".

## A postura: ferramenta educacional, não conselheiro
O que **NÃO somos**:
- **RIA / investment adviser registado** (US: SEC ou estadual) — não damos conselho personalizado mediante remuneração.
- **Consultor de valores mobiliários** ou **analista** registado na **CVM** (BR: Res. CVM 19 / Res. CVM 20; certificação APIMEC) — não emitimos "recomendações" como analista registado.

→ Toda a saída é **análise / ferramenta / educacional**, com disclaimers visíveis. O sistema analisa o *ticker / a carteira* de forma genérica e transparente; **não diz a *ti especificamente* o que fazer com o teu dinheiro**.

## Regras concretas (consequências da postura)
1. **Disclaimer em toda saída que toca um verdict** buy/hold/sell: *"ferramenta educacional; não constitui recomendação de investimento; decisões são suas; considere consultar um profissional registado."* Visível, não escondido no rodapé.
2. **Nunca "compre X agora"** sem o *porquê* e sem o disclaimer. Enquadrar como análise / cenários, não como ordem. Linguagem BR: usar "análise", "verdict do sistema", "cenários" — **evitar a palavra "recomendação"**.
3. **Nunca executar ordens.** Importar carteira (read-only) é OK; rotear ordens para a corretora **não** — isso muda a categoria regulatória inteira.
4. **Nunca prometer ou insinuar retorno.** Backtests rotulados claramente como históricos, *não* preditivos. Sem "rentabilidade passada" como argumento de venda.
5. **Verdicts = output analítico do sistema para a consideração do utilizador**, com transparência de metodologia e confiança (banda de fair value, `data_confidence`) — como um *flag* de screener, não uma recomendação personalizada.

## A linha a pisar — por jurisdição
**US** — existe o "publisher's exemption" / safe harbor de publicação financeira (*Lowe v. SEC*): publicações bona fide de circulação geral, não-personalizadas, são protegidas. → análise geral disponível a todos os subscritores = OK; "*tu* especificamente devias vender o teu ITSA4" = arriscado. Mitigação: o sistema analisa o *ticker/carteira* genericamente; não te diz a *ti* o que fazer; disclaimers em todo o lado.

**BR** — a CVM é mais restritiva sobre quem pode chamar-se "analista" e emitir "recomendações". Mitigação: não usar "recomendação"/"consultoria"; enquadramento educacional/ferramenta. Se o lado BR crescer, **ponto de decisão**: avaliar se certificação APIMEC / registo CVM se torna necessário — não assumir que sim, não assumir que não; rever com jurídico.

## Licenciamento de dados
- **Fontes públicas** (yfinance/Yahoo, SEC EDGAR, CVM, B3 público, Status Invest scrape, fiis.com.br): geralmente OK para um produto, **mas rever ToS** — a ToS do Yahoo Finance restringe redistribuição comercial; SEC/CVM são domínio público; scraping tem zonas cinzentas. Mitigação: para o produto comercial, migrar para feeds devidamente licenciados onde a ToS da fonte pública for restritiva (é uma linha de custo em [[Comercial/Pricing]]).
- **Providers premium** (FactSet/Daloopa/Morningstar/Moody's/S&P/PitchBook/…): **só com contrato**; nunca redistribuir fora dos termos. (Os 11 MCPs que vêm com o plugin `financial-analysis` ficam não-autenticados até haver contrato — ver memória `anthropic_fsi_plugins.md`.)

## Privacidade
- **LGPD** (BR) + **GDPR** (utilizadores EU) + CCPA (CA): dados de carteira são informação financeira sensível.
- Mitigação: **isolamento de tenant** (já é não-negociável do Mundo Comercial), encriptação at rest, política clara de retenção/eliminação, **não vender/partilhar dados de utilizador** (já é não-negociável), DPA com sub-processadores.

## Bottom line
A postura é **defensiva por design** — somos uma *ferramenta*, não um conselheiro. Pôr isto por escrito nos Termos de Uso **+** em cada superfície relevante da UI. É um item "advogado antes do B6", mas a postura está decidida agora.

## O que isto desbloqueia
Antes: "isto é legal?" era uma pergunta em aberto que paralisava o pensamento sobre comercializar. Agora: a postura está decidida (ferramenta não-conselheiro · disclaimers · sem execução · sem promessas de retorno · linguagem BR cuidada) → da próxima vez que desenharmos *qualquer* superfície virada a cliente (o report tier, alertas, o gestor de tese), os guardrails já estão definidos e não temos de re-litigar a questão. E os pontos de decisão jurídica (registo CVM? licenciar dados?) estão *nomeados* — sabemos exatamente o que perguntar a um advogado.
