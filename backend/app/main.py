"""FastAPI application — Dungeon Tycoon LLM."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes_game import router as game_router
from backend.app.api.routes_setup import router as setup_router
from backend.app.api.routes_grid import router as grid_router
from backend.app.api.routes_raid import router as raid_router
from backend.app.api.routes_dialogue import router as dialogue_router
from backend.app.api.routes_characters import router as characters_router
from backend.app.api.routes_bestiary import router as bestiary_router
from backend.app.api.routes_patterns import router as patterns_router
from backend.app.api.routes_llm import router as llm_router
from backend.app.api.routes_admin import router as admin_router

app = FastAPI(
    title="Dungeon Tycoon LLM",
    description="A dungeon management game with LLM-powered NPC dialogue",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_router)
app.include_router(setup_router)
app.include_router(grid_router)
app.include_router(raid_router)
app.include_router(dialogue_router)
app.include_router(characters_router)
app.include_router(bestiary_router)
app.include_router(patterns_router)
app.include_router(llm_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {"message": "Dungeon Tycoon LLM API", "version": "0.1.0"}
