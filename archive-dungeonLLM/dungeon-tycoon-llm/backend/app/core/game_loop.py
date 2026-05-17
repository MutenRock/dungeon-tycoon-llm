from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.raid_service import RaidService


class GameLoop:
    def __init__(self, repo: GameStateRepository) -> None:
        self.repo = repo
        self.raid_service = RaidService(repo=repo)

    def run_day_cycle(self):
        self.raid_service.resolve_night()
        return self.raid_service.start_raid()
