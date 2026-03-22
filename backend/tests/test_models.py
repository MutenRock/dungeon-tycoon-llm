"""Tests for Pydantic models — serialization, defaults, and validation."""

from backend.app.models import (
    CharacterSheet, CharacterStats, KnowledgeSheet,
    GameConfig, PlayerProfile,
    Advisor, HiddenWish,
    DungeonPattern, PatternRoom,
    Hero, Monster, Room, DoorConnection,
    Resources, Dungeon, PlayerState, RaidResult,
)


def test_character_sheet_defaults():
    sheet = CharacterSheet(id="cs_1", name="Test", entity_type="hero", species="human", role="knight")
    assert sheet.status == "alive"
    assert sheet.version == 1
    assert sheet.knowledge.rooms_seen == []
    assert sheet.personality_traits == []


def test_character_sheet_serialization():
    sheet = CharacterSheet(
        id="cs_1", name="Sir Test", entity_type="hero", species="human", role="knight",
        stats=CharacterStats(hp=20, max_hp=20, attack=5, defense=3),
        personality_traits=["brave", "stubborn"],
    )
    data = sheet.model_dump()
    assert data["name"] == "Sir Test"
    assert data["stats"]["hp"] == 20
    restored = CharacterSheet(**data)
    assert restored.stats.attack == 5


def test_knowledge_sheet_append():
    k = KnowledgeSheet()
    k.rooms_seen.append("room_1")
    k.traps_triggered.append("trap_1")
    assert len(k.rooms_seen) == 1
    assert "trap_1" in k.traps_triggered


def test_game_config_defaults():
    config = GameConfig()
    assert config.language == "en"
    assert config.monster_species == "goblin"


def test_advisor_with_hidden_wish():
    wish = HiddenWish(
        objective="wants more meat",
        trigger_condition="conversation",
        outcome_positive="meat_boost",
        outcome_negative="morale_drop",
    )
    advisor = Advisor(id="adv_1", role="counselor", character_sheet_id="cs_1", hidden_wish=wish)
    assert advisor.hidden_wish.success_threshold == 0.5
    assert not advisor.hidden_wish.resolved


def test_hero_defaults():
    hero = Hero()
    assert hero.hero_class == "knight"
    assert hero.tier == "common"
    assert hero.hp == 10


def test_monster_fields():
    m = Monster(id="m1", name="Grak", kind="orc", species="orc", power=6)
    assert m.assigned_task is None
    assert m.assigned_room_id is None


def test_room_with_doors():
    door = DoorConnection(direction="north", connects_to="room_2")
    room = Room(id="r1", type="monster_room", x=3, y=4, doors=[door])
    assert room.doors[0].direction == "north"
    assert room.trap_type is None


def test_dungeon_defaults():
    d = Dungeon()
    assert d.width == 10
    assert d.height == 10
    assert d.rooms == []


def test_resources_defaults():
    r = Resources()
    assert r.wood == 50
    assert r.vegetables == 0


def test_player_state_full():
    state = PlayerState(
        game_config=GameConfig(dungeon_name="Test Dungeon"),
        day=5, phase="night", lives=2, treasure=200,
    )
    assert state.game_config.dungeon_name == "Test Dungeon"
    assert state.advisors == []
    assert state.character_registry == []


def test_raid_result():
    result = RaidResult(raid_id="raid_1", day=3, success=False, treasure_delta=15)
    assert not result.success
    assert result.boss_damage == 0


def test_dungeon_pattern():
    room = PatternRoom(type="corridor", dx=0, dy=0)
    pattern = DungeonPattern(id="pat_1", name="Test Pattern", rooms=[room])
    data = pattern.model_dump()
    restored = DungeonPattern(**data)
    assert len(restored.rooms) == 1
    assert restored.rooms[0].type == "corridor"
