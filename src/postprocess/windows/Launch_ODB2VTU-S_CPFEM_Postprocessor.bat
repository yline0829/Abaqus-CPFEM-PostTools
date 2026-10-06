@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ODB2VTU-S_CPFEM_Postprocessor.ps1"
endlocal
