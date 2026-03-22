"""Request/Response schemas for game setup."""

from pydantic import BaseModel


class CreateGameRequest(BaseModel):
    dungeon_name: str = "The Unnamed Depths"
    monster_species: str = "goblin"
    advisor_race: str = "goblin"
    player_race: str = "demon"
    language: str = "en"


class LuciferRespondRequest(BaseModel):
    step: int
    question: str
    answer: str
    previous_exchanges: list[dict] = []
    language: str = "en"
