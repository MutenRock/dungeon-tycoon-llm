"""Advisor NPCs — the dungeon master's inner circle.

Each advisor has a role (counselor, high guard, kitchen chief, etc.) and can
initiate conversations with the player via the hidden-wish mechanic.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class HiddenWish(BaseModel):
    """A secret objective assigned when an advisor initiates a conversation.

    The LLM scores the player's response (0.0–1.0).  If the score is below
    success_threshold the negative outcome fires; otherwise the positive one.
    Outcomes are pre-defined in data — the LLM never invents game logic.
    """
    objective: str  # what the NPC secretly wants
    trigger_condition: str  # when they'll bring it up
    success_threshold: float = 0.5
    outcome_positive: str  # event/reward key
    outcome_negative: str  # penalty key
    resolved: bool = False
    score: float | None = None


class Advisor(BaseModel):
    """A named advisor NPC in the dungeon master's court."""
    id: str
    role: str  # counselor, high_guard, kitchen_chief, spy_master, architect
    character_sheet_id: str
    hidden_wish: HiddenWish | None = None
    last_interaction_day: int | None = None
    conversation_history: list[dict] = Field(default_factory=list)
