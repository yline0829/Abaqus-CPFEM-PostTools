$ErrorActionPreference = "SilentlyContinue"

Write-Host "Abaqus Data Exporter - Environment Check" -ForegroundColor Cyan
Write-Host ""

$abaqus = Get-Command abaqus -ErrorAction SilentlyContinue
if ($abaqus) {
    Write-Host "[OK] Abaqus command found:" -ForegroundColor Green
    Write-Host "     $($abaqus.Source)"
} else {
    Write-Host "[WARN] Abaqus command was not found in PATH." -ForegroundColor Yellow
    Write-Host "       The GUI can still launch, but ODB reading/export requires"
    Write-Host "       a working Abaqus installation and the 'abaqus' command."
}

$ps = $PSVersionTable.PSVersion
Write-Host ""
Write-Host "[OK] PowerShell: $ps" -ForegroundColor Green

Write-Host ""
Write-Host "Required runtime:"
Write-Host "  - Windows"
Write-Host "  - Abaqus/CAE or Abaqus Python with odbAccess"
Write-Host "  - 'abaqus' command available from Command Prompt"
Write-Host ""
Read-Host "Press Enter to close"
