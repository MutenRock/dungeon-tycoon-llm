# Data — Static Game Data

JSON files holding all game-balancing values, entity definitions, and fallback content.

## Files

| File | Description |
|------|-------------|
| `monsters.json` | Monster species bestiary with traits, tasks, and variants |
| `heroes.json` | Hero classes with tiered stats (common → legendary) |
| `rooms.json` | Room types with costs, sizes, door limits, and production |
| `advisors.json` | 5 advisor roles with personality templates per monster race |
| `dungeon_names.json` | Dungeon name lists by theme (dark, fire, bone, swamp, ice) — EN/FR |
| `balance.json` | Numeric balance: resource rates, party sizes, damage values, death penalties |
| `fallback_dialogue.json` | Pre-written dialogue when LLM is unavailable — EN/FR |

## Design Rules

- All balance values live here, **not** in code constants
- Every text entry has EN and FR variants
- LLM fallback content covers: daily summaries, monster chatter, raid narration, advisor interjections
- Monster species define which tasks they can perform (guard, worker, cook, spy)
- Hero tiers scale with `day_thresholds` from balance.json
