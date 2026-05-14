@echo off
REM daily_run.bat - Phase EE Tiered Scheduler - tier daily (~2h, 23:30)
REM Pipeline pesado completo BR + US. Acquires the daily lock, which blocks
REM hourly + q4h tiers from starting (they yield).
REM Time-sensitive steps (sec_monitor, cvm_monitor, notify_events, etc) moved
REM to hourly_run.bat / q4h_run.bat after Phase EE 2026-05-08.
REM Log rotativo em logs/daily_run_YYYY-MM-DD.log

setlocal
set ROOT=C:\Users\paidu\investment-intelligence
set PY=%ROOT%\.venv\Scripts\python.exe
set PYTHONIOENCODING=utf-8

for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set DATESTAMP=%%a
set LOG=%ROOT%\logs\daily_run_%DATESTAMP%.log

echo ======================================== >> "%LOG%"
echo daily_run.bat  %date% %time% >> "%LOG%"
echo ======================================== >> "%LOG%"

cd /d "%ROOT%"

REM Acquire daily lock - heaviest tier, blocks hourly + q4h until done
"%PY%" -m agents._lock acquire daily >> "%LOG%" 2>&1
if errorlevel 1 (
    echo Daily lock busy ^- another daily run in progress, aborting >> "%LOG%"
    goto :end
)

echo [BR] daily_update.py  ^(retry x3, network heavy^) >> "%LOG%"
"%PY%" scripts\_retry.py --tag BR-DAILY --attempts 3 --backoff 60,300,900 --timeout 1800 -- "%PY%" scripts\daily_update.py >> "%LOG%" 2>&1
echo BR exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [TAXLOTS] auto_import_taxlots.py  ^(picks up Downloads/taxlots.csv if newer^) >> "%LOG%"
"%PY%" scripts\auto_import_taxlots.py --quiet >> "%LOG%" 2>&1
echo TAXLOTS exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [US] daily_update_us.py  ^(retry x3, network heavy^) >> "%LOG%"
"%PY%" scripts\_retry.py --tag US-DAILY --attempts 3 --backoff 60,300,900 --timeout 1800 -- "%PY%" scripts\daily_update_us.py >> "%LOG%" 2>&1
echo US exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [EXA-NEWS] exa_news_monitor.py --holdings --md  ^(Exa neural news -^> news table^) >> "%LOG%"
"%PY%" scripts\_retry.py --tag EXA-NEWS --attempts 2 --backoff 120 --timeout 600 -- "%PY%" scripts\exa_news_monitor.py --holdings --md >> "%LOG%" 2>&1
echo EXA-NEWS exit code: %errorlevel% >> "%LOG%"

REM === SEC + CVM monitors moved to hourly_run.bat (Phase EE 2026-05-08) ===
REM === CVM PDF extractor + dividend/earnings calendars + benchmarks    ===
REM === + auto_verdict + trigger_monitor moved to q4h_run.bat           ===

REM === Phase LL — filings-first fundamentals (must run BEFORE fair_value) ===
REM     SEC XBRL US -> derive_fundamentals_from_filings BR ->
REM     Fundamentus BR -> fiis.com.br BR FIIs -> data_confidence refresh ->
REM     fair_value (consumes all of the above).

