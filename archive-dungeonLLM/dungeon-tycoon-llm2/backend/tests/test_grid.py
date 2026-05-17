from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.dungeon_service import DungeonService
from backend.app.schemas.grid import PlaceRoomRequest


def test_place_room_success():
    repo = GameStateRepository()
    service = DungeonService(repo=repo)
    ok, error = service.place_room(
        PlaceRoomRequest(room_id="r1", room_type="corridor", x=0, y=0)
    )
    assert ok is True
    assert error is None
    assert len(repo.get_state().dungeon.rooms) == 1
