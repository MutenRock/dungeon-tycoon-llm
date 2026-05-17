from backend.app.models.monster import Monster
from backend.app.models.player import PlayerState


class GameStateRepository:
    def __init__(self) -> None:
        self._state = self._build_default_state()

    def _build_default_state(self) -> PlayerState:
        state = PlayerState()
        state.monsters = [
            Monster(id="goblin_01", name="Snag", kind="goblin", power=4),
            Monster(id="skeleton_01", name="Rattle", kind="skeleton", power=5),
            Monster(id="beast_01", name="Maw", kind="beast", power=6),
        ]
        return state

    def get_state(self) -> PlayerState:
        return self._state

    def save_state(self, state: PlayerState) -> None:
        self._state = state

    def reset(self) -> PlayerState:
        self._state = self._build_default_state()
        return self._state