echo. >> "%LOG%"
echo [SEC-XBRL] sec_xbrl_fetcher --holdings  ^(US filings primary; cached 24h^) >> "%LOG%"
"%PY%" -m fetchers.sec_xbrl_fetcher --holdings >> "%LOG%" 2>&1
echo SEC-XBRL exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [CVM-DERIVE] derive_fundamentals_from_filings --holdings  ^(BR ITR/DFP -^> TTM^) >> "%LOG%"
"%PY%" scripts\derive_fundamentals_from_filings.py --holdings >> "%LOG%" 2>&1
echo CVM-DERIVE exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [FUNDAMENTUS] fundamentus_fetcher --holdings  ^(BR 3rd source for triangulation^) >> "%LOG%"
"%PY%" -m fetchers.fundamentus_fetcher --holdings >> "%LOG%" 2>&1
echo FUNDAMENTUS exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [FIIS-COM-BR] fiis_com_br_fetcher --holdings  ^(FII-specialized depth^) >> "%LOG%"
"%PY%" -m fetchers.fiis_com_br_fetcher --holdings >> "%LOG%" 2>&1
echo FIIS-COM-BR exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [DATA-CONFIDENCE] analytics.data_confidence --holdings  ^(refresh after fetchers^) >> "%LOG%"
"%PY%" -m analytics.data_confidence --holdings >> "%LOG%" 2>&1
echo DATA-CONFIDENCE exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [INTANGIBLES] backfill_intangibles.py --us-only  ^(re-populate goodwill/TBV so fair_value intangible gate fires; daily fundamentals refresh drops these cols^) >> "%LOG%"
"%PY%" scripts\backfill_intangibles.py --us-only --sleep 0.3 >> "%LOG%" 2>&1
echo INTANGIBLES exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [FAIR-VALUE] scoring.fair_value --holdings  ^(target price + upside%%; uses filings^) >> "%LOG%"
"%PY%" -m scoring.fair_value --holdings >> "%LOG%" 2>&1
echo FAIR-VALUE exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [CROSS-SOURCE] cross_source_spotcheck.py  ^(Phase FF Bloco 3.3: yfinance SPOF^) >> "%LOG%"
"%PY%" scripts\cross_source_spotcheck.py --quiet >> "%LOG%" 2>&1
echo CROSS-SOURCE exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [VH-RECORD] verdict_history record  ^(Phase FF: snapshot today's verdicts^) >> "%LOG%"
"%PY%" scripts\verdict_history.py record >> "%LOG%" 2>&1
echo VH-RECORD exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [DECISION-QUALITY] decision_quality update --window 30  ^(Phase FF: closed-loop^) >> "%LOG%"
"%PY%" -m analytics.decision_quality update --window 30 --market both >> "%LOG%" 2>&1
echo DECISION-QUALITY exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [ANOMALIES] data_anomalies  ^(Phase FF Bloco 2.2: Benford + MAD^) >> "%LOG%"
"%PY%" -m analytics.data_anomalies >> "%LOG%" 2>&1
echo ANOMALIES exit code (informational): %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [REPORT US] us_portfolio_report.py >> "%LOG%"
"%PY%" scripts\us_portfolio_report.py >> "%LOG%" 2>&1
echo REPORT-US exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [WEEKLY] weekly_report.py >> "%LOG%"
"%PY%" scripts\weekly_report.py --days 7 >> "%LOG%" 2>&1
echo WEEKLY exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [BRIEFING] portfolio_report.py --md >> "%LOG%"
"%PY%" scripts\portfolio_report.py --md >> "%LOG%" 2>&1
echo BRIEFING exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [PERPETUUM] perpetuum_master.py  ^(retry x2, Ollama+Tavily heavy^) >> "%LOG%"
"%PY%" scripts\_retry.py --tag PERPETUUM --attempts 2 --backoff 300 --timeout 3600 -- "%PY%" agents\perpetuum_master.py >> "%LOG%" 2>&1
echo PERPETUUM exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [PAPER-CLOSE] paper_trade_close.py  ^(F1: fecha signals expirados^) >> "%LOG%"
"%PY%" scripts\paper_trade_close.py >> "%LOG%" 2>&1
echo PAPER-CLOSE exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [PRED-EVAL] predictions_evaluate.py  ^(C.2: track record analysts^) >> "%LOG%"
"%PY%" scripts\predictions_evaluate.py >> "%LOG%" 2>&1
echo PRED-EVAL exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [CLIPPINGS-INGEST] library.clippings_ingest --rag-build >> "%LOG%"
"%PY%" -m library.clippings_ingest --rag-build >> "%LOG%" 2>&1
echo CLIPPINGS-INGEST exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [GLOSSARY] build_glossary.py  ^(idempotent - re-build entries + index^) >> "%LOG%"
"%PY%" scripts\build_glossary.py --backlinks --quiet >> "%LOG%" 2>&1
echo GLOSSARY exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [TUTOR] dossier_tutor.py  ^(re-inject tutor sections idempotently^) >> "%LOG%"
"%PY%" scripts\dossier_tutor.py --quiet >> "%LOG%" 2>&1
echo TUTOR exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [TICKER-INSIGHTS] inject_ticker_insights.py  ^(YouTube+Podcast+Analyst per ticker^) >> "%LOG%"
"%PY%" scripts\inject_ticker_insights.py --quiet >> "%LOG%" 2>&1
echo TICKER-INSIGHTS exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [KNOWLEDGE-CARDS] build_knowledge_cards.py  ^(skip-existing, only new^) >> "%LOG%"
"%PY%" scripts\build_knowledge_cards.py --quiet >> "%LOG%" 2>&1
echo KNOWLEDGE-CARDS exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [RESEARCH-DIGEST] research_digest.py  ^(Bibliotheca daily report^) >> "%LOG%"
"%PY%" scripts\research_digest.py --quiet >> "%LOG%" 2>&1
echo RESEARCH-DIGEST exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [DAILY-SYNTHESIS] daily_synthesizer  ^(24h aggregator + Qwen narrative^) >> "%LOG%"
"%PY%" -m agents.daily_synthesizer --hours 24 --max-top 8 --quiet >> "%LOG%" 2>&1
echo DAILY-SYNTHESIS exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [TELEGRAM-BRIEF] captains_log_telegram.py  ^(retry x3, Telegram API^) >> "%LOG%"
"%PY%" scripts\_retry.py --tag TELEGRAM-BRIEF --attempts 3 --backoff 30,120,300 --timeout 120 -- "%PY%" scripts\captains_log_telegram.py --silent >> "%LOG%" 2>&1
echo TELEGRAM-BRIEF exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [CSV] export_macro_csv.py >> "%LOG%"
"%PY%" scripts\export_macro_csv.py >> "%LOG%" 2>&1
echo CSV exit code: %errorlevel% >> "%LOG%"

REM ─── Hub consolidation (Wave 3 Deep Merge, 2026-05-14) ───
REM Refresh per-ticker hubs from latest JSON/filings/etc, then bury any per-ticker
REM source files that appeared during the day, then refresh the master index.
set PYTHONIOENCODING=utf-8
echo. >> "%LOG%"
echo [HUBS-BUILD] build_merged_hubs.py  ^(refresh 187 ticker hubs from filesystem^) >> "%LOG%"
"%PY%" scripts\build_merged_hubs.py >> "%LOG%" 2>&1
echo HUBS-BUILD exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [HUBS-BURY] bury_per_ticker_sources.py  ^(cemetery any new per-ticker source^) >> "%LOG%"
"%PY%" scripts\bury_per_ticker_sources.py >> "%LOG%" 2>&1
echo HUBS-BURY exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [HUBS-INDEX] build_tickers_index.py >> "%LOG%"
"%PY%" scripts\build_tickers_index.py >> "%LOG%" 2>&1
echo HUBS-INDEX exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [ROTATE] rotate_logs.py --days 30 >> "%LOG%"
"%PY%" scripts\rotate_logs.py --days 30 >> "%LOG%" 2>&1
echo ROTATE exit code: %errorlevel% >> "%LOG%"

REM Weekly tasks - only on Sunday (DayOfWeek 0)
for /f %%a in ('powershell -NoProfile -Command "(Get-Date).DayOfWeek.value__"') do set DOW=%%a
if "%DOW%"=="0" (
    echo. >> "%LOG%"
    echo [WEEKLY-SUNDAY] design_research.py  ^(retry x3, GitHub+RSS^) >> "%LOG%"
    "%PY%" scripts\_retry.py --tag DESIGN-SCOUT --attempts 3 --backoff 60,300,900 --timeout 600 -- "%PY%" scripts\design_research.py >> "%LOG%" 2>&1
    echo DESIGN-RESEARCH exit code: %errorlevel% >> "%LOG%"
)

:end
REM Release daily lock - hourly/q4h tiers can resume on next tick
"%PY%" -m agents._lock release daily >> "%LOG%" 2>&1
echo Done %time% >> "%LOG%"
endlocal
