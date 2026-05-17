from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.economy_service import EconomyService


def test_night_income_increases_resources():
    repo = GameStateRepository()
    service = EconomyService(repo=repo)
    before = repo.get_state().resources.wood
    state = service.resolve_night_income()
    assert state.resources.wood == before + 2
