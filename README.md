# Music Discovery Assistant

A CodePath AI110 final project extending **Module 3 Music Recommender Simulation**. Pass 1 implements a richer manual recommender over a versioned real-track catalog. **Natural-language AI interpretation and the browser app are planned for Pass 2 and are not implemented yet.** Current examples make no model calls and do not demonstrate a live AI feature.

## Original project and the extension

The original Music Recommender Simulation ranked 20 synthetic songs against a genre, mood, and target energy, printing results for three example profiles in a terminal. It used fixed weights and factual score explanations, with tests and a reproducible weight experiment. It had no LLM, trained model, streaming integration, or real listener feedback.

The foundation now supports multiple genre choices, genre exclusions, required feature limits, and optional targets for energy, tempo, valence, acousticness, danceability, and instrumentalness. It selects real catalog records and explains their actual attributes. The original source, synthetic CSV, tests, CLI, and evaluation behavior are preserved; original documentation is archived in [docs/baseline](docs/baseline/README.md).

| Capability | Original baseline | Pass 1 foundation |
| --- | --- | --- |
| Catalog | 20 synthetic songs | 1,200 real tracks, 775 artists |
| Genre representation | 17 flat genre labels | 113 represented labels with explicit source ancestors |
| Preferences | One genre, one mood, energy | Multiple genres, exclusions, six optional numeric targets |
| Required conditions | Input validation | Required genre alternatives and inclusive numeric bounds |
| Output | Top five weighted matches | Up to requested count; no forced filling or silent relaxation |
| AI interpretation | None | Pending Pass 2 |

This comparison describes capabilities and catalog coverage. It does not measure listening enjoyment or isolate a live LLM improvement.

## Install and run

Use Python 3.11 or 3.12. Local validation used Python **3.11.18**, pytest **8.4.2**, and Streamlit **1.67.0**. Streamlit is installed in preparation for Pass 2; there is currently no browser app to launch. No API key, audio files, or download is needed to run the manual recommender.

```bash
cd "/Users/alexreifel/Coding Programs/CodePath AI 110/ai110-applied-ai-system-project"
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -c requirements-lock.txt
python -m src.cli --preferences examples/acoustic_folk.json
python -m src.cli --list-genres
python -m pytest -q
```

The version constraints record the complete validated dependency environment. A fresh temporary Python environment installed these dependencies, passed `pip check`, and passed the same 127 tests; see [clean setup result](evaluation/pass1/clean_setup_pytest.txt). On Windows, activate with `.venv\Scripts\Activate.ps1` instead. The default catalog path is anchored to the package; run module commands from the repository root.

For JSON output add `--json`; for ranking event counts add `--verbose`. `--limit` accepts integers 1–20 (default 5). Exit status is 0 for results, 2 for invalid input/configuration/file errors, and 3 for no results or a condition requiring clarification. No-result status is intentional and does not mean the application crashed.

## Enter your own preferences

Create a JSON file or pass `--preferences-json`. Omit dimensions you do not care about. Multiple required genres mean **any one** may match; excluded genres always remove a candidate, including tracks labeled with a descendant of an excluded genre. Supported genre spellings are shown by `--list-genres`; labels are stripped and case-insensitive. Unknown genres are reported, not silently translated into a preset.

```json
{
  "preferred_genres": ["folk", "country"],
  "required_genres": ["folk", "country"],
  "targets": {"energy": 0.25, "acousticness": 0.9, "tempo_bpm": 85},
  "bounds": {"acousticness": {"minimum": 0.6}}
}
```

`targets` are soft preferences. `bounds` are hard conditions with optional `minimum`/`maximum`. Unit-interval targets/bounds must lie in [0,1]; tempo is positive BPM. Booleans, numeric strings, nonfinite values, contradictory target/bound conditions, unknown fields, and duplicate JSON keys are rejected. If an essential condition lacks evidence, include it in `unsupported`; recommendations are withheld until it is resolved or explicitly revised. Pass 2 will interpret language into this same validated contract.

## Architecture and design tradeoffs

[Editable Mermaid source](diagrams/architecture.mmd) describes implemented Pass 1 code:

Human-authored JSON -> strict preference checks -> validated catalog/vocabulary -> hard-condition filtering -> soft scoring -> deterministic ordering -> real tracks with metadata explanations and source references.

