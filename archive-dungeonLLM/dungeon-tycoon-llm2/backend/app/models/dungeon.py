from pydantic import BaseModel, Field

from backend.app.models.room import Room


class Dungeon(BaseModel):
    width: int = 10
    height: int = 10
    rooms: list[Room] = Field(default_factory=list)
