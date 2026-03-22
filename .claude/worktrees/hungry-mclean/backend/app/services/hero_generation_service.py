"""Procedural hero generation with tiers, classes, and recurring NPCs."""

from __future__ import annotations

import json
import random
from pathlib import Path

from backend.app.models.character_sheet import CharacterSheet, CharacterStats
from backend.app.models.hero import Hero
from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.character_service import CharacterService
from backend.app.services.llm_service import LLMService
from backend.app.utils.ids import generate_id

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _load_heroes_data() -> list[dict]:
    path = DATA_DIR / "heroes.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def _load_balance() -> dict:
    path = DATA_DIR / "balance.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


class HeroGenerationService:
    def __init__(self, repo: GameStateRepository, llm: LLMService, char_service: CharacterService):
        self.repo = repo
        self.llm = llm
        self.char_service = char_service
        self._heroes_data = _load_heroes_data()
        self._balance = _load_balance()

    def generate_party(self, day: int) -> list[Hero]:
        """Generate a hero raid party appropriate for the current day."""
        size = self._determine_party_size(day)
        heroes: list[Hero] = []
        state = self.repo.get_state()
        lang = state.game_config.language if state.game_config else "en"
        group_id = generate_id("grp")

        # Include recurring heroes (survived previous raids)
        recurring = self._pick_recurring_heroes()
        for sheet in recurring[:max(1, size // 3)]:
            hero = self._hero_from_sheet(sheet, group_id)
            heroes.append(hero)

        # Fill remaining slots with new heroes
        while len(heroes) < size:
            tier = self._pick_tier(day)
            hero_class = random.choice(["knight", "archer", "mage", "rogue", "cleric"])
            name = self.llm.generate_name("hero", "human", lang)
            stats = self._generate_stats(hero_class, tier)

            sheet = self.char_service.create_sheet(
                entity_type="hero",
                name=name,
                species="human",
                role=hero_class,
                stats=stats,
                traits=self._class_traits(hero_class),
            )

            hero = Hero(
                id=generate_id("hero"),
                name=name,
                hero_class=hero_class,
                tier=tier,
                hp=stats.hp,
                max_hp=stats.max_hp,
                attack=stats.attack,
                defense=stats.defense,
                character_sheet_id=sheet.id,
                group_id=group_id,
            )
            heroes.append(hero)

        state.hero_groups_history.append(group_id)
        return heroes

    def _determine_party_size(self, day: int) -> int:
        cfg = self._balance.get("hero_party_size", {"min": 1, "max": 10, "day_scaling": 0.3})
        base = cfg["min"] + int(day * cfg["day_scaling"])
        return min(max(cfg["min"], base + random.randint(-1, 1)), cfg["max"])

    def _pick_tier(self, day: int) -> str:
        thresholds = self._balance.get("day_thresholds", {"early": 1, "mid": 6, "late": 15})
        if day >= thresholds["late"]:
            phase = "late"
        elif day >= thresholds["mid"]:
            phase = "mid"
        else:
            phase = "early"

        weights = self._balance.get("hero_tier_weights_by_day", {}).get(phase, {})
        tiers = list(weights.keys())
        probs = list(weights.values())
        if not tiers:
            return "common"
        return random.choices(tiers, weights=probs, k=1)[0]

    def _generate_stats(self, hero_class: str, tier: str) -> CharacterStats:
        class_data = next((h for h in self._heroes_data if h["hero_class"] == hero_class), None)
        if class_data:
            tier_stats = class_data.get("tier_stats", {}).get(tier, {})
            return CharacterStats(
                hp=tier_stats.get("hp", 10),
                max_hp=tier_stats.get("hp", 10),
                attack=tier_stats.get("attack", 3),
                defense=tier_stats.get("defense", 0),
                speed=tier_stats.get("speed", 1),
            )
        return CharacterStats()

    def _pick_recurring_heroes(self) -> list[CharacterSheet]:
        """Find hero sheets that survived previous raids (status=alive or fled)."""
        all_heroes = self.char_service.get_all(entity_type="hero")
        survivors = [s for s in all_heroes if s.status in ("alive", "fled")]
        if not survivors:
            return []
        random.shuffle(survivors)
        return survivors[:3]

    def _hero_from_sheet(self, sheet: CharacterSheet, group_id: str) -> Hero:
        return Hero(
            id=generate_id("hero"),
            name=sheet.name,
            hero_class=sheet.role,
            tier="veteran",  # recurring heroes are at least veteran
            hp=sheet.stats.max_hp,
            max_hp=sheet.stats.max_hp,
            attack=sheet.stats.attack,
            defense=sheet.stats.defense,
            character_sheet_id=sheet.id,
            group_id=group_id,
        )

    def _class_traits(self, hero_class: str) -> list[str]:
        traits_map = {
            "knight": ["brave", "honorable", "stubborn"],
            "archer": ["cautious", "precise", "patient"],
            "mage": ["intellectual", "curious", "fragile"],
            "rogue": ["sneaky", "opportunistic", "quick"],
            "cleric": ["devout", "compassionate", "stern"],
        }
        return traits_map.get(hero_class, ["adventurous"])
