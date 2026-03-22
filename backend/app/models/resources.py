"""Resource model — dungeon economy."""

from __future__ import annotations

from pydantic import BaseModel


class Resources(BaseModel):
    """Resources available to the dungeon master."""
    wood: int = 50
    stone: int = 50
    meat: int = 30  # human meat or animal meat
    vegetables: int = 0  # alternative food source
    gold: int = 0  # currency for special purchases
