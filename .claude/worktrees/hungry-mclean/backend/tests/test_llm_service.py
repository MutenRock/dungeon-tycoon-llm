"""Tests for LLM service — fallback behavior without API key."""

from backend.app.services.llm_service import LLMService


def test_llm_unavailable_without_key():
    llm = LLMService(api_key=None)
    assert not llm.available


def test_fallback_daily_summary():
    llm = LLMService(api_key=None)
    result = llm.daily_summary("Day 1, all quiet", "en")
    assert isinstance(result, str)
    assert len(result) > 0


def test_fallback_monster_chatter():
    llm = LLMService(api_key=None)
    result = llm.monster_chatter(["Grak", "Snig"], "idle time", "en")
    assert isinstance(result, list)
    assert len(result) > 0


def test_fallback_raid_narration():
    llm = LLMService(api_key=None)
    result = llm.raid_narration("Heroes enter the dungeon", "en")
    assert isinstance(result, str)


def test_fallback_lucifer_question():
    llm = LLMService(api_key=None)
    q = llm.lucifer_question(1, [], "en")
    assert isinstance(q, str)
    assert len(q) > 10


def test_fallback_lucifer_question_fr():
    llm = LLMService(api_key=None)
    q = llm.lucifer_question(1, [], "fr")
    assert isinstance(q, str)


def test_fallback_judge_wish():
    llm = LLMService(api_key=None)
    score = llm.judge_hidden_wish("wants more meat", [], "en")
    assert score == 0.5  # neutral fallback


def test_fallback_generate_name():
    llm = LLMService(api_key=None)
    name = llm.generate_name("hero", "human", "en")
    assert isinstance(name, str)
    assert len(name) > 0


def test_prompt_loader_list():
    llm = LLMService(api_key=None)
    templates = llm.prompt_loader.list_templates()
    assert "lucifer_intro" in templates
    assert "advisor_dialogue" in templates


def test_fallback_chatter_fr():
    llm = LLMService(api_key=None)
    result = llm.monster_chatter(["Gobu", "Orky"], "", "fr")
    assert isinstance(result, list)
