from __future__ import annotations
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import GameState, Resources, PlaceRoomRequest, AssignMonsterRequest
from .constants import STARTING_RESOURCES, STARTING_TREASURE, BOSS_MAX_LIVES, Phase, RoomType
from .grid import place_room, remove_room, assign_monster
from .raid import simulate_raid
from .economy import generate_resources, apply_upkeep
from .llm import generate_narrative

SAVE_PATH = Path("saves/game.json")

app = FastAPI(title="Dungeon Tycoon LLM", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_state: GameState | None = None


def _get() -> GameState:
    if _state is None:
        raise HTTPException(400, detail="Aucune partie en cours. POST /game/new d'abord.")
    return _state


@app.post("/game/new", response_model=GameState, tags=["game"])
def new_game():
    global _state
    _state = GameState(
        resources=Resources(**STARTING_RESOURCES),
        treasure=STARTING_TREASURE,
        boss_lives=BOSS_MAX_LIVES,
    )
    return _state


@app.get("/game", response_model=GameState, tags=["game"])
def get_game():
    return _get()


@app.post("/game/room", tags=["game"])
def add_room(req: PlaceRoomRequest):
    s = _get()
    if s.phase != Phase.NIGHT:
        raise HTTPException(400, "Construction possible seulement la nuit.")
    ok, msg = place_room(s, req)
    if not ok:
        raise HTTPException(400, msg)
    return {"message": msg, "state": s}


@app.delete("/game/room/{x}/{y}", tags=["game"])
def delete_room(x: int, y: int):
    s = _get()
    if s.phase != Phase.NIGHT:
        raise HTTPException(400, "Démolition possible seulement la nuit.")
    ok, msg = remove_room(s, x, y)
    if not ok:
        raise HTTPException(400, msg)
    return {"message": msg, "state": s}


@app.post("/game/assign", tags=["game"])
def assign(req: AssignMonsterRequest):
    s = _get()
    if s.phase != Phase.NIGHT:
        raise HTTPException(400, "Assignation possible seulement la nuit.")
    ok, msg = assign_monster(s, req.x, req.y, req.monster_type)
    if not ok:
        raise HTTPException(400, msg)
    return {"message": msg, "state": s}


@app.post("/game/end-night", tags=["game"])
def end_night():
    s = _get()
    if s.phase != Phase.NIGHT:
        raise HTTPException(400, "Ce n'est pas la nuit.")
    if not any(r.room_type == RoomType.BOSS_ROOM for r in s.grid):
        raise HTTPException(400, "Placez d'abord la salle du boss (2×1).")
    generate_resources(s)
    s.phase = Phase.DAY
    return {"message": "Le jour se lève… Les héros approchent.", "state": s}


@app.post("/raid/start", tags=["raid"])
async def start_raid():
    s = _get()
    if s.phase != Phase.DAY:
        raise HTTPException(400, "Le raid ne se déclenche que de jour.")
    if s.game_over:
        raise HTTPException(400, "Partie terminée.")

    result = simulate_raid(s)
    apply_upkeep(s)
    result.narrative = await generate_narrative(result, s)
    s.last_raid = result
    s.game_over  = result.game_over
    s.phase      = Phase.NIGHT
    s.turn      += 1
    return result


@app.post("/game/save", tags=["persistence"])
def save_game():
    s = _get()
    SAVE_PATH.parent.mkdir(exist_ok=True)
    SAVE_PATH.write_text(s.model_dump_json(indent=2), encoding="utf-8")
    return {"message": "Partie sauvegardée."}


@app.post("/game/load", response_model=GameState, tags=["persistence"])
def load_game():
    global _state
    if not SAVE_PATH.exists():
        raise HTTPException(404, "Aucune sauvegarde trouvée.")
    _state = GameState(**json.loads(SAVE_PATH.read_text(encoding="utf-8")))
    return _state
