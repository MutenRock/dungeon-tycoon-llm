"""Dungeon model — the grid and its rooms."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .room import Room


class Dungeon(BaseModel):
    """The dungeon grid (default 10x10) containing placed rooms."""
    width: int = 10
    height: int = 10
    rooms: list[Room] = Field(default_factory=list)