- `scripts/prepare_catalog.py`: checksum-verified CSV import, deterministic selection, provenance, and coverage report.
- `src/catalog.py`: immutable track records, represented vocabulary, JSONL loading, and source/feature validation.
- `src/preferences.py`: strict preferences, inclusive bounds, supported dimensions, and contradictions.
- `src/ranking.py`: required-condition filtering, requested-dimension scoring, and honest empty results.
- `src/cli.py`: manual user entry point and JSON/text output; shared services are ready for the browser/AI layer.

Genre similarity has weight 2, each requested numeric feature weight 1. Similarity is `max(0, 1 - absolute_gap)` for unit-interval attributes and `max(0, 1 - bpm_gap / 100)` for tempo. The score is the weighted mean over requested soft dimensions only. With no soft preferences, eligible results are explicitly unscored. Ties use ascending source track ID. Candidates below 0.6 soft similarity are not returned; individual feature similarities below 0.75 are labeled compromises. These thresholds and weights are transparent engineering choices, not calibrated confidence or enjoyment probabilities.

Hard conditions are never relaxed to fill the requested count. A missing attribute excludes a track if that attribute is needed by the request; missing values are not treated as zero. Unsupported essential conditions block results. Plain Python services and a compact local snapshot keep this inspectable and independent of network availability.

## Three captured manual end-to-end examples

The following are actual terminal runs. They are **manual mode, model: none**; AI interpretation will require separate live evidence in later passes. Each command reads a committed input file and traverses catalog loading, preference validation, filtering, scoring, and output.

### Acoustic folk or country

Input: [examples/acoustic_folk.json](examples/acoustic_folk.json).

```text
$ python -m src.cli --preferences examples/acoustic_folk.json --limit 3
Mode: manual (no LLM calls)
Preferences: {"bounds": {"acousticness": {"maximum": null, "minimum": 0.6}}, "excluded_genres": [], "preferred_genres": ["folk", "country"], "required_genres": ["folk", "country"], "targets": {"acousticness": 0.9, "energy": 0.25, "tempo_bpm": 85.0}, "unsupported": []}
Catalog: 1200; eligible: 162; returned: 3
Recommendations from catalog metadata; scores are similarities, not probabilities.
1. B 6 Ce matin — Yves Rakotomalala | Match: 0.987 | FMA 42474
   Genres: psych-folk
   genre: matched folk; similarity 1.000, weight 2
   acousticness: observed 0.9338, target 0.9000; similarity 0.9662, weight 1
   energy: observed 0.2751, target 0.2500; similarity 0.9749, weight 1
   tempo_bpm: observed 84.1640, target 85.0000; similarity 0.9916, weight 1
   required acousticness: at least 0.6; observed 0.9338
   required genre matched: folk
   Source: https://freemusicarchive.org/music/Yves_Rakotomalala/Ce_matin_encore/B_6_Ce_matin
2. Long Nights I — Daniel Bachman | Match: 0.985 | FMA 62880
   Genres: americana, folk
   genre: matched country, folk; similarity 1.000, weight 2
   acousticness: observed 0.8535, target 0.9000; similarity 0.9535, weight 1
   energy: observed 0.2673, target 0.2500; similarity 0.9827, weight 1
   tempo_bpm: observed 83.9580, target 85.0000; similarity 0.9896, weight 1
   required acousticness: at least 0.6; observed 0.8535
   required genre matched: country, folk
   Source: https://freemusicarchive.org/music/Daniel_Bachman/Live_at_WFMU_on_Irene_Trudels_Show_on_March_26_2012/Daniel_Bachman_-_05_-_Long_Nights_I
3. Kamikaze Economy Christmas — Travis Taylor | Match: 0.971 | FMA 40878
   Genres: folk, holiday
   genre: matched folk; similarity 1.000, weight 2
   acousticness: observed 0.7748, target 0.9000; similarity 0.8748, weight 1
   energy: observed 0.2482, target 0.2500; similarity 0.9982, weight 1
   tempo_bpm: observed 86.9420, target 85.0000; similarity 0.9806, weight 1
   required acousticness: at least 0.6; observed 0.7748
   required genre matched: folk
   Source: https://freemusicarchive.org/music/Travis_Taylor/Thee_Christmas_Mix_Tape_2010/badgerland_-_Thee_Christmas_Mix_Tape_-_13_Kamikaze_Economy_Christmas
```

### Lower-energy jazz

Input: [examples/evening_jazz.json](examples/evening_jazz.json).

