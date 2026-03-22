#!/bin/bash
# Start both backend and frontend dev servers

echo "Starting Dungeon Tycoon LLM..."
echo ""

# Backend
echo "Starting backend on http://localhost:8000"
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Frontend
echo "Starting frontend on http://localhost:3000"
python -m http.server 3000 --directory frontend &
FRONTEND_PID=$!

echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "New Game: http://localhost:3000/setup.html"
echo "Game:     http://localhost:3000/index.html"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
