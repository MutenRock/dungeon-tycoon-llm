from .models import GameState
from .constants import RoomType


def generate_resources(state: GameState) -> None:
    bonus = sum(1 for r in state.grid if r.room_type == RoomType.TREASURE_ROOM)
    state.resources.wood  += 2 + bonus
    state.resources.stone += 1
    state.resources.meat  += 1


def apply_upkeep(state: GameState) -> None:
    monsters = sum(1 for r in state.grid if r.monster is not None)
    state.resources.meat = max(0, state.resources.meat - monsters)
