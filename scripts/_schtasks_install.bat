@echo off
REM Regista a tarefa diária no Windows Task Scheduler.
REM Corre diariamente às 23:30 (pós-fecho BR + US).
REM Para remover: schtasks /Delete /TN "investment-intelligence-daily" /F

schtasks /Create /TN "investment-intelligence-daily" /TR "\"C:\Users\paidu\investment-intelligence\scripts\daily_run.bat\"" /SC DAILY /ST 23:30 /F
