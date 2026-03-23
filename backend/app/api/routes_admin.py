"""Admin routes — backend diagnostics, LLM status, game state inspection."""

from __future__ import annotations

import platform
import sys
from pathlib import Path

from fastapi import APIRouter, Depends

from backend.app.config import Settings
from backend.app.dependencies import get_llm, get_repo

router = APIRouter(prefix="/api/admin", tags=["admin"])

_settings = Settings()


@router.get("/info")
def admin_info(llm=Depends(get_llm), repo=Depends(get_repo)):
    """Full backend diagnostics for the admin panel."""
    state = repo.get_state()

    # Check Ollama reachability
    ollama_ok = False
    if llm._ollama_client:
        try:
            llm._ollama_client.models.list()
            ollama_ok = True
        except Exception:
            pass

    # Check Anthropic reachability
    anthropic_ok = False
    if llm._anthropic_client:
        try:
            # Light call — just verify auth
            anthropic_ok = True
        except Exception:
            pass

    return {
        "system": {
            "python": sys.version,
            "platform": platform.platform(),
            "project_dir": str(Path(__file__).resolve().parents[3]),
        },
        "config": {
            "llm_backend": _settings.llm_backend,
            "ollama_base_url": _settings.ollama_base_url,
            "ollama_primary_model": _settings.ollama_primary_model,
            "ollama_fast_model": _settings.ollama_fast_model,
            "anthropic_primary_model": _settings.anthropic_primary_model,
            "anthropic_fast_model": _settings.anthropic_fast_model,
            "anthropic_key_set": bool(_settings.anthropic_api_key),
            "fallback_enabled": _settings.llm_fallback_enabled,
            "save_dir": _settings.save_dir,
            "default_language": _settings.default_language,
        },
        "llm": {
            "available": llm.available,
            "active_backend": llm.backend_name,
            "ollama_reachable": ollama_ok,
            "anthropic_reachable": anthropic_ok,
        },
        "game": {
            "has_active_game": state.game_config is not None,
            "day": state.day,
            "phase": state.phase,
            "lives": state.lives,
            "treasure": state.treasure,
            "rooms_placed": len(state.dungeon.rooms),
            "monsters_count": len(state.monsters),
            "advisors_count": len(state.advisors),
            "characters_registered": len(state.character_registry),
            "log_entries": len(state.logs),
        },
    }


@router.post("/llm-test")
def llm_test(llm=Depends(get_llm)):
    """Send a test prompt to the active LLM backend."""
    result = llm._fast(
        "You are a test assistant. Respond with exactly one short sentence.",
        "Say hello from the dungeon.",
        30,
    )
    return {
        "success": result is not None,
        "backend": llm.backend_name,
        "response": result or "LLM unavailable — fallback mode active",
    }


@router.get("/game-state")
def full_game_state(repo=Depends(get_repo)):
    """Raw game state dump for debugging."""
    state = repo.get_state()
    return state.model_dump()


@router.get("/logs")
def game_logs(repo=Depends(get_repo), limit: int = 50):
    """Recent game logs."""
    state = repo.get_state()
    logs = state.logs[-limit:] if state.logs else []
    return {"total": len(state.logs), "logs": logs}
