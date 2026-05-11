@echo off
REM start_mission_control.bat — duplo-clique abre tudo.
REM 1) garante que o Next.js dev server está a correr
REM 2) abre o browser default na URL
REM 3) deixa uma janela do servidor visível para fechar quando acabares

setlocal
set "ROOT=%~dp0"
set "URL=http://localhost:3000/"

REM Se já está a correr, só abre o browser e sai
curl -sf -o NUL -w "%%{http_code}" %URL% > "%TEMP%\mc_status.txt" 2>nul
set /p STATUS= < "%TEMP%\mc_status.txt"
del "%TEMP%\mc_status.txt" 2>nul

if "%STATUS%"=="200" (
    echo Mission Control ja esta online — a abrir browser…
    start "" "%URL%"
    exit /b 0
)

echo Mission Control nao esta a correr — a iniciar…
cd /d "%ROOT%mission-control"

REM Inicia o servidor numa nova janela (visivel — fechas quando quiseres)
start "Mission Control [LocalClaw]" cmd /k "npm run dev"

REM Espera o servidor responder antes de abrir o browser
echo A aguardar servidor (max 60s)…
set /a tries=0
:WAIT_LOOP
set /a tries+=1
timeout /t 1 /nobreak >nul
curl -sf -o NUL %URL% >nul 2>&1
if errorlevel 1 (
    if %tries% LSS 60 goto :WAIT_LOOP
    echo Servidor demorou demasiado. Verifica a janela "Mission Control [LocalClaw]".
    pause
    exit /b 1
)

echo OK — a abrir browser.
start "" "%URL%"
exit /b 0
