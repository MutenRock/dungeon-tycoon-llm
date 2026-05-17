import json
from pathlib import Path

from backend.app.models.player import PlayerState


class SaveRepository:
    def save_to_file(self, state: PlayerState, filepath: str) -> None:
        Path(filepath).write_text(state.model_dump_json(indent=2), encoding="utf-8")

    def load_from_file(self, filepath: str) -> PlayerState:
        data = json.loads(Path(filepath).read_text(encoding="utf-8"))
        return PlayerState.model_validate(data)
