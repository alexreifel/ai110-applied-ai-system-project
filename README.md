# Music Discovery Assistant

Describe music in ordinary language, review the interpreted preferences, and receive real independent tracks with source-backed explanations. This CodePath AI110 final project extends **Module 3 Music Recommender Simulation**.

**Current checkpoint:** the Gemini adapter, specialized prompt, browser review flow, shared CLI, and evaluation harness are implemented. Browser/manual/offline behavior is verified. **Live Gemini behavior and the generic-versus-specialized comparison remain unverified:** the existing key was rejected, and Alex instructed that generation stay offline until access and billing are confirmed. No fixture result below is represented as live AI.

## Original project and new behavior

The original Music Recommender Simulation ranked 20 synthetic songs using a single genre, mood, and target energy, and printed recommendations for three example profiles. It used fixed weights, numerical explanations, tests, and a reproducible weight experiment. It had no LLM, browser interface, trained model, or listener-feedback model.

The extension uses 1,200 real tracks from 775 artists, with 113 represented genre labels and source-derived ancestry. It supports multiple genres, explicit exclusions, hard limits, six optional numeric preferences, honest missing-data/unsupported handling, and human review before ranking. The AI interpreter translates language into this preference contract; Python chooses catalog tracks and explains actual score contributions.

| Layer | Original | Current extension |
| --- | --- | --- |
| Catalog | 20 synthetic tracks | 1,200 real tracks with attribution and coverage audit |
| Preferences | One genre/mood/energy | Genre alternatives/exclusions, bounds and six optional numeric targets |
| User entry | Fixed terminal demonstrations | Browser request/review/results; shared CLI; manual fallback |
| New AI capability | None | Prompt-specialized Gemini preference interpretation, pending live verification |
| Reliability | Base validation and tests | Response checks, effective constraints, safe provider errors, UI-state tests and evaluation harness |

Original code, synthetic CSV, tests, CLI/evaluation behavior, and both Git histories are preserved. Historical documentation is in [docs/baseline](docs/baseline/README.md); the [Pass 1 report](docs/pass1_report.md) records the foundation checkpoint. Coverage/feature differences do not establish listener satisfaction or an LLM quality improvement.

## Install and launch

Python 3.11 or 3.12. Local verification used Python 3.11.18, Streamlit 1.67.0, pytest 8.4.2 and mypy 2.4.1.

```bash
cd "/Users/alexreifel/Coding Programs/CodePath AI 110/ai110-applied-ai-system-project"
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt -c requirements-lock.txt
python -m streamlit run app.py
```

For app/runtime only, use `requirements.txt` instead of `requirements-dev.txt`. On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. The catalog is checked in; no dataset download, audio files or API key is needed for manual mode/offline demo. A separate clean environment passed the complete suite. Developer dependencies include the type checker; exact dependency constraints are retained for reproducibility.

### Choose a mode

- **AI assistant:** type a request, click Interpret, review/edit the preferences and assumptions, then Recommend. This makes one Gemini request per interpretation; subsequent preference edits rerank locally.
- **Manual preferences:** select genres/attributes/limits directly. No model call is made.
- **Offline demo (mock):** choose a predefined request and exercise the same validation/review/ranking path with a test reply. This does not interpret arbitrary new language or demonstrate model quality.

Changing a request or input mode clears old review/results. The form applies edits only when submitted; displayed results correspond to the last submitted preferences. Unsupported conditions block results until explicitly revised. Source links identify historical catalog records; playback is not guaranteed.

### Configure Gemini locally

Copy `.env.example` to the ignored `.env` file, replace its key placeholder locally, and check current model access and account billing/free-tier status. **Do not paste or commit a key.** Configuration uses simple `KEY=value` or quoted values; it does not execute shell expressions.

```text
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
GEMINI_TIMEOUT_SECONDS=20
```

