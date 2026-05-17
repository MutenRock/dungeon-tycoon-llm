from enum import Enum


class Phase(str, Enum):
    NIGHT = "night"
    DAY = "day"


class RoomType(str, Enum):
    CORRIDOR = "corridor"
    MONSTER_ROOM = "monster_room"
    TRAP_ROOM = "trap_room"
    TREASURE_ROOM = "treasure_room"
    BOSS_ROOM = "boss_room"


class MonsterType(str, Enum):
    GOBLIN = "goblin"
    SKELETON = "skeleton"
    ORC = "orc"
    TROLL = "troll"


GRID_SIZE = 10
BOSS_ROOM_WIDTH = 2
BOSS_ROOM_HEIGHT = 1
BOSS_MAX_LIVES = 3

STARTING_RESOURCES = {"wood": 15, "stone": 10, "meat": 5}
STARTING_TREASURE = 100

ROOM_COSTS: dict[RoomType, dict[str, int]] = {
    RoomType.CORRIDOR:      {"wood": 1, "stone": 0},
    RoomType.MONSTER_ROOM:  {"wood": 2, "stone": 1},
    RoomType.TRAP_ROOM:     {"wood": 1, "stone": 2},
    RoomType.TREASURE_ROOM: {"wood": 2, "stone": 2},
    RoomType.BOSS_ROOM:     {"wood": 3, "stone": 3},
}

MONSTER_STATS = {
    MonsterType.GOBLIN:   {"hp": 10, "attack": 3, "defense": 1},
    MonsterType.SKELETON: {"hp": 15, "attack": 5, "defense": 2},
    MonsterType.ORC:      {"hp": 22, "attack": 6, "defense": 3},
    MonsterType.TROLL:    {"hp": 35, "attack": 8, "defense": 4},
}

HERO_STATS = {
    "warrior": {"hp": 40, "attack": 8, "defense": 4, "trap_dodge": 0.0, "heal": 0},
    "mage":    {"hp": 25, "attack": 13, "defense": 2, "trap_dodge": 0.0, "heal": 0},
    "rogue":   {"hp": 30, "attack": 7,  "defense": 3, "trap_dodge": 0.5, "heal": 0},
    "cleric":  {"hp": 35, "attack": 6,  "defense": 3, "trap_dodge": 0.0, "heal": 10},
}

BOSS_STATS = {"hp": 60, "attack": 11, "defense": 5}
TRAP_BASE_DAMAGE = 8

DEATH_PENALTIES = {1: 0.25, 2: 0.50}
