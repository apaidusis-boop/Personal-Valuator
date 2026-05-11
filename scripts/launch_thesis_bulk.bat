@echo off
REM launch_thesis_bulk.bat — corre watchlist thesis bulk em background detached.
REM Sobrevive ao fim da sessão Claude Code.
REM Output em logs/thesis_bulk_YYYY-MM-DD.log

setlocal
set ROOT=C:\Users\paidu\investment-intelligence
set PY=%ROOT%\.venv\Scripts\python.exe
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1

for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HHmmss"') do set STAMP=%%a
set LOG=%ROOT%\logs\thesis_bulk_%STAMP%.log

cd /d "%ROOT%"
echo ======================================== > "%LOG%"
echo thesis_bulk launch %date% %time% >> "%LOG%"
echo ======================================== >> "%LOG%"

"%PY%" -u -m agents.thesis_synthesizer --watchlist-missing >> "%LOG%" 2>&1
echo. >> "%LOG%"
echo Exit code: %errorlevel% >> "%LOG%"
echo Done %date% %time% >> "%LOG%"

endlocal
exit /b 0
