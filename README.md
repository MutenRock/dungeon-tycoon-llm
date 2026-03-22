# Dungeon Tycoon LLM 🏰

A dungeon management web game prototype where you play as a Dungeon Master, building rooms, managing monsters, and defending against hero raids — powered by LLM-driven NPC dialogue.

## Game Concept

- **Night Phase**: Build rooms on a 10×10 grid, assign monsters to guard or work, manage resources
- **Day Phase**: Procedurally generated hero parties raid your dungeon
- **3 Lives**: Death 1 = -25% treasure, Death 2 = -50%, Death 3 = Game Over
- **Goal**: Maximize your treasure before death
- **LLM Feature**: NPCs talk, advise, gossip, and scheme — powered by Claude AI

## Quick Start

### Requirements

- Python 3.11+
- An Anthropic API key (optional — game works with fallback dialogue)

### Installation

```bash
# Clone and enter the project
git clone <repo-url>
cd dungeon-tycoon-llm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure (optional — for LLM features)
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Run

```bash
# Start the backend API server
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, serve the frontend
python -m http.server 3000 --directory frontend
```

Then open:
- **New Game**: http://localhost:3000/setup.html
- **Game**: http://localhost:3000/index.html
- **API Docs**: http://localhost:8000/docs

## Architecture

```
backend/
  app/
    api/          # FastAPI routes (game, setup, grid, raid, dialogue, characters, bestiary, patterns, llm)
    core/         # Constants and enums
    models/       # Pydantic data models (see models/README.md)
    services/     # Business logic (see services/README.md)
    data/         # Static JSON data (see data/README.md)
    repositories/ # In-memory state + JSON persistence
    schemas/      # Request/Response schemas
    utils/        # ID generation helpers
  tests/          # pytest test suite

frontend/
  index.html      # Main game interface
  setup.html      # Game creation wizard
  assets/
    css/          # Styles (theme, game, dialogue, setup)
    js/           # Modules (api, state, grid, ui, dialogue, chatter, raid_view, i18n, setup)

prompts/          # LLM prompt templates (see prompts/README.md)
docs/             # Game design and technical documentation
saves/            # Game save files (gitignored)
```

## LLM Integration

Two-tier system using the Anthropic SDK:

| Tier | Model | Purpose |
|------|-------|---------|
| **Primary** | Claude Sonnet/Opus | Advisor conversations, Lucifer intro, hidden wish scoring |
| **Fast** | Claude Haiku | Monster chatter, hero dialogue, raid narration, naming |

**The LLM never decides game logic.** Only the hidden-wish score (a float) influences gameplay — outcomes are pre-defined.

Without an API key, all dialogue falls back to pre-written templates.

## Key Features

- **Snap-grid room placement** with 10 room types (corridor, monster, trap, treasure, boss, bonus, barracks, kitchen, workshop, prison)
- **Monster bestiary** with 8 species (goblin, orc, skeleton, imp, troll, centaur, slime, dark elf)
- **5 Advisor NPCs** with personalities shaped by race — counselor, high guard, kitchen chief, spy master, architect
- **Hidden wish mechanic** — advisors have secret objectives; your conversation responses trigger positive or negative events
- **Hero knowledge system** — recurring heroes learn your dungeon's traps and won't fall for them twice
- **Procedural hero generation** — parties of 1-10 heroes with 5 classes and 4 tiers
- **Lucifer intro** — 5-question interview at game start to profile the player
- **Background monster chatter** — goblins gossiping, orcs flirting, skeletons philosophizing
- **Dungeon pattern save/export** — save and share your layouts
- **Bilingual EN/FR** — all UI and LLM prompts support both languages
- **D&D-style lore** — dark fantasy setting with themed dungeon names

## API Endpoints

| Route | Description |
|-------|-------------|
| `GET /api/game/state` | Current game state |
| `POST /api/setup/create-game` | Create new game with config |
| `POST /api/setup/lucifer/start` | Begin Lucifer intro |
| `POST /api/setup/lucifer/respond` | Answer Lucifer's question |
| `POST /api/grid/place-room` | Place room on grid |
| `POST /api/grid/remove-room` | Remove room |
| `POST /api/turn/night/resolve` | Resolve night phase |
| `POST /api/turn/day/start-raid` | Start hero raid |
| `POST /api/dialogue/advisor/{id}/talk` | Talk to advisor |
| `GET /api/dialogue/chatter` | Get monster chatter |
| `GET /api/characters/` | List all character sheets |
| `GET /api/bestiary/species` | List monster species |
| `POST /api/patterns/save` | Save dungeon pattern |
| `GET /api/llm/status` | Check LLM availability |

Full API docs at http://localhost:8000/docs when running.

## Testing

```bash
pytest backend/tests/ -v
```

## License

MIT
