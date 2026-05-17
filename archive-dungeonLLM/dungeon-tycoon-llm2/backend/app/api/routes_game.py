from fastapi import APIRouter

from backend.app.dependencies import repo
from backend.app.schemas.game import GameStateResponse

router = APIRouter()


@router.get("/state", response_model=GameStateResponse)
def get_state() -> GameStateResponse:
    return GameStateResponse.model_validate(repo.get_state().model_dump())


@router.post("/new", response_model=GameStateResponse)
def new_game() -> GameStateResponse:
    state = repo.reset()
    return GameStateResponse.model_validate(state.model_dump())
