@echo off
REM Investment Intelligence — live dashboard launcher
REM Helena Linha v1 (2026-04-25)
REM
REM Comportamento:
REM   1. Se streamlit ja esta a correr na porta 8501 -> apenas abre o browser.
REM   2. Caso contrario -> arranca streamlit com hot-reload (runOnSave),
REM      espera ~4s, abre o browser.
REM
REM Hot-reload: qualquer save em scripts/*.py ou ficheiros importados re-renderiza
REM o dashboard automaticamente. O shortcut no Desktop nao precisa ser recriado.

setlocal
set "ROOT=%~dp0.."
pushd "%ROOT%"

REM Detect if port 8501 is already listening
netstat -an | findstr "LISTENING" | findstr ":8501" >nul 2>&1
if %errorlevel%==0 (
    echo [Investment Intelligence] Server already running on :8501. Opening browser...
    start "" "http://localhost:8501"
    goto :done
)

REM Start streamlit in a minimized persistent window with hot-reload enabled
echo [Investment Intelligence] Starting dashboard with hot-reload...
start "Investment Intelligence" /MIN cmd /k ".venv\Scripts\streamlit.exe run scripts\dashboard_app.py --server.port 8501 --server.runOnSave true --server.headless true --browser.gatherUsageStats false"

REM Wait for streamlit to bind to 8501 (poll up to ~10s)
set /a tries=0
:wait
timeout /t 1 /nobreak >nul
netstat -an | findstr "LISTENING" | findstr ":8501" >nul 2>&1
if %errorlevel%==0 goto :open
set /a tries+=1
if %tries% lss 10 goto :wait
echo [Investment Intelligence] Warning: server slow to start, opening browser anyway.

:open
start "" "http://localhost:8501"

:done
popd
endlocal
exit /b 0
