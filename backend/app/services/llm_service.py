"""Two-tier LLM service supporting Ollama (local) and Anthropic (cloud).

Primary tier  — Stronger model for real conversations (advisors, Lucifer, wish scoring)
Fast tier     — Lighter model for background chatter, narration, naming

Falls back to cached/template responses when no LLM backend is available.
"""

from __future__ import annotations

import json
import logging
import random
from pathlib import Path
from typing import Any

from backend.app.services.prompt_loader import PromptLoader

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _load_fallbacks() -> dict:
    path = DATA_DIR / "fallback_dialogue.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


class LLMService:
    """Unified interface for all LLM calls, split into primary and fast tiers.

    Supports two backends:
    - **ollama**: Local models via OpenAI-compatible API (default)
    - **anthropic**: Claude models via Anthropic SDK
    """

    def __init__(
        self,
        backend: str = "ollama",
        # Ollama settings
        ollama_base_url: str = "http://localhost:11434/v1",
        ollama_primary_model: str = "mistral",
        ollama_fast_model: str = "mistral",
        # Anthropic settings
        anthropic_api_key: str | None = None,
        anthropic_primary_model: str = "claude-sonnet-4-20250514",
        anthropic_fast_model: str = "claude-haiku-4-5-20251001",
        # Shared settings
        primary_timeout: int = 10,
        fast_timeout: int = 3,
        fallback_enabled: bool = True,
    ):
        """Initialise the LLM service.

        Args:
            primary_timeout: Timeout for primary-tier calls **in seconds**.
                The application config stores milliseconds; the caller
                (``dependencies.py``) is responsible for converting to seconds
                before passing them here.
            fast_timeout: Timeout for fast-tier calls **in seconds**.
                Same conversion note as *primary_timeout*.
        """
        self.backend = backend
        self.primary_timeout = primary_timeout
        self.fast_timeout = fast_timeout
        self.fallback_enabled = fallback_enabled
        self.prompt_loader = PromptLoader()
        self._fallbacks = _load_fallbacks()

        self._ollama_client = None
        self._anthropic_client = None
        self._primary_model: str = ""
        self._fast_model: str = ""

        if backend == "ollama":
            self._init_ollama(ollama_base_url, ollama_primary_model, ollama_fast_model, primary_timeout)
            self.check_ollama_models()
        elif backend == "anthropic":
            self._init_anthropic(anthropic_api_key, anthropic_primary_model, anthropic_fast_model, primary_timeout)

    def _init_ollama(self, base_url: str, primary_model: str, fast_model: str, timeout: int) -> None:
        self._primary_model = primary_model
        self._fast_model = fast_model
        self._ollama_base_url = base_url
        try:
            from openai import OpenAI
            self._ollama_client = OpenAI(base_url=base_url, api_key="ollama", timeout=timeout)
        except ImportError:
            logger.warning("openai package not installed — Ollama backend unavailable")

    def _init_anthropic(self, api_key: str | None, primary_model: str, fast_model: str, timeout: int) -> None:
        self._primary_model = primary_model
        self._fast_model = fast_model
        if api_key:
            try:
                from anthropic import Anthropic
                self._anthropic_client = Anthropic(api_key=api_key, timeout=timeout)
            except ImportError:
                logger.warning("anthropic package not installed — Anthropic backend unavailable")

    def check_ollama_models(self) -> None:
        """Verify that the configured Ollama models are available.

        Logs warnings for any missing models. Never raises — failures are
        silently tolerated so the service can still fall back to templates.
        """
        if self._ollama_client is None:
            return
        # Ollama exposes a model listing on its native API (not the OpenAI shim).
        # Derive the native URL from the OpenAI-compat base_url.
        import urllib.request
        import urllib.error
        base = getattr(self, "_ollama_base_url", "http://localhost:11434/v1")
        native_url = base.replace("/v1", "") + "/api/tags"
        try:
            with urllib.request.urlopen(native_url, timeout=5) as resp:
                data = json.loads(resp.read().decode())
            available = {m["name"].split(":")[0] for m in data.get("models", [])}
            for label, model in [("primary", self._primary_model), ("fast", self._fast_model)]:
                short = model.split(":")[0]
                if short not in available:
                    logger.warning(
                        "Ollama %s model '%s' not found locally. "
                        "Available models: %s. Pull it with: ollama pull %s",
                        label, model, ", ".join(sorted(available)) or "(none)", model,
                    )
        except Exception as e:
            logger.warning("Could not list Ollama models at %s: %s", native_url, e)

    def health(self) -> dict:
        """Return a lightweight status dict for monitoring / health-check endpoints."""
        return {
            "available": self.available,
            "backend_name": self.backend_name,
            "ollama_ok": self._ollama_client is not None,
            "anthropic_ok": self._anthropic_client is not None,
        }

    @property
    def available(self) -> bool:
        return self._ollama_client is not None or self._anthropic_client is not None

    @property
    def backend_name(self) -> str:
        if self._ollama_client:
            return f"ollama ({self._primary_model})"
        if self._anthropic_client:
            return f"anthropic ({self._primary_model})"
        return "fallback"

    # ------------------------------------------------------------------
    # Internal call helpers
    # ------------------------------------------------------------------

    def _call(self, model: str, system: str, user_msg: str, max_tokens: int = 300) -> str | None:
        """Route the call to the active backend. Returns None on failure."""
        if self._ollama_client:
            return self._call_ollama(model, system, user_msg, max_tokens)
        if self._anthropic_client:
            return self._call_anthropic(model, system, user_msg, max_tokens)
        return None

    def _call_ollama(self, model: str, system: str, user_msg: str, max_tokens: int) -> str | None:
        try:
            response = self._ollama_client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_msg},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.warning("LLM call failed (%s): %s", model, e)
            return None

    def _call_anthropic(self, model: str, system: str, user_msg: str, max_tokens: int) -> str | None:
        try:
            response = self._anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user_msg}],
            )
            return response.content[0].text
        except Exception as e:
            logger.warning("LLM call failed (%s): %s", model, e)
            return None

    def _primary(self, system: str, user_msg: str, max_tokens: int = 300) -> str | None:
        return self._call(self._primary_model, system, user_msg, max_tokens)

    def _fast(self, system: str, user_msg: str, max_tokens: int = 150) -> str | None:
        return self._call(self._fast_model, system, user_msg, max_tokens)

    def _fallback(self, category: str, lang: str = "en") -> str:
        items = self._fallbacks.get(category, {}).get(lang, [])
        if isinstance(items, list) and items:
            pick = random.choice(items)
            if isinstance(pick, list):
                return " — ".join(pick)
            return pick
        if isinstance(items, dict):
            return random.choice(list(items.values())) if items else ""
        return ""

    # ------------------------------------------------------------------
    # PRIMARY TIER — real conversations
    # ------------------------------------------------------------------

    def lucifer_question(self, step: int, previous_answers: list[dict], language: str = "en") -> str:
        """Generate the next Lucifer intro question."""
        system = self.prompt_loader.load(
            "lucifer_intro", step=str(step), language=language
        )
        context = json.dumps(previous_answers, ensure_ascii=False) if previous_answers else "[]"
        result = self._primary(system, f"Previous exchanges:\n{context}\n\nGenerate question {step}.", 200)
        if result:
            return result
        # Fallback questions
        fallback_q = {
            "en": [
                "What drives you to seek power in the depths?",
                "How do you treat those who serve you?",
                "What is your greatest fear?",
                "Do you prefer cunning or brute force?",
                "What would you sacrifice for victory?",
            ],
            "fr": [
                "Qu'est-ce qui vous pousse à chercher le pouvoir dans les profondeurs ?",
                "Comment traitez-vous ceux qui vous servent ?",
                "Quelle est votre plus grande peur ?",
                "Préférez-vous la ruse ou la force brute ?",
                "Que sacrifieriez-vous pour la victoire ?",
            ],
        }
        questions = fallback_q.get(language, fallback_q["en"])
        return questions[min(step - 1, len(questions) - 1)]

    def lucifer_analyze(self, question: str, answer: str, language: str = "en") -> str:
        """Analyze a player's answer to a Lucifer question."""
        system = self.prompt_loader.load("lucifer_analysis", language=language)
        result = self._primary(system, f"Question: {question}\nAnswer: {answer}", 150)
        return result or "The answer reveals a complex character..."

    def advisor_dialogue(
        self,
        advisor_name: str,
        advisor_role: str,
        personality: str,
        player_message: str,
        context: dict[str, Any] | None = None,
        language: str = "en",
    ) -> str:
        """Generate advisor response in a conversation with the player."""
        system = self.prompt_loader.load(
            "advisor_dialogue",
            advisor_name=advisor_name,
            advisor_role=advisor_role,
            personality=personality,
            language=language,
        )
        ctx = json.dumps(context or {}, ensure_ascii=False)
        result = self._primary(system, f"Context: {ctx}\n\nPlayer says: {player_message}", 250)
        if result:
            return result
        return self._fallback("advisor_interjection", language)

    def judge_hidden_wish(
        self,
        wish_objective: str,
        conversation: list[dict],
        language: str = "en",
    ) -> float:
        """Score how well the player satisfied a hidden wish (0.0–1.0)."""
        system = self.prompt_loader.load(
            "hidden_wish_judge", objective=wish_objective, language=language
        )
        conv_text = json.dumps(conversation, ensure_ascii=False)
        result = self._primary(system, f"Conversation:\n{conv_text}\n\nReturn ONLY a number between 0.0 and 1.0.", 20)
        if result:
            try:
                score = float(result.strip())
                return max(0.0, min(1.0, score))
            except ValueError:
                pass
        return 0.5  # neutral fallback

    # ------------------------------------------------------------------
    # FAST TIER — background / ambient
    # ------------------------------------------------------------------

    def monster_chatter(self, monster_names: list[str], context: str = "", language: str = "en") -> list[str]:
        """Generate ambient monster dialogue lines."""
        system = self.prompt_loader.load("monster_chatter", language=language)
        user_msg = f"Monsters present: {', '.join(monster_names)}\nContext: {context}"
        result = self._fast(system, user_msg, 200)
        if result:
            return [line.strip("- ").strip() for line in result.strip().split("\n") if line.strip()]
        fb = self._fallbacks.get("monster_chatter", {}).get(language, [])
        return random.choice(fb) if fb else ["..."]

    def hero_dialogue(self, hero_names: list[str], room_type: str, language: str = "en") -> list[str]:
        """Generate hero party dialogue during a raid."""
        system = self.prompt_loader.load("hero_dialogue", language=language)
        user_msg = f"Heroes: {', '.join(hero_names)}\nRoom: {room_type}"
        result = self._fast(system, user_msg, 150)
        if result:
            return [line.strip("- ").strip() for line in result.strip().split("\n") if line.strip()]
        return [f"The heroes cautiously enter the {room_type}..."]

    def raid_narration(self, raid_summary: str, language: str = "en") -> str:
        """Generate a dramatic raid narration line."""
        system = self.prompt_loader.load("hero_raid_narration", language=language)
        result = self._fast(system, raid_summary, 120)
        return result or self._fallback("raid_narration", language)

    def daily_summary(self, state_summary: str, language: str = "en") -> str:
        """Generate an end-of-day narrative summary."""
        system = self.prompt_loader.load("dungeon_summary", language=language)
        result = self._fast(system, state_summary, 150)
        return result or self._fallback("daily_summary", language)

    def generate_name(self, entity_type: str, species: str = "", language: str = "en") -> str:
        """Generate a procedural name for a hero or monster."""
        system = self.prompt_loader.load("naming", language=language)
        result = self._fast(system, f"Generate a name for a {species} {entity_type}.", 30)
        return result.strip().strip('"').strip() if result else f"Unknown {entity_type.title()}"
