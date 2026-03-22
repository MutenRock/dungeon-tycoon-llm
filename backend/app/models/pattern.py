"""Dungeon layout patterns — saveable and exportable room configurations."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PatternRoom(BaseModel):
    """A room in a pattern, stored with relative offsets."""
    type: str
    dx: int  # relative x offset from origin
    dy: int  # relative y offset from origin
    w: int = 1
    h: int = 1
    doors: list[str] = Field(default_factory=list)  # directions


class DungeonPattern(BaseModel):
    """A reusable dungeon layout that can be saved/loaded/exported."""
    id: str
    name: str
    rooms: list[PatternRoom] = Field(default_factory=list)
    created_at: str = ""
    metadata: dict = Field(default_factory=dict)
