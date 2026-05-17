from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field
from .constants import Phase, RoomType, MonsterType


class Room(BaseModel):
    x: int
    y: int
    width: int = 1
    height: int = 1
    room_type: RoomType
    monster: Optional[MonsterType] = None
    trap_active: bool = True


class Resources(BaseModel):
    wood: int = 0
    stone: int = 0
    meat: int = 0


class HeroInstance(BaseModel):
    name: str
    hero_class: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    alive: bool = True
    trap_dodge: float = 0.0
    heal: int = 0


class MonsterInstance(BaseModel):
    monster_type: MonsterType
    hp: int
    max_hp: int
    attack: int
    defense: int


class RaidEvent(BaseModel):
    room_id: str
    event_type: str
    description: str
    heroes_alive: int
    details: dict[str, Any] = Field(default_factory=dict)


class RaidResult(BaseModel):
    heroes_won: bool
    events: list[RaidEvent]
    treasure_stolen: int
    boss_lives_remaining: int
    game_over: bool
    narrative: Optional[str] = None


class GameState(BaseModel):
    phase: Phase = Phase.NIGHT
    grid: list[Room] = Field(default_factory=list)
    resources: Resources = Field(default_factory=Resources)
    treasure: int = 100
    boss_lives: int = 3
    turn: int = 1
    game_over: bool = False
    last_raid: Optional[RaidResult] = None


class PlaceRoomRequest(BaseModel):
    x: int
    y: int
    room_type: RoomType
    width: int = 1
    height: int = 1


class AssignMonsterRequest(BaseModel):
    x: int
    y: int
    monster_type: Optional[MonsterType] = None
