"""Tests for LLM service — fallback behavior and backend selection."""

from backend.app.services.llm_service import LLMService


def _no_backend():
    """Create an LLM service with no backend available (for fallback tests)."""
    return LLMService(backend="anthropic", anthropic_api_key=None)


def test_llm_unavailable_without_key():
    llm = _no_backend()
    assert not llm.available


def test_ollama_backend_name():
    # Won't connect but should set backend correctly
    llm = LLMService(backend="ollama", ollama_primary_model="mistral")
    assert "ollama" in llm.backend_name or "fallback" in llm.backend_name


def test_fallback_daily_summary():
    llm = _no_backend()
    result = llm.daily_summary("Day 1, all quiet", "en")
    assert isinstance(result, str)
    assert len(result) > 0


def test_fallback_monster_chatter():
    llm = _no_backend()
    result = llm.monster_chatter(["Grak", "Snig"], "idle time", "en")
    assert isinstance(result, list)
    assert len(result) > 0


def test_fallback_raid_narration():
    llm = _no_backend()
    result = llm.raid_narration("Heroes enter the dungeon", "en")
    assert isinstance(result, str)


def test_fallback_lucifer_question():
    llm = _no_backend()
    q = llm.lucifer_question(1, [], "en")
    assert isinstance(q, str)
    assert len(q) > 10


def test_fallback_lucifer_question_fr():
    llm = _no_backend()
    q = llm.lucifer_question(1, [], "fr")
    assert isinstance(q, str)


def test_fallback_judge_wish():
    llm = _no_backend()
    score = llm.judge_hidden_wish("wants more meat", [], "en")
    assert score == 0.5  # neutral fallback


def test_fallback_generate_name():
    llm = _no_backend()
    name = llm.generate_name("hero", "human", "en")
    assert isinstance(name, str)
    assert len(name) > 0


def test_prompt_loader_list():
    llm = _no_backend()
    templates = llm.prompt_loader.list_templates()
    assert "lucifer_intro" in templates
    assert "advisor_dialogue" in templates


def test_fallback_chatter_fr():
    llm = _no_backend()
    result = llm.monster_chatter(["Gobu", "Orky"], "", "fr")
    assert isinstance(result, list)
