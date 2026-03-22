"""Game constants and enumerations."""

from enum import Enum


class TurnPhase(str, Enum):
    NIGHT = "night"
    DAY = "day"
    RESOLUTION = "resolution"


class EntityType(str, Enum):
    HERO = "hero"
    MONSTER = "monster"
    ADVISOR = "advisor"


class HeroClass(str, Enum):
    KNIGHT = "knight"
    ARCHER = "archer"
    MAGE = "mage"
    ROGUE = "rogue"
    CLERIC = "cleric"


class HeroTier(str, Enum):
    COMMON = "common"
    VETERAN = "veteran"
    LOCAL_LEGEND = "local_legend"
    LEGENDARY = "legendary"


class RoomType(str, Enum):
    CORRIDOR = "corridor"
    MONSTER_ROOM = "monster_room"
    TRAP_ROOM = "trap_room"
    TREASURE_ROOM = "treasure_room"
    BOSS_ROOM = "boss_room"
    BONUS_ROOM = "bonus_room"
    BARRACKS = "barracks"
    KITCHEN = "kitchen"
    WORKSHOP = "workshop"
    PRISON = "prison"


class AdvisorRole(str, Enum):
    COUNSELOR = "counselor"
    HIGH_GUARD = "high_guard"
    KITCHEN_CHIEF = "kitchen_chief"
    SPY_MASTER = "spy_master"
    ARCHITECT = "architect"


class MonsterTask(str, Enum):
    GUARD = "guard"
    WORKER = "worker"
    COOK = "cook"
    SPY = "spy"
    IDLE = "idle"


# Game balance
GRID_WIDTH = 10
GRID_HEIGHT = 10
BOSS_ROOM_W = 2
BOSS_ROOM_H = 1
MAX_LIVES = 3
DEATH_PENALTIES = {1: 0.0, 2: 0.25, 3: 0.50}  # life_lost: treasure_penalty
MAX_PARTY_SIZE = 10
LUCIFER_QUESTIONS = 5
