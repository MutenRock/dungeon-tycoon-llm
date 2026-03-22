"""Hero model — adventurers that raid the dungeon."""

from __future__ import annotations

from pydantic import BaseModel


class Hero(BaseModel):
    """A single hero in a raid party."""
    id: str = ""
    name: str = "Unknown Hero"
    hero_class: str = "knight"  # knight, archer, mage, rogue, cleric
    tier: str = "common"  # common, veteran, local_legend, legendary
    hp: int = 10
    max_hp: int = 10
    attack: int = 3
    defense: int = 0
    character_sheet_id: str = ""
    group_id: str | None = None
