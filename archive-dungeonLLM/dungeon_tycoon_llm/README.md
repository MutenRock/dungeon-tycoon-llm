# Dungeon Tycoon LLM

Prototype de jeu web : gérez votre donjon la nuit, résistez aux héros le jour.

## Stack
- Backend : FastAPI + Pydantic v2
- Frontend : HTML / CSS / JavaScript (Vanilla)
- Sauvegarde : JSON local (`saves/game.json`)
- LLM : Ollama (couche narrative uniquement, optionnelle)

## Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Lancement

```bash
# Terminal 1 — backend
uvicorn backend.app.main:app --reload

# Terminal 2 — frontend
cd frontend && python -m http.server 8080
```

- API docs : http://127.0.0.1:8000/docs
- Front    : http://localhost:8080
