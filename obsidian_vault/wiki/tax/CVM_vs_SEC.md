---
type: tax
name: CVM vs SEC — regulatory filings
region: BR-US
tags: [regulatory, cvm, sec, filings, disclosure]
related: ["[[BR_dividend_isencao]]", "[[US_LTCG_STCG]]"]
---

# 📜 CVM (BR) vs SEC (US) — comparação regulatória

## Quem é quem

| Autoridade | País | Escopo | Análogo |
|---|---|---|---|
| **CVM** — Comissão de Valores Mobiliários | 🇧🇷 | Mercado de capitais BR | = SEC |
| **B3** | 🇧🇷 | Bolsa + clearing (SRO) | = NYSE + DTCC |
| **Bacen** | 🇧🇷 | Sistema financeiro + câmbio | = Fed |
| **SEC** — Securities Exchange Commission | 🇺🇸 | Mercado de capitais US | = CVM |
| **NYSE / NASDAQ** | 🇺🇸 | Bolsas | = B3 |
| **FINRA** | 🇺🇸 | Broker-dealer self-regulator | — |
| **Fed / OCC** | 🇺🇸 | Bancos | = Bacen |

## Taxonomia de filings

### Materiality events

| Evento | BR (CVM) | US (SEC) |
|---|---|---|
| Incidente material | **Fato Relevante** | **8-K** |
| Resultado trimestral | ITR (Informações Trimestrais) | 10-Q |
| Resultado anual | DFP (Demonstrações Financeiras Padronizadas) | 10-K |
| Oferta pública | Prospecto + RG 400/476 | S-1 / S-3 / 424 prospectus |
| Cadastro anual | Formulário de Referência (FR) | — (proxy statement parcial) |
| Assembleia | Proposta da Administração | Proxy (DEF 14A) |
| Ações execs | Fato Relevante / FR | Form 4 (trades), 10-K item 11 |

### Timing

- **Fato Relevante** (BR): **imediato** (antes de abertura do mercado se fora horário).
- **8-K** (US): **4 business days** após trigger event.
- **Earnings** BR: 45 dias pós-trimestre (ITR), 3 meses após exercício (DFP).
- **Earnings** US: 10-Q 40-45 dias trimestre, 10-K 60-90 dias exercício.
- **Proxy / Assembleia**: BR 30 dias antes; US 40-50 dias antes.

## O que vigiar em Fatos Relevantes

Typical red/yellow flags:
- Mudança auditor (bad) ou auditoria pendente.
- Investigação CVM / SEC / Receita.
- Covenant breach ou renegociação dívida.
- Aquisição > 10% capital.
- Dividend policy change.
- CEO/CFO change.
- Fusões, spin-offs, incorporações.
- Liquidação.

**Critérios CVM** para fato relevante (RCVM 44/2021):
- Qualquer evento que "influencie a decisão de investir".
- Operações > 5% do PL.
- Mudança controle > 5%.

## Insider trading — disclosures

### BR
- **Item 12.5** do Formulário de Referência (anual) — trades executivos cumulados.
- Divulgação mensal via CVM ofício para membros.
- **15 dias para divulgar**.

### US
- **Form 4** — 2 business days após trade (insider corporativo).
- **13D/13G** — 10 dias após ≥ 5% ownership passive (G) or active (D).
- **Form 3** — initial insider notification.

**Para retail**: monitore insider buys (bullish) vs sells (neutral, many reasons). SEC tools: OpenInsider, RoboInvestor.

## Proxy / Assembleia

### BR
- **AGO** (Assembleia Geral Ordinária): anual até abril, aprova contas + eleição.
- **AGE** (Extraordinária): quando necessária.
- Quorum variable (CVM + empresa bylaws).
- Voto **eletrônico** via corretora or TED → Assembleia.

### US
- **Annual Meeting**: 1×/y, ~May.
- **Proxy statement (DEF 14A)**: todos os itens de voto.
- Say-on-pay (non-binding), board elections, auditor approval.
- Voto eletrônico via broker (proxy.com, etc).
- **Shareholder proposals** allowed (SOX, Dodd-Frank reforms).

## Dividends — regulatory mechanics

### BR
- **Ex-date = data-com** BR.
- Data de pagamento: geralmente 30-60 dias pós-ex.
- Semi-anual comum (empresas); mensal FIIs (obrigatório ao cotista).
- **Notice via CVM**: "Aviso aos Acionistas" antes ex-date.

### US
- **Ex-date**: 1 business day antes record date (T+1 após reforma 2023; era T+2).
- **Record date**: cutoff.
- **Payment date**: geralmente 2-4 semanas pós-ex.
- Quarterly comum; monthly raros (O, MAIN, STAG).
- **Notice via 8-K** para mudanças policy.

## Insurance tax compliance

### BR
- **IR sobre serviços financeiros** IOF variável.
- **Zero IOF** em ações B3 para PF.
- **CDE** tax em câmbio (0.38% flat).

### US
- Trades sem transaction tax (except tiny SEC fee 0.008% em sells).
- Stamp duty UK-style: **zero** em US; 0.5% UK; 0.2% China A; 3% França CFT (large caps).

## Private placements

### BR
- **Instrução 476** (agora RCVM 476): efforts restrita a 75 investidores qualificados.
- Menor disclosure, mais rápido.
- Usada em FIDCs, CRIs, debentures.

### US
- **Rule 144A**: QIBs (qualified institutional buyers).
- **Reg D**: accredited investors (high net worth).
- Menor disclosure.

## Financial statements — GAAP differences

### BR (IFRS)
- Desde 2010 BR corporate uses IFRS (full).
- CPC (Comitê de Pronunciamentos Contábeis) = BR IFRS.

### US (US GAAP)
- Different in: lease accounting (ASC 842 vs IFRS 16 subtle differences).
- LIFO inventory allowed US (proibido IFRS).
- R&D capitalisation: IFRS permite development phase; US GAAP expenses everything.
- Goodwill: US tests annual impairment; IFRS mesmo.

**Impacto em comparison** [[ACN]] (US GAAP) vs BR IT company (IFRS): subtle differences em margem operational.

## Listagem cross-listing

- **BDR** (Brazilian Depositary Receipts): US stocks tradeable B3. Ex: DISB34 (Disney), TSMB34 (TSMC).
- **ADR** (American Depositary Receipts): foreign stocks tradeable NYSE/NASDAQ. Ex: VALE (VALE3), ITUB (ITUB4), PBR (PETR4).

### BR investidor holding US via BDR
- Tax treatment: equivalente BR stock domestic.
- **Sem withholding 30%** US (BDR é instrument BR).
- **Isento IR dividend** if BDR reflete stock qualifying.
- Cash flow mais eficiente que direct US stock para PF BR!
- **Drawback**: liquidity menor, spread maior, tracking error.

## Red flags — regulatory

- CVM Ofício de exigência (empresa tem fraqueza compliance).
- Auditor resignation sem sucessor anunciado.
- 8-K Item 4.02 (financial statements non-reliance — forced restatement).
- 10-Q delay > 30 dias — Nasdaq delisting risk.
- Proxy fight ativo (investidor ativista) — sempre volatility.

## Tools

- **CVM.gov.br** → Sistema IPE, Consulta Documentos.
- **B3** → dados/empresas listadas.
- **SEC.gov** → EDGAR full-text search.
- No nosso sistema: `monitors/cvm_monitor.py`, `monitors/sec_monitor.py`.

---

> Ver [[BR_dividend_isencao]] side BR tax. [[US_LTCG_STCG]] side US. [[Tax_lot_selection]] aplicado prático JPM UI.
