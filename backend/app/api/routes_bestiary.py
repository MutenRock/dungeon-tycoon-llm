"""Bestiary routes — monster species and task assignment."""

from fastapi import APIRouter, Depends

from backend.app.dependencies import get_bestiary_service
from backend.app.schemas.dialogue_schemas import AssignTaskRequest, AssignRoomRequest

router = APIRouter(prefix="/api/bestiary", tags=["bestiary"])


@router.get("/species")
def list_species(bestiary=Depends(get_bestiary_service)):
    return bestiary.get_all_species()


@router.get("/species/{species_id}")
def get_species(species_id: str, bestiary=Depends(get_bestiary_service)):
    species = bestiary.get_species(species_id)
    if not species:
        return {"error": "Species not found"}
    return species


@router.post("/assign-task")
def assign_task(req: AssignTaskRequest, bestiary=Depends(get_bestiary_service)):
    ok, msg = bestiary.assign_task(req.monster_id, req.task)
    return {"success": ok, "message": msg}


@router.post("/assign-room")
def assign_room(req: AssignRoomRequest, bestiary=Depends(get_bestiary_service)):
    ok, msg = bestiary.assign_room(req.monster_id, req.room_id)
    return {"success": ok, "message": msg}
