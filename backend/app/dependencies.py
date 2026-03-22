"""Dependency injection — singleton service instances."""

from __future__ import annotations

from backend.app.config import Settings
from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.llm_service import LLMService
from backend.app.services.character_service import CharacterService
from backend.app.services.economy_service import EconomyService
from backend.app.services.dungeon_service import DungeonService
from backend.app.services.pathfinding_service import PathfindingService
from backend.app.services.combat_service import CombatService
from backend.app.services.hero_generation_service import HeroGenerationService
from backend.app.services.raid_service import RaidService
from backend.app.services.advisor_service import AdvisorService
from backend.app.services.bestiary_service import BestiaryService
from backend.app.services.pattern_service import PatternService
from backend.app.services.game_setup_service import GameSetupService

# Load settings
settings = Settings()

# Singletons
_repo = GameStateRepository(save_dir=settings.save_dir)
_llm = LLMService(
    api_key=settings.anthropic_api_key,
    primary_model=settings.anthropic_primary_model,
    fast_model=settings.anthropic_fast_model,
    primary_timeout=settings.llm_primary_timeout // 1000,
    fast_timeout=settings.llm_fast_timeout // 1000,
    fallback_enabled=settings.llm_fallback_enabled,
)
_char_service = CharacterService(repo=_repo)
_economy = EconomyService(repo=_repo)
_dungeon = DungeonService(repo=_repo, economy=_economy)
_pathfinding = PathfindingService()
_combat = CombatService(char_service=_char_service)
_hero_gen = HeroGenerationService(repo=_repo, llm=_llm, char_service=_char_service)
_raid = RaidService(
    repo=_repo, hero_gen=_hero_gen, combat=_combat,
    pathfinding=_pathfinding, economy=_economy, llm=_llm,
    char_service=_char_service,
)
_advisor = AdvisorService(repo=_repo, llm=_llm, char_service=_char_service)
_bestiary = BestiaryService(repo=_repo)
_pattern = PatternService(repo=_repo)
_setup = GameSetupService(repo=_repo, llm=_llm)


# FastAPI dependency functions
def get_repo() -> GameStateRepository:
    return _repo

def get_llm() -> LLMService:
    return _llm

def get_char_service() -> CharacterService:
    return _char_service

def get_dungeon_service() -> DungeonService:
    return _dungeon

def get_raid_service() -> RaidService:
    return _raid

def get_advisor_service() -> AdvisorService:
    return _advisor

def get_bestiary_service() -> BestiaryService:
    return _bestiary

def get_pattern_service() -> PatternService:
    return _pattern

def get_setup_service() -> GameSetupService:
    return _setup
