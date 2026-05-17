from backend.app.models.hero import Hero
from backend.app.models.room import Room
from backend.app.services.combat_service import CombatService


def test_trap_room_damages_first_hero():
    heroes = [Hero(name="A", hero_class="knight", hp=10, attack=3)]
    room = Room(id="trap1", type="trap_room", x=0, y=0)
    alive, logs = CombatService().resolve_room(heroes, room)
    assert alive[0].hp == 8
    assert logs
