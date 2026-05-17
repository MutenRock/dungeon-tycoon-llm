from backend.app.models.room import Room
from backend.app.services.pathfinding_service import PathfindingService


def test_build_simple_path_orders_rooms():
    service = PathfindingService()
    rooms = [
        Room(id="b", type="corridor", x=5, y=1),
        Room(id="a", type="corridor", x=0, y=1),
    ]
    assert service.build_simple_path(rooms) == ["a", "b"]
