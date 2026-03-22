"""Game creation configuration and Lucifer intro models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LuciferExchange(BaseModel):
    """One question/answer pair from the Lucifer intro sequence."""
    question: str
    answer: str
    analysis: str = ""  # LLM-derived interpretation


class PlayerProfile(BaseModel):
    """Profile built from the 5-question Lucifer intro."""
    lucifer_answers: list[LuciferExchange] = Field(default_factory=list)
    personality_summary: str = ""
    play_style_hints: list[str] = Field(default_factory=list)


class GameConfig(BaseModel):
    """Choices made at game creation, immutable after start."""
    dungeon_name: str = "The Unnamed Depths"
    monster_species: str = "goblin"  # chosen from bestiary
    advisor_race: str = "goblin"
    player_race: str = "demon"  # the dungeon master's own race
    player_profile: PlayerProfile = Field(default_factory=PlayerProfile)
    language: str = "en"  # "en" | "fr"
