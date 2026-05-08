# Personal Investment OS — Blueprint de Produto

> Documento de referência para desenvolvimento de um sistema operacional pessoal de investimentos.
> Público-alvo do produto: investidor pessoa física BR + US, estratégia de longo prazo (DRIP / Buffett).
> Desenvolvido por não-programador com auxílio de IA.

---

## 1. MVP — O que entra, o que fica de fora

### Entra no MVP

- Screening de ações (BR + US) com scores automáticos
- Dashboard com posições + alertas
- 1 relatório semanal automático por e-mail/notificação
- Autenticação básica (1 usuário por conta)

### Fica de fora do MVP

- Multi-usuário / times
- App mobile
- Integrações com corretoras
- Análise de opções / derivativos
- Chat livre com IA

**Critério de corte**: se não responde "devo comprar, manter ou vender X?", não entra.

---

## 2. Interface — Funcionalidades por tela

| Tela | O que mostra |
|---|---|
| **Home / Briefing** | Resumo matinal: alertas + mercado + posições em risco |
| **Screening** | Tabela de ações filtrada por critérios (DY, P/E, ROE, etc.) |
| **Ticker** | Ficha completa: fundamentals + score + histórico + verdict |
| **Carteira** | Posições reais + performance + peso por setor |
| **Alertas** | Eventos CVM/SEC + triggers de preço + sinais |

Sem CLI. Sem config JSON visível. Tudo via formulários e botões.

---

## 3. IA — Few-shots, RAG ou híbrido?

**Resposta: híbrido, mas em camadas.**

```
Camada 1 — SQL puro (zero IA)
  Scores, screening, alertas de preço → regras determinísticas

Camada 2 — RAG local (Ollama)
  "O que os analistas dizem sobre PETR4?" → busca em vault local

Camada 3 — Few-shots (Claude API — último recurso)
  Síntese narrativa, dossiers, debate de teses → caro, só quando necessário
```

**Regra de ouro**: IA só entra quando há texto não-estruturado para interpretar. Números são SQL.

---

## 4. Local-first — Como desenvolver

### Stack recomendada

| Componente | Tecnologia |
|---|---|
| Backend | Python (FastAPI ou scripts diretos) |
| Banco de dados | SQLite → PostgreSQL só se SaaS multi-user |
| LLM local | Ollama (Qwen 2.5 14B para análise, 3B para classificação) |
| Frontend | Next.js (mais escalável) ou Streamlit (mais simples para começar) |
| Desktop (opcional) | Tauri v2 — empacota o Next.js → .exe instalável |

### Vantagens do local-first

- Custo zero de infraestrutura no início
- Dados do usuário ficam com ele (diferencial de privacidade)
- Funciona offline

### Desvantagens

- Distribuição mais trabalhosa (precisa instalar)
- Atualizações exigem nova versão do instalador

---

## 5. Ferramentas de IA para o desenvolvimento

| Ferramenta | Papel | Recomendação |
|---|---|---|
| **Claude Code** | Arquitetura, features complexas, debugging difícil | ✅ Principal |
| **Cursor Pro** | Edição rápida, autocompletar, refactor inline | ✅ Complementar |
| **GitHub Copilot** | Redundante se tem Cursor | ❌ Pular |
| **Tauri v2** | Framework desktop (não é IA) | ✅ Para versão instalável |

**Setup real**: Claude Code para sessões de trabalho (sessão = feature completa), Cursor para edições pontuais no dia a dia.

---

## 6. Cronograma e custo

### Cronograma — não-programador com IA como par (1–2h/dia)

| Fase | Duração | Entrega |
|---|---|---|
| Semana 1–2 | 2 semanas | Setup + autenticação + DB schema |
| Semana 3–4 | 2 semanas | Screening BR + dashboard básico |
| Semana 5–6 | 2 semanas | Screening US + alertas |
| Semana 7–8 | 2 semanas | Relatório automático + polish |
| Semana 9–10 | 2 semanas | Beta fechado (5–10 usuários) |
| Semana 11–12 | 2 semanas | Ajustes + lançamento MVP |

**Total: ~3 meses** com consistência de 1–2h/dia.

### Custo mensal de desenvolvimento

| Item | Custo/mês |
|---|---|
| Claude Code (Max plan) | ~$100 |
| Cursor Pro | ~$20 |
| Servidor VPS (Hetzner 4 vCPU / 8 GB) | ~$15 |
| Domínio + e-mail | ~$5 |
| **Total mensal** | **~$140** |

**Custo até MVP**: ~$420 (3 meses) + máquina própria.

---

## 7. Configuração mínima da máquina de desenvolvimento

