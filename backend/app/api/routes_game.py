"""Game state routes."""

from fastapi import APIRouter, Depends

from backend.app.dependencies import get_repo, get_llm

router = APIRouter(prefix="/api/game", tags=["game"])


@router.get("/state")
def get_game_state(repo=Depends(get_repo)):
    return repo.get_state().model_dump()


@router.post("/save")
def save_game(repo=Depends(get_repo)):
    path = repo.save_to_file()
    return {"saved": str(path)}


@router.post("/load")
def load_game(repo=Depends(get_repo)):
    state = repo.load_from_file()
    return state.model_dump()


@router.get("/saves")
def list_saves(repo=Depends(get_repo)):
    return {"saves": repo.list_saves()}
