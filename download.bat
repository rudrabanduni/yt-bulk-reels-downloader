@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py -u "%~dp0download.py" %*
    goto end
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python -u "%~dp0download.py" %*
    goto end
)

where python3 >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python3 -u "%~dp0download.py" %*
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
