@echo off
REM start_dashboard.bat — Phase Z one-click launcher
REM Arranca Streamlit dashboard + abre browser. Zero CLI necessário.
REM
REM Uso:
REM   1. Double-click neste ficheiro
REM   2. (Opcional) Cria shortcut no Desktop apontando para este .bat
REM
REM Para parar: fecha a janela ou Ctrl+C.

setlocal
title Investment Intelligence — Dashboard

set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

set "PORT=8501"
set "URL=http://localhost:%PORT%"

REM Check if dashboard is already running on the port
powershell -NoProfile -Command "try { (Invoke-WebRequest -Uri '%URL%/_stcore/health' -TimeoutSec 2 -UseBasicParsing).StatusCode } catch { 0 }" > "%TEMP%\ii_health.txt" 2>nul
set /p HEALTH=<"%TEMP%\ii_health.txt"
del "%TEMP%\ii_health.txt" 2>nul

if "%HEALTH%"=="200" (
    echo.
    echo [INFO] Dashboard ja esta a rodar em %URL%
    echo [INFO] A abrir browser...
    start "" "%URL%"
    timeout /t 2 /nobreak >nul
    exit /b 0
)

echo.
echo ====================================================
echo   Investment Intelligence — Dashboard
echo ====================================================
echo.
echo   Porta:  %PORT%
echo   URL:    %URL%
echo.
echo   A arrancar Streamlit... (~5s)
echo   Browser abre automaticamente.
echo.
echo   Para parar: fecha esta janela.
echo ====================================================
echo.

REM Start streamlit (browser opens automatically by default)
"%PY%" -X utf8 -m streamlit run "%ROOT%scripts\dashboard_app.py" ^
    --server.port %PORT% ^
    --server.headless false ^
    --browser.gatherUsageStats false

endlocal
