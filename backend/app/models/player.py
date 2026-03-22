"""Player state — the central game state model."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .advisor import Advisor
from .character_sheet import CharacterSheet
from .dungeon import Dungeon
from .game_setup import GameConfig
from .monster import Monster
from .pattern import DungeonPattern
from .resources import Resources


class PlayerState(BaseModel):
    """Complete game state.  Serialised to JSON for save/load."""
    game_config: GameConfig | None = None
    day: int = 1
    phase: str = "night"  # night | day | resolution
    lives: int = 3
    treasure: int = 100
    resources: Resources = Field(default_factory=Resources)
    dungeon: Dungeon = Field(default_factory=Dungeon)
    monsters: list[Monster] = Field(default_factory=list)
    advisors: list[Advisor] = Field(default_factory=list)
    character_registry: list[CharacterSheet] = Field(default_factory=list)
    hero_groups_history: list[str] = Field(default_factory=list)
    saved_patterns: list[DungeonPattern] = Field(default_factory=list)
    logs: list[str] = Field(default_factory=list)
