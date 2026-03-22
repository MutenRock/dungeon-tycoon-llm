"""Persistent character sheet system.

Every NPC (hero, monster, advisor) gets a CharacterSheet that is NEVER deleted,
even when the entity dies. This enables recurring heroes, historical lore, and
the knowledge-based learning system.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class CharacterStats(BaseModel):
    """Combat and attribute stats for any entity."""
    hp: int = 10
    max_hp: int = 10
    attack: int = 3
    defense: int = 0
    speed: int = 1
    power: int = 0  # monster-specific


class KnowledgeSheet(BaseModel):
    """Codified knowledge an NPC has about the dungeon.

    Uses IDs (not free text) for deterministic checks in combat/pathfinding.
    The LLM only provides flavour around these mechanical facts.
    """
    rooms_seen: list[str] = Field(default_factory=list)
    traps_triggered: list[str] = Field(default_factory=list)
    monsters_encountered: list[str] = Field(default_factory=list)
    patterns_known: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)  # LLM-generated flavour


class HistoryEntry(BaseModel):
    """A single event in an NPC's life."""
    day: int
    event: str  # entered_dungeon, died, fled, promoted, hired, etc.
    details: str = ""


class CharacterSheet(BaseModel):
    """Persistent identity card for every NPC in the game.

    Append-only in the character registry — dead characters keep status='dead'
    but are never removed.
    """
    id: str
    name: str
    entity_type: str  # "hero" | "monster" | "advisor"
    species: str  # "human", "goblin", "orc", "centaur", etc.
    role: str  # "knight", "counselor", "kitchen_chief", etc.
    stats: CharacterStats = Field(default_factory=CharacterStats)
    status: str = "alive"  # "alive" | "dead" | "fled" | "imprisoned"
    knowledge: KnowledgeSheet = Field(default_factory=KnowledgeSheet)
    personality_traits: list[str] = Field(default_factory=list)
    history: list[HistoryEntry] = Field(default_factory=list)
    created_at: str = ""  # ISO timestamp
    last_seen_day: int | None = None
    version: int = 1
