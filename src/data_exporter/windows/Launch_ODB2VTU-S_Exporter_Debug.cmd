@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ODB2VTU-S_Exporter.ps1"
echo.
echo Press any key to close...
pause >nul
endlocal
