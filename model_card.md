# Model card — Music Discovery Assistant

The assistant uses a user-supplied Gemini API key (BYOK), configured through `GEMINI_API_KEY` in a local `.env` file. Explore without AI supports custom settings and examples without a key. Evaluation outputs identify their response source, including predefined offline fixtures.

## Original scope and current system

The base is Module 3 Music Recommender Simulation, a deterministic weighted ranker over 20 synthetic songs. Its original source, CSV, interfaces, CLI/evaluation behavior, tests, and history are retained. The extension currently ranks a versioned catalog of 1,200 real FMA tracks using multiple genres, exclusions, required conditions, and numeric targets. It has no trained weights or listener-feedback model. The assistant specializes an existing model through structured prompting and examples, not fine-tuning. The configured default is gemini-2.5-flash-lite, temperature 0, maxOutputTokens 2048, with the same schema and vocabulary in comparison arms.

## Data, assumptions, and ranking

See `data/README.md` and `data/catalog_report.json` for attribution, exact source/rebuild details, observed coverage, and cleaning. The snapshot has 775 artists and 113 represented genre labels. Artist-capped genre stratification improves available variety but changes the source distribution. Genre labels overlap and include explicit ancestors from the source hierarchy.

Hard conditions are checked before scoring. Only requested soft attributes contribute to a weighted mean: preferred-genre match has weight 2; each numeric target has weight 1. Unit-interval features use similarity `max(0, 1 - abs(observed - target))`; tempo uses `max(0, 1 - abs(observed_bpm - target_bpm) / 100)`. Omitted preferences have no contribution. Required-only requests are marked unscored. Ties use stable track IDs.

The 0.6 soft-match threshold and 0.75 per-feature compromise indicator are explicit engineering heuristics. The recorded examples exercise them, but they are not empirically calibrated satisfaction thresholds. Match scores are not confidence, accuracy, or probabilities of enjoyment. A deterministic score does not establish that a person will like the recommendation.

## Limitations and biases

- Historical independent-music coverage excludes much of contemporary/mainstream listening. A larger catalog is still finite, and absent genres are rejected rather than forced into presets.
- Fifteen broad genres have at least 20 tracks; spoken has only seven. Other subgenres can remain sparse. Selection is not representative of music globally, listener demographics, or cultural tastes.
- Genre labels reflect source classification; categorical boundaries and hierarchical overlap can be debatable. Broad exclusions may remove crossover tracks a user would enjoy.
- Energy, acousticness, danceability, valence, tempo, and instrumentalness are algorithmic estimates. They cannot verify emotional impact, lyrics, actual instrumentation, or absence of vocals. No verified explicit-lyrics guarantee is available.
- Missing metadata causes exclusion when needed for a requested condition/target. It is not replaced with a fabricated zero.
- Source links were imported from historical records. The three top demo references returned HTTP 200 in HEAD checks, which does not verify playback or content identity for all tracks.
- Ranking uses hand-chosen weights and no listening history. Strict checks and repeatable tests do not establish subjective recommendation quality or exhaustive correctness.
- The browser’s Explore without AI mode provides custom settings or prefilled examples, with no interpretation call. The CLI’s offline fixture mode recognizes only predefined requests and cannot interpret arbitrary language. A live interpretation may misunderstand requests even when its schema is valid; human review and model-specific evaluation remain necessary.

## Misuse and mitigations

The app should not be used to guarantee child-safe lyrics, medical/therapeutic effects, or universal emotional responses. Unsupported essential conditions return `needs_clarification`; the current manual schema exposes unsupported conditions instead of silently claiming compliance. Hard exclusions and bounds are never relaxed to fill results. Recommendations cite catalog records rather than generated tracks.

The application executes no model-generated code, remote tools, audio downloads, or account actions. Its live adapter sends only the request/task/schema/vocabulary to Gemini, uses a header for the key, rejects malformed keys, bounds request/output sizes and timeout, and does not retry. Model “thought” parts are excluded; no hidden chain-of-thought is requested or retained. Strict preference/catalog validation rejects unknown fields, invalid numbers, contradictory conditions, duplicate JSON keys, and unrepresented genres. Source data preparation checks the archive checksum before reading CSVs and never deserializes its pickle member. Logs contain aggregate ranking outcomes rather than credentials or personal request history. Provider errors are safely categorized; no key or raw error body is exposed. The browser does not write request text to disk, while the evaluation harness intentionally records predefined nonpersonal cases. Provider retention follows its terms; free-tier usage may be used by the provider to improve products.