The model is configurable. Its listed free-tier availability does not establish this account's quota or billing configuration. Verify these before live tests. Canonical `GEMINI_API_KEY` takes precedence over the legacy `GOOGLE_API_KEY` alias; environment settings override matching file settings. The adapter uses the [official Gemini generation API](https://ai.google.dev/api/generate-content) with a JSON response schema, temperature 0, at most 2,048 output tokens, a configurable 1–45 second network timeout, and no retries/tools. Schema validity does not prove that language was understood. The [provider's pricing/usage terms](https://ai.google.dev/gemini-api/docs/pricing) can differ between free and paid tiers.

Only the request, task instructions, supported genre vocabulary and schema go to Gemini. The catalog's track records and API key are not included in the prompt. The browser app does not write request text to disk; evaluation commands intentionally save the supplied predefined, nonpersonal test inputs and outputs. Provider-side retention is governed by the provider's terms.

## Shared CLI and testing

```bash
python -m src.cli --preferences examples/acoustic_folk.json
python -m src.cli --list-genres
python -m src.cli --mode offline --request "I want jazz around 95 BPM with moderate energy." --yes
python -m pytest -q
python -m src.evaluate_assistant --mode offline
python -m mypy app.py --follow-imports=silent --ignore-missing-imports
```

With confirmed usable access, `--mode live --request ... --yes` invokes Gemini. In interactive terminals, omitting `--yes` displays the interpretation and asks for confirmation. Noninteractive requests require `--yes` before a call is made. `--json` produces parseable output and includes interpretation provenance; `--verbose` logs aggregate events without private request text. `--limit` accepts 1–20, default 5. Exit 0 means results, 2 means invalid input/provider/configuration failure, and 3 means clarification/no-results.

Manual preferences accept `preferred_genres`, `required_genres`, `excluded_genres`, numeric `targets`, hard `bounds`, and `unsupported` conditions. Multiple required genres mean any one may match; exclusions always win. All bounds are inclusive. Omitted dimensions do not contribute to ranking. See [examples](examples/acoustic_folk.json) and [data meanings](data/README.md).

## Architecture and decisions

[Editable Mermaid architecture](diagrams/architecture.mmd): request -> specialized prompt/client -> strict response and vocabulary checks -> unsupported-guarantee checks -> human review -> hard filtering -> deterministic scoring -> actual catalog tracks and explanations. Manual and explicitly mocked paths join the same preference/ranking services.

- `src/llm_client.py`: bounded Gemini adapter, safe error categories, local configuration and explicitly labeled fixtures.
- `prompts/specialized.txt` and `prompts/generic.txt`: actual experimental prompt variants; both receive the same schema and vocabulary.
- `src/assistant.py`: input checks, interpretation contract, visible assumptions and local evidence-gap checks.
- `app.py` / `src/cli.py`: user entry points with explicit review/confirmation and shared backend.
- `src/catalog.py`, `src/preferences.py`, `src/ranking.py`: source facts, strict preferences, required-condition filtering and scoring.
- `src/evaluate_assistant.py`: predefined request evaluation, per-case results, JSON reports and live comparison mode.

Genre similarity has weight 2; each requested numeric feature has weight 1. Numeric similarity is `max(0, 1 - gap)` for [0,1] features and `max(0, 1 - bpm_gap/100)` for tempo. The score is the weighted mean over requested soft dimensions. Required-only results are unscored; ties use source ID. The 0.6 selection threshold and 0.75 per-feature compromise indicator are transparent heuristics, not calibrated confidence or enjoyment probabilities. Missing evidence excludes a candidate when needed, and hard conditions are never relaxed to fill results.

The selected AI feature is **structured prompting / specialization**, not fine-tuning or RAG. One provider and plain Python modules keep the system approachable. Model interpretation is useful for varied language; deterministic code controls catalog facts and constraints.

## Three actual assistant-workflow examples

These are captured CLI executions through the real interpretation/validation/ranking path using **offline predefined replies, model none**. They demonstrate plumbing and downstream behavior. They do not verify live language understanding; three live examples are still required for the intended final evidence package.

### acoustic evening

```text
$ python -m src.cli --mode offline --request "Find mellow acoustic folk or country for a quiet evening; keep it at or below 100 BPM." --yes --limit 3
Mode: offline_fixture
Interpretation: Offline test fixture for acoustic evening.
Model: none (predefined fixture)
Assumption: This is a predefined fixture, not a model interpretation.
Preferences: {"bounds": {"tempo_bpm": {"maximum": 100.0, "minimum": null}}, "excluded_genres": [], "preferred_genres": ["folk", "country"], "required_genres": [], "targets": {"acousticness": 0.85, "energy": 0.25}, "unsupported": []}
Catalog: 1200; eligible: 405; returned: 3
Recommendations from catalog metadata; scores are similarities, not probabilities.
1. Long Nights I — Daniel Bachman | Match: 0.995 | FMA 62880
   Genres: americana, folk
   genre: matched country, folk; similarity 1.000, weight 2
   acousticness: observed 0.8535, target 0.8500; similarity 0.9965, weight 1
   energy: observed 0.2673, target 0.2500; similarity 0.9827, weight 1
   required tempo_bpm: at most 100.0; observed 83.9580
   Source: https://freemusicarchive.org/music/Daniel_Bachman/Live_at_WFMU_on_Irene_Trudels_Show_on_March_26_2012/Daniel_Bachman_-_05_-_Long_Nights_I
2. Musicawi Silt [Walias Band] — Debo Band | Match: 0.995 | FMA 31342
   Genres: folk, international, middle east
   genre: matched folk; similarity 1.000, weight 2
   acousticness: observed 0.8522, target 0.8500; similarity 0.9978, weight 1
   energy: observed 0.2303, target 0.2500; similarity 0.9803, weight 1
   required tempo_bpm: at most 100.0; observed 66.6810
   Source: https://freemusicarchive.org/music/Debo_Band/Live_on_WFMUs_Transpacific_Sound_Paradise_with_Bob_Weisberg_12122009/Debo_Band_-_07_-_Musicawi_Silt__Walias_Band
3. Nothing Much — My Bubba & Mi | Match: 0.994 | FMA 57802
   Genres: blues, folk, pop
   genre: matched folk; similarity 1.000, weight 2
   acousticness: observed 0.8280, target 0.8500; similarity 0.9780, weight 1
   energy: observed 0.2494, target 0.2500; similarity 0.9994, weight 1
   required tempo_bpm: at most 100.0; observed 99.9410
   Source: https://freemusicarchive.org/music/My_Bubba__Mi/Wild__You/My_bubba__Mi_-_Wild__You_-_01_Nothing_Much
```

### jazz tempo

```text
$ python -m src.cli --mode offline --request "I want jazz around 95 BPM with moderate energy." --yes --limit 3
Mode: offline_fixture
Interpretation: Offline test fixture for jazz tempo.
Model: none (predefined fixture)
Assumption: This is a predefined fixture, not a model interpretation.
Preferences: {"bounds": {}, "excluded_genres": [], "preferred_genres": ["jazz"], "required_genres": [], "targets": {"energy": 0.5, "tempo_bpm": 95.0}, "unsupported": []}
Catalog: 1200; eligible: 1200; returned: 3
Recommendations from catalog metadata; scores are similarities, not probabilities.
1. Love Languid — Matt Darriau's Paradox Trio | Match: 0.995 | FMA 6375
   Genres: balkan, europe, free-jazz, international
   genre: matched jazz; similarity 1.000, weight 2
   energy: observed 0.4998, target 0.5000; similarity 0.9998, weight 1
   tempo_bpm: observed 93.2160, target 95.0000; similarity 0.9822, weight 1
   Source: https://freemusicarchive.org/music/Matt_Darriaus_Paradox_Trio/Paradox_Trio_Live_on_WFMU_from_the_2009_Golden_Festival_in_NYC/Love_Languid
2. Forward — Northbound | Match: 0.989 | FMA 39361
   Genres: downtempo, funk, jazz
   genre: matched jazz; similarity 1.000, weight 2
   energy: observed 0.5182, target 0.5000; similarity 0.9818, weight 1
   tempo_bpm: observed 97.4720, target 95.0000; similarity 0.9753, weight 1
   Source: https://freemusicarchive.org/music/Northbound/Landscapes_of_Late/9404_Northbound_Forward_Monotonik_Creative_Commons___by_nc_nd_25_wwwdogmazicnet
3. Handful of Dust [remix of Fabryka original] — Musetta | Match: 0.989 | FMA 41565
   Genres: jazz, lounge
   genre: matched jazz; similarity 1.000, weight 2
   energy: observed 0.5441, target 0.5000; similarity 0.9559, weight 1
   tempo_bpm: observed 94.9770, target 95.0000; similarity 0.9998, weight 1
   Source: https://freemusicarchive.org/music/Musetta/Absolute_Balance/01_-_musetta_-_handful_of_dust_remix_of_song_by_fabryka
```

### dance exclusion

```text
$ python -m src.cli --mode offline --request "Danceable electronic or pop, high energy, no experimental tracks." --yes --limit 3
Mode: offline_fixture
Interpretation: Offline test fixture for dance exclusion.
Model: none (predefined fixture)
Assumption: This is a predefined fixture, not a model interpretation.
Preferences: {"bounds": {}, "excluded_genres": ["experimental"], "preferred_genres": ["electronic", "pop"], "required_genres": [], "targets": {"danceability": 0.85, "energy": 0.85}, "unsupported": []}
Catalog: 1200; eligible: 1090; returned: 3
Recommendations from catalog metadata; scores are similarities, not probabilities.
1. Snake In A Box — M.W.D. | Match: 0.998 | FMA 33322
   Genres: downtempo, hip-hop, jazz
   genre: matched electronic; similarity 1.000, weight 2
   danceability: observed 0.8436, target 0.8500; similarity 0.9936, weight 1
   energy: observed 0.8483, target 0.8500; similarity 0.9983, weight 1
   excluded genres absent: experimental
   Source: https://freemusicarchive.org/music/MWD/Singing_Forest/07_mwd-snake_in_a_box
2. Quittin' Time — Patrick Lee | Match: 0.982 | FMA 33850
   Genres: electronic, funk
   genre: matched electronic; similarity 1.000, weight 2
   danceability: observed 0.8008, target 0.8500; similarity 0.9508, weight 1
   energy: observed 0.8286, target 0.8500; similarity 0.9786, weight 1
   excluded genres absent: experimental
   Source: https://freemusicarchive.org/music/Patrick_Lee/Bad_Panda_42/Quittin_Time
3. Vapor (Kupa Mix) — MHV | Match: 0.981 | FMA 40817
   Genres: chip music, dubstep, electronic
   genre: matched electronic; similarity 1.000, weight 2
   danceability: observed 0.8240, target 0.8500; similarity 0.9740, weight 1
   energy: observed 0.8015, target 0.8500; similarity 0.9515, weight 1
   excluded genres absent: experimental
   Source: https://freemusicarchive.org/music/MHV/Vapor_Remixes/vira_-_VIRANET01_MHV_-_VAPOR_Remixes_-_02_Vapor_Kupa_Mix
```

## Guardrails, evaluation and observed evidence

| Case | Observed behavior | Evidence |
| --- | --- | --- |
| Invalid key | Read-only model-list check returned HTTP 400 / API_KEY_INVALID; no generation run | `evaluation/pass23/access_status.json` |
| Malformed/missing credentials | Safe categorized errors; credential format checked before constructing a header | Provider tests; `.env` ignored |
| Invalid model output | Bad types/unknown genres/extra fields rejected before preferences are applied | `tests/test_assistant.py` |
| Model overlooks lyric condition in a controlled fixture | Local guard blocks results; model-understanding check still fails | `test_lyric_guard_changes_overlooked_model_condition_but_preserves_raw_evidence` |
| Unsupported guarantee in UI | No results until the user explicitly removes the unsupported condition | `tests/test_app.py`; captured CLI reliability example |
| Old results after request/mode change | Review/results cleared; no provider call on rerender/edit | UI tests and runtime checks |
| Effective exclusion check | Guard on returns no prohibited rock tracks; bypass returns 3 | Pass 1 controlled ablation |
| Provider errors | Missing config, auth/access, model unavailable, quota, timeout, network, bad output separated; no retry | Provider fault tests |

Actual offline harness output:

```text
$ .venv/bin/python -m src.evaluate_assistant --mode offline --output evaluation/pass23/offline_evaluation.json
Mode: offline_fixture; model: none
offline orchestration/guardrail checks using predefined replies; no measured model behavior
PASS specialized acoustic_evening
PASS specialized jazz_tempo
PASS specialized dance_exclusion
PASS specialized no_assumed_genre
PASS specialized rock_limit
PASS specialized acoustic_exclusion
PASS specialized required_interval
PASS specialized genre_alternatives
PASS specialized lyric_guarantee
PASS specialized conflicting_genres
PASS specialized release_date
PASS specialized instruction_override
specialized: 12/12 passed
```

The harness checks predefined semantic expectations, result presence/clarification, catalog membership, and required-condition satisfaction. Model preference checks use the validated original model fields **before local semantic corrections**; a guardrail fix cannot inflate interpretation quality. Offline fixtures are exact replies, so 12/12 establishes orchestration and constraints for these cases, not an observed model success rate. Provider-failure fixtures and browser behavior are covered in pytest.

```text
$ .venv/bin/python -m pytest -q
........................................................................ [ 42%]
........................................................................ [ 84%]
..........................                                               [100%]
170 passed in 2.90s
```

**170 tests passed**, including all 52 original tests. The clean environment passed the same suite; [structured verification](evaluation/pass23/verification.json), [running-app checks](evaluation/pass23/runtime_checks.json), [captured CLI runs](evaluation/pass23/cli_runs.json), and [offline JSON evaluation](evaluation/pass23/offline_evaluation.json) retain observed evidence. Syntax, dependency consistency and Streamlit API type checks pass. The runtime check used a temporary localhost server and offline mode; no human visual or listening evaluation is claimed.

### Selected bonuses

The **evaluation harness** is implemented and verified: it evaluates multiple predefined requests and prints per-case/aggregate results. The **specialization comparison** is implemented but not verified live. After usable access/free-tier confirmation, run:

```bash
python -m src.evaluate_assistant --mode live --compare-prompts --output evaluation/live_comparison.json
```

The current 12-case comparison makes at most 24 generation calls and stops on unavailable access/quota/network errors. Both arms use the same model/settings/schema/vocabulary/catalog/cases. It changes only task instructions/examples. Report actual differences, ties or regressions in `model_card.md`; no improvement or bonus credit is claimed in advance. Offline comparison is refused because fixtures cannot establish specialized-model behavior. See [model card](model_card.md) for the exact outstanding evidence.

## Limitations, reflection and next checkpoint

See [catalog provenance/audit](data/README.md), [catalog report](data/catalog_report.json), and [model card](model_card.md). Data is historical and independent-music focused; some categories are sparse. Musical attributes are estimates, not verified moods, lyrics, instrumentation, medical effects or absence of vocals. Valid JSON can still misunderstand a request. Human review and data coverage remain necessary even when code checks pass.

Alex accepted the language-assistant direction, revised the tiny-catalog proposal and rejected repeated LLM binary-search coaching. Codex implemented and tested the code with those decisions; personal testing reflection remains for Alex's review. A useful observed design lesson is that local guardrail success and model understanding must be measured separately.

The [presentation outline](docs/presentation_outline.md) and [portfolio draft](docs/portfolio_draft.md) are prepared for review, not delivered/published. The [combined-pass report](docs/pass23_report.md) and [requirements checklist](docs/requirements_checklist.md) record remaining live/model/personal-review gaps. Pass 4's explicit full audit, final publication, and remote CI verification remain pending. CI is configured for offline tests/harness/type checks with no API secrets; no new remote run is claimed. The original baseline still runs with `python -m src.main` and `python -m src.evaluate`. No CodePath submission has occurred; prior course timing remains unverified.
