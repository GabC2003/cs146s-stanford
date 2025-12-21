from ..app.config import settings
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_llm_empty():
    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("   ") == []


@pytest.mark.skipif(settings.SKIP_LLM_TESTS, reason="Skipping LLM tests")
def test_extract_llm_bullets():
    text = """
    - Finish the report
    * [ ] Send email to team
    1. Update the wiki
    """
    items = extract_action_items_llm(text)
    # LLM might rephrase slightly, but should capture the core
    assert any("report" in item.lower() for item in items)
    assert any("email" in item.lower() for item in items)
    assert any("wiki" in item.lower() for item in items)


@pytest.mark.skipif(settings.SKIP_LLM_TESTS, reason="Skipping LLM tests")
def test_extract_llm_keywords():
    text = """
    todo: buy milk
    action: fix the bug
    next: refactor the code
    """
    items = extract_action_items_llm(text)
    assert any("milk" in item.lower() for item in items)
    assert any("bug" in item.lower() for item in items)
    assert any("refactor" in item.lower() for item in items)


@pytest.mark.skipif(settings.SKIP_LLM_TESTS, reason="Skipping LLM tests")
def test_extract_llm_narrative():
    text = "We had a meeting today. Gabriel should update the documentation by Friday and we need to schedule a follow-up."
    items = extract_action_items_llm(text)
    assert any("documentation" in item.lower() for item in items)
    assert any("follow" in item.lower() for item in items)
