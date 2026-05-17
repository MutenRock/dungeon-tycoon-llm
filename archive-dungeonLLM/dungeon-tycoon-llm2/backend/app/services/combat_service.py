from backend.app.models.hero import Hero
from backend.app.models.room import Room


class CombatService:
    def resolve_room(self, heroes: list[Hero], room: Room) -> tuple[list[Hero], list[str]]:
        logs: list[str] = []

        if room.type == "trap_room":
            if heroes:
                heroes[0].hp -= 2
                logs.append(f"{heroes[0].name} triggers a trap and loses 2 HP.")

        if room.type == "monster_room":
            for hero in heroes:
                hero.hp -= 1
            logs.append("The heroes fight dungeon monsters and each lose 1 HP.")

        alive = [hero for hero in heroes if hero.hp > 0]
        if len(alive) < len(heroes):
            logs.append("One or more heroes fall in battle.")

        return alive, logs
