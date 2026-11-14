# Model card — Music Discovery Assistant

Status: **Final local audit complete; implementation verified offline. Live Gemini validation and the measured specialization comparison remain pending usable access and Alex’s confirmation.** The browser/CLI interpreter and provider adapter exist; current captured assistant runs use explicitly labeled fixtures, not a live LLM. Historical Module 3 documentation is preserved in `docs/baseline/`.

## Original scope and current system

The base is Module 3 Music Recommender Simulation, a deterministic weighted ranker over 20 synthetic songs. Its original source, CSV, interfaces, CLI/evaluation behavior, tests, and history are retained. The extension currently ranks a versioned catalog of 1,200 real FMA tracks using multiple genres, exclusions, required conditions, and numeric targets. It has no trained weights or listener-feedback model. The assistant specializes an existing model through structured prompting and examples, not fine-tuning. The configured default is gemini-2.5-flash-lite, temperature 0, maxOutputTokens 2048, with the same schema and vocabulary in comparison arms. No model content-generation call has been made during these passes.

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
- The implemented live adapter has not yet been verified against usable access. The browser’s Explore without AI mode provides custom settings or prefilled examples, with no interpretation call. The CLI’s offline fixture mode recognizes only predefined requests and cannot interpret arbitrary language. A live interpretation may misunderstand requests even when its schema is valid; human review and model-specific evaluation remain necessary.

## Misuse and mitigations

The app should not be used to guarantee child-safe lyrics, medical/therapeutic effects, or universal emotional responses. Unsupported essential conditions return `needs_clarification`; the current manual schema exposes unsupported conditions instead of silently claiming compliance. Hard exclusions and bounds are never relaxed to fill results. Recommendations cite catalog records rather than generated tracks.

The application executes no model-generated code, remote tools, audio downloads, or account actions. Its live adapter sends only the request/task/schema/vocabulary to Gemini, uses a header for the key, rejects malformed keys, bounds request/output sizes and timeout, and does not retry. Model “thought” parts are excluded; no hidden chain-of-thought is requested or retained. Strict preference/catalog validation rejects unknown fields, invalid numbers, contradictory conditions, duplicate JSON keys, and unrepresented genres. Source data preparation checks the archive checksum before reading CSVs and never deserializes its pickle member. Logs contain aggregate ranking outcomes rather than credentials or personal request history. Live verification still requires usable access and Alex’s confirmation of billing/free-tier scope. Provider errors are safely categorized; no key or raw error body is exposed. The browser does not write request text to disk, while the evaluation harness intentionally records predefined nonpersonal cases. Provider retention follows its terms; free-tier usage may be used by the provider to improve products.

## Reliability testing observations

Before changes, the original 52 tests passed and the original CLI/evaluation outputs matched the committed reports. Pass 1 adds behavioral checks around actual ranking changes, real CLI examples, source integrity, and invalid-input/error handling. The full suite now passes 174 tests in both project and separate clean environments; see `evaluation/final/pytest.txt` and `evaluation/final/clean_setup_pytest.txt`. The twelve-case offline harness passes 12/12, explicitly measuring fixture orchestration/guardrails rather than model quality. Mypy and actual localhost runtime checks also pass. These are observed runs, not estimated counts. The first real CI run passed Python 3.11 but exposed Python 3.12 accepting deeply nested JSON without a recursion error. Codex corrected the guard to enforce 32 nested containers explicitly and added boundary/string tests; the actual initial run and correction are recorded in evaluation/final/ci_followup.json. Latest rerun status is reported at delivery.

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

## Future improvements and remaining work

The interpreter, editable browser review, shared CLI, bounded provider errors, offline harness, and live comparison machinery are implemented. Remaining work is usable live access and confirmation, three captured live examples, and actual generic-vs-specialized measurements. Publication and actual CI verification are reported separately after the final commit. The complete source/rubric audit is in `docs/final_audit.md`. Alex supplied his actual personal reflection during the final review. Presentation outline and portfolio draft are prepared; neither is delivered or published.

Later research could evaluate listener satisfaction, improve data coverage and semantics, or learn weights from consented feedback. These are future ideas, not implemented features or authorized extra scope for this pass.

## Specialization comparison and live-access status

The specialized prompt (`prompts/specialized.txt`) supplies task rules and four illustrative examples. It separates hard/soft conditions, preserves alternatives/exclusions, leaves unrequested dimensions unset, exposes assumptions, and identifies unsupported requests. `prompts/generic.txt` is a minimal extraction baseline. Both receive the identical represented genre vocabulary and JSON response schema. Neither trains model weights or retrieves facts to generate song descriptions.

| Comparison requirement | Current observed status |
| --- | --- |
| Same model/settings/schema/vocabulary/catalog/cases | Implemented in `src/evaluate_assistant.py`; hashes/settings saved per run |
| Actual generic-prompt outputs | Not collected; live access unverified |
| Actual specialized-prompt outputs | Not collected; live access unverified |
| Measured output differences | Not measured; no superiority or specialization bonus claimed |
| Runnable evaluation harness | Verified offline on 12 predefined inputs; prints per-case and aggregate results |

The read-only model-list probe returned HTTP 400, INVALID_ARGUMENT, reason API_KEY_INVALID. Alex instructed the agent to keep content generation offline until key and billing/free-tier access are confirmed, and said the key would be configured locally. No generation request, live success, model-quality score, or bonus-specialization result is invented. `evaluation/pass23/access_status.json` records that gap.

The future live comparison uses the same twelve predefined requests and holds model, generation settings (temperature 0 and 2,048 output tokens), schema, vocabulary, and catalog constant. Only generic versus specialized instructions/examples change. Checks inspect original validated model preferences before deterministic corrections, then separately check downstream constraint satisfaction. Report individual outcomes and aggregate schema/semantic/constraint checks, actual outputs, ties/regressions and any stopped cases. Small-case results do not establish global accuracy, calibrated confidence, or listener enjoyment. The evaluation explicitly refuses to treat fixtures as a live specialization experiment.

A controlled test illustrates why this separation matters: a deliberately incomplete test reply omits lyric safety; the local guard blocks recommendations, but the evaluator still marks model identification of that requirement as failed. That is evidence about the guard/evaluator implementation, not observed Gemini behavior.
