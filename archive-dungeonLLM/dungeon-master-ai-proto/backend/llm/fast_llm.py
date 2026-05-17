import json

async def generate_npc_encounter(client, model: str, race1: str, race2: str) -> dict:
    system_prompt = (
        "Tu génères une très courte discussion entre deux monstres de donjon qui se croisent. "
        "Ils sont sadiques, stupides ou se plaignent du boss. "
        "Réponds EXCLUSIVEMENT en JSON strict avec ce format : "
        "{\"npc1_text\": \"phrase du monstre 1\", \"npc2_text\": \"réponse du monstre 2\"}"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Un {race1} rencontre un {race2}."}
    ]
    try:
        res = await client.chat.completions.create(model=model, messages=messages, temperature=0.9, response_format={"type": "json_object"})
        raw = res.choices[0].message.content.strip()
        if raw.startswith("```json"): raw = raw[7:]
        if raw.endswith("```"): raw = raw[:-3]
        return json.loads(raw)
    except:
        return {"npc1_text": "Grmbl...", "npc2_text": "Zzz..."}
