# Services — Business Logic

All game logic lives in service classes. Services receive a `GameStateRepository` and operate on Pydantic models.

## LLM Architecture

The `LLMService` implements a **two-tier** system:

| Tier | Model | Timeout | Use Cases |
|------|-------|---------|-----------|
| **Primary** | Claude Sonnet/Opus | 10 s | Advisor dialogue, Lucifer intro, hidden-wish scoring, event resolution |
| **Fast** | Claude Haiku | 3 s | Monster chatter, hero dialogue, raid narration, naming, daily summaries |

**Fallback**: When the API is unavailable, pre-written responses from `data/fallback_dialogue.json` are used.

**Key rule**: The LLM never decides game logic. Only the hidden-wish score (a float 0.0–1.0) crosses the LLM→game boundary, and outcomes are pre-defined in data.

## Prompt Loading

`PromptLoader` reads Markdown templates from `prompts/` and fills `{{ variable }}` placeholders with game state.

## Service List

| Service | File | Description |
|---------|------|-------------|
| `LLMService` | `llm_service.py` | Two-tier LLM calls + fallback |
| `PromptLoader` | `prompt_loader.py` | Template loading and variable substitution |
