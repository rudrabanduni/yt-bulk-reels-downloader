@echo off
setlocal
cd /d "%~dp0"

set "TARGET_SCRIPT=%~dp0gui.py"
if not "%~1"=="" set "TARGET_SCRIPT=%~dp0download.py"

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py -u "%TARGET_SCRIPT%" %*
    goto end
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python -u "%TARGET_SCRIPT%" %*
    goto end
)

where python3 >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python3 -u "%TARGET_SCRIPT%" %*
    goto end
)

echo [WARNING] Python not found. Running PowerShell fallback...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0download.ps1" %*

:end
if %ERRORLEVEL% neq 0 (
    echo.
    echo Process exited with code %ERRORLEVEL%.
)
pause
