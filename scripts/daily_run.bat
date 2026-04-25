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
echo [US] daily_update_us.py >> "%LOG%"
"%PY%" scripts\daily_update_us.py >> "%LOG%" 2>&1
echo US exit code: %errorlevel% >> "%LOG%"

echo. >> "%LOG%"
echo [SEC] sec_monitor.py --lookback-days 30 >> "%LOG%"
"%PY%" monitors\sec_monitor.py --lookback-days 30 >> "%LOG%" 2>&1
echo SEC exit code: %errorlevel% >> "%LOG%"

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
