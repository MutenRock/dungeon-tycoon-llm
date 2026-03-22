"""Room model — dungeon rooms placed on the grid."""

from __future__ import annotations

from pydantic import BaseModel, Field


class DoorConnection(BaseModel):
    """A door on one side of a room, optionally connected to another room."""
    direction: str  # north, south, east, west
    connects_to: str | None = None  # room_id of connected room


class Room(BaseModel):
    """A room placed on the dungeon grid.

    Rooms snap to integer grid coordinates. The boss room is 2x1.
    Doors define the graph edges used by the pathfinding service.
    """
    id: str = ""
    type: str = "corridor"
    # corridor, monster_room, trap_room, treasure_room, boss_room,
    # bonus_room, barracks, kitchen, workshop, prison
    x: int = 0
    y: int = 0
    w: int = 1
    h: int = 1
    doors: list[DoorConnection] = Field(default_factory=list)
    assigned_monsters: list[str] = Field(default_factory=list)  # monster IDs
    trap_type: str | None = None  # for trap rooms
    bonus_type: str | None = None  # for hero bonus rooms
    times_triggered: int = 0
