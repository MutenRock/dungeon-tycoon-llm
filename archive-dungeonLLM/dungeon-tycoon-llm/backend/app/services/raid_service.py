from uuid import uuid4

from backend.app.models.hero import Hero
from backend.app.models.raid import RaidResult
from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.combat_service import CombatService
from backend.app.services.economy_service import EconomyService
from backend.app.services.pathfinding_service import PathfindingService
from backend.app.schemas.raid import RaidResponse


class RaidService:
    def __init__(self, repo: GameStateRepository) -> None:
        self.repo = repo
        self.pathfinding = PathfindingService()
        self.combat = CombatService()
        self.economy = EconomyService(repo=repo)
        self._last_raid: RaidResult | None = None

    def resolve_night(self):
        state = self.repo.get_state()
        state.phase = "day"
        state.logs.append("Night phase resolved.")
        self.repo.save_state(state)
        return self.economy.resolve_night_income()

    def start_raid(self) -> RaidResponse:
        state = self.repo.get_state()
        heroes = [
            Hero(name="Elaine", hero_class="knight", hp=10, attack=3),
            Hero(name="Miro", hero_class="rogue", hp=8, attack=4),
            Hero(name="Vale", hero_class="cleric", hp=9, attack=2),
        ]
        path = self.pathfinding.build_simple_path(state.dungeon.rooms)
        logs = ["A party of heroes enters the dungeon."]

        alive = heroes
        for room_id in path:
            room = next((room for room in state.dungeon.rooms if room.id == room_id), None)
            if room is None:
                continue
            alive, room_logs = self.combat.resolve_room(alive, room)
            logs.extend(room_logs)
            if not alive:
                break

        success = bool(alive)
        treasure_delta = -10 if success else 15
        boss_damage = 1 if success else 0

        state.treasure = max(0, state.treasure + treasure_delta)
        if boss_damage:
            state.lives = max(0, state.lives - boss_damage)

        if state.lives == 2:
            state.treasure = int(state.treasure * 0.75)
        elif state.lives == 1:
            state.treasure = int(state.treasure * 0.50)

        state.phase = "night"
        state.day += 1
        state.logs.extend(logs)
        self.repo.save_state(state)

        raid = RaidResult(
            id=str(uuid4()),
            heroes=alive,
            path=path,
            success=success,
            treasure_delta=treasure_delta,
            boss_damage=boss_damage,
            logs=logs,
        )
        self._last_raid = raid
        return RaidResponse.model_validate(raid.model_dump())

    def get_last_raid(self, raid_id: str) -> RaidResponse:
        if self._last_raid is None or self._last_raid.id != raid_id:
            # Fallback proto simple : renvoie le dernier raid même si l'id ne correspond pas.
            if self._last_raid is None:
                empty = RaidResult(id=raid_id, heroes=[], logs=["No raid found."])
                return RaidResponse.model_validate(empty.model_dump())
        return RaidResponse.model_validate(self._last_raid.model_dump())
