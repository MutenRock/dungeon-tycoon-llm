"""Game creation and Lucifer intro routes."""

from fastapi import APIRouter, Depends

from backend.app.dependencies import get_setup_service
from backend.app.schemas.setup_schemas import CreateGameRequest, LuciferRespondRequest

router = APIRouter(prefix="/api/setup", tags=["setup"])


@router.get("/bestiary")
def get_bestiary(setup=Depends(get_setup_service)):
    return setup.get_bestiary()


@router.get("/dungeon-names")
def get_dungeon_names(setup=Depends(get_setup_service)):
    return setup.get_dungeon_names()


@router.get("/races")
def get_races(setup=Depends(get_setup_service)):
    return {"races": setup.get_available_races()}


@router.post("/create-game")
def create_game(req: CreateGameRequest, setup=Depends(get_setup_service)):
    from backend.app.models.game_setup import GameConfig
    config = GameConfig(
        dungeon_name=req.dungeon_name,
        monster_species=req.monster_species,
        advisor_race=req.advisor_race,
        player_race=req.player_race,
        language=req.language,
    )
    state = setup.create_game(config)
    return state.model_dump()


@router.post("/lucifer/start")
def start_lucifer(language: str = "en", setup=Depends(get_setup_service)):
    question = setup.start_lucifer_intro(language)
    return {"step": 1, "question": question}


@router.post("/lucifer/respond")
def respond_lucifer(req: LuciferRespondRequest, setup=Depends(get_setup_service)):
    result = setup.process_lucifer_answer(
        step=req.step,
        question=req.question,
        answer=req.answer,
        previous=req.previous_exchanges,
        language=req.language,
    )
    return result