| Componente | Mínimo | Recomendado |
|---|---|---|
| CPU | Core i5 12ª gen | Core i7/i9 ou Ryzen 7/9 |
| RAM | 32 GB | 64 GB |
| GPU | RTX 3060 12 GB | RTX 4070+ |
| Storage | SSD 500 GB | SSD 1 TB NVMe |
| SO | Windows 11 ou Ubuntu 22 | Windows 11 (Tauri + WSL2) |

> **Atenção**: sem GPU dedicada ≥12 GB de VRAM, o Ollama com modelos 14B é inutilizável na prática. É o componente mais crítico para o desenvolvimento local-first.

---

## 8. Formulário de validação das premissas

Aplicar com 20–30 potenciais usuários antes de começar a codar.

```
1. Você acompanha ações BR, US ou ambos?

2. Quanto tempo por semana você gasta pesquisando investimentos?
   [ ] Menos de 1h   [ ] 1–3h   [ ] 3–6h   [ ] Mais de 6h

3. Qual sua maior dor hoje? (escolha apenas 1)
   [ ] Não sei quais ações comprar
   [ ] Não sei quando vender
   [ ] Perco tempo compilando dados de várias fontes
   [ ] Não consigo acompanhar o que muda nos meus ativos
   [ ] Não entendo os dados que vejo

4. Você já usa alguma ferramenta de análise?
   (Fundamentei, Status Invest, Investidor10, etc.)
   → Se sim: o que falta nelas?

5. Você pagaria por uma ferramenta que faz isso automaticamente?
   [ ] Não pagaria
   [ ] Até R$30/mês
   [ ] Até R$60/mês
   [ ] Até R$120/mês

6. Prefere uma ferramenta que instala no computador
   ou que acessa pelo navegador? Por quê?

7. Você tem receio de colocar dados da sua carteira
   em uma ferramenta de terceiros?

8. Se eu te desse acesso a uma beta hoje, você usaria?
   [ ] Sim, agora
   [ ] Sim, em até 1 mês
   [ ] Talvez
   [ ] Não
```

**Meta mínima de validação**: 5 pessoas respondendo "pagaria R$39/mês" antes de escrever uma linha de código.

---

## 9. Web vs Desktop — Estratégia por fases

```
Fase 0 — Validação (mês 1)
  → Streamlit local, sem servidor, sem domínio
  → Objetivo: mostrar para 5 pessoas e ver se usam

Fase 1 — MVP (meses 2–3)
  → Next.js hospedado (Vercel gratuito)
  → Sem login ainda — link direto para beta testers
  → Objetivo: 20 usuários ativos por semana

Fase 2 — Produto (meses 4–6)
  → Autenticação real + planos pagos
  → Continua web (menor atrito para novos usuários)

Fase 3 — Expansão (meses 7+)
  → Tauri v2 para versão desktop (usuários power, privacidade)
  → Mobile (React Native) se dados mostrarem demanda
```

**Regra**: web primeiro porque elimina o passo de instalação, que mata a conversão de novos usuários.

---

## 10. Estrutura de ofertas e precificação

### Modelo SaaS (web)

| Plano | Preço | O que inclui |
|---|---|---|
| **Free** | R$0 | Apenas BR, 10 tickers, sem alertas |
| **Essencial** | R$39/mês | BR + US, 50 tickers, alertas básicos |
| **Profissional** | R$89/mês | Ilimitado + análise IA + relatórios |
| **Anual** | –20% | Desconto por fidelidade |

### Modelo desktop (local-first / privacidade como diferencial)

| Plano | Preço | O que inclui |
|---|---|---|
| **Licença única** | R$297 | Vitalício, atualizações por 1 ano |
| **Licença + suporte** | R$49/mês | Atualizações contínuas + canal direto |

### Estratégia de entrada recomendada

1. **Lista de espera gratuita** — 60 dias grátis para os primeiros 50 inscritos
2. **Cobrar apenas** quando houver 3 pessoas dizendo "quando você cobrar, pago"
3. **Primeiro plano pago**: preço baixo mas com compromisso anual (R$297/ano)

---

## Resumo executivo

| Decisão | Escolha |
|---|---|
| Stack | Next.js + FastAPI + SQLite |
| IA em produção | Ollama local (Qwen 14B) + Claude API ocasional |
| Ferramentas de dev | Claude Code (principal) + Cursor Pro (secundário) |
| Distribuição | Web primeiro → Desktop (Tauri v2) depois |
| Tempo até MVP | ~3 meses (1–2h/dia) |
| Custo de infra | ~$140/mês (~R$750) |
| Custo até lançar | ~$420 total de ferramentas + servidor |
| Antes de codar | Formulário com ≥20 respostas + 5 "sim, pagaria" |

---

*Documento gerado em 2026-05-06.*
