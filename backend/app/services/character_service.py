"""CRUD operations on the persistent character registry."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.app.models.character_sheet import CharacterSheet, CharacterStats, HistoryEntry
from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.utils.ids import generate_id


class CharacterService:
    def __init__(self, repo: GameStateRepository):
        self.repo = repo

    def create_sheet(
        self,
        entity_type: str,
        name: str,
        species: str,
        role: str,
        stats: CharacterStats | None = None,
        traits: list[str] | None = None,
    ) -> CharacterSheet:
        sheet = CharacterSheet(
            id=generate_id("cs"),
            name=name,
            entity_type=entity_type,
            species=species,
            role=role,
            stats=stats or CharacterStats(),
            personality_traits=traits or [],
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        state = self.repo.get_state()
        state.character_registry.append(sheet)
        return sheet

    def get_sheet(self, character_id: str) -> CharacterSheet | None:
        state = self.repo.get_state()
        for sheet in state.character_registry:
            if sheet.id == character_id:
                return sheet
        return None

    def get_all(
        self, entity_type: str | None = None, status: str | None = None
    ) -> list[CharacterSheet]:
        state = self.repo.get_state()
        results = state.character_registry
        if entity_type:
            results = [s for s in results if s.entity_type == entity_type]
        if status:
            results = [s for s in results if s.status == status]
        return results

    def update_knowledge(
        self,
        character_id: str,
        room_id: str | None = None,
        trap_id: str | None = None,
        monster_id: str | None = None,
        pattern_id: str | None = None,
    ) -> bool:
        sheet = self.get_sheet(character_id)
        if not sheet:
            return False
        if room_id and room_id not in sheet.knowledge.rooms_seen:
            sheet.knowledge.rooms_seen.append(room_id)
        if trap_id and trap_id not in sheet.knowledge.traps_triggered:
            sheet.knowledge.traps_triggered.append(trap_id)
        if monster_id and monster_id not in sheet.knowledge.monsters_encountered:
            sheet.knowledge.monsters_encountered.append(monster_id)
        if pattern_id and pattern_id not in sheet.knowledge.patterns_known:
            sheet.knowledge.patterns_known.append(pattern_id)
        return True

    def record_event(self, character_id: str, day: int, event: str, details: str = "") -> bool:
        sheet = self.get_sheet(character_id)
        if not sheet:
            return False
        sheet.history.append(HistoryEntry(day=day, event=event, details=details))
        sheet.last_seen_day = day
        return True

    def mark_dead(self, character_id: str, day: int) -> bool:
        sheet = self.get_sheet(character_id)
        if not sheet:
            return False
        sheet.status = "dead"
        sheet.history.append(HistoryEntry(day=day, event="died", details="Fell in the dungeon"))
        sheet.last_seen_day = day
        return True
