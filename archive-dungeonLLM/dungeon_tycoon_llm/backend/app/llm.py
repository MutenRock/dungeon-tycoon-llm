from __future__ import annotations
import httpx
from .models import RaidResult, GameState

OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"


def _fallback_narrative(raid: RaidResult) -> str:
    if raid.game_over:
        return "Le donjon est tombé. Le boss git dans les ruines, vaincu pour la dernière fois."
    if raid.heroes_won:
        return (f"Les héros ont vaincu le boss et emporté {raid.treasure_stolen} pièces d'or. "
                f"Il reste {raid.boss_lives_remaining} vie(s) au boss.")
    return f"Le donjon a résisté à l'assaut. {raid.treasure_stolen} pièces perdues en chemin."


async def generate_narrative(raid: RaidResult, state: GameState) -> str:
    events_text = "
".join(f"- {e.description}" for e in raid.events)
    result_line = "Les héros ont vaincu le boss !" if raid.heroes_won else "Le donjon a tenu bon."

    prompt = (
        "Tu es le narrateur épique d'un donjon fantastique. "
        "Résume l'incursion suivante en 3-4 phrases dramatiques en français. "
        "Sois concis, vivant, sans liste.

"
        f"Événements :
{events_text}

"
        f"Résultat : {result_line}
"
        f"Trésor perdu : {raid.treasure_stolen} pièces.
"
        f"Vies du boss restantes : {raid.boss_lives_remaining}/3.

"
        "Narratif :"
    )
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            })
            if resp.status_code == 200:
                return resp.json().get("response", "").strip()
    except Exception:
        pass
    return _fallback_narrative(raid)
