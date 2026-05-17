from backend.app.repositories.game_state_repository import GameStateRepository

repo = GameStateRepository()
state = repo.get_state()
print("Seed preview:")
print(state.model_dump_json(indent=2))
