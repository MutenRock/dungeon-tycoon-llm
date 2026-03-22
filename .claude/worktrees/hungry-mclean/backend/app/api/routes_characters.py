"""Character sheet routes."""

from fastapi import APIRouter, Depends

from backend.app.dependencies import get_char_service

router = APIRouter(prefix="/api/characters", tags=["characters"])


@router.get("/")
def list_characters(
    entity_type: str | None = None,
    status: str | None = None,
    chars=Depends(get_char_service),
):
    sheets = chars.get_all(entity_type=entity_type, status=status)
    return [s.model_dump() for s in sheets]


@router.get("/{character_id}")
def get_character(character_id: str, chars=Depends(get_char_service)):
    sheet = chars.get_sheet(character_id)
    if not sheet:
        return {"error": "Character not found"}
    return sheet.model_dump()


@router.get("/heroes/all")
def list_heroes(chars=Depends(get_char_service)):
    return [s.model_dump() for s in chars.get_all(entity_type="hero")]


@router.get("/monsters/all")
def list_monsters(chars=Depends(get_char_service)):
    return [s.model_dump() for s in chars.get_all(entity_type="monster")]


@router.get("/advisors/all")
def list_advisors(chars=Depends(get_char_service)):
    return [s.model_dump() for s in chars.get_all(entity_type="advisor")]
