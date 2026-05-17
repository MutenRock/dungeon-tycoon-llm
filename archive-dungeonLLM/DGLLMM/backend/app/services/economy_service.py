from backend.app.core.balance import ROOM_COSTS
from backend.app.repositories.game_state_repository import GameStateRepository


class EconomyService:
    def __init__(self, repo: GameStateRepository) -> None:
        self.repo = repo

    def pay_room_cost(self, room_type: str) -> tuple[bool, str | None]:
        state = self.repo.get_state()
        costs = ROOM_COSTS.get(room_type)
        if costs is None:
            return False, "Unknown room type."

        if (
            state.resources.wood < costs["wood"]
            or state.resources.stone < costs["stone"]
            or state.resources.meat < costs["meat"]
        ):
            return False, "Not enough resources."

        state.resources.wood -= costs["wood"]
        state.resources.stone -= costs["stone"]
        state.resources.meat -= costs["meat"]
        self.repo.save_state(state)
        return True, None

    def resolve_night_income(self):
        state = self.repo.get_state()
        state.resources.wood += 2
        state.resources.stone += 1
        state.resources.meat += 1
        state.logs.append("Night workers gather basic resources.")
        self.repo.save_state(state)
        return state
