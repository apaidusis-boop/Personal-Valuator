@echo off
REM vault_autocommit.bat — Phase U.0.5
REM
REM Faz commit horário das mudanças em obsidian_vault/ com timestamp.
REM Não dá push — user controla quando sincronizar com remoto.
REM
REM Instalar como Scheduled Task (Windows):
REM   1. Abre "Task Scheduler"
REM   2. Create Basic Task → "Vault auto-commit"
REM   3. Trigger: Daily, recur every 1 day, every 1 hour for 24 hours
REM   4. Action: Start a program → este .bat
REM   5. Run whether user logged on or not (sem prompt)
REM
REM Para correr manualmente: double-click ou `scripts\vault_autocommit.bat`

setlocal
cd /d "%~dp0.."

REM Verifica se há mudanças no vault (working tree OU staged)
git diff --quiet -- obsidian_vault/
set "WORK=%errorlevel%"
git diff --cached --quiet -- obsidian_vault/
set "STAGED=%errorlevel%"

if "%WORK%"=="0" if "%STAGED%"=="0" (
    REM Sem mudanças, sai silenciosamente
    exit /b 0
)

REM Stage + commit ONLY paths within obsidian_vault/
git add obsidian_vault/
git commit -o obsidian_vault/ -m "vault: auto-commit %date% %time%" --no-verify

if %errorlevel% neq 0 (
    echo [vault_autocommit] commit failed >> logs\vault_autocommit.log
    exit /b 1
)

echo [%date% %time%] vault commit OK >> logs\vault_autocommit.log
endlocal
exit /b 0
