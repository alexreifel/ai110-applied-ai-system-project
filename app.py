"""Local music discovery: describe, review, and recommend."""

import json
from pathlib import Path

import streamlit as st

from src.assistant import interpret_request
from src.catalog import FEATURES, load_catalog
from src.llm_client import FixtureClient, GeminiClient, ProviderError
from src.preferences import Preferences
from src.ranking import recommend


ROOT = Path(__file__).resolve().parent
LABELS = {"energy": "Energy", "tempo_bpm": "Tempo (BPM)", "valence": "Musical positiveness",
          "acousticness": "Acoustic character", "danceability": "Danceability",
          "instrumentalness": "Instrumental character (estimate)"}
st.set_page_config(page_title="Music discovery assistant", page_icon=":material/music_note:")


@st.cache_data
def catalog_data():
    return load_catalog()


def invalidate():
    st.session_state.review = None
    st.session_state.results = None


def install_review(preferences, provenance):
    st.session_state.review = preferences.to_dict()
    st.session_state.provenance = provenance
    st.session_state.results = None
    st.session_state.revision += 1


initial_state: dict[str, object] = {"review": None, "results": None, "revision": 0, "provenance": {}}
for state_key, initial_value in initial_state.items():
    st.session_state.setdefault(state_key, initial_value)

st.title("Music discovery assistant")
st.write("Describe a sound. Review what matters. Discover real independent tracks.")
catalog = catalog_data()
with st.sidebar:
    st.subheader("Your catalog")
    st.metric("Real tracks", len(catalog.tracks))
    st.caption(f"{len({track.artist_id for track in catalog.tracks})} artists · {len(catalog.vocabulary)} genre labels")
    st.caption("Historical FMA metadata. Audio attributes are estimates. No verified lyrics, vocal-absence, or playback guarantees.")
    mode = st.selectbox("Input mode", ["AI assistant", "Manual preferences", "Offline demo (mock)"], key="input_mode", on_change=invalidate)
    st.caption("Requests go to Gemini only when you click Interpret in AI mode. They are not written to disk by this app.")

st.subheader("1. Describe your music")
if mode == "Manual preferences":
    if st.session_state.review is None:
        install_review(Preferences(targets={"energy": .5}), {"mode": "manual", "model": None})
    st.caption("Choose your own preferences below. No model call is made.")
else:
    if mode == "Offline demo (mock)":
        st.info("Predefined test replies demonstrate the workflow. This mode does not interpret new language or call an AI model.")
        cases = json.loads((ROOT / "evaluation/cases.json").read_text())
        request = st.selectbox("Demo request", [case["request"] for case in cases], key="demo_request", on_change=invalidate)
    else:
        request = st.text_area("What would you like to hear?", placeholder="Mellow acoustic folk or country, below 100 BPM…", max_chars=1200, key="music_request", on_change=invalidate)
    if st.button("Interpret request", key="interpret", type="primary", icon=":material/auto_awesome:"):
        invalidate()
        try:
            client = FixtureClient() if mode == "Offline demo (mock)" else GeminiClient()
            with st.spinner("Interpreting your preferences…"):
                interpretation = interpret_request(request, catalog, client)
            install_review(interpretation.preferences, interpretation.to_dict())
        except ProviderError as exc:
            st.error(str(exc))
            st.caption(f"Error category: {exc.kind}. Manual preferences and offline demo remain available.")
        except ValueError as exc:
            st.error(str(exc))

