"""Raid orchestration: day-phase hero raids with procedural generation."""

from __future__ import annotations

from backend.app.models.raid import RaidResult
from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.combat_service import CombatService
from backend.app.services.hero_generation_service import HeroGenerationService
from backend.app.services.llm_service import LLMService
from backend.app.services.pathfinding_service import PathfindingService
from backend.app.services.economy_service import EconomyService
from backend.app.services.character_service import CharacterService
from backend.app.utils.ids import generate_id

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _load_balance() -> dict:
    path = DATA_DIR / "balance.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


class RaidService:
    def __init__(
        self,
        repo: GameStateRepository,
        hero_gen: HeroGenerationService,
        combat: CombatService,
        pathfinding: PathfindingService,
        economy: EconomyService,
        llm: LLMService,
        char_service: CharacterService,
    ):
        self.repo = repo
        self.hero_gen = hero_gen
        self.combat = combat
        self.pathfinding = pathfinding
        self.economy = economy
        self.llm = llm
        self.char_service = char_service
        self._balance = _load_balance()

    def resolve_night(self) -> dict:
        """Resolve night phase: gather resources, transition to day."""
        state = self.repo.get_state()
        income = self.economy.resolve_night_income()
        state.phase = "day"
        state.logs.append(f"Night resolved. Resources gathered: {income}")
        return income

    def start_raid(self) -> RaidResult:
        """Execute a full hero raid."""
        state = self.repo.get_state()
        lang = state.game_config.language if state.game_config else "en"

        # Generate hero party
        heroes = self.hero_gen.generate_party(state.day)
        hero_names = [h.name for h in heroes]

        # Build path
        path = self.pathfinding.build_simple_path(state.dungeon.rooms)
        logs: list[str] = [f"A party of {len(heroes)} heroes enters the dungeon!"]
        hero_dialogue: list[str] = []

        # Raid narration
        narration = self.llm.raid_narration(
            f"Day {state.day}: {len(heroes)} heroes enter. Classes: {', '.join(h.hero_class for h in heroes)}",
            lang,
        )
        if narration:
            logs.append(narration)

        # Traverse rooms
        alive = heroes
        for room_id in path:
            room = next((r for r in state.dungeon.rooms if r.id == room_id), None)
            if not room:
                continue

            # Hero dialogue for this room
            dialogue = self.llm.hero_dialogue(
                [h.name for h in alive], room.type, lang
            )
            hero_dialogue.extend(dialogue)

            # Calculate monster power in room
            monsters_power = 0
            for mid in room.assigned_monsters:
                for m in state.monsters:
                    if m.id == mid:
                        monsters_power += m.power

            # Resolve combat
            alive, room_logs = self.combat.resolve_room(alive, room, monsters_power)
            logs.extend(room_logs)

            # Update knowledge for surviving heroes
            for hero in alive:
                self.char_service.update_knowledge(hero.character_sheet_id, room_id=room_id)

            if not alive:
                break

        # Determine outcome
        success = bool(alive)
        balance = self._balance
        treasure_gain = balance.get("raid_treasure_gain_on_defense", 15)
        treasure_loss = balance.get("raid_treasure_loss_on_breach", 10)
        boss_damage = balance.get("boss_damage_on_breach", 1)

        treasure_delta = -treasure_loss if success else treasure_gain
        actual_boss_damage = boss_damage if success else 0

        # Apply results
        state.treasure = max(0, state.treasure + treasure_delta)
        if actual_boss_damage > 0:
            state.lives = max(0, state.lives - actual_boss_damage)
            # Apply death penalty
            penalties = balance.get("death_penalties", {})
            lives_lost = 3 - state.lives
            penalty = penalties.get(str(lives_lost), 0.0)
            if penalty > 0:
                lost = int(state.treasure * penalty)
                state.treasure -= lost
                logs.append(f"Death penalty: lost {int(penalty * 100)}% of treasure ({lost} gold)!")

        # Mark dead heroes
        for hero in heroes:
            if hero not in alive:
                self.char_service.mark_dead(hero.character_sheet_id, state.day)
            else:
                # Survivors marked as fled (they escaped with knowledge)
                sheet = self.char_service.get_sheet(hero.character_sheet_id)
                if sheet:
                    sheet.status = "fled" if not success else "alive"

        # Transition to night
        state.phase = "night"
        state.day += 1
        state.logs.extend(logs)

        result = RaidResult(
            raid_id=generate_id("raid"),
            day=state.day - 1,
            heroes=heroes,
            survivors=[h for h in alive],
            path=path,
            success=success,
            boss_damage=actual_boss_damage,
            treasure_delta=treasure_delta,
            logs=logs,
            hero_dialogue=hero_dialogue,
        )

        return result
