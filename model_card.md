# Model card — Music Discovery Assistant

Status: **Pass 1 foundation implemented; AI interpretation and browser interface are pending Pass 2.** Current runs use manual structured preferences and no LLM. Historical Module 3 documentation is preserved in `docs/baseline/`.

## Original scope and current system

The base is Module 3 Music Recommender Simulation, a deterministic weighted ranker over 20 synthetic songs. Its original source, CSV, interfaces, CLI/evaluation behavior, tests, and history are retained. The extension currently ranks a versioned catalog of 1,200 real FMA tracks using multiple genres, exclusions, required conditions, and numeric targets. It has no trained weights or listener-feedback model. The planned assistant will specialize an LLM through structured prompting, not fine-tuning; no live model has been verified or called in Pass 1.

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
- Pass 1 does not yet understand natural language. Planned LLM interpretation may misunderstand requests even when its output schema is valid; human review and additional model-specific evaluation remain necessary.

## Misuse and mitigations

The app should not be used to guarantee child-safe lyrics, medical/therapeutic effects, or universal emotional responses. Unsupported essential conditions return `needs_clarification`; the current manual schema exposes unsupported conditions instead of silently claiming compliance. Hard exclusions and bounds are never relaxed to fill results. Recommendations cite catalog records rather than generated tracks.

Pass 1 executes no model-generated code, remote tool calls, audio downloads, or account actions. Strict preference/catalog validation rejects unknown fields, invalid numbers, contradictory conditions, duplicate JSON keys, and unrepresented genres. Source data preparation checks the archive checksum before reading CSVs and never deserializes its pickle member. Logs contain aggregate ranking outcomes rather than credentials or personal request history. Future provider calls will need explicit access/cost checks and bounded errors before live verification.

## Reliability testing observations

Before changes, the original 52 tests passed and the original CLI/evaluation outputs matched the committed reports. Pass 1 adds behavioral checks around actual ranking changes, real CLI examples, source integrity, and invalid-input/error handling. Recorded test results are in `evaluation/pass1/pytest.txt`; they are observed runs rather than an estimated test count.

An observed boundary case in the metadata audit was a feature record whose track had no title (ID 26620). Rejecting that record avoided publishing an incomplete recommendation. The controlled exclusion ablation in `evaluation/pass1/guardrail_ablation.json` returned prohibited rock tracks when the rejection guard was bypassed and none when it was enabled. This demonstrates the guard's effect on that case, not a claim about all possible mistakes. No independent human listening evaluation has been performed.

## What surprised Alex while testing reliability?

**Requires Alex review after trying the system.** The missing-title finding and guardrail comparison above are Codex-observed technical results. They are not attributed to Alex as a personal surprise or experience. Record Alex's actual observation here during review before submission.

## Collaboration with AI

Alex used Codex to inspect earlier projects, compare extensions, research data sources, plan the architecture, implement and test the foundation, and prepare factual documentation. Codex selected the current numeric weights, thresholds, sampling procedure, and module organization; these are agent implementation choices for Alex to inspect, not claims that Alex personally designed each detail. Alex chose the base, revised the initial scope, and selected the interface/data priorities in this chat.

## Accepted and rejected or revised AI suggestions

- **Accepted:** Alex chose the natural-language music recommender extension because translating user requests into usable preferences adds value to the existing ranker.
- **Revised:** Alex challenged the initial idea of placing the assistant over only 20 fictional songs and narrow preferences. The plan and foundation were expanded to real-track variety, multiple genres, exclusions, and additional attributes so varied requests could lead to meaningful choices.
- **Rejected:** Alex rejected the proposed repeated LLM coaching for the guessing game: binary search can be explained once, then computed algorithmically without ongoing model calls.

These decisions occurred in the session. Alex should review the final wording and add personal reflection without inventing development or listening experiences.

## Future improvements and remaining work

Pass 2 will integrate the specialized interpreter, browser UI, and shared CLI workflow with visible preference review and provider failure handling. Pass 3 will add the explicitly requested evaluation harness and actual same-model generic-vs-specialized prompt comparison. Pass 4 will audit all 21 required rubric rows and selected bonuses, finish evidence/personal review, and verify publication/CI.

Later research could evaluate listener satisfaction, improve data coverage and semantics, or learn weights from consented feedback. These are future ideas, not implemented features or authorized extra scope for this pass.

## Specialization comparison and live-access status

**Pending Passes 2–3.** No model identifier, live outputs, specialization comparison, fine-tuning, or model-quality score is claimed. Offline/manual foundation evidence cannot substantiate live LLM behavior or the specialization bonus. Usable credentials, model access, quotas, and cost constraints remain unverified.
