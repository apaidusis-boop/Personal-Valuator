---
type: skill
tier: Gold
skill_name: remotion
source: remotion-dev/remotion
status: backlog
sprint: W.9
tags: [skill, gold, remotion, video, overkill]
---

# 🎥 Remotion — Auto-generated Portfolio Videos

**Repo**: https://github.com/remotion-dev/remotion
**Fit**: 🟡 overkill-puro, mas **Gold** por request explícito "overkill is fine".

## O que faz
Video rendering programático em React. Cada frame é um componente. Output MP4/WebM.

## Onde integra — "Portfolio Recap Video" semanal 🎬

### Weekly Recap video (60-90 segundos)
Auto-gerado todo domingo às 20h:
- **0-10s**: Capa animada "Week YYYY-WW recap"
- **10-30s**: Portfolio total em BRL (contador animado de X → Y, diff %)
- **30-50s**: Top 3 movers (winner/loser) com sparklines
- **50-70s**: Thesis health heatmap animado (feed do perpetuum validator)
- **70-80s**: Dividends received esta semana
- **80-90s**: Regime macro BR/US + call to action

### Monthly deep recap (3-5 min)
Mais rico:
- Performance vs benchmarks
- Sector drift animation
- Thesis decay timeline
- Key news narrative (gerado por LLM, voice-over via TTS)

### Distribution
- Upload automático para Google Drive (usa MCP já loaded)
- Telegram send (já temos Jarbas bot) — "📹 Recap semanal está pronto"
- Ficheiro local em `reports/videos/YYYY-WW.mp4`

## Por que vale o overkill?
1. **Consumo passivo no iPhone** enquanto faz outra coisa — vs abrir dashboard e navegar
2. **Memória histórica visual** — daqui a 2 anos, 104 videos de 60s = rewatch history
3. **Motivador emocional** — ver património + thesis health animado cria commitment
4. **Compound learning** — ouvir narração "esta semana TFC thesis perdeu 8 pontos porque..." ensina

## Sprint W.9 — entregáveis
- [ ] Projeto Remotion em `video/` folder separado (deps pesados, isolar)
- [ ] Component library: `<PortfolioTotal>`, `<SparklineTicker>`, `<ThesisHeatmap>`, `<RegimeDial>`
- [ ] Script `video/render_weekly.ts`
- [ ] Cron Sunday 20h
- [ ] Integração Telegram + Drive upload

## Custo
- **Dev time**: ~2 semanas para MVP
- **Render**: local, grátis (Remotion renders on-device)
- **TTS**: ElevenLabs free tier OR Coqui TTS local (alinhado in-house first)
- **Deps**: Node.js + ffmpeg (já instalado provável)

## Blockers
- Node.js + ffmpeg setup (verify first)
- Aprender Remotion (curva média, baseado em React)

## Decisão
**Só arrancar W.9 depois de W.5 (perpetuum validator) e W.8 (canvas) estarem done** — Remotion consome outputs deles. Sem eles, o video está vazio de substance.