if st.session_state.review is not None:
    prefs = Preferences.from_dict(st.session_state.review)
    provenance = st.session_state.provenance
    st.subheader("2. Review and edit")
    if provenance.get("summary"):
        st.write(provenance["summary"])
    for assumption in provenance.get("assumptions", []):
        st.caption(assumption)
    if provenance.get("mode") == "offline_fixture":
        st.caption("Interpretation source: offline test fixture. Recommendations use the real catalog.")
    elif provenance.get("model"):
        st.caption(f"Interpretation source: {provenance['model']}. Check the assumptions before continuing.")
    prefix = f"review_{st.session_state.revision}_"
    with st.form("review_form"):
        vocabulary = sorted(catalog.vocabulary)
        preferred = st.multiselect("Preferred genres (any of these)", vocabulary, default=list(prefs.preferred_genres), key=prefix+"preferred")
        required = st.multiselect("Required genres (at least one)", vocabulary, default=list(prefs.required_genres), key=prefix+"required")
        excluded = st.multiselect("Exclude these genres", vocabulary, default=list(prefs.excluded_genres), key=prefix+"excluded")
        active = st.multiselect("Characteristics to match", list(FEATURES), default=list(prefs.targets), format_func=lambda f: LABELS[f], key=prefix+"active")
        # Render every numeric control so changes to the form's selection need no extra rerun.
        # Only selected characteristics affect ranking.
        targets = {}
        with st.expander("Adjust target values", expanded=True):
            st.caption("Only characteristics selected above affect recommendations.")
            for feature in FEATURES:
                default = float(prefs.targets.get(feature, 100 if feature == "tempo_bpm" else .5))
                if feature == "tempo_bpm":
                    value = st.number_input(LABELS[feature], min_value=0.0, value=default, step=5.0, key=prefix+feature)
                else:
                    value = st.slider(LABELS[feature], min_value=0.0, max_value=1.0, value=default, step=.01, key=prefix+feature)
                if feature in active:
                    targets[feature] = value
        bounds = {}
        with st.expander("Required limits", expanded=bool(prefs.bounds)):
            st.caption("Leave a limit empty when it is not required. Limits will not be relaxed.")
            for feature in FEATURES:
                interval = prefs.bounds.get(feature)
                lower = interval.minimum if interval else None
                upper = interval.maximum if interval else None
                low = st.number_input("Minimum "+LABELS[feature], min_value=0.0, max_value=None if feature == "tempo_bpm" else 1.0, value=lower, key=prefix+feature+"_min")
                high = st.number_input("Maximum "+LABELS[feature], min_value=0.0, max_value=None if feature == "tempo_bpm" else 1.0, value=upper, key=prefix+feature+"_max")
                if low is not None or high is not None:
                    bounds[feature] = {"minimum": low, "maximum": high}
        unsupported = list(prefs.unsupported)
        if unsupported:
            for condition in unsupported:
                st.warning(condition)
            if st.checkbox("Remove the unsupported conditions from my request", key=prefix+"revise_unsupported"):
                unsupported = []
        limit = st.number_input("Number of recommendations", min_value=1, max_value=20, value=5, step=1, key=prefix+"limit")
        submit = st.form_submit_button("Recommend tracks", key="recommend", type="primary", icon=":material/queue_music:")
    if submit:
        st.session_state.results = None
        try:
            final_preferences = Preferences.from_dict({"preferred_genres": preferred, "required_genres": required,
                "excluded_genres": excluded, "targets": targets, "bounds": bounds, "unsupported": unsupported})
            result = recommend(catalog, final_preferences, limit)
            st.session_state.results = {"result": result, "preferences": final_preferences.to_dict()}
        except ValueError as exc:
            st.error(str(exc))

if st.session_state.results is not None:
    result = st.session_state.results["result"]
    st.subheader("3. Your recommendations")
    st.caption("These results reflect your last submitted preferences. Editing and submitting again reranks locally.")
    if result.status != "ok":
        st.warning(result.message)
    else:
        st.caption(f"{result.eligible_count} eligible tracks · similarity scores are not confidence or enjoyment probabilities")
        for rank, item in enumerate(result.recommendations, 1):
            with st.container(border=True):
                st.subheader(f"{rank}. {item.track.title}")
                st.write(item.track.artist)
                st.caption(", ".join(item.track.direct_genres))
                if item.score is not None:
                    st.caption(f"Metadata similarity: {item.score:.3f}")
                else:
                    st.caption("Eligible by required conditions; no soft score")
                for compromise in item.compromises:
                    st.warning(compromise)
                with st.expander("Why this matches"):
                    for reason in item.explanations:
                        st.text(reason)
                st.link_button("Source record", item.track.source_url, icon=":material/open_in_new:")
