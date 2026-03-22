"""Request/Response schemas for dialogue."""

from pydantic import BaseModel


class TalkRequest(BaseModel):
    message: str


class PatternSaveRequest(BaseModel):
    name: str


class PatternImportRequest(BaseModel):
    data: dict


class AssignTaskRequest(BaseModel):
    monster_id: str
    task: str


class AssignRoomRequest(BaseModel):
    monster_id: str
    room_id: str
