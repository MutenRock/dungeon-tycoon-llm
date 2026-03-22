# Models — Data Structures

All game data is defined as **Pydantic v2 models** for validation, serialisation, and type safety.

## Core Models

| File | Description |
|------|-------------|
| `player.py` | `PlayerState` — the central game state, serialised for save/load |
| `dungeon.py` | `Dungeon` — the 10×10 grid and its rooms |
| `room.py` | `Room`, `DoorConnection` — rooms with multi-size support and door-based pathfinding |
| `hero.py` | `Hero` — adventurers that raid the dungeon, with tiers and classes |
| `monster.py` | `Monster` — creatures assigned to rooms or tasks |
| `resources.py` | `Resources` — wood, stone, meat, vegetables, gold |
| `raid.py` | `RaidResult` — outcome of a day-phase hero raid |

## Extended Models

| File | Description |
|------|-------------|
| `character_sheet.py` | `CharacterSheet`, `KnowledgeSheet` — persistent identity for every NPC (never deleted) |
| `game_setup.py` | `GameConfig`, `PlayerProfile`, `LuciferExchange` — game creation choices |
| `advisor.py` | `Advisor`, `HiddenWish` — dungeon master's inner circle with dialogue mechanics |
| `pattern.py` | `DungeonPattern`, `PatternRoom` — saveable/exportable room layouts |

## Key Design Rules

1. **Character sheets are append-only** — dead entities get `status="dead"` but stay in the registry
2. **Knowledge is codified** — `KnowledgeSheet` uses ID lists, not free text, for deterministic game logic
3. **LLM never decides game logic** — only the hidden-wish score (a float) crosses the LLM→game boundary
4. **Doors are graph edges** — pathfinding uses `DoorConnection`, not position sorting
