from pydantic import BaseModel, Field

from backend.app.models.dungeon import Dungeon
from backend.app.models.monster import Monster
from backend.app.models.resources import Resources


class PlayerState(BaseModel):
    day: int = 1
    phase: str = "night"
    lives: int = 3
    treasure: int = 100
    resources: Resources = Field(default_factory=Resources)
    dungeon: Dungeon = Field(default_factory=Dungeon)
    monsters: list[Monster] = Field(default_factory=list)
    logs: list[str] = Field(default_factory=list)
