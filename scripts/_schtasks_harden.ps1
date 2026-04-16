# Endurece a tarefa 'investment-intelligence-daily':
#   - corre mesmo em bateria
#   - não para se for para bateria durante a execução
#   - permite que se a hora de início for perdida (PC desligado), corra ao ligar
#
# Corre uma vez. Idempotente. Verifica com schtasks /Query.

$ErrorActionPreference = "Stop"
$name = "investment-intelligence-daily"

$task = Get-ScheduledTask -TaskName $name -ErrorAction Stop
$s = $task.Settings
$s.DisallowStartIfOnBatteries = $false
$s.StopIfGoingOnBatteries = $false
$s.StartWhenAvailable = $true
Set-ScheduledTask -TaskName $name -Settings $s | Out-Null

Write-Host "[ok] $name endurecida:"
Write-Host "  DisallowStartIfOnBatteries = $($s.DisallowStartIfOnBatteries)"
Write-Host "  StopIfGoingOnBatteries     = $($s.StopIfGoingOnBatteries)"
Write-Host "  StartWhenAvailable         = $($s.StartWhenAvailable)"
