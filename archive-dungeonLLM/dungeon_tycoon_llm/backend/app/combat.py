from __future__ import annotations
import random
from .models import HeroInstance, MonsterInstance, RaidEvent
from .constants import MONSTER_STATS, BOSS_STATS, TRAP_BASE_DAMAGE, MonsterType


def make_monster(monster_type: MonsterType) -> MonsterInstance:
    s = MONSTER_STATS[monster_type]
    return MonsterInstance(monster_type=monster_type, hp=s["hp"], max_hp=s["hp"],
                           attack=s["attack"], defense=s["defense"])


def make_boss() -> MonsterInstance:
    s = BOSS_STATS
    return MonsterInstance(monster_type=MonsterType.TROLL, hp=s["hp"], max_hp=s["hp"],
                           attack=s["attack"], defense=s["defense"])


def resolve_combat(heroes: list[HeroInstance], monster: MonsterInstance, room_label: str = "?"):
    events = []
    round_num = 0

    while monster.hp > 0 and any(h.alive for h in heroes):
        round_num += 1
        if round_num > 30:
            break

        for hero in heroes:
            if not hero.alive:
                continue
            dmg = max(1, hero.attack - monster.defense + random.randint(-2, 3))
            monster.hp -= dmg
            if monster.hp <= 0:
                break

        if monster.hp <= 0:
            break

        targets = [h for h in heroes if h.alive]
        if targets:
            target = random.choice(targets)
            dmg = max(1, monster.attack - target.defense + random.randint(-2, 3))
            target.hp -= dmg
            if target.hp <= 0:
                target.alive = False
                target.hp = 0

        cleric = next((h for h in heroes if h.alive and h.heal > 0), None)
        if cleric and round_num % 2 == 0:
            weakest = min((h for h in heroes if h.alive), key=lambda h: h.hp, default=None)
            if weakest:
                weakest.hp = min(weakest.max_hp, weakest.hp + cleric.heal)

    alive_count = sum(1 for h in heroes if h.alive)
    monster_defeated = monster.hp <= 0
    outcome = "vaincu" if monster_defeated else "toujours debout"
    events.append(RaidEvent(
        room_id=room_label,
        event_type="combat",
        description=(
            f"Combat ({round_num} tours) contre {monster.monster_type.value} — {outcome}. "
            f"{alive_count} héros survivants."
        ),
        heroes_alive=alive_count,
        details={"rounds": round_num, "monster_defeated": monster_defeated,
                 "monster_hp_left": max(0, monster.hp)},
    ))
    return heroes, events


def resolve_trap(heroes: list[HeroInstance]):
    casualties = []
    for hero in [h for h in heroes if h.alive]:
        if random.random() < hero.trap_dodge:
            continue
        dmg = TRAP_BASE_DAMAGE + random.randint(-2, 3)
        hero.hp -= dmg
        if hero.hp <= 0:
            hero.alive = False
            hero.hp = 0
            casualties.append(hero.name)

    alive_count = sum(1 for h in heroes if h.alive)
    if casualties:
        desc = f"Piège ! {', '.join(casualties)} {'est tué' if len(casualties)==1 else 'sont tués'}."
    else:
        desc = "Piège déclenché — les héros esquivent ou résistent."

    return heroes, RaidEvent(
        room_id="trap", event_type="trap",
        description=desc, heroes_alive=alive_count,
        details={"casualties": casualties},
    )
