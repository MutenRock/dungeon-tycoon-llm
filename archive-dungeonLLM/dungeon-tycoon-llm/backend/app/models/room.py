from pydantic import BaseModel, Field


class Room(BaseModel):
    id: str
    type: str
    x: int
    y: int
    w: int = 1
    h: int = 1
    doors: list[str] = Field(default_factory=list)
    assigned_monsters: list[str] = Field(default_factory=list)
