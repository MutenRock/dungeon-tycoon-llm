from pydantic import BaseModel, Field


class PlaceRoomRequest(BaseModel):
    room_id: str
    room_type: str
    x: int
    y: int
    w: int = 1
    h: int = 1
    doors: list[str] = Field(default_factory=list)


class RemoveRoomRequest(BaseModel):
    room_id: str
