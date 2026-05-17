from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import settings
from backend.app.api.routes_game import router as game_router
from backend.app.api.routes_grid import router as grid_router
from backend.app.api.routes_raid import router as raid_router
from backend.app.api.routes_llm import router as llm_router

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_router, prefix="/api/game", tags=["game"])
app.include_router(grid_router, prefix="/api/grid", tags=["grid"])
app.include_router(raid_router, prefix="/api/turn", tags=["turn"])
app.include_router(llm_router, prefix="/api/llm", tags=["llm"])


@app.get("/")
def root() -> dict:
    return {
        "name": settings.app_name,
        "status": "ok",
        "message": "Dungeon Tycoon LLM backend is running."
    }
