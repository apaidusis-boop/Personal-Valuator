"""Camada de narrativa de mercado (sector-level).

Pipeline:
    scrapers/*           -> narrative_items (raw)
    classifier.classify  -> narrative_items (sector, direction, thesis_tag, ...)
    aggregator.aggregate -> sector_sentiment (rolling 7/30/90d por sector/subsector)
    regime.classify      -> macro_regime (4D: rate/growth/fx/risk)
    base_rates.compute   -> sector_base_rates (histórico forward returns)
    rules.decide         -> sinal final (combina fundamentals × sentiment × regime)

Filosofia:
    - Tudo é sector-level, não ticker-level. Fundamentals decidem QUAL ticker
      dentro do sector. Narrativa decide SE entrar/sair do sector e QUANDO.
    - Narrativa muito negativa + fundamentals OK + tese 'macro/panic' = REFORÇO
      (contrarian). Mesma narrativa com tese 'credit/governance/fraud' = PAUSA
      (fundamentals trimestrais ainda não reflectem).
    - Nada aqui chama bolsa/preços. Consome `series` e `prices` já populadas
      pelos fetchers existentes.
"""
