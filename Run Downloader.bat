@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    start py -u "%~dp0gui.py" %*
    exit /b
)
where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    start python -u "%~dp0gui.py" %*
    exit /b
)
where python3 >nul 2>nul
if %ERRORLEVEL% equ 0 (
    start python3 -u "%~dp0gui.py" %*
    exit /b
)
echo [ERROR] Python 3 not found. Please install Python from https://www.python.org/
pause
