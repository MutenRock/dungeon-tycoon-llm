"""Raid and turn routes."""

from fastapi import APIRouter, Depends

from backend.app.dependencies import get_raid_service

router = APIRouter(prefix="/api/turn", tags=["turn"])


@router.post("/night/resolve")
def resolve_night(raid=Depends(get_raid_service)):
    income = raid.resolve_night()
    return {"income": income}


@router.post("/day/start-raid")
def start_raid(raid=Depends(get_raid_service)):
    result = raid.start_raid()
    return result.model_dump()
