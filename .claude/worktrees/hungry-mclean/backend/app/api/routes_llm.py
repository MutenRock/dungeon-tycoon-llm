"""LLM routes — daily summary, configuration, and testing."""

from fastapi import APIRouter, Depends

from backend.app.dependencies import get_llm, get_repo

router = APIRouter(prefix="/api/llm", tags=["llm"])


@router.post("/daily-summary")
def daily_summary(llm=Depends(get_llm), repo=Depends(get_repo)):
    state = repo.get_state()
    lang = state.game_config.language if state.game_config else "en"
    summary_input = (
        f"Day {state.day}, phase {state.phase}, "
        f"treasure {state.treasure}, lives {state.lives}, "
        f"resources: wood={state.resources.wood} stone={state.resources.stone} "
        f"meat={state.resources.meat} vegetables={state.resources.vegetables}, "
        f"rooms={len(state.dungeon.rooms)}, monsters={len(state.monsters)}"
    )
    text = llm.daily_summary(summary_input, lang)
    return {"summary": text}


@router.get("/status")
def llm_status(llm=Depends(get_llm)):
    return {
        "available": llm.available,
        "primary_model": llm.primary_model,
        "fast_model": llm.fast_model,
    }


@router.post("/test")
def test_llm(llm=Depends(get_llm)):
    result = llm._fast(
        "You are a test. Respond with exactly: OK",
        "Say OK",
        10,
    )
    return {"success": result is not None, "response": result or "LLM unavailable"}
