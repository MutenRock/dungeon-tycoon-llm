@echo off
REM ============================================================
REM Dungeon Tycoon LLM — Launch script (Windows)
REM ============================================================

cd /d "%~dp0\.."
call venv\Scripts\activate.bat

echo ==========================================
echo   Dungeon Tycoon LLM — Starting...
echo ==========================================
echo.

echo [...] Starting backend on http://localhost:8000
start /b python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

echo [...] Starting frontend on http://localhost:3000
start /b python -m http.server 3000 --directory frontend

timeout /t 2 /nobreak >nul

echo.
echo ==========================================
echo   Servers running!
echo.
echo   New Game:    http://localhost:3000/setup.html
echo   Game:        http://localhost:3000/index.html
echo   Admin Panel: http://localhost:3000/admin.html
echo   API Docs:    http://localhost:8000/docs
echo.
echo   Close this window to stop servers
echo ==========================================

pause >nul
