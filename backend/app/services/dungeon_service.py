"""Dungeon management: room placement, removal, and validation."""

from __future__ import annotations

from backend.app.core.constants import GRID_WIDTH, GRID_HEIGHT
from backend.app.models.room import DoorConnection, Room
from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.economy_service import EconomyService
from backend.app.utils.ids import generate_id


class DungeonService:
    def __init__(self, repo: GameStateRepository, economy: EconomyService):
        self.repo = repo
        self.economy = economy

    def place_room(
        self,
        room_type: str,
        x: int,
        y: int,
        w: int = 1,
        h: int = 1,
        doors: list[dict] | None = None,
        trap_type: str | None = None,
        bonus_type: str | None = None,
    ) -> tuple[bool, str | None, Room | None]:
        state = self.repo.get_state()

        # Boundary check
        if x < 0 or y < 0 or x + w > GRID_WIDTH or y + h > GRID_HEIGHT:
            return False, "Room exceeds dungeon bounds.", None

        # Collision check
        for room in state.dungeon.rooms:
            overlap_x = x < room.x + room.w and x + w > room.x
            overlap_y = y < room.y + room.h and y + h > room.y
            if overlap_x and overlap_y:
                return False, "Room overlaps with an existing room.", None

        # Boss room uniqueness
        if room_type == "boss_room":
            if any(r.type == "boss_room" for r in state.dungeon.rooms):
                return False, "Only one boss room allowed.", None

        # Pay cost
        ok, error = self.economy.pay_room_cost(room_type)
        if not ok:
            return False, error, None

        # Create room
        door_connections = []
        if doors:
            for d in doors:
                door_connections.append(DoorConnection(
                    direction=d.get("direction", "north"),
                    connects_to=d.get("connects_to"),
                ))

        room = Room(
            id=generate_id("room"),
            type=room_type,
            x=x, y=y, w=w, h=h,
            doors=door_connections,
            trap_type=trap_type,
            bonus_type=bonus_type,
        )
        state.dungeon.rooms.append(room)
        return True, None, room

    def remove_room(self, room_id: str) -> tuple[bool, str | None]:
        state = self.repo.get_state()
        for i, room in enumerate(state.dungeon.rooms):
            if room.id == room_id:
                if room.type == "boss_room":
                    return False, "Cannot remove the boss room."
                state.dungeon.rooms.pop(i)
                return True, None
        return False, "Room not found."

    def get_room(self, room_id: str) -> Room | None:
        state = self.repo.get_state()
        for room in state.dungeon.rooms:
            if room.id == room_id:
                return room
        return None
