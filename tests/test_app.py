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


def test_offline_full_flow_and_editing_does_not_reinterpret(monkeypatch):
    from src.llm_client import FixtureClient
    original=FixtureClient.generate
    calls=[]
    def count(self,*args):
        calls.append(1)
        return original(self,*args)
    monkeypatch.setattr(FixtureClient,"generate",count)
    at=app()
    at.selectbox(key="input_mode").select("Offline demo (mock)").run()
    at.button(key="interpret").click().run()
    assert not at.exception
    assert len(calls)==1
    at.button(key="recommend").click().run()
    assert not at.exception
    assert at.session_state["results"]["result"].status == "ok"
    first=[r.track.id for r in at.session_state["results"]["result"].recommendations]
    prefix=f'review_{at.session_state["revision"]}_'
    at.slider(key=prefix+"acousticness").set_value(.1)
    at.button(key="recommend").click().run()
    assert not at.exception and len(calls)==1
    second=[r.track.id for r in at.session_state["results"]["result"].recommendations]
    assert first!=second
    # New request invalidates old review/results before any new interpretation.
    at.selectbox(key="demo_request").select("I want jazz around 95 BPM with moderate energy.").run()
    assert at.session_state["results"] is None
    assert at.session_state["review"] is None and len(calls)==1


def test_manual_mode_and_mode_switch_clear_results():
    at=app()
    at.selectbox(key="input_mode").select("Manual preferences").run()
    at.button(key="recommend").click().run()
    assert not at.exception and at.session_state["results"]["result"].status=="ok"
    at.selectbox(key="input_mode").select("AI assistant").run()
    assert at.session_state["results"] is None and at.session_state["review"] is None


def test_unsupported_condition_blocks_ui_results_until_explicitly_revised():
    at=app()
    at.selectbox(key="input_mode").select("Offline demo (mock)").run()
    at.selectbox(key="demo_request").select("Pop songs guaranteed safe for children with no explicit lyrics.").run()
    at.button(key="interpret").click().run()
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
