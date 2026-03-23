#!/bin/bash
# ============================================================
# Dungeon Tycoon LLM — Install script (Linux / macOS)
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "  Dungeon Tycoon LLM — Installation"
echo "=========================================="
echo ""

cd "$PROJECT_DIR"

# --- Python check ---
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python 3.11+ is required. Install it from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "[OK] Python $PYTHON_VERSION found"

# --- Virtual environment ---
if [ ! -d "venv" ]; then
    echo "[...] Creating virtual environment..."
    python3 -m venv venv
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment already exists"
fi

# --- Activate & install ---
source venv/bin/activate
echo "[...] Installing Python dependencies..."
pip install -r requirements.txt --quiet
echo "[OK] Dependencies installed"

# --- .env file ---
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "[OK] .env created from .env.example"
else
    echo "[OK] .env already exists"
fi

# --- Saves directory ---
mkdir -p saves
echo "[OK] saves/ directory ready"

# --- Ollama check ---
echo ""
if command -v ollama &>/dev/null; then
    echo "[OK] Ollama found"
    if ollama list 2>/dev/null | grep -q "mistral"; then
        echo "[OK] Model 'mistral' available"
    else
        echo "[!] Model 'mistral' not found. Pull it with:"
        echo "    ollama pull mistral"
    fi
else
    echo "[!] Ollama not found. Install from https://ollama.com"
    echo "    Or set LLM_BACKEND=anthropic in .env"
fi

echo ""
echo "=========================================="
echo "  Installation complete!"
echo "  Run: bash scripts/start.sh"
echo "=========================================="
