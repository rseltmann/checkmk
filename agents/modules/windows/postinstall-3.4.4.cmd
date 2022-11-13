:: *********************************************
:: Post installer scripts for Python Module
:: Windows Agent will call this script after 
:: module installation
:: *********************************************

@echo off

if not exist .\.venv\Scripts powershell Write-Host "`absent required folder .venv" -foreground red && exit /b 1
if not exist .\Lib powershell Write-Host "`absent required folder lib" -foreground red && exit /b 2

mklink /J DLLs .\.venv\Scripts
