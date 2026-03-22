# Prompts — LLM Template System

Markdown templates loaded by `PromptLoader`. Each file uses `{{ variable }}` placeholders filled at runtime.

## Template List

| Template | Tier | Purpose |
|----------|------|---------|
| `lucifer_intro.md` | Primary | Lucifer's 5 interview questions at game start |
| `lucifer_analysis.md` | Primary | Analyze player's answer for personality profiling |
| `advisor_dialogue.md` | Primary | Advisor conversation with character injection |
| `advisor_interjection.md` | Primary | Advisor initiates a conversation with hidden objective |
| `hidden_wish_judge.md` | Primary | Score player response vs hidden wish (returns float) |
| `event_resolution.md` | Primary | Narrate the outcome of a triggered event |
| `hero_dialogue.md` | Fast | Heroes talking during raids |
| `monster_chatter.md` | Fast | Ambient monster background dialogue |
| `hero_raid_narration.md` | Fast | Dramatic raid narration |
| `dungeon_summary.md` | Fast | End-of-day chronicle entry |
| `naming.md` | Fast | Procedural name generation |

## Variable Convention

All templates receive `{{ language }}` ("en" or "fr") and adjust their output accordingly.
Other variables are template-specific (e.g., `{{ advisor_name }}`, `{{ step }}`).
