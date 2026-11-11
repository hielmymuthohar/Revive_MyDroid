@echo off
title ReviveMyDroid - Old Android to Headunit Automation
echo ====================================================================
echo   ReviveMyDroid - Launching Interactive CLI...
echo ====================================================================

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python 3 is not installed or not in your system PATH.
    echo Please install Python 3 from https://www.python.org/downloads/
    pause
    exit /b 1
)

python "%~dp0revive.py"
pause
