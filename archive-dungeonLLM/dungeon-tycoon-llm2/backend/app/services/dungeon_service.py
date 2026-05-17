from backend.app.models.room import Room
from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.schemas.grid import PlaceRoomRequest
from backend.app.services.economy_service import EconomyService


class DungeonService:
    def __init__(self, repo: GameStateRepository) -> None:
        self.repo = repo
        self.economy = EconomyService(repo=repo)

    def place_room(self, payload: PlaceRoomRequest) -> tuple[bool, str | None]:
        state = self.repo.get_state()

        for room in state.dungeon.rooms:
            overlap_x = payload.x < room.x + room.w and payload.x + payload.w > room.x
            overlap_y = payload.y < room.y + room.h and payload.y + payload.h > room.y
            if overlap_x and overlap_y:
                return False, "Room overlaps with an existing room."

        if payload.x < 0 or payload.y < 0:
            return False, "Coordinates must be positive."

        if payload.x + payload.w > state.dungeon.width or payload.y + payload.h > state.dungeon.height:
            return False, "Room exceeds dungeon bounds."

        ok, error = self.economy.pay_room_cost(payload.room_type)
        if not ok:
            return False, error

        room = Room(
            id=payload.room_id,
            type=payload.room_type,
            x=payload.x,
            y=payload.y,
            w=payload.w,
            h=payload.h,
            doors=payload.doors,
        )
        state.dungeon.rooms.append(room)
        state.logs.append(f"Placed room {payload.room_type} at ({payload.x}, {payload.y}).")
        self.repo.save_state(state)
        return True, None

    def remove_room(self, room_id: str) -> tuple[bool, str | None]:
        state = self.repo.get_state()
        initial = len(state.dungeon.rooms)
        state.dungeon.rooms = [room for room in state.dungeon.rooms if room.id != room_id]
        if len(state.dungeon.rooms) == initial:
            return False, "Room not found."
        state.logs.append(f"Removed room {room_id}.")
        self.repo.save_state(state)
        return True, None
