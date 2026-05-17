import json

async def generate_lucifer_response(client, model: str, user_message: str, history: list, context: dict) -> tuple[str, str]:
    turn_count = len(history) // 2 
    p_name = context.get("name", "Candidat")
    p_race = context.get("race", "Créature")
    d_name = context.get("dungeonName", "Le Donjon")

    # Nouveau système : Intro plus courte (3 tours max), explique les règles, et donne une récompense à la fin
    lore_context = (
        f"Tu es Lucifer. Tu envoies le joueur ({p_name}, un {p_race}) conquérir le monde des humains. "
        f"Il va gérer un donjon nommé '{d_name}'. "
        "Ton ton doit être direct, autoritaire mais tu dois aussi lui expliquer brièvement ce qu'il va faire (construire la nuit, tuer des héros le jour). "
    )

    if turn_count == 0:
        system_prompt = (
            lore_context + 
            "C'est le début de l'entretien (Tour 1/3). "
            "Accueille-le brièvement, rappelle-lui qu'il doit amasser de l'or en tuant des héros, et pose-lui une question sur ce qu'il préfère : "
            "la force brute, la magie, ou la ruse. "
            "Réponds EXCLUSIVEMENT au format JSON : {\"reply\": \"Ton texte ici\", \"reward\": \"none\"}"
        )
    elif turn_count == 1:
        system_prompt = (
            lore_context + 
            "C'est la suite de l'entretien (Tour 2/3). "
            "Réagis brièvement à sa réponse. Explique-lui qu'il aura 3 vies (si 3 héros atteignent sa salle, il est mort). "
            "Demande-lui quelle créature spéciale il aimerait avoir pour l'aider dans sa tâche. "
            "Réponds EXCLUSIVEMENT au format JSON : {\"reply\": \"Ton texte ici\", \"reward\": \"none\"}"
        )
    else:
        system_prompt = (
            lore_context + 
            "C'est la fin (Tour 3/3). "
            "Conclus l'entretien. Donne-lui les clés de son donjon. "
            "En fonction de ses réponses précédentes, attribue-lui UNE unité spéciale en récompense (ex: 'Banshee', 'Ogre', 'Assassin', 'Troll'). "
            "Réponds EXCLUSIVEMENT au format JSON strict : "
            "{\"reply\": \"Ton texte de conclusion ici\", \"reward\": \"Nom de la créature spéciale\"}"
        )

    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": user_message}]

    try:
        response = await client.chat.completions.create(
            model=model, messages=messages, temperature=0.7, response_format={"type": "json_object"}
        )
        raw_content = response.choices[0].message.content.strip()
        if raw_content.startswith("```json"): raw_content = raw_content[7:]
        if raw_content.endswith("```"): raw_content = raw_content[:-3]

        data = json.loads(raw_content)
        return data.get("reply", "Bien. Descends sur terre maintenant."), data.get("reward", "none")
    except Exception as e:
        print("Erreur Heavy LLM:", e)
        return "Le portail est ouvert. Vas-y.", "none"
