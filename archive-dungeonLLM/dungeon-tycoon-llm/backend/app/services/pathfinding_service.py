from backend.app.models.room import Room


class PathfindingService:
    def build_simple_path(self, rooms: list[Room]) -> list[str]:
        # Prototype simple : tri par position pour produire un chemin stable.
        ordered = sorted(rooms, key=lambda r: (r.x, r.y))
        return [room.id for room in ordered]
