#!/bin/bash
# ============================================================
# Dungeon Tycoon LLM — Launch script (Linux / macOS)
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"
source venv/bin/activate

echo "=========================================="
echo "  Dungeon Tycoon LLM — Starting..."
echo "=========================================="
echo ""

# Backend API (port 8000)
echo "[...] Starting backend on http://localhost:8000"
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Frontend (port 3000)
echo "[...] Starting frontend on http://localhost:3000"
python -m http.server 3000 --directory frontend &
FRONTEND_PID=$!

sleep 1
echo ""
echo "=========================================="
echo "  Servers running!"
echo ""
echo "  New Game:    http://localhost:3000/setup.html"
echo "  Game:        http://localhost:3000/index.html"
echo "  Admin Panel: http://localhost:3000/admin.html"
echo "  API Docs:    http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop"
echo "=========================================="

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
