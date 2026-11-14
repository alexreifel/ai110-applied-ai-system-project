"""Actual UI review, edits, stale-state invalidation and safe fallback modes."""

from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


def app():
    return AppTest.from_file(str(ROOT/"app.py"),default_timeout=15).run()


def test_initial_load_never_calls_provider(monkeypatch):
    def forbidden(*args,**kwargs):
        raise AssertionError("Unexpected network generation")
    monkeypatch.setattr("src.llm_client.GeminiClient.generate",forbidden)
    at=app()
    assert not at.exception
    assert not at.session_state["results"]


def test_explore_examples_and_edits_never_call_ai_or_mock_interpretation(monkeypatch):
    def forbidden(*args,**kwargs):
        raise AssertionError("Explore mode must use preferences directly, without a model or mock interpretation")
    monkeypatch.setattr("src.llm_client.GeminiClient.generate",forbidden)
    monkeypatch.setattr("src.llm_client.FixtureClient.generate",forbidden)
    at=app()
    at.selectbox(key="input_mode").select("Explore without AI").run()
    assert at.selectbox(key="explore_start").value == "Custom preferences"
    at.selectbox(key="explore_start").select("Find mellow acoustic folk or country for a quiet evening; keep it at or below 100 BPM.").run()
    assert not at.exception
    assert not any(button.key == "interpret" for button in at.button)
    at.button(key="recommend").click().run()
    assert not at.exception
    assert at.session_state["results"]["result"].status == "ok"
    first=[r.track.id for r in at.session_state["results"]["result"].recommendations]
    prefix=f'review_{at.session_state["revision"]}_'
    at.slider(key=prefix+"acousticness").set_value(.1)
    at.button(key="recommend").click().run()
    assert not at.exception
    second=[r.track.id for r in at.session_state["results"]["result"].recommendations]
    assert first!=second
    # A different example loads its preferences immediately and clears old results.
    at.selectbox(key="explore_start").select("I want jazz around 95 BPM with moderate energy.").run()
    assert at.session_state["results"] is None
    assert at.session_state["review"]["preferred_genres"] == ["jazz"]


def test_custom_preferences_and_mode_switch_clear_results():
    at=app()
    at.selectbox(key="input_mode").select("Explore without AI").run()
    at.button(key="recommend").click().run()
    assert not at.exception and at.session_state["results"]["result"].status=="ok"
    at.selectbox(key="input_mode").select("AI assistant").run()
    assert at.session_state["results"] is None and at.session_state["review"] is None


def test_unsupported_example_blocks_results_until_explicitly_revised():
    at=app()
    at.selectbox(key="input_mode").select("Explore without AI").run()
    at.selectbox(key="explore_start").select("Pop songs guaranteed safe for children with no explicit lyrics.").run()
    at.button(key="recommend").click().run()
    assert not at.exception
    assert at.session_state["results"]["result"].status=="needs_clarification"
    assert not at.session_state["results"]["result"].recommendations
    prefix=f'review_{at.session_state["revision"]}_'
    at.checkbox(key=prefix+"revise_unsupported").check()
    at.button(key="recommend").click().run()
    assert at.session_state["results"]["result"].status=="ok"


def test_provider_failure_is_visible_and_never_leaves_stale_results(monkeypatch):
    from src.llm_client import ProviderError
    def failed(*args,**kwargs):
        raise ProviderError("authentication","Check the local key.")
    monkeypatch.setattr("src.llm_client.GeminiClient.generate",failed)
    at=app()
    at.text_area(key="music_request").set_value("Jazz for an evening").run()
    at.button(key="interpret").click().run()
    assert not at.exception and at.error
    assert at.session_state["review"] is None and at.session_state["results"] is None


def test_ai_review_submission_and_edits_use_one_explicit_interpretation(monkeypatch):
    """Exercise the AI UI success path with an explicitly injected offline client."""
    from src.llm_client import FixtureClient
    calls=[]
    class TestClient(FixtureClient):
        def generate(self,instructions,request,schema):
            calls.append(request)
            return super().generate(instructions,request,schema)
    monkeypatch.setattr("src.llm_client.GeminiClient",TestClient)
    at=app()
    request="Find mellow acoustic folk or country for a quiet evening; keep it at or below 100 BPM."
    at.text_area(key="music_request").set_value(request).run()
    assert calls==[]
    at.button(key="interpret").click().run()
    assert not at.exception and calls==[request]
    assert at.session_state["provenance"]["mode"]=="offline_fixture"
    assert at.session_state["review"]["preferred_genres"]==["folk","country"]
    at.button(key="recommend").click().run()
    assert not at.exception and at.session_state["results"]["result"].status=="ok"
    first=[r.track.id for r in at.session_state["results"]["result"].recommendations]
    prefix=f'review_{at.session_state["revision"]}_'
    at.slider(key=prefix+"acousticness").set_value(.1)
    at.button(key="recommend").click().run()
    second=[r.track.id for r in at.session_state["results"]["result"].recommendations]
    assert not at.exception and first!=second and calls==[request]
    at.text_area(key="music_request").set_value("A different request").run()
    assert at.session_state["review"] is None and at.session_state["results"] is None
    assert calls==[request]