```text
$ python -m src.cli --preferences examples/evening_jazz.json --limit 3
Mode: manual (no LLM calls)
Preferences: {"bounds": {}, "excluded_genres": [], "preferred_genres": ["jazz"], "required_genres": ["jazz"], "targets": {"energy": 0.35, "tempo_bpm": 95.0, "valence": 0.55}, "unsupported": []}
Catalog: 1200; eligible: 144; returned: 3
Recommendations from catalog metadata; scores are similarities, not probabilities.
1. Passionate conjugate chemistry — Hat City Intuitive | Match: 0.960 | FMA 6967
   Genres: jazz
   genre: matched jazz; similarity 1.000, weight 2
   energy: observed 0.2937, target 0.3500; similarity 0.9437, weight 1
   tempo_bpm: observed 98.6300, target 95.0000; similarity 0.9637, weight 1
   valence: observed 0.4416, target 0.5500; similarity 0.8916, weight 1
   required genre matched: jazz
   Source: https://freemusicarchive.org/music/Hat_City_Intuitive/Live_at_WFMU_on_Storks_Show_on_10121997/Passionate_conjugate_chemistry
2. Blue Drag — The Swing Ninjas | Match: 0.953 | FMA 64361
   Genres: jazz
   genre: matched jazz; similarity 1.000, weight 2
   energy: observed 0.3623, target 0.3500; similarity 0.9877, weight 1
   tempo_bpm: observed 97.9080, target 95.0000; similarity 0.9709, weight 1
   valence: observed 0.7425, target 0.5500; similarity 0.8075, weight 1
   required genre matched: jazz
   Source: https://freemusicarchive.org/music/The_Swing_Ninjas/Tears_Of_The_Tuba_The_Difficult_Second_Album/The_Swing_Ninjas_-_Blue_Drag_1649
3. What is the What — BJ Block & Dawn Pemberton | Match: 0.953 | FMA 77378
   Genres: funk, jazz, soul-rnb
   genre: matched jazz; similarity 1.000, weight 2
   energy: observed 0.5223, target 0.3500; similarity 0.8277, weight 1
   tempo_bpm: observed 99.9990, target 95.0000; similarity 0.9500, weight 1
   valence: observed 0.5623, target 0.5500; similarity 0.9877, weight 1
   required genre matched: jazz
   Source: https://freemusicarchive.org/music/BJ_Block__Dawn_Pemberton/II_1060/06_BJ_Block_n_Dawn_Pemberton_What_is_the_What_II_FROSTWIRE_FROSTCLICK_CREATIVE_COMMONS_1366
```

### Danceable pop or electronic, excluding experimental

Input: [examples/dance_pop.json](examples/dance_pop.json).

```text
$ python -m src.cli --preferences examples/dance_pop.json --limit 3
Mode: manual (no LLM calls)
Preferences: {"bounds": {"danceability": {"maximum": null, "minimum": 0.65}}, "excluded_genres": ["experimental"], "preferred_genres": ["pop", "electronic"], "required_genres": ["pop", "electronic"], "targets": {"danceability": 0.85, "energy": 0.85, "tempo_bpm": 125.0, "valence": 0.8}, "unsupported": []}
Catalog: 1200; eligible: 154; returned: 3
Recommendations from catalog metadata; scores are similarities, not probabilities.
1. Quittin' Time — Patrick Lee | Match: 0.984 | FMA 33850
   Genres: electronic, funk
   genre: matched electronic; similarity 1.000, weight 2
   danceability: observed 0.8008, target 0.8500; similarity 0.9508, weight 1
   energy: observed 0.8286, target 0.8500; similarity 0.9786, weight 1
   tempo_bpm: observed 125.0020, target 125.0000; similarity 1.0000, weight 1
   valence: observed 0.8226, target 0.8000; similarity 0.9774, weight 1
   required danceability: at least 0.65; observed 0.8008
   required genre matched: electronic
   excluded genres absent: experimental
   Source: https://freemusicarchive.org/music/Patrick_Lee/Bad_Panda_42/Quittin_Time
2. Snake In A Box — M.W.D. | Match: 0.945 | FMA 33322
   Genres: downtempo, hip-hop, jazz
   genre: matched electronic; similarity 1.000, weight 2
   danceability: observed 0.8436, target 0.8500; similarity 0.9936, weight 1
   energy: observed 0.8483, target 0.8500; similarity 0.9983, weight 1
   tempo_bpm: observed 144.0120, target 125.0000; similarity 0.8099, weight 1
   valence: observed 0.9332, target 0.8000; similarity 0.8668, weight 1
   required danceability: at least 0.65; observed 0.8436
   required genre matched: electronic
   excluded genres absent: experimental
   Source: https://freemusicarchive.org/music/MWD/Singing_Forest/07_mwd-snake_in_a_box
3. uluroo — markojux & stuart mckeown | Match: 0.942 | FMA 14996
   Genres: electronic, techno
   genre: matched electronic; similarity 1.000, weight 2
   danceability: observed 0.7763, target 0.8500; similarity 0.9263, weight 1
   energy: observed 0.6766, target 0.8500; similarity 0.8266, weight 1
   tempo_bpm: observed 124.0170, target 125.0000; similarity 0.9902, weight 1
   valence: observed 0.7093, target 0.8000; similarity 0.9093, weight 1
   required danceability: at least 0.65; observed 0.7763
   required genre matched: electronic
   excluded genres absent: experimental
   Source: https://freemusicarchive.org/music/markojux_amp_stuart_mckeown/Melbourne_Macropus/uluroo
```

