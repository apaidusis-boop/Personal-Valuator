# create_desktop_shortcut.ps1 - Phase Z Z.7
# Cria shortcut no Desktop para o launcher do dashboard.
# Uso: powershell -ExecutionPolicy Bypass -File scripts\create_desktop_shortcut.ps1

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$BatPath = Join-Path $ProjectRoot "start_dashboard.bat"

if (-not (Test-Path $BatPath)) {
    Write-Error "start_dashboard.bat nao encontrado em $BatPath"
    exit 1
}

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Investment Intelligence.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $BatPath
$Shortcut.WorkingDirectory = $ProjectRoot
$Shortcut.Description = "Investment Intelligence Dashboard (Streamlit local)"
$Shortcut.IconLocation = "imageres.dll,67"
$Shortcut.WindowStyle = 1
$Shortcut.Save()

Write-Host ""
Write-Host "OK - Shortcut criado: $ShortcutPath" -ForegroundColor Green
Write-Host "Double-click no Desktop para abrir o dashboard." -ForegroundColor Cyan
Write-Host ""
