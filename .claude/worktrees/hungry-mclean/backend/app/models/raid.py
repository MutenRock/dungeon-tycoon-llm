"""Raid result model — outcome of a hero raid."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .hero import Hero


class RaidResult(BaseModel):
    """Result of a day-phase hero raid."""
    raid_id: str = ""
    day: int = 0
    heroes: list[Hero] = Field(default_factory=list)
    survivors: list[Hero] = Field(default_factory=list)
    path: list[str] = Field(default_factory=list)  # room IDs traversed
    success: bool = False  # True if heroes reached boss room
    boss_damage: int = 0
    treasure_delta: int = 0
    logs: list[str] = Field(default_factory=list)
    hero_dialogue: list[str] = Field(default_factory=list)
