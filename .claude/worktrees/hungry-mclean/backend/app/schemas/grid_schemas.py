"""Request/Response schemas for grid operations."""

from pydantic import BaseModel


class PlaceRoomRequest(BaseModel):
    room_type: str = "corridor"
    x: int = 0
    y: int = 0
    w: int = 1
    h: int = 1
    doors: list[dict] | None = None
    trap_type: str | None = None
    bonus_type: str | None = None


class RemoveRoomRequest(BaseModel):
    room_id: str
