from fastapi import APIRouter, HTTPException

from backend.app.dependencies import dungeon_service, repo
from backend.app.schemas.grid import PlaceRoomRequest, RemoveRoomRequest
from backend.app.schemas.game import GameStateResponse

router = APIRouter()


@router.post("/place-room", response_model=GameStateResponse)
def place_room(payload: PlaceRoomRequest) -> GameStateResponse:
    success, error = dungeon_service.place_room(payload)
    if not success:
        raise HTTPException(status_code=400, detail=error)
    return GameStateResponse.model_validate(repo.get_state().model_dump())


@router.post("/remove-room", response_model=GameStateResponse)
def remove_room(payload: RemoveRoomRequest) -> GameStateResponse:
    success, error = dungeon_service.remove_room(payload.room_id)
    if not success:
        raise HTTPException(status_code=400, detail=error)
    return GameStateResponse.model_validate(repo.get_state().model_dump())
