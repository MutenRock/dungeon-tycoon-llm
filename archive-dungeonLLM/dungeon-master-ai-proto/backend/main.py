from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
import asyncio
import os
from openai import AsyncOpenAI
from .llm.heavy_llm import generate_lucifer_response
from .llm.fast_llm import generate_npc_encounter
from .llm.hero_llm import generate_combat_bark, add_memory, load_memories

app = FastAPI(title="Dungeon Master AI Proto")
client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
HEAVY_MODEL = "gemma3:4b"
FAST_MODEL = "gemma3:4b"

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []
    player_context: Dict[str, str] = {}

@app.post("/api/chat/lucifer")
async def chat_lucifer(req: ChatRequest):
    reply, reward = await generate_lucifer_response(client, HEAVY_MODEL, req.message, req.history, req.player_context)
    return {"reply": reply, "reward": reward}

class EncounterRequest(BaseModel):
    race1: str
    race2: str

@app.post("/api/chat/npc-encounter")
async def npc_encounter(req: EncounterRequest):
    res = await generate_npc_encounter(client, FAST_MODEL, req.race1, req.race2)
    return res

class HeroBarkRequest(BaseModel):
    hero_name: str
    event: str

@app.post("/api/chat/hero-bark")
async def hero_bark(req: HeroBarkRequest):
    bark = await generate_combat_bark(client, FAST_MODEL, req.hero_name, req.event)
    return {"bark": bark}

class MemoryRequest(BaseModel):
    hero_name: str
    memory: str

@app.post("/api/heroes/memory")
async def save_hero_memory(req: MemoryRequest):
    add_memory(req.hero_name, req.memory)
    return {"status": "success"}

@app.get("/api/heroes/memories")
async def get_all_memories():
    return load_memories()

current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))
