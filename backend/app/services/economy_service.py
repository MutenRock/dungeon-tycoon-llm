"""Economy: resource production, room costs, and worker-based generation."""

from __future__ import annotations

import json
from pathlib import Path

from backend.app.repositories.game_state_repository import GameStateRepository

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _load_balance() -> dict:
    path = DATA_DIR / "balance.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _load_rooms() -> list[dict]:
    path = DATA_DIR / "rooms.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


class EconomyService:
    def __init__(self, repo: GameStateRepository):
        self.repo = repo
        self._balance = _load_balance()
        self._rooms_data = _load_rooms()

    def resolve_night_income(self) -> dict:
        """Calculate and apply night-phase resource income."""
        state = self.repo.get_state()
        income = dict(self._balance.get("night_income", {"wood": 10, "stone": 10, "meat": 5}))
        worker_cfg = self._balance.get("worker_production", {})

        # Count workers by task
        task_counts: dict[str, int] = {}
        for monster in state.monsters:
            if monster.assigned_task == "worker":
                task_counts["worker"] = task_counts.get("worker", 0) + 1
            elif monster.assigned_task == "cook":
                task_counts["cook"] = task_counts.get("cook", 0) + 1

        # Production rooms also contribute
        for room in state.dungeon.rooms:
            room_def = next((r for r in self._rooms_data if r["type"] == room.type), None)
            if room_def and "production" in room_def:
                workers_in_room = len(room.assigned_monsters)
                for resource, amount in room_def["production"].items():
                    income[resource] = income.get(resource, 0) + amount * max(1, workers_in_room)

        # Worker bonus
        for resource in ["wood", "stone"]:
            cfg = worker_cfg.get(resource, {})
            income[resource] = income.get(resource, 0) + cfg.get("per_worker", 0) * task_counts.get("worker", 0)

        for resource in ["meat", "vegetables"]:
            cfg = worker_cfg.get(resource, {})
            income[resource] = income.get(resource, 0) + cfg.get("per_worker", 0) * task_counts.get("cook", 0)

        # Apply income
        state.resources.wood += income.get("wood", 0)
        state.resources.stone += income.get("stone", 0)
        state.resources.meat += income.get("meat", 0)
        state.resources.vegetables += income.get("vegetables", 0)

        return income

    def pay_room_cost(self, room_type: str) -> tuple[bool, str | None]:
        """Deduct room cost from resources. Returns (success, error)."""
        room_def = next((r for r in self._rooms_data if r["type"] == room_type), None)
        if not room_def:
            return False, f"Unknown room type: {room_type}"

        cost = room_def.get("cost", {})
        state = self.repo.get_state()

        if state.resources.wood < cost.get("wood", 0):
            return False, "Not enough wood"
        if state.resources.stone < cost.get("stone", 0):
            return False, "Not enough stone"

        state.resources.wood -= cost.get("wood", 0)
        state.resources.stone -= cost.get("stone", 0)
        return True, None
