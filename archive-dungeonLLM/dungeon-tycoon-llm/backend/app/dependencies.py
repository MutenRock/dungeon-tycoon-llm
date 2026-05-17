from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.dungeon_service import DungeonService
from backend.app.services.raid_service import RaidService
from backend.app.services.event_service import EventService
from backend.app.services.llm_service import LLMService


repo = GameStateRepository()
dungeon_service = DungeonService(repo=repo)
raid_service = RaidService(repo=repo)
event_service = EventService()
llm_service = LLMService()
