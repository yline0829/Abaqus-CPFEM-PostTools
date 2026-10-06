@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Abaqus_Postprocess_GUI.ps1"
endlocal
