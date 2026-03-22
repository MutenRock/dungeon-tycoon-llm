"""Loads prompt templates from the prompts/ directory and substitutes variables."""

from __future__ import annotations

import os
import re
from pathlib import Path


PROMPTS_DIR = Path(__file__).resolve().parents[3] / "prompts"


class PromptLoader:
    """Reads .md prompt templates and fills {{ variable }} placeholders."""

    def __init__(self, prompts_dir: Path | str | None = None):
        self.prompts_dir = Path(prompts_dir) if prompts_dir else PROMPTS_DIR

    def load(self, template_name: str, **kwargs: str) -> str:
        """Load a template by name (without .md) and substitute variables.

        Example::

            loader.load("lucifer_intro", step="1", language="fr")
        """
        path = self.prompts_dir / f"{template_name}.md"
        if not path.exists():
            return f"[missing template: {template_name}]"

        text = path.read_text(encoding="utf-8")
        # Replace {{ var }} placeholders
        def _replace(match: re.Match) -> str:
            key = match.group(1).strip()
            return kwargs.get(key, match.group(0))

        return re.sub(r"\{\{\s*(\w+)\s*\}\}", _replace, text)

    def list_templates(self) -> list[str]:
        """Return available template names."""
        if not self.prompts_dir.exists():
            return []
        return sorted(
            p.stem for p in self.prompts_dir.glob("*.md") if p.is_file()
        )
