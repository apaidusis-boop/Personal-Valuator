@echo off
REM hourly_run.bat - Phase EE Tiered Scheduler - tier hourly (~5min)
REM Steps: SEC monitor lookback 1d + CVM monitor + notify_events --hours 4
REM Yields to daily (blocked_by) - if daily is running, this tier aborts cleanly.
REM Log: logs/hourly_run_YYYY-MM-DD.log (appended across the day's invocations)

setlocal
set ROOT=C:\Users\paidu\investment-intelligence
set PY=%ROOT%\.venv\Scripts\python.exe
set PYTHONIOENCODING=utf-8

for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set DATESTAMP=%%a
for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format HH:mm"') do set TIMESTAMP=%%a
set LOG=%ROOT%\logs\hourly_run_%DATESTAMP%.log

cd /d "%ROOT%"

echo ---------------------------------------- >> "%LOG%"
echo hourly_run %DATESTAMP% %TIMESTAMP% >> "%LOG%"

REM Acquire hourly lock; yield to daily (heavy cron) if running
"%PY%" -m agents._lock acquire hourly --blocked-by daily >> "%LOG%" 2>&1
if errorlevel 1 (
    echo Lock busy or daily running - aborting hourly tier >> "%LOG%"
    goto :end
)

REM Health-first: skip tier if required services down (Phase HH-AOW)
"%PY%" -m agents._health check --required ollama yfinance >> "%LOG%" 2>&1
if errorlevel 1 (
    echo Health check failed - required service down, aborting hourly tier >> "%LOG%"
    goto :end
)

echo. >> "%LOG%"
echo [SEC] sec_monitor.py --lookback-days 1 >> "%LOG%"
"%PY%" monitors\sec_monitor.py --lookback-days 1 >> "%LOG%" 2>&1
echo SEC exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [CVM] cvm_monitor.py >> "%LOG%"
"%PY%" monitors\cvm_monitor.py >> "%LOG%" 2>&1
echo CVM exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [NEWS] news_fetch.py --classify  (Phase II-AOW: stream layer mini) >> "%LOG%"
"%PY%" fetchers\news_fetch.py --classify >> "%LOG%" 2>&1
echo NEWS exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [NOTIFY] notify_events.py --hours 4 >> "%LOG%"
"%PY%" scripts\notify_events.py --hours 4 >> "%LOG%" 2>&1
echo NOTIFY exit code: %errorlevel% >> "%LOG%"

:end
REM Always-release lock on graceful exit. If bat is killed mid-run, the
REM next invocation detects the dead PID and steals the stale lock.
"%PY%" -m agents._lock release hourly >> "%LOG%" 2>&1
echo Done %TIMESTAMP% >> "%LOG%"
endlocal
