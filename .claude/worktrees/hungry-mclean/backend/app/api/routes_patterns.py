"""Pattern routes — save/load/export/import dungeon layouts."""

from fastapi import APIRouter, Depends

from backend.app.dependencies import get_pattern_service
from backend.app.schemas.dialogue_schemas import PatternSaveRequest, PatternImportRequest

router = APIRouter(prefix="/api/patterns", tags=["patterns"])


@router.get("/")
def list_patterns(patterns=Depends(get_pattern_service)):
    return [p.model_dump() for p in patterns.list_patterns()]


@router.post("/save")
def save_pattern(req: PatternSaveRequest, patterns=Depends(get_pattern_service)):
    pattern = patterns.save_current_layout(req.name)
    return pattern.model_dump()


@router.post("/load/{pattern_id}")
def load_pattern(pattern_id: str, patterns=Depends(get_pattern_service)):
    pattern = patterns.get_pattern(pattern_id)
    if not pattern:
        return {"error": "Pattern not found"}
    return pattern.model_dump()


@router.post("/export/{pattern_id}")
def export_pattern(pattern_id: str, patterns=Depends(get_pattern_service)):
    data = patterns.export_pattern(pattern_id)
    if not data:
        return {"error": "Pattern not found"}
    return data


@router.post("/import")
def import_pattern(req: PatternImportRequest, patterns=Depends(get_pattern_service)):
    pattern = patterns.import_pattern(req.data)
    return pattern.model_dump()
