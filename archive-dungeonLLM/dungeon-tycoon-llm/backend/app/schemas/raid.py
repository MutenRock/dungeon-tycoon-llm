from pydantic import BaseModel, Field

from backend.app.models.hero import Hero


class RaidResponse(BaseModel):
    id: str
    heroes: list[Hero] = Field(default_factory=list)
    path: list[str] = Field(default_factory=list)
    success: bool = False
    treasure_delta: int = 0
    boss_damage: int = 0
    logs: list[str] = Field(default_factory=list)
