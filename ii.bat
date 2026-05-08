@echo off
REM ii — wrapper para os scripts Python do investment-intelligence.
REM Uso: ii <comando> [args]
REM Exemplos:
REM   ii research ACN --intraday
REM   ii refresh ACN
REM   ii digest --channel "Virtual Asset" --days 30
REM   ii vault "tickers com tese turnaround"
REM   ii fx --total
REM   ii notes add ACN "texto" --tags bull
REM   ii portfolio   (briefing completo)
REM   ii brief       (alias portfolio)
REM   ii obsidian --refresh --holdings-only
REM   ii help

setlocal enabledelayedexpansion
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

set "CMD=%~1"
if "%CMD%"=="" goto :HELP

REM Rebuild args without the first token (the command itself)
set "ARGS="
:COLLECT_ARGS
shift
if "%~1"=="" goto :DONE_ARGS
if defined ARGS (set "ARGS=!ARGS! %1") else (set "ARGS=%1")
goto :COLLECT_ARGS
:DONE_ARGS

REM map shortcuts → python scripts
if /i "%CMD%"=="help" goto :HELP
if /i "%CMD%"=="research" (set "SCRIPT=scripts\research.py") & goto :RUN
if /i "%CMD%"=="analyze" (set "SCRIPT=scripts\analyze_ticker.py") & goto :RUN
if /i "%CMD%"=="refresh" (set "SCRIPT=scripts\refresh_ticker.py") & goto :RUN
if /i "%CMD%"=="digest" (set "SCRIPT=scripts\yt_digest.py") & goto :RUN
if /i "%CMD%"=="ingest" (set "SCRIPT=scripts\yt_ingest.py") & goto :RUN
if /i "%CMD%"=="batch" (set "SCRIPT=scripts\yt_ingest_batch.py") & goto :RUN
if /i "%CMD%"=="reextract" (set "SCRIPT=scripts\yt_reextract.py") & goto :RUN
if /i "%CMD%"=="vault" (set "SCRIPT=scripts\vault_ask.py") & goto :RUN
if /i "%CMD%"=="obsidian" (set "SCRIPT=scripts\obsidian_bridge.py") & goto :RUN
if /i "%CMD%"=="notes" (set "SCRIPT=scripts\notes_cli.py") & goto :RUN
if /i "%CMD%"=="tx" (set "SCRIPT=scripts\tx_cli.py") & goto :RUN
if /i "%CMD%"=="diff" (set "SCRIPT=scripts\daily_diff.py") & goto :RUN
if /i "%CMD%"=="earnings" (set "SCRIPT=fetchers\earnings_calendar.py") & goto :RUN
if /i "%CMD%"=="verdict" (set "SCRIPT=scripts\verdict.py") & goto :RUN
if /i "%CMD%"=="divcal" (set "SCRIPT=fetchers\dividend_calendar.py") & goto :RUN
if /i "%CMD%"=="fairvalue" (set "MODULE=scoring.fair_value") & goto :RUN_MODULE
if /i "%CMD%"=="fv" (set "MODULE=scoring.fair_value") & goto :RUN_MODULE
if /i "%CMD%"=="autoverdict" (set "SCRIPT=scripts\auto_verdict_on_filing.py") & goto :RUN
if /i "%CMD%"=="snapshot" (set "SCRIPT=scripts\snapshot_portfolio.py") & goto :RUN
if /i "%CMD%"=="react" (set "SCRIPT=scripts\earnings_react.py") & goto :RUN
if /i "%CMD%"=="agent" (set "SCRIPT=scripts\agent_morning.py") & goto :RUN
if /i "%CMD%"=="peers" (set "SCRIPT=scripts\peer_compare.py") & goto :RUN
if /i "%CMD%"=="rebalance" (set "SCRIPT=scripts\rebalance.py") & goto :RUN
if /i "%CMD%"=="size" (set "SCRIPT=scripts\position_size.py") & goto :RUN
if /i "%CMD%"=="vh" (set "SCRIPT=scripts\verdict_history.py") & goto :RUN
if /i "%CMD%"=="surprise" (set "SCRIPT=scripts\earnings_surprise.py") & goto :RUN
if /i "%CMD%"=="news" (set "SCRIPT=fetchers\news_fetch.py") & goto :RUN
if /i "%CMD%"=="lots" (set "SCRIPT=scripts\tax_lots_page.py") & goto :RUN
if /i "%CMD%"=="import-lots" (set "SCRIPT=scripts\import_taxlots.py") & goto :RUN
if /i "%CMD%"=="import-positions" (set "SCRIPT=scripts\import_positions.py") & goto :RUN
if /i "%CMD%"=="dashboard" ("%PY%" -m streamlit run "%ROOT%scripts\dashboard_app.py" %ARGS%) & goto :EOF
if /i "%CMD%"=="telegram" ("%PY%" -X utf8 -m notifiers.telegram %ARGS%) & goto :EOF
if /i "%CMD%"=="portfolio" (set "SCRIPT=scripts\portfolio_report.py") & goto :RUN
if /i "%CMD%"=="brief" (set "SCRIPT=scripts\portfolio_report.py") & goto :RUN
if /i "%CMD%"=="drip" (set "SCRIPT=scripts\drip_projection.py") & goto :RUN
if /i "%CMD%"=="triggers" (set "SCRIPT=scripts\trigger_monitor.py") & goto :RUN
if /i "%CMD%"=="actions" (set "SCRIPT=scripts\action_cli.py") & goto :RUN
if /i "%CMD%"=="decide" (set "SCRIPT=scripts\decide.py") & goto :RUN
if /i "%CMD%"=="compare" (set "SCRIPT=scripts\compare_tickers.py") & goto :RUN
if /i "%CMD%"=="weekly" (set "SCRIPT=scripts\weekly_report.py") & goto :RUN
if /i "%CMD%"=="daily" (set "SCRIPT=scripts\daily_update.py") & goto :RUN
if /i "%CMD%"=="megawatch" (set "SCRIPT=scripts\megawatchlist.py") & goto :RUN
if /i "%CMD%"=="fx" ("%PY%" -X utf8 -m analytics.fx %ARGS%) & goto :EOF
if /i "%CMD%"=="altman" ("%PY%" -X utf8 -m scoring.altman %ARGS%) & goto :EOF
if /i "%CMD%"=="piotroski" ("%PY%" -X utf8 -m scoring.piotroski %ARGS%) & goto :EOF
if /i "%CMD%"=="safety" ("%PY%" -X utf8 -m scoring.dividend_safety %ARGS%) & goto :EOF
if /i "%CMD%"=="regime" ("%PY%" -X utf8 -m analytics.regime %ARGS%) & goto :EOF
if /i "%CMD%"=="screen-trend" ("%PY%" -X utf8 -m analytics.screen_trend %ARGS%) & goto :EOF
if /i "%CMD%"=="backtest-yield" ("%PY%" -X utf8 -m analytics.backtest_yield %ARGS%) & goto :EOF
if /i "%CMD%"=="panorama" (set "SCRIPT=scripts\panorama.py") & goto :RUN
if /i "%CMD%"=="dossier" (set "SCRIPT=scripts\dossier.py") & goto :RUN
if /i "%CMD%"=="deepdive" (set "SCRIPT=scripts\deepdive.py") & goto :RUN
if /i "%CMD%"=="beneish" ("%PY%" -X utf8 -m scoring.beneish %ARGS%) & goto :EOF
if /i "%CMD%"=="antonio" ("%PY%" -X utf8 -m agents.chief_of_staff %ARGS%) & goto :EOF
if /i "%CMD%"=="setup" (set "SCRIPT=scripts\localclaw_setup.py") & goto :RUN
if /i "%CMD%"=="crew" (set "SCRIPT=scripts\crew_designer.py") & goto :RUN
if /i "%CMD%"=="topics" ("%PY%" -X utf8 -m analytics.topic_scorer %ARGS%) & goto :EOF
if /i "%CMD%"=="data-health" ("%PY%" -X utf8 -m analytics.data_health %ARGS%) & goto :EOF
if /i "%CMD%"=="health" ("%PY%" -X utf8 -m agents._health %ARGS%) & goto :EOF
if /i "%CMD%"=="skill-scout" ("%PY%" -X utf8 -m agents.skill_scout %ARGS%) & goto :EOF
if /i "%CMD%"=="anomalies" ("%PY%" -X utf8 -m analytics.data_anomalies %ARGS%) & goto :EOF
if /i "%CMD%"=="fetch" ("%PY%" -X utf8 -m fetchers._fallback %ARGS%) & goto :EOF
if /i "%CMD%"=="allocate" ("%PY%" -X utf8 -m strategies.portfolio_engine %ARGS%) & goto :EOF
if /i "%CMD%"=="strategy" ("%PY%" -X utf8 -m strategies.cli %ARGS%) & goto :EOF
if /i "%CMD%"=="roic" ("%PY%" -X utf8 -m scoring.roic %ARGS%) & goto :EOF
if /i "%CMD%"=="hedge" ("%PY%" -X utf8 -c "from strategies.hedge import status; import sys; print(status(sys.argv[1] if len(sys.argv)>1 else 'us'))" %ARGS%) & goto :EOF
if /i "%CMD%"=="overnight" ("%PY%" -X utf8 "%ROOT%scripts\overnight_backfill.py" %ARGS%) & goto :EOF
if /i "%CMD%"=="agent" (set "SCRIPT=agents\_agent.py") & goto :RUN
if /i "%CMD%"=="agent-stats" ("%PY%" -X utf8 -m agents._memory %ARGS%) & goto :EOF
if /i "%CMD%"=="missioncontrol" (cd /d "%ROOT%mission-control" ^&^& npm run dev) & goto :EOF
if /i "%CMD%"=="mission-control" (cd /d "%ROOT%mission-control" ^&^& npm run dev) & goto :EOF
if /i "%CMD%"=="mc" (cd /d "%ROOT%mc-app" ^&^& npm run dev) & goto :EOF
if /i "%CMD%"=="mc-api" (cd /d "%ROOT%mission-control" ^&^& npm run api) & goto :EOF
if /i "%CMD%"=="subs" (set "SCRIPT=scripts\subscriptions_cli.py") & goto :RUN
if /i "%CMD%"=="stats" ("%PY%" -X utf8 -m analytics.metrics %ARGS%) & goto :EOF
if /i "%CMD%"=="refresh-thesis" (set "SCRIPT=scripts\thesis_refresh.py") & goto :RUN
if /i "%CMD%"=="agents" (set "SCRIPT=scripts\agents_cli.py") & goto :RUN
if /i "%CMD%"=="agent-runner" (set "SCRIPT=scripts\agent_runner.py") & goto :RUN
if /i "%CMD%"=="gemma" (call :GEMMA) & goto :EOF
if /i "%CMD%"=="voice" (set "SCRIPT=scripts\voice_cli.py") & goto :RUN

