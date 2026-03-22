"""In-memory game state repository with JSON save/load."""

from __future__ import annotations

import json
from pathlib import Path

from backend.app.models.player import PlayerState


class GameStateRepository:
    """Holds the current game state in memory, with optional file persistence."""

    def __init__(self, save_dir: str = "./saves"):
        self._state: PlayerState = PlayerState()
        self._save_dir = Path(save_dir)
        self._save_dir.mkdir(parents=True, exist_ok=True)

    def get_state(self) -> PlayerState:
        return self._state

    def set_state(self, state: PlayerState) -> None:
        self._state = state

    def reset(self) -> PlayerState:
        self._state = PlayerState()
        return self._state

    def save_to_file(self, filename: str = "save.json") -> Path:
        path = self._save_dir / filename
        path.write_text(self._state.model_dump_json(indent=2), encoding="utf-8")
        return path

    def load_from_file(self, filename: str = "save.json") -> PlayerState:
        path = self._save_dir / filename
        if not path.exists():
            return self._state
        data = json.loads(path.read_text(encoding="utf-8"))
        self._state = PlayerState(**data)
        return self._state

    def list_saves(self) -> list[str]:
        return sorted(p.name for p in self._save_dir.glob("*.json"))
