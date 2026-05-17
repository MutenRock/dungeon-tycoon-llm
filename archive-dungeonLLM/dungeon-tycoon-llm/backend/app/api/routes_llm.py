from fastapi import APIRouter

from backend.app.dependencies import llm_service, repo
from backend.app.schemas.llm import DailySummaryResponse

router = APIRouter()


@router.post("/daily-summary", response_model=DailySummaryResponse)
def daily_summary() -> DailySummaryResponse:
    state = repo.get_state()
    summary = llm_service.generate_daily_summary(state)
    return DailySummaryResponse(summary=summary)
