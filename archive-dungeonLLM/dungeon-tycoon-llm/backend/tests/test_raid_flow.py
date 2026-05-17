from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.raid_service import RaidService


def test_start_raid_returns_result():
    repo = GameStateRepository()
    service = RaidService(repo=repo)
    result = service.start_raid()
    assert result.id
    assert isinstance(result.logs, list)