echo Unknown command: %CMD%
echo Run 'ii help' for list.
exit /b 1

:RUN
"%PY%" -X utf8 "%ROOT%%SCRIPT%" %ARGS%
goto :EOF

:RUN_MODULE
"%PY%" -X utf8 -m %MODULE% %ARGS%
goto :EOF

:GEMMA
REM Launch Open WebUI (requires Python 3.11; our .venv is 3.13).
set "OWUI=%LOCALAPPDATA%\Programs\Python\Python311\Scripts\open-webui.exe"
if not exist "%OWUI%" (
    echo [gemma] open-webui nao encontrado em %OWUI%.
    echo         Instala com: "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" -m pip install open-webui
    exit /b 1
)
echo [gemma] A arrancar Open WebUI em http://localhost:8080 ...
echo [gemma] Modelo: gemma4:31b (Ollama em localhost:11434)
echo [gemma] Ctrl+C para parar.
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"
start "" http://localhost:8080
"%OWUI%" serve %ARGS%
goto :EOF

:HELP
echo ii - investment-intelligence CLI
echo.
echo ANALYSIS:
echo   ii deepdive ^<TK^> [--save-obsidian]       ** ELITE DOSSIER ** (Piotroski+Altman+Beneish+Scout+Strategist 5k palavras Llama)
echo   ii deepdive ^<TK^> --no-llm                Quick (3 scores+scout, no dossier)
echo   ii antonio "pergunta livre"               Antonio Carlos (Chief of Staff CLI)
echo   ii dossier ^<TK^>                          Skeleton research dossier (cached, ~5s)
echo   ii dossier --list                        List existing dossiers
echo   ii panorama ^<TK^> [--write]               ** SUPER-COMMAND ** (verdict+peers+triggers+notes+videos+analyst)
echo   ii research ^<TK^> [--intraday] [--md]     Unified memo (PT)
echo   ii analyze ^<TK^>                          Deep dive (legacy)
echo   ii portfolio                             Daily briefing BR+US+RF
echo   ii compare ^<TK1^> ^<TK2^> ...              Side-by-side
echo   ii drip --ticker ^<TK^>                    DRIP projection
echo.
echo SUBSCRIPTIONS (Suno, XP, WSJ, Fool, Finclass):
echo   ii subs setup                            Prepare dirs + instructions
echo   ii subs login --source ^<X^>               Manual login headful (Suno/Finclass)
echo   ii subs test [--source X]                Validate cookies
echo   ii subs fetch [--source X] [--days 7]    Download new reports
echo   ii subs extract [--source X]             Ollama extract insights
echo   ii subs query ^<TK^> [--days 90]           Views on ticker
echo   ii subs latest [--source X]              Recent reports
echo.
echo DATA:
echo   ii refresh ^<TK^>                          Intraday quote (yfinance)
echo   ii refresh --all-holdings                Refresh all holdings
echo   ii fx --total                            Portfolio total BRL
echo   ii fx --usd 1000                         Convert USD to BRL
echo   ii daily                                 Daily fetchers + scoring
echo.
echo QUALITY SCORES:
echo   ii altman ^<TK^>                           Altman Z-Score
echo   ii piotroski ^<TK^>                        Piotroski F-Score
echo   ii beneish ^<TK^>                          Beneish M-Score (manipulation detector)
echo   ii safety ^<TK^>                           Dividend Safety
echo   ii fairvalue ^<TK^>                        Target price (Graham/Buffett/REIT/bank); --holdings, --all, --upside
echo   ii fv --holdings                          Alias para fairvalue
echo.
echo CALENDAR ^& AUTO-VERDICT:
echo   ii divcal --holdings                      Forward ex-dividend dates
echo   ii divcal --upcoming 60                   Lista 60d sem fetch
echo   ii earnings --holdings                    Próximas earnings dates
echo   ii autoverdict --hours 48                 Re-verdict tickers com filing recente
echo   ii autoverdict --since-id                 Watermark mode (cron-friendly)
echo.
echo YOUTUBE:
echo   ii ingest ^<url^>                          Single video
echo   ii batch --channel-last ^<id^> --count N   Batch from channel
echo   ii reextract --all                       Re-run on cached transcripts
echo   ii digest --channel "Virtual Asset" --days 30
echo.
echo OBSIDIAN ^& MEMORY:
echo   ii obsidian --refresh --holdings-only    Export vault
echo   ii vault "^<pergunta em PT^>"              Semantic search
echo   ii notes add ^<TK^> "texto" --tags a,b
echo   ii notes show ^<TK^>
echo.
echo TRANSACTIONS:
echo   ii tx buy ACN 2 176.50 "thesis turnaround"
echo   ii tx sell TEN 35 38.76 "distress signal"
echo   ii tx list --recent 30
echo   ii diff --since 1                        Daily diff
echo   ii earnings --upcoming 30                Earnings ahead
echo.
echo TRIGGERS:
echo   ii triggers                              Dry-run monitor
echo   ii actions list                          Open actions
echo   ii screen-trend                          Quality drift
echo.
echo BACKTEST:
echo   ii backtest-yield --market br --start 2019
echo   ii regime --market us
echo.
echo WATCHLIST:
echo   ii megawatch                             Unified watchlist
echo   ii weekly                                Weekly report
echo.
echo VOICE (local Whisper + Qwen intent + Windows TTS):
echo   ii voice analyze ^<TK^>                    Record voice note for ticker (Whisper + Qwen parse)
echo   ii voice note                            Free-form note (ticker auto-detected from speech)
echo   ii voice brief                           Read morning brief aloud (TTS)
echo   ii voice test                            Check mic + whisper + TTS + Ollama
echo.
echo LOCAL LLM UI:
echo   ii gemma                                 Launch Open WebUI (localhost:8080) com Gemma 3 27B QAT

:EOF
endlocal
