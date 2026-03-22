"""Dialogue routes — advisor conversations, chatter, hero dialogue."""

from fastapi import APIRouter, Depends

from backend.app.dependencies import get_advisor_service, get_llm, get_repo
from backend.app.schemas.dialogue_schemas import TalkRequest

router = APIRouter(prefix="/api/dialogue", tags=["dialogue"])


@router.post("/advisor/{advisor_id}/talk")
def talk_to_advisor(advisor_id: str, req: TalkRequest, advisors=Depends(get_advisor_service)):
    return advisors.talk_to(advisor_id, req.message)


@router.get("/advisor/{advisor_id}/history")
def advisor_history(advisor_id: str, advisors=Depends(get_advisor_service)):
    advisor = advisors.get_advisor(advisor_id)
    if not advisor:
        return {"error": "Advisor not found"}
    return {"history": advisor.conversation_history}


@router.post("/advisor/check-interjections")
def check_interjections(advisors=Depends(get_advisor_service)):
    return {"interjections": advisors.check_interjections()}


@router.get("/chatter")
def get_chatter(llm=Depends(get_llm), repo=Depends(get_repo)):
    state = repo.get_state()
    lang = state.game_config.language if state.game_config else "en"
    names = [m.name for m in state.monsters[:4]]
    lines = llm.monster_chatter(names, f"Day {state.day}, phase {state.phase}", lang)
    return {"lines": lines}