## Reliability testing observations

The suite passes 176 tests in both the project and a separately installed environment, including all 52 original tests. The original CLI and evaluation outputs remain byte-identical to their committed reports. See `evaluation/submission_check/pytest.txt` and `evaluation/submission_check/clean_setup_pytest.txt`.

The twelve-case offline harness passes 12/12, measuring fixture orchestration and guardrails. Type, syntax, dependency and actual localhost runtime checks also pass. The browser checks cover 14 states, six CLI cases exercise normal and error behavior, and catalog reconstruction is byte-identical. JSON input has an explicit 32-container nesting limit. API key validation accepts standard and dotted authorization-key formats while rejecting whitespace and control characters.

An observed boundary case in the metadata audit was a feature record whose track had no title (ID 26620). Rejecting that record avoided publishing an incomplete recommendation. The controlled exclusion ablation in `evaluation/pass1/guardrail_ablation.json` returned prohibited rock tracks when the rejection guard was bypassed and none when it was enabled. This demonstrates the guard's effect on that case, not a claim about all possible mistakes. Alex supplied qualitative feedback about discovery/variety; no scored independent listening study has been performed.

## What surprised Alex while testing reliability?

After trying the app, Alex described his reaction in the final review:

> I really liked how the recommendations were so diverse, most of the songs it recommended I had never heard before. Some of the perks of upgrading to such a large dataset.

This is Alex's actual qualitative observation about variety and discovery. No numerical listening-quality evaluation was collected. The metadata rejection and guardrail ablation above remain Codex-observed engineering findings.

## Collaboration with AI

Alex used Codex to inspect earlier projects, compare extensions, research data sources, plan the architecture, implement and test the foundation, and prepare factual documentation. Codex selected the current numeric weights, thresholds, sampling procedure, and module organization; these are agent implementation choices for Alex to inspect, not claims that Alex personally designed each detail. Alex chose the base, revised the initial scope, and selected the interface/data priorities in this chat.

## Accepted and rejected or revised AI suggestions

- **Accepted:** Alex chose the natural-language music recommender extension because translating user requests into usable preferences adds value to the existing ranker.
- **Revised:** Alex challenged the initial idea of placing the assistant over only 20 fictional songs and narrow preferences. The plan and foundation were expanded to real-track variety, multiple genres, exclusions, and additional attributes so varied requests could lead to meaningful choices.
- **Further revised:** Alex identified the separate manual and offline browser modes as redundant, requested the unified Explore without AI flow, and simplified its explanatory copy.
- **Rejected:** Alex rejected the proposed repeated LLM coaching for the guessing game: binary search can be explained once, then computed algorithmically without ongoing model calls.

These decisions occurred in the session. Alex supplied the personal observation above during final review. The final wording remains grounded in his actual choices and feedback.

## Future improvements

Future research could evaluate listener satisfaction, improve data coverage and semantics, or learn ranking weights from consented feedback. Broader request sets could examine interpretation across languages, ambiguous preferences and sparse genre coverage.

## Prompt specialization and evaluation

The specialized prompt (`prompts/specialized.txt`) supplies task rules and four illustrative examples. It separates hard/soft conditions, preserves alternatives/exclusions, leaves unrequested dimensions unset, exposes assumptions, and identifies unsupported requests. `prompts/generic.txt` is a minimal extraction baseline. Both receive the identical represented genre vocabulary and JSON response schema. Neither trains model weights or retrieves facts to generate song descriptions.

The comparison command uses the same twelve predefined requests and holds model, generation settings (temperature 0 and 2,048 output tokens), schema, vocabulary, and catalog constant. Only generic versus specialized instructions/examples change. Checks inspect original validated model preferences before deterministic corrections, then separately check downstream constraint satisfaction. The report includes individual outcomes, aggregate schema/semantic/constraint checks, actual outputs and stopped cases for inspecting differences, ties and regressions. Small-case results do not establish global accuracy, calibrated confidence, or listener enjoyment. The evaluation explicitly refuses to treat fixtures as a live specialization experiment.

A controlled test illustrates why this separation matters: a deliberately incomplete test reply omits lyric safety; the local guard blocks recommendations, but the evaluator still marks model identification of that requirement as failed. This tests the guard and evaluator as separate components.
