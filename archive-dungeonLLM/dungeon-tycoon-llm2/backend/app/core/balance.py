STARTING_TREASURE = 100
STARTING_LIVES = 3
STARTING_RESOURCES = {"wood": 20, "stone": 20, "meat": 10}

ROOM_COSTS = {
    "corridor": {"wood": 1, "stone": 0, "meat": 0},
    "monster_room": {"wood": 2, "stone": 2, "meat": 0},
    "trap_room": {"wood": 1, "stone": 3, "meat": 0},
    "treasure_room": {"wood": 2, "stone": 1, "meat": 0},
    "boss_room": {"wood": 0, "stone": 0, "meat": 0},
}

MONSTER_POWER = {
    "goblin": 4,
    "skeleton": 5,
    "beast": 6,
}
