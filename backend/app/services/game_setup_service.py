"""Orchestrates game creation: config, advisors, initial monsters, Lucifer intro."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from backend.app.core.constants import AdvisorRole, LUCIFER_QUESTIONS
from backend.app.models.advisor import Advisor, HiddenWish
from backend.app.models.character_sheet import CharacterSheet, CharacterStats
from backend.app.models.game_setup import GameConfig, LuciferExchange, PlayerProfile
from backend.app.models.monster import Monster
from backend.app.models.player import PlayerState
from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.llm_service import LLMService
from backend.app.utils.ids import generate_id

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _load_json(name: str) -> list | dict:
    path = DATA_DIR / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


class GameSetupService:
    def __init__(self, repo: GameStateRepository, llm: LLMService):
        self.repo = repo
        self.llm = llm
        self._advisors_data = _load_json("advisors.json")
        self._monsters_data = _load_json("monsters.json")
        self._names_data = _load_json("dungeon_names.json")

    # ------------------------------------------------------------------
    # Data queries
    # ------------------------------------------------------------------

    def get_bestiary(self) -> list[dict]:
        return self._monsters_data if isinstance(self._monsters_data, list) else []

    def get_dungeon_names(self) -> dict:
        return self._names_data

    def get_advisor_roles(self) -> list[dict]:
        return self._advisors_data.get("roles", [])

    def get_available_races(self) -> list[str]:
        return [s["species_id"] for s in self.get_bestiary()]

    # ------------------------------------------------------------------
    # Lucifer intro
    # ------------------------------------------------------------------

    def start_lucifer_intro(self, language: str = "en") -> str:
        """Return the first Lucifer question."""
        return self.llm.lucifer_question(1, [], language)

    def process_lucifer_answer(
        self, step: int, question: str, answer: str, previous: list[dict], language: str = "en"
    ) -> dict:
        """Process a player answer and return analysis + next question (if any)."""
        analysis = self.llm.lucifer_analyze(question, answer, language)
        exchange = {"question": question, "answer": answer, "analysis": analysis}
        previous = previous + [exchange]

        next_question = None
        if step < LUCIFER_QUESTIONS:
            next_question = self.llm.lucifer_question(step + 1, previous, language)

        return {
            "exchange": exchange,
            "next_question": next_question,
            "complete": step >= LUCIFER_QUESTIONS,
            "step": step,
        }

    # ------------------------------------------------------------------
    # Game creation
    # ------------------------------------------------------------------

    def create_game(self, config: GameConfig) -> PlayerState:
        """Create a new game with the given configuration."""
        state = self.repo.reset()
        state.game_config = config

        # Create advisor NPCs
        state.advisors = self._create_advisors(config.advisor_race, config.language)
        for advisor in state.advisors:
            sheet = self._find_sheet(state, advisor.character_sheet_id)
            if sheet:
                state.character_registry.append(sheet)

        # Create starting monsters
        species_data = self._find_species(config.monster_species)
        if species_data:
            for i in range(5):  # start with 5 monsters
                monster, sheet = self._create_monster(species_data, config.language)
                state.monsters.append(monster)
                state.character_registry.append(sheet)

        state.logs.append(f"The dungeon '{config.dungeon_name}' has been founded.")
        self.repo.set_state(state)
        return state

    def _create_advisors(self, race: str, language: str) -> list[Advisor]:
        advisors = []
        roles = self._advisors_data.get("roles", [])
        for role_data in roles:
            role = role_data["role"]
            sheet_id = generate_id("adv")
            name = self.llm.generate_name("advisor", race, language)

            personality = role_data.get("personality_by_race", {}).get(race, {})
            traits = personality.get("traits", [])

            sheet = CharacterSheet(
                id=sheet_id,
                name=name,
                entity_type="advisor",
                species=race,
                role=role,
                stats=CharacterStats(hp=100, max_hp=100, attack=0, defense=0),
                personality_traits=traits,
                created_at=datetime.now(timezone.utc).isoformat(),
            )

            advisor = Advisor(
                id=generate_id("advisor"),
                role=role,
                character_sheet_id=sheet_id,
            )
            advisors.append(advisor)
            # Sheet stored separately — caller adds to registry
            self._temp_sheets = getattr(self, "_temp_sheets", {})
            self._temp_sheets[sheet_id] = sheet

        return advisors

    def _find_sheet(self, state: PlayerState, sheet_id: str) -> CharacterSheet | None:
        sheets = getattr(self, "_temp_sheets", {})
        return sheets.get(sheet_id)

    def _find_species(self, species_id: str) -> dict | None:
        for s in self.get_bestiary():
            if s["species_id"] == species_id:
                return s
        return None

    def _create_monster(self, species_data: dict, language: str) -> tuple[Monster, CharacterSheet]:
        sheet_id = generate_id("cs")
        monster_id = generate_id("mon")
        name = self.llm.generate_name("monster", species_data["species_id"], language)

        sheet = CharacterSheet(
            id=sheet_id,
            name=name,
            entity_type="monster",
            species=species_data["species_id"],
            role="minion",
            stats=CharacterStats(
                hp=species_data.get("base_hp", 8),
                max_hp=species_data.get("base_hp", 8),
                power=species_data.get("base_power", 3),
            ),
            personality_traits=species_data.get("traits", []),
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        monster = Monster(
            id=monster_id,
            name=name,
            kind=species_data["species_id"],
            species=species_data["species_id"],
            power=species_data.get("base_power", 3),
            character_sheet_id=sheet_id,
        )

        return monster, sheet
