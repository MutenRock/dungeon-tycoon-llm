"""Advisor system: conversations, interjections, and hidden wish resolution."""

from __future__ import annotations

import json
import random
from pathlib import Path

from backend.app.models.advisor import Advisor, HiddenWish
from backend.app.models.player import PlayerState
from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.character_service import CharacterService
from backend.app.services.llm_service import LLMService

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _load_advisors_data() -> dict:
    path = DATA_DIR / "advisors.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


# Pre-defined hidden wish objectives
WISH_OBJECTIVES = [
    {"objective": "wants more meat in the dungeon diet", "outcome_positive": "meat_boost", "outcome_negative": "morale_drop"},
    {"objective": "wants the dungeon to focus on vegetable farming", "outcome_positive": "veggie_boost", "outcome_negative": "food_shortage"},
    {"objective": "wants a new trap room built", "outcome_positive": "free_trap_room", "outcome_negative": "monster_injured"},
    {"objective": "wants a day off for the monsters", "outcome_positive": "morale_boost", "outcome_negative": "productivity_drop"},
    {"objective": "wants a promotion to a higher rank", "outcome_positive": "advisor_buff", "outcome_negative": "advisor_sulk"},
    {"objective": "wants to redecorate the boss room", "outcome_positive": "boss_room_buff", "outcome_negative": "wasted_resources"},
    {"objective": "wants revenge on the last hero party", "outcome_positive": "trap_buff", "outcome_negative": "reckless_attack"},
    {"objective": "wants the dungeon master to acknowledge their work", "outcome_positive": "loyalty_boost", "outcome_negative": "loyalty_drop"},
]


class AdvisorService:
    def __init__(self, repo: GameStateRepository, llm: LLMService, char_service: CharacterService):
        self.repo = repo
        self.llm = llm
        self.char_service = char_service
        self._advisors_data = _load_advisors_data()

    def get_advisor(self, advisor_id: str) -> Advisor | None:
        state = self.repo.get_state()
        for a in state.advisors:
            if a.id == advisor_id:
                return a
        return None

    def talk_to(self, advisor_id: str, player_message: str) -> dict:
        """Handle a player message to an advisor. Returns response + wish status."""
        state = self.repo.get_state()
        advisor = self.get_advisor(advisor_id)
        if not advisor:
            return {"error": "Advisor not found"}

        sheet = self.char_service.get_sheet(advisor.character_sheet_id)
        if not sheet:
            return {"error": "Character sheet not found"}

        lang = state.game_config.language if state.game_config else "en"

        # Get personality info
        role_data = self._get_role_data(advisor.role)
        race = sheet.species
        personality = role_data.get("personality_by_race", {}).get(race, {})
        personality_str = json.dumps(personality, ensure_ascii=False)

        # Generate response
        response = self.llm.advisor_dialogue(
            advisor_name=sheet.name,
            advisor_role=advisor.role,
            personality=personality_str,
            player_message=player_message,
            context={"day": state.day, "phase": state.phase, "treasure": state.treasure},
            language=lang,
        )

        # Track conversation
        advisor.conversation_history.append({"role": "player", "content": player_message})
        advisor.conversation_history.append({"role": "advisor", "content": response})
        advisor.last_interaction_day = state.day

        result: dict = {"response": response, "advisor_name": sheet.name}

        # Check if hidden wish should be resolved (after 3+ exchanges)
        if advisor.hidden_wish and not advisor.hidden_wish.resolved and len(advisor.conversation_history) >= 6:
            wish_result = self._resolve_wish(advisor, lang)
            result["wish_resolved"] = wish_result

        return result

    def check_interjections(self) -> list[dict]:
        """Check which advisors want to start a conversation."""
        state = self.repo.get_state()
        interjections = []

        for advisor in state.advisors:
            # 20% chance per advisor per check, if no active conversation
            if advisor.hidden_wish and not advisor.hidden_wish.resolved:
                continue  # already has an active wish
            if random.random() < 0.2:
                self._assign_hidden_wish(advisor)
                sheet = self.char_service.get_sheet(advisor.character_sheet_id)
                name = sheet.name if sheet else advisor.role
                interjections.append({
                    "advisor_id": advisor.id,
                    "advisor_name": name,
                    "role": advisor.role,
                    "message": self._generate_interjection(advisor, state),
                })

        return interjections

    def _assign_hidden_wish(self, advisor: Advisor) -> None:
        wish_data = random.choice(WISH_OBJECTIVES)
        advisor.hidden_wish = HiddenWish(
            objective=wish_data["objective"],
            trigger_condition="conversation",
            outcome_positive=wish_data["outcome_positive"],
            outcome_negative=wish_data["outcome_negative"],
        )
        advisor.conversation_history = []

    def _resolve_wish(self, advisor: Advisor, language: str) -> dict:
        wish = advisor.hidden_wish
        if not wish:
            return {}

        score = self.llm.judge_hidden_wish(
            wish.objective, advisor.conversation_history, language
        )
        wish.score = score
        wish.resolved = True

        success = score >= wish.success_threshold
        outcome = wish.outcome_positive if success else wish.outcome_negative

        return {
            "score": score,
            "success": success,
            "outcome": outcome,
            "objective": wish.objective,
        }

    def _generate_interjection(self, advisor: Advisor, state: PlayerState) -> str:
        lang = state.game_config.language if state.game_config else "en"
        fallback_data = json.loads(
            (DATA_DIR / "fallback_dialogue.json").read_text(encoding="utf-8")
        ) if (DATA_DIR / "fallback_dialogue.json").exists() else {}

        interjections = fallback_data.get("advisor_interjection", {}).get(lang, {})
        return interjections.get(advisor.role, "Ahem... a word, if you please.")

    def _get_role_data(self, role: str) -> dict:
        for r in self._advisors_data.get("roles", []):
            if r["role"] == role:
                return r
        return {}
