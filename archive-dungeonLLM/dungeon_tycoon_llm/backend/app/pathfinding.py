from __future__ import annotations
from collections import deque
from .models import Room
from .constants import RoomType, GRID_SIZE


def _cell_map(rooms: list[Room]):
    m = {}
    for room in rooms:
        for dx in range(room.width):
            for dy in range(room.height):
                m[(room.x + dx, room.y + dy)] = room
    return m


def find_path_to_boss(rooms: list[Room]) -> list[Room] | None:
    boss_room = next((r for r in rooms if r.room_type == RoomType.BOSS_ROOM), None)
    if not boss_room:
        return None

    cell_map = _cell_map(rooms)
    boss_cells = {
        (boss_room.x + dx, boss_room.y + dy)
        for dx in range(boss_room.width)
        for dy in range(boss_room.height)
    }

    entrances = [
        (0, y) for y in range(GRID_SIZE)
        if (0, y) in cell_map and (0, y) not in boss_cells
    ]
    if not entrances:
        return None

    for start in entrances:
        visited = {start}
        queue = deque([(start, [start])])

        while queue:
            (cx, cy), path = queue.popleft()

            if (cx, cy) in boss_cells:
                seen = set()
                result = []
                for cell in path:
                    r = cell_map.get(cell)
                    if r and id(r) not in seen:
                        result.append(r)
                        seen.add(id(r))
                return result

            for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nxt = (cx + ddx, cy + ddy)
                if nxt not in visited and nxt in cell_map:
                    visited.add(nxt)
                    queue.append((nxt, path + [nxt]))

    return None
