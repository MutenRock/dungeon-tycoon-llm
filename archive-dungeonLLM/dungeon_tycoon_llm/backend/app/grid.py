from __future__ import annotations
from typing import Optional
from .models import Room, GameState, PlaceRoomRequest
from .constants import RoomType, GRID_SIZE, BOSS_ROOM_WIDTH, BOSS_ROOM_HEIGHT, ROOM_COSTS, MonsterType


def get_room_at(grid: list[Room], x: int, y: int) -> Optional[Room]:
    for room in grid:
        if room.x <= x < room.x + room.width and room.y <= y < room.y + room.height:
            return room
    return None


def is_valid_placement(grid: list[Room], req: PlaceRoomRequest) -> tuple[bool, str]:
    if req.x < 0 or req.y < 0:
        return False, "Position hors grille (valeurs négatives)"
    if req.x + req.width > GRID_SIZE or req.y + req.height > GRID_SIZE:
        return False, "Salle hors limites de la grille (10×10)"

    if req.room_type == RoomType.BOSS_ROOM:
        if req.width != BOSS_ROOM_WIDTH or req.height != BOSS_ROOM_HEIGHT:
            return False, f"La salle du boss doit être {BOSS_ROOM_WIDTH}×{BOSS_ROOM_HEIGHT}"
        if any(r.room_type == RoomType.BOSS_ROOM for r in grid):
            return False, "Une seule salle du boss est autorisée"

    for rx in range(req.x, req.x + req.width):
        for ry in range(req.y, req.y + req.height):
            if get_room_at(grid, rx, ry):
                return False, f"Case ({rx},{ry}) déjà occupée"

    return True, ""


def place_room(state: GameState, req: PlaceRoomRequest) -> tuple[bool, str]:
    valid, msg = is_valid_placement(state.grid, req)
    if not valid:
        return False, msg

    costs = ROOM_COSTS.get(req.room_type, {})
    for resource, amount in costs.items():
        if getattr(state.resources, resource, 0) < amount:
            return False, f"Ressources insuffisantes : manque de {resource}"

    for resource, amount in costs.items():
        setattr(state.resources, resource, getattr(state.resources, resource) - amount)

    state.grid.append(Room(
        x=req.x, y=req.y,
        width=req.width, height=req.height,
        room_type=req.room_type,
    ))
    return True, "Salle placée"


def remove_room(state: GameState, x: int, y: int) -> tuple[bool, str]:
    root = get_room_at(state.grid, x, y)
    if not root:
        return False, "Aucune salle à cette position"
    state.grid.remove(root)
    for resource, amount in ROOM_COSTS.get(root.room_type, {}).items():
        setattr(state.resources, resource, getattr(state.resources, resource) + amount // 2)
    return True, "Salle démolie (remboursement 50 %)"


def assign_monster(state: GameState, x: int, y: int, monster_type: Optional[MonsterType]) -> tuple[bool, str]:
    room = get_room_at(state.grid, x, y)
    if not room:
        return False, "Aucune salle à cette position"
    if room.room_type != RoomType.MONSTER_ROOM:
        return False, "Seules les salles monster_room peuvent accueillir des monstres"
    room.monster = monster_type
    return (True, "Monstre assigné") if monster_type else (True, "Monstre retiré")
