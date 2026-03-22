"""Bestiary: monster species management and task assignment."""

from __future__ import annotations

import json
from pathlib import Path

from backend.app.repositories.game_state_repository import GameStateRepository

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


class BestiaryService:
    def __init__(self, repo: GameStateRepository):
        self.repo = repo
        self._species = self._load_species()

    def _load_species(self) -> list[dict]:
        path = DATA_DIR / "monsters.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return []

    def get_all_species(self) -> list[dict]:
        return self._species

    def get_species(self, species_id: str) -> dict | None:
        for s in self._species:
            if s["species_id"] == species_id:
                return s
        return None

    def assign_task(self, monster_id: str, task: str) -> tuple[bool, str]:
        state = self.repo.get_state()
        for monster in state.monsters:
            if monster.id == monster_id:
                species = self.get_species(monster.species)
                if species and task not in species.get("tasks", []):
                    return False, f"{monster.species} cannot perform task '{task}'"
                monster.assigned_task = task
                return True, "ok"
        return False, "Monster not found"

    def assign_room(self, monster_id: str, room_id: str) -> tuple[bool, str]:
        state = self.repo.get_state()
        monster = None
        for m in state.monsters:
            if m.id == monster_id:
                monster = m
                break
        if not monster:
            return False, "Monster not found"

        room = None
        for r in state.dungeon.rooms:
            if r.id == room_id:
                room = r
                break
        if not room:
            return False, "Room not found"

        # Check room capacity from data
        rooms_data = json.loads((DATA_DIR / "rooms.json").read_text(encoding="utf-8"))
        room_def = next((rd for rd in rooms_data if rd["type"] == room.type), None)
        max_monsters = room_def.get("max_monsters", 0) if room_def else 0

        if len(room.assigned_monsters) >= max_monsters:
            return False, f"Room is full ({max_monsters} max)"

        # Remove from previous room
        if monster.assigned_room_id:
            for r in state.dungeon.rooms:
                if r.id == monster.assigned_room_id and monster.id in r.assigned_monsters:
                    r.assigned_monsters.remove(monster.id)

        monster.assigned_room_id = room_id
        room.assigned_monsters.append(monster.id)
        return True, "ok"