## Reliability and observed results

| Case | Input / condition | Observed result |
| --- | --- | --- |
| Blank-title source record | FMA track 26620 | Excluded during preparation; 13,128 usable candidates remained |
| Unsupported lyric guarantee | `examples/unsupported_lyrics.json` | `needs_clarification`, no recommendations, exit 3 |
| No matching required conditions | Jazz at 1,000–1,001 BPM | `no_results`, no relaxed conditions, exit 3 |
| Wrong JSON type | `{"targets":{"energy":true}}` | Clear validation error, exit 2, no traceback |
| Effective exclusion guard | Fixed catalog and energy target, exclude rock | Enabled: 0 prohibited results; guard bypassed: 3 prohibited results |
| Baseline regression | Original CLI/evaluation | Byte-identical to inherited reports |
| Deterministic preparation | Rebuild snapshot/report/hierarchy | All three files byte-identical |

The exclusion comparison changes only the rejection guard for a request with an exclusion and energy target. [Recorded ablation](evaluation/pass1/guardrail_ablation.json) includes actual track IDs/preferences; the corresponding unit test makes the expected difference explicit. It establishes that guard's effect on this case, not universal reliability.

Actual full-suite output:

```text
........................................................................ [ 56%]
.......................................................                  [100%]
127 passed in 0.65s
```

Before changes: **52 passed**, no pre-existing failures. After Pass 1: **127 passed**, including all inherited tests and 75 new checks. Tests cover real CLI examples, changed ranking behavior, required conditions, unknown metadata, validation/error cases, deterministic ties, snapshot integrity, and the guardrail ablation. [Structured verification](evaluation/pass1/verification.json), [all captured CLI runs](evaluation/pass1/cli_runs.json), and [baseline evidence](evaluation/baseline/run.json) are parseable. No human listening evaluation has been performed.

To reproduce the original demonstration and experiment:

```bash
python -m src.main
python -m src.evaluate
```

The inherited CI workflow is retained and now uses the validated dependency constraints while preserving its baseline-output comparisons. **Pass 1 has not been pushed; no new GitHub Actions result is claimed.** Publication and remote CI verification remain scheduled for Pass 4.

## Catalog, limitations, and reflection

See [data provenance and rebuild recipe](data/README.md), [observed catalog report](data/catalog_report.json), and [model card](model_card.md). The real-track metadata is historical and primarily independent music; 15 broad genres have useful depth, while spoken has only seven tracks. Feature estimates do not verify mood, lyrics, instrumentation, absent vocals, or listening satisfaction. Source references are not playback guarantees; the three top demo references returned HTTP 200 in HEAD checks, recorded [here](evaluation/pass1/source_reference_checks.json).

The technical lesson observed in this pass is that data coverage and enforceable conditions must be verified independently of the assistant. The accepted/revised/rejected AI suggestions are documented in the model card; Alex's personal testing reflection remains for review. No personal surprise, human rating, live-model success, bonus completion, or official grade is claimed.

[Pass 1 completion report](docs/pass1_report.md) lists the checkpoint and commands. [Final requirements checklist](docs/requirements_checklist.md) tracks all 21 required rows and the two selected bonus categories. The [four-pass plan](docs/execution_passes.md) preserves the remaining assistant/UI, evaluation, and final-audit work. Course submission has not been performed; previously observed final-project timing remains unverified.
