from backend.app.models.player import PlayerState


class LLMService:
    def generate_daily_summary(self, state: PlayerState) -> str:
        # Stub local. À remplacer par un vrai appel API plus tard.
        return (
            f"Day {state.day} summary: the dungeon holds {state.treasure} treasure, "
            f"{state.lives} lives remain, and the workers report "
            f"{state.resources.wood} wood / {state.resources.stone} stone / {state.resources.meat} meat."
        )
