@echo off
REM q4h_run.bat - Phase EE Tiered Scheduler - tier 4-hourly (~10-15min)
REM Steps: cvm_pdf_extractor + dividend/earnings calendars + benchmarks
REM        + auto_verdict_on_filing + trigger_monitor
REM Yields to daily (blocked_by). Hourly does NOT block this; both can run
REM serially via their own locks (this tier holds q4h.lock).
REM Log: logs/q4h_run_YYYY-MM-DD.log (appended across day's 6 invocations)

setlocal
set ROOT=C:\Users\paidu\investment-intelligence
set PY=%ROOT%\.venv\Scripts\python.exe
set PYTHONIOENCODING=utf-8

for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set DATESTAMP=%%a
for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format HH:mm"') do set TIMESTAMP=%%a
set LOG=%ROOT%\logs\q4h_run_%DATESTAMP%.log

cd /d "%ROOT%"

echo ---------------------------------------- >> "%LOG%"
echo q4h_run %DATESTAMP% %TIMESTAMP% >> "%LOG%"

"%PY%" -m agents._lock acquire q4h --blocked-by daily >> "%LOG%" 2>&1
if errorlevel 1 (
    echo Lock busy or daily running - aborting q4h tier >> "%LOG%"
    goto :end
)

REM Health-first: skip tier if required services down (Phase HH-AOW)
"%PY%" -m agents._health check --required ollama yfinance >> "%LOG%" 2>&1
if errorlevel 1 (
    echo Health check failed - required service down, aborting q4h tier >> "%LOG%"
    goto :end
)

echo. >> "%LOG%"
echo [CVM-PDF] cvm_pdf_extractor.py --limit 20 >> "%LOG%"
"%PY%" monitors\cvm_pdf_extractor.py --limit 20 >> "%LOG%" 2>&1
echo CVM-PDF exit code (ignored): %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [DIV-CAL] dividend_calendar.py --holdings >> "%LOG%"
"%PY%" fetchers\dividend_calendar.py --holdings >> "%LOG%" 2>&1
echo DIV-CAL exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [EARN-CAL] earnings_calendar.py --holdings >> "%LOG%"
"%PY%" fetchers\earnings_calendar.py --holdings >> "%LOG%" 2>&1
echo EARN-CAL exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [BENCHMARKS] refresh_benchmarks.py --quiet >> "%LOG%"
"%PY%" scripts\refresh_benchmarks.py --quiet >> "%LOG%" 2>&1
echo BENCHMARKS exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [AUTO-VERDICT] auto_verdict_on_filing.py --since-id >> "%LOG%"
"%PY%" scripts\auto_verdict_on_filing.py --since-id >> "%LOG%" 2>&1
echo AUTO-VERDICT exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [TRIGGERS] trigger_monitor.py >> "%LOG%"
"%PY%" scripts\trigger_monitor.py >> "%LOG%" 2>&1
echo TRIGGERS exit code: %errorlevel% >> "%LOG%"

:end
"%PY%" -m agents._lock release q4h >> "%LOG%" 2>&1
echo Done %TIMESTAMP% >> "%LOG%"
endlocal
