"""Dungeon pattern save/load/export/import."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.app.models.pattern import DungeonPattern, PatternRoom
from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.utils.ids import generate_id


class PatternService:
    def __init__(self, repo: GameStateRepository):
        self.repo = repo

    def save_current_layout(self, name: str) -> DungeonPattern:
        """Save current dungeon layout as a reusable pattern."""
        state = self.repo.get_state()
        rooms = []
        for room in state.dungeon.rooms:
            rooms.append(PatternRoom(
                type=room.type,
                dx=room.x,
                dy=room.y,
                w=room.w,
                h=room.h,
                doors=[d.direction for d in room.doors],
            ))

        pattern = DungeonPattern(
            id=generate_id("pat"),
            name=name,
            rooms=rooms,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        state.saved_patterns.append(pattern)
        return pattern

    def list_patterns(self) -> list[DungeonPattern]:
        return self.repo.get_state().saved_patterns

    def get_pattern(self, pattern_id: str) -> DungeonPattern | None:
        for p in self.repo.get_state().saved_patterns:
            if p.id == pattern_id:
                return p
        return None

    def export_pattern(self, pattern_id: str) -> dict | None:
        pattern = self.get_pattern(pattern_id)
        if not pattern:
            return None
        return pattern.model_dump()

    def import_pattern(self, data: dict) -> DungeonPattern:
        pattern = DungeonPattern(**data)
        pattern.id = generate_id("pat")  # new ID on import
        self.repo.get_state().saved_patterns.append(pattern)
        return pattern
