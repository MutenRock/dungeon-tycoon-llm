from fastapi import APIRouter

from backend.app.dependencies import raid_service, repo
from backend.app.schemas.game import GameStateResponse
from backend.app.schemas.raid import RaidResponse

router = APIRouter()


@router.post("/night/resolve", response_model=GameStateResponse)
def resolve_night() -> GameStateResponse:
    state = raid_service.resolve_night()
    return GameStateResponse.model_validate(state.model_dump())


@router.post("/day/start-raid", response_model=RaidResponse)
def start_raid() -> RaidResponse:
    return raid_service.start_raid()


@router.get("/raid/{raid_id}", response_model=RaidResponse)
def get_raid(raid_id: str) -> RaidResponse:
    return raid_service.get_last_raid(raid_id)
