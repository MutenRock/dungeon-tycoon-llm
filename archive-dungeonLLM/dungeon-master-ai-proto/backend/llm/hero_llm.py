import json
import os

# Fichier de mémoire persistante pour les héros
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "heroes_memory.json")

HERO_PROFILES = {
    "Amelios": "Mage. Doux, bienveillant, poétique, émerveillé par la magie. Parle calmement. Rôle: Arrière-ligne, soutien magique.",
    "Léorian": "Archer. Serein, intelligent, méthodique, posé. Analyse la situation, parle peu mais utilement. Rôle: Arrière-ligne, tactique.",
    "Yanskar": "Assassin. Moqueur, provocateur, joueur, sadique avec les monstres. Humour noir, insolent. Rôle: Avant-ligne, dégâts.",
    "Pierrick": "Chevalier. Jeune, hyperactif, enthousiaste, courageux. Veut toujours avancer, parle avec fougue. Rôle: Avant-ligne, tank."
}

def load_memories():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_memories(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_memory(hero_name: str, event_summary: str):
    memories = load_memories()
    if hero_name not in memories:
        memories[hero_name] = []

    memories[hero_name].append(event_summary)

    # On garde seulement les 5 derniers souvenirs majeurs pour ne pas exploser le contexte LLM
    if len(memories[hero_name]) > 5:
        memories[hero_name] = memories[hero_name][-5:]

    save_memories(memories)

def get_memory_string(hero_name: str) -> str:
    memories = load_memories().get(hero_name, [])
    if not memories:
        return "Aucun souvenir particulier pour le moment."
    return " | ".join(memories)

async def generate_combat_bark(client, model: str, hero_name: str, context_event: str) -> str:
    profile = HERO_PROFILES.get(hero_name, "Héros basique.")
    memory_context = get_memory_string(hero_name)

    system_prompt = (
        f"Tu es {hero_name}, un héros explorant un donjon. "
        f"Ta personnalité : {profile}\n"
        f"Tes traumatismes/souvenirs récents : {memory_context}\n"
        f"Tu dois réagir à cet événement : '{context_event}'. "
        "Si l'événement fait écho à tes souvenirs (ex: revoir un monstre qui a tué ton ami), mentionne-le subtilement en respectant ta personnalité. "
        "Génère UNE SEULE phrase courte (max 15 mots). Ne mets pas de guillemets."
    )

    messages = [{"role": "system", "content": system_prompt}]

    try:
        response = await client.chat.completions.create(
            model=model, messages=messages, temperature=0.8, max_tokens=40
        )
        return response.choices[0].message.content.strip().replace('"', '')
    except Exception as e:
        return "..."
