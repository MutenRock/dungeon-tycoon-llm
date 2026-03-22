"""Dungeon grid routes — room placement and removal."""

from fastapi import APIRouter, Depends

from backend.app.dependencies import get_dungeon_service
from backend.app.schemas.grid_schemas import PlaceRoomRequest, RemoveRoomRequest

router = APIRouter(prefix="/api/grid", tags=["grid"])


@router.post("/place-room")
def place_room(req: PlaceRoomRequest, dungeon=Depends(get_dungeon_service)):
    ok, error, room = dungeon.place_room(
        room_type=req.room_type,
        x=req.x, y=req.y, w=req.w, h=req.h,
        doors=req.doors,
        trap_type=req.trap_type,
        bonus_type=req.bonus_type,
    )
    if not ok:
        return {"success": False, "error": error}
    return {"success": True, "room": room.model_dump() if room else None}


@router.post("/remove-room")
def remove_room(req: RemoveRoomRequest, dungeon=Depends(get_dungeon_service)):
    ok, error = dungeon.remove_room(req.room_id)
    if not ok:
        return {"success": False, "error": error}
    return {"success": True}
