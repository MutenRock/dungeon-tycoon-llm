from pydantic import BaseModel


class DailySummaryResponse(BaseModel):
    summary: str
