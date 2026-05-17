import json

# Contexte global des personnalités pour le LLM
HERO_PROFILES = {
    "Amelios": "Mage. Doux, bienveillant, poétique, émerveillé par la magie. Parle calmement. Rôle: Arrière-ligne, soutien magique.",
    "Léorian": "Archer. Serein, intelligent, méthodique, posé. Analyse la situation, parle peu mais utilement. Rôle: Arrière-ligne, tactique.",
    "Yanskar": "Assassin. Moqueur, provocateur, joueur, sadique avec les monstres. Humour noir, insolent. Rôle: Avant-ligne, dégâts.",
    "Pierrick": "Chevalier. Jeune, hyperactif, enthousiaste, courageux. Veut toujours avancer, parle avec fougue. Rôle: Avant-ligne, tank."
}

async def generate_combat_bark(client, model: str, hero_name: str, context_event: str) -> str:
    profile = HERO_PROFILES.get(hero_name, "Héros basique.")

    system_prompt = (
        f"Tu es {hero_name}, un héros dans un jeu vidéo explorant un donjon. "
        f"Ta personnalité : {profile} "
        f"Tu dois réagir à cet événement : '{context_event}'. "
        "Génère UNE SEULE phrase courte (max 10 mots) qui correspond parfaitement à ta personnalité. "
        "Ne mets pas de guillemets, juste la phrase. Reste très concis."
    )

    messages = [{"role": "system", "content": system_prompt}]

    try:
        response = await client.chat.completions.create(
            model=model, messages=messages, temperature=0.8, max_tokens=30
        )
        return response.choices[0].message.content.strip().replace('"', '')
    except Exception as e:
        return "..."
