"""Monster model — creatures living in the dungeon."""

from __future__ import annotations

from pydantic import BaseModel


class Monster(BaseModel):
    """A monster under the dungeon master's command."""
    id: str = ""
    name: str = "Unnamed Beast"
    kind: str = "goblin"  # visual/lore subtype
    species: str = "goblin"  # from bestiary species list
    power: int = 4
    assigned_room_id: str | None = None
    assigned_task: str | None = None  # guard, worker, cook, spy, etc.
    character_sheet_id: str = ""
