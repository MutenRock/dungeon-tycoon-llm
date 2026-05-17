from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
import asyncio
import json
import os
from openai import AsyncOpenAI

app = FastAPI(title="Dungeon Master AI Proto - Ollama Edition")

# --- Configuration Ollama via l'API compatible OpenAI ---
# Assurez-vous d'avoir lancé Ollama localement avec : ollama run llama3 (ou mistral)
client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama" # Clé factice requise par le client OpenAI
)

# Modèles locaux à utiliser (doivent être "pull" via Ollama)
HEAVY_MODEL = "llama3" # ou "mistral" ou "phi3"
FAST_MODEL = "llama3"  # Idéalement un modèle plus petit comme "qwen2:0.5b" ou "phi3"

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

# --- HEAVY LLM: Lucifer Intro & Deep Conversations ---
@app.post("/api/chat/lucifer")
async def chat_lucifer(req: ChatRequest):
    """
    Endpoint pour le dialogue 'Heavy LLM' propulsé par Ollama.
    """
    try:
        # Construction du prompt
        system_prompt = {
            "role": "system", 
            "content": "Tu es Lucifer. Tu confies un donjon au joueur. Sois cynique, sombre mais amusant. Pose-lui des questions courtes pour cerner sa personnalité. Limite tes réponses à 2 ou 3 phrases maximum."
        }
        messages = [system_prompt] + req.history + [{"role": "user", "content": req.message}]

        # Appel à Ollama en local
        response = await client.chat.completions.create(
            model=HEAVY_MODEL, 
            messages=messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content

        # Logique d'évaluation fictive pour le prototype (à remplacer par une vraie analyse LLM JSON)
        score = 50 + len(req.message) % 20 

    except Exception as e:
        reply = f"Erreur avec Ollama (Vérifiez que l'application Ollama est lancée) : {str(e)}"
        score = 0

    return {"reply": reply, "hidden_wish_score": score}

# --- FAST LLM: Background Barks via WebSockets ---
@app.websocket("/ws/background-chat")
async def websocket_endpoint(websocket: WebSocket):
    """
    Envoie des messages d'ambiance en temps réel.
    Généré à la volée par le Fast LLM local.
    """
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(10) # Un message toutes les 10 secondes
            try:
                # Génération d'une petite phrase d'ambiance avec Ollama
                response = await client.chat.completions.create(
                    model=FAST_MODEL,
                    messages=[{
                        "role": "system",
                        "content": "Tu es un gobelin de donjon. Dis une phrase très courte (max 10 mots) sur ton travail ou le Boss."
                    }],
                    max_tokens=30,
                    temperature=0.9
                )
                msg = response.choices[0].message.content.replace('"', '')
                bark = {"npc": "Gobelin", "msg": msg}
            except Exception:
                # Fallback si l'IA rame ou plante
                bark = {"npc": "Système", "msg": "Zzz... (Ollama hors ligne)"}

            await websocket.send_json(bark)
    except WebSocketDisconnect:
        print("Client déconnecté du background chat")

# Mount frontend
os.makedirs("dungeon_proto/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="dungeon_proto/static"), name="static")

@app.get("/")
async def root():
    return FileResponse("dungeon_proto/static/index.html")
