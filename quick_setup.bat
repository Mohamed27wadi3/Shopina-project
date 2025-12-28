@echo off
REM Windows Quick Setup launcher for Shopina
REM Runs the PowerShell setup script

set SCRIPT_DIR=%~dp0
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%quick_setup.ps1"
