from pydantic import BaseModel


class Monster(BaseModel):
    id: str
    name: str
    kind: str
    power: int
    assigned_room_id: str | None = None
