from __future__ import annotations
import random
from .models import GameState, HeroInstance, RaidResult, RaidEvent
from .constants import HERO_STATS, DEATH_PENALTIES, BOSS_MAX_LIVES, RoomType, MonsterType
from .pathfinding import find_path_to_boss
from .combat import resolve_combat, resolve_trap, make_monster, make_boss

_NAMES  = ["Aldric", "Sera", "Thane", "Lyra", "Gorin", "Mira", "Brom", "Zira",
           "Dorn", "Elara", "Fenn", "Hilda"]
_CLASSES = list(HERO_STATS.keys())


def _make_party(size: int = 4) -> list[HeroInstance]:
    shuffled = _CLASSES[:]
    random.shuffle(shuffled)
    heroes = []
    for i in range(size):
        cls = shuffled[i % len(shuffled)]
        s   = HERO_STATS[cls]
        heroes.append(HeroInstance(
            name=random.choice(_NAMES), hero_class=cls,
            hp=s["hp"], max_hp=s["hp"],
            attack=s["attack"], defense=s["defense"],
            trap_dodge=s["trap_dodge"], heal=s["heal"],
        ))
    return heroes


def simulate_raid(state: GameState) -> RaidResult:
    events = []
    heroes = _make_party()
    alive_count = len(heroes)

    intro = (
        "Un groupe de héros pénètre dans le donjon : "
        + ", ".join(f"{h.name} ({h.hero_class})" for h in heroes) + "."
    )
    events.append(RaidEvent(room_id="entrance", event_type="move",
                             description=intro, heroes_alive=alive_count))

    path = find_path_to_boss(state.grid)
    if not path:
        events.append(RaidEvent(
            room_id="exit", event_type="escape",
            description="Aucun chemin vers le boss — les héros repartent bredouilles.",
            heroes_alive=alive_count,
        ))
        return RaidResult(heroes_won=False, events=events, treasure_stolen=0,
                          boss_lives_remaining=state.boss_lives, game_over=False)

    heroes_won    = False
    treasure_stolen = 0

    for room in path:
        if not any(h.alive for h in heroes):
            break
        alive_count = sum(1 for h in heroes if h.alive)

        if room.room_type == RoomType.CORRIDOR:
            events.append(RaidEvent(
                room_id=f"{room.x},{room.y}", event_type="move",
                description=f"Les héros progressent dans un corridor ({room.x},{room.y}).",
                heroes_alive=alive_count,
            ))

        elif room.room_type == RoomType.TRAP_ROOM and room.trap_active:
            heroes, ev = resolve_trap(heroes)
            ev.room_id = f"{room.x},{room.y}"
            events.append(ev)

        elif room.room_type == RoomType.MONSTER_ROOM and room.monster:
            monster = make_monster(room.monster)
            heroes, evs = resolve_combat(heroes, monster, room_label=f"{room.x},{room.y}")
            events.extend(evs)

        elif room.room_type == RoomType.TREASURE_ROOM:
            loot = random.randint(10, 30)
            treasure_stolen += loot
            alive_count = sum(1 for h in heroes if h.alive)
            events.append(RaidEvent(
                room_id=f"{room.x},{room.y}", event_type="loot",
                description=f"Les héros pillent une salle au trésor — {loot} pièces d'or volées !",
                heroes_alive=alive_count, details={"loot": loot},
            ))

        elif room.room_type == RoomType.BOSS_ROOM:
            alive_count = sum(1 for h in heroes if h.alive)
            events.append(RaidEvent(
                room_id=f"{room.x},{room.y}", event_type="boss_fight",
                description=f"Les héros ({alive_count} survivants) affrontent le BOSS !",
                heroes_alive=alive_count,
            ))
            boss = make_boss()
            heroes, evs = resolve_combat(heroes, boss, room_label=f"boss_{room.x},{room.y}")
            for e in evs:
                e.event_type = "boss_fight"
            events.extend(evs)

            if boss.hp <= 0:
                heroes_won = True
                bonus = random.randint(30, 60)
                treasure_stolen += bonus
                alive_count = sum(1 for h in heroes if h.alive)
                events.append(RaidEvent(
                    room_id=f"boss_{room.x},{room.y}", event_type="loot",
                    description=f"Le boss est vaincu ! {bonus} pièces d'or emportées.",
                    heroes_alive=alive_count, details={"boss_loot": bonus},
                ))

    game_over = False

    if heroes_won:
        deaths_before = BOSS_MAX_LIVES - state.boss_lives
        death_number  = deaths_before + 1

        state.boss_lives -= 1

        if state.boss_lives <= 0:
            game_over = True
            state.treasure = 0
        else:
            penalty_pct = DEATH_PENALTIES.get(death_number, 0.0)
            treasury_loss = int(state.treasure * penalty_pct)
            state.treasure = max(0, state.treasure - treasury_loss)
    else:
        state.treasure = max(0, state.treasure - treasure_stolen)

    return RaidResult(
        heroes_won=heroes_won,
        events=events,
        treasure_stolen=treasure_stolen,
        boss_lives_remaining=state.boss_lives,
        game_over=game_over,
    )
