"""Tests for core services — dungeon, economy, combat, pathfinding, patterns."""

import pytest

from backend.app.models.hero import Hero
from backend.app.models.room import Room, DoorConnection
from backend.app.models.player import PlayerState
from backend.app.repositories.game_state_repository import GameStateRepository
from backend.app.services.economy_service import EconomyService
from backend.app.services.dungeon_service import DungeonService
from backend.app.services.pathfinding_service import PathfindingService
from backend.app.services.combat_service import CombatService
from backend.app.services.character_service import CharacterService
from backend.app.services.pattern_service import PatternService


@pytest.fixture
def repo():
    return GameStateRepository(save_dir="./test_saves")


@pytest.fixture
def economy(repo):
    return EconomyService(repo=repo)


@pytest.fixture
def dungeon(repo, economy):
    return DungeonService(repo=repo, economy=economy)


@pytest.fixture
def char_service(repo):
    return CharacterService(repo=repo)


@pytest.fixture
def combat(char_service):
    return CombatService(char_service=char_service)


# --- Dungeon Service ---

def test_place_room(dungeon, repo):
    ok, error, room = dungeon.place_room("corridor", 0, 0)
    assert ok
    assert room is not None
    assert room.type == "corridor"
    state = repo.get_state()
    assert len(state.dungeon.rooms) == 1


def test_place_room_collision(dungeon):
    dungeon.place_room("corridor", 0, 0)
    ok, error, _ = dungeon.place_room("corridor", 0, 0)
    assert not ok
    assert "overlaps" in error.lower()


def test_place_room_out_of_bounds(dungeon):
    ok, error, _ = dungeon.place_room("corridor", 10, 10)
    assert not ok
    assert "bounds" in error.lower()


def test_remove_room(dungeon, repo):
    _, _, room = dungeon.place_room("corridor", 0, 0)
    ok, _ = dungeon.remove_room(room.id)
    assert ok
    assert len(repo.get_state().dungeon.rooms) == 0


def test_cannot_remove_boss_room(dungeon):
    dungeon.place_room("boss_room", 0, 0, w=2, h=1)
    state = dungeon.repo.get_state()
    boss = state.dungeon.rooms[0]
    ok, error = dungeon.remove_room(boss.id)
    assert not ok
    assert "boss" in error.lower()


def test_only_one_boss_room(dungeon):
    dungeon.place_room("boss_room", 0, 0, w=2, h=1)
    ok, error, _ = dungeon.place_room("boss_room", 4, 4, w=2, h=1)
    assert not ok
    assert "one boss" in error.lower()


# --- Economy Service ---

def test_night_income(economy, repo):
    state = repo.get_state()
    old_wood = state.resources.wood
    income = economy.resolve_night_income()
    assert state.resources.wood > old_wood
    assert "wood" in income


def test_pay_room_cost(economy, repo):
    ok, error = economy.pay_room_cost("corridor")
    assert ok
    state = repo.get_state()
    assert state.resources.wood < 50  # default is 50, corridor costs 5


def test_pay_room_cost_insufficient(economy, repo):
    state = repo.get_state()
    state.resources.wood = 0
    state.resources.stone = 0
    ok, error = economy.pay_room_cost("corridor")
    assert not ok


# --- Pathfinding ---

def test_simple_path():
    pf = PathfindingService()
    rooms = [
        Room(id="r1", type="corridor", x=0, y=0),
        Room(id="r2", type="monster_room", x=1, y=0),
        Room(id="r3", type="boss_room", x=2, y=0, w=2),
    ]
    path = pf.build_simple_path(rooms)
    assert path[-1] == "r3"  # boss room last
    assert len(path) == 3


def test_graph_path():
    pf = PathfindingService()
    rooms = [
        Room(id="r1", type="corridor", x=0, y=0, doors=[DoorConnection(direction="east", connects_to="r2")]),
        Room(id="r2", type="monster_room", x=1, y=0, doors=[
            DoorConnection(direction="west", connects_to="r1"),
            DoorConnection(direction="east", connects_to="r3"),
        ]),
        Room(id="r3", type="boss_room", x=2, y=0, doors=[DoorConnection(direction="west", connects_to="r2")]),
    ]
    path = pf.find_path(rooms, "r1", "r3")
    assert path == ["r1", "r2", "r3"]


# --- Combat ---

def test_combat_empty_room(combat):
    heroes = [Hero(id="h1", name="Test", hp=10, attack=3)]
    room = Room(id="r1", type="corridor")
    alive, logs = combat.resolve_room(heroes, room)
    assert len(alive) == 1


def test_combat_trap_room(combat, char_service, repo):
    sheet = char_service.create_sheet("hero", "Test", "human", "knight")
    heroes = [Hero(id="h1", name="Test", hp=10, attack=3, defense=0, character_sheet_id=sheet.id)]
    room = Room(id="r1", type="trap_room", trap_type="spikes")
    alive, logs = combat.resolve_room(heroes, room)
    assert any("trap" in l.lower() for l in logs)


def test_combat_trap_avoidance(combat, char_service, repo):
    """Hero who already triggered a trap should avoid it on second encounter."""
    sheet = char_service.create_sheet("hero", "Veteran", "human", "knight")
    # Manually add trap knowledge
    sheet.knowledge.traps_triggered.append("trap_room_1")

    heroes = [Hero(id="h1", name="Veteran", hp=10, attack=3, character_sheet_id=sheet.id)]
    room = Room(id="trap_room_1", type="trap_room", trap_type="spikes")
    alive, logs = combat.resolve_room(heroes, room)
    assert any("recognizes" in l.lower() or "avoids" in l.lower() for l in logs)
    assert len(alive) == 1


# --- Character Service ---

def test_create_and_get_sheet(char_service):
    sheet = char_service.create_sheet("hero", "TestHero", "human", "knight")
    found = char_service.get_sheet(sheet.id)
    assert found is not None
    assert found.name == "TestHero"


def test_mark_dead(char_service):
    sheet = char_service.create_sheet("hero", "Doomed", "human", "mage")
    char_service.mark_dead(sheet.id, day=5)
    assert sheet.status == "dead"
    assert len(sheet.history) == 1


def test_update_knowledge(char_service):
    sheet = char_service.create_sheet("hero", "Scout", "human", "rogue")
    char_service.update_knowledge(sheet.id, room_id="r1", trap_id="t1")
    assert "r1" in sheet.knowledge.rooms_seen
    assert "t1" in sheet.knowledge.traps_triggered


# --- Pattern Service ---

def test_save_and_get_pattern(repo):
    state = repo.get_state()
    state.dungeon.rooms.append(Room(id="r1", type="corridor", x=0, y=0))
    patterns = PatternService(repo=repo)
    pattern = patterns.save_current_layout("Test")
    assert pattern.name == "Test"
    assert len(pattern.rooms) == 1
    found = patterns.get_pattern(pattern.id)
    assert found is not None


def test_export_import_pattern(repo):
    state = repo.get_state()
    state.dungeon.rooms.append(Room(id="r1", type="trap_room", x=2, y=3))
    patterns = PatternService(repo=repo)
    pattern = patterns.save_current_layout("Export Test")
    exported = patterns.export_pattern(pattern.id)
    assert exported is not None

    imported = patterns.import_pattern(exported)
    assert imported.name == "Export Test"
    assert imported.id != pattern.id  # new ID
