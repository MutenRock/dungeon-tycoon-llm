from pydantic import BaseModel

from backend.app.models.dungeon import Dungeon
from backend.app.models.monster import Monster
from backend.app.models.resources import Resources


class GameStateResponse(BaseModel):
    day: int
    phase: str
    lives: int
    treasure: int
    resources: Resources
    dungeon: Dungeon
    monsters: list[Monster]
    logs: list[str]
