"""Combat resolution: heroes vs rooms (monsters + traps) with knowledge system."""

from __future__ import annotations

import json
from pathlib import Path

from backend.app.models.hero import Hero
from backend.app.models.room import Room
from backend.app.services.character_service import CharacterService

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _load_balance() -> dict:
    path = DATA_DIR / "balance.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


class CombatService:
    def __init__(self, char_service: CharacterService):
        self.char_service = char_service
        self._balance = _load_balance()

    def resolve_room(
        self, heroes: list[Hero], room: Room, monsters_power: int = 0
    ) -> tuple[list[Hero], list[str]]:
        """Resolve combat for a list of heroes entering a room.

        Returns (surviving_heroes, combat_logs).
        """
        logs: list[str] = []
        alive = list(heroes)

        if room.type == "trap_room":
            alive, trap_logs = self._resolve_trap(alive, room)
            logs.extend(trap_logs)

        elif room.type == "monster_room" or room.type == "barracks":
            alive, combat_logs = self._resolve_monster_combat(alive, room, monsters_power)
            logs.extend(combat_logs)

        elif room.type == "bonus_room":
            alive, bonus_logs = self._resolve_bonus(alive, room)
            logs.extend(bonus_logs)

        elif room.type == "boss_room":
            logs.append("The heroes reach the boss room!")

        else:
            logs.append(f"The heroes pass through the {room.type}.")

        room.times_triggered += 1
        return alive, logs

    def _resolve_trap(self, heroes: list[Hero], room: Room) -> tuple[list[Hero], list[str]]:
        logs: list[str] = []
        trap_damage = self._balance.get("trap_base_damage", {}).get(room.trap_type or "spikes", 8)
        alive: list[Hero] = []

        for hero in heroes:
            # Knowledge check: has this hero seen this trap before?
            sheet = self.char_service.get_sheet(hero.character_sheet_id)
            if sheet and room.id in sheet.knowledge.traps_triggered:
                logs.append(f"{hero.name} recognizes the trap and avoids it!")
                alive.append(hero)
                continue

            # Apply trap damage (reduced by defense)
            effective_damage = max(1, trap_damage - hero.defense)
            hero.hp -= effective_damage
            logs.append(f"{hero.name} takes {effective_damage} trap damage!")

            # Record trap knowledge for survivors
            if sheet:
                self.char_service.update_knowledge(hero.character_sheet_id, trap_id=room.id)

            if hero.hp > 0:
                alive.append(hero)
            else:
                logs.append(f"{hero.name} has fallen to the trap!")
                if sheet:
                    self.char_service.mark_dead(hero.character_sheet_id, 0)

        return alive, logs

    def _resolve_monster_combat(
        self, heroes: list[Hero], room: Room, monsters_power: int
    ) -> tuple[list[Hero], list[str]]:
        logs: list[str] = []
        total_monster_power = monsters_power or len(room.assigned_monsters) * 4

        if total_monster_power == 0:
            logs.append(f"The {room.type} is empty.")
            return heroes, logs

        # Simple combat: monster power distributed as damage across heroes
        damage_per_hero = max(1, total_monster_power // max(1, len(heroes)))
        alive: list[Hero] = []

        # Heroes deal damage to monsters first (simplified)
        total_hero_damage = sum(h.attack for h in heroes)
        monster_remaining = max(0, total_monster_power - total_hero_damage)

        if monster_remaining == 0:
            logs.append(f"The heroes clear the {room.type}!")
            # Heroes take some damage but survive
            for hero in heroes:
                hero.hp -= max(0, damage_per_hero // 2)
                if hero.hp > 0:
                    alive.append(hero)
                else:
                    logs.append(f"{hero.name} falls in combat!")
            return alive, logs

        # Monsters fight back
        for hero in heroes:
            hero.hp -= max(1, damage_per_hero - hero.defense)
            if hero.hp > 0:
                alive.append(hero)
            else:
                logs.append(f"{hero.name} is slain by the dungeon's defenders!")

        return alive, logs

    def _resolve_bonus(self, heroes: list[Hero], room: Room) -> tuple[list[Hero], list[str]]:
        logs: list[str] = []
        bonus = room.bonus_type or "heal"

        if bonus == "heal":
            for hero in heroes:
                heal = min(hero.max_hp - hero.hp, 5)
                hero.hp += heal
            logs.append("The heroes find a healing spring!")
        elif bonus == "buff_attack":
            for hero in heroes:
                hero.attack += 2
            logs.append("The heroes find enchanted weapons!")
        elif bonus == "buff_defense":
            for hero in heroes:
                hero.defense += 2
            logs.append("The heroes find enchanted armor!")
        else:
            logs.append("The heroes find a mysterious room...")

        return heroes, logs
