@echo off
REM daily_run.bat — pipeline completo BR + US
REM Agendado no Windows Task Scheduler (tarefa: investment-intelligence-daily)
REM Log rotativo em logs/daily_run_YYYY-MM-DD.log

setlocal
set ROOT=C:\Users\paidu\investment-intelligence
set PY=%ROOT%\.venv\Scripts\python.exe
set PYTHONIOENCODING=utf-8

REM timestamp (locale-independent via PowerShell)
for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set DATESTAMP=%%a
set LOG=%ROOT%\logs\daily_run_%DATESTAMP%.log

echo ======================================== >> "%LOG%"
echo daily_run.bat  %date% %time% >> "%LOG%"
echo ======================================== >> "%LOG%"

cd /d "%ROOT%"

echo [BR] daily_update.py >> "%LOG%"
"%PY%" scripts\daily_update.py >> "%LOG%" 2>&1
echo BR exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [CVM] cvm_monitor.py >> "%LOG%"
"%PY%" monitors\cvm_monitor.py >> "%LOG%" 2>&1
echo CVM exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [CVM-PDF] cvm_pdf_extractor.py --limit 20  (best-effort, CVM RAD flaky) >> "%LOG%"
"%PY%" monitors\cvm_pdf_extractor.py --limit 20 >> "%LOG%" 2>&1
REM não propagamos exit code — extractor é best-effort
echo CVM-PDF exit code (ignored): %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [TAXLOTS] auto_import_taxlots.py  ^(picks up Downloads/taxlots.csv if newer^) >> "%LOG%"
"%PY%" scripts\auto_import_taxlots.py --quiet >> "%LOG%" 2>&1
echo TAXLOTS exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [US] daily_update_us.py >> "%LOG%"
"%PY%" scripts\daily_update_us.py >> "%LOG%" 2>&1
echo US exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [SEC] sec_monitor.py --lookback-days 30 >> "%LOG%"
"%PY%" monitors\sec_monitor.py --lookback-days 30 >> "%LOG%" 2>&1
echo SEC exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [BENCHMARKS] refresh_benchmarks.py  ^(Phase FF: SPY/BOVA11/sector ETFs^) >> "%LOG%"
"%PY%" scripts\refresh_benchmarks.py --quiet >> "%LOG%" 2>&1
echo BENCHMARKS exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [VH-RECORD] verdict_history record  ^(Phase FF: snapshot today's verdicts, idempotent per ticker+date^) >> "%LOG%"
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
echo [TRIGGERS] trigger_monitor.py >> "%LOG%"
"%PY%" scripts\trigger_monitor.py >> "%LOG%" 2>&1
echo TRIGGERS exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [PERPETUUM] perpetuum_master.py  ^(11 perpetuums incl. autoresearch K^) >> "%LOG%"
"%PY%" agents\perpetuum_master.py >> "%LOG%" 2>&1
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
echo [CLIPPINGS-INGEST] library.clippings_ingest --rag-build  ^(novos clippings -> RAG^) >> "%LOG%"
"%PY%" -m library.clippings_ingest --rag-build >> "%LOG%" 2>&1
echo CLIPPINGS-INGEST exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [GLOSSARY] build_glossary.py  ^(idempotent — re-build entries + index^) >> "%LOG%"
"%PY%" scripts\build_glossary.py --backlinks --quiet >> "%LOG%" 2>&1
echo GLOSSARY exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [TUTOR] dossier_tutor.py  ^(re-inject tutor sections idempotently^) >> "%LOG%"
"%PY%" scripts\dossier_tutor.py --quiet >> "%LOG%" 2>&1
echo TUTOR exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [KNOWLEDGE-CARDS] build_knowledge_cards.py  ^(skip-existing, only new^) >> "%LOG%"
"%PY%" scripts\build_knowledge_cards.py --quiet >> "%LOG%" 2>&1
echo KNOWLEDGE-CARDS exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [RESEARCH-DIGEST] research_digest.py  ^(Bibliotheca daily report^) >> "%LOG%"
"%PY%" scripts\research_digest.py --quiet >> "%LOG%" 2>&1
echo RESEARCH-DIGEST exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [TELEGRAM-BRIEF] captains_log_telegram.py  ^(Phase H: morning push^) >> "%LOG%"
"%PY%" scripts\captains_log_telegram.py --silent >> "%LOG%" 2>&1
echo TELEGRAM-BRIEF exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [NOTIFY] notify_events.py --hours 48 >> "%LOG%"
"%PY%" scripts\notify_events.py --hours 48 >> "%LOG%" 2>&1
echo NOTIFY exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [CSV] export_macro_csv.py >> "%LOG%"
"%PY%" scripts\export_macro_csv.py >> "%LOG%" 2>&1
echo CSV exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [ROTATE] rotate_logs.py --days 30 >> "%LOG%"
"%PY%" scripts\rotate_logs.py --days 30 >> "%LOG%" 2>&1
echo ROTATE exit code: %errorlevel% >> "%LOG%"

REM Weekly tasks — only on Sunday (DayOfWeek 0)
for /f %%a in ('powershell -NoProfile -Command "(Get-Date).DayOfWeek.value__"') do set DOW=%%a
if "%DOW%"=="0" (
    echo. >> "%LOG%"
    echo [WEEKLY-SUNDAY] design_research.py  ^(Helena Linha continuous scout^) >> "%LOG%"
    "%PY%" scripts\design_research.py >> "%LOG%" 2>&1
    echo DESIGN-RESEARCH exit code: %errorlevel% >> "%LOG%"
)

echo Done %time% >> "%LOG%"
endlocal
