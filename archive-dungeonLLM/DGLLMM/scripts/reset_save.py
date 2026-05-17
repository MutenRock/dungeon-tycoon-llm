from backend.app.repositories.game_state_repository import GameStateRepository

repo = GameStateRepository()
repo.reset()
print("Game state reset.")
