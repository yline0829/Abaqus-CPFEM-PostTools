@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Abaqus_Data_Exporter.ps1"
echo.
echo Press any key to close...
pause >nul
endlocal
