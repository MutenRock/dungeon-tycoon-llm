@echo off
REM ============================================================
REM Dungeon Tycoon LLM — Install script (Windows)
REM ============================================================

echo ==========================================
echo   Dungeon Tycoon LLM — Installation
echo ==========================================
echo.

cd /d "%~dp0\.."

REM --- Python check ---
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.11+ is required. Install from https://python.org
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set PYVER=%%i
echo [OK] Python %PYVER% found

REM --- Virtual environment ---
if not exist "venv" (
    echo [...] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM --- Activate and install ---
call venv\Scripts\activate.bat
echo [...] Installing Python dependencies...
pip install -r requirements.txt --quiet
echo [OK] Dependencies installed

REM --- .env file ---
if not exist ".env" (
    copy .env.example .env >nul
    echo [OK] .env created from .env.example
) else (
    echo [OK] .env already exists
)

REM --- Saves directory ---
if not exist "saves" mkdir saves
echo [OK] saves\ directory ready

REM --- Ollama check ---
echo.
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [!] Ollama not found. Install from https://ollama.com
    echo     Or set LLM_BACKEND=anthropic in .env
) else (
    echo [OK] Ollama found
    echo [!] Make sure to run: ollama pull mistral
)

echo.
echo ==========================================
echo   Installation complete!
echo   Run: scripts\start.bat
echo ==========================================
pause
