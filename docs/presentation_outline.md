# Presentation outline — 6 minutes

Prepared for Alex's review. This outline is preparation, not evidence that a presentation was delivered. Current model access is unverified; use the offline demo honestly until actual live verification is completed.

## 0:00–0:45 — Problem and useful role for AI

People describe music through mixed preferences: acoustic folk or country, a tempo limit, an excluded genre. A useful assistant must interpret that request and have enough suitable tracks to recommend. Alex selected this extension and challenged the initial tiny-catalog proposal. Explain that the LLM translates language into preferences; catalog facts and ranking come from Python and source metadata.

## 0:45–1:30 — Original project versus extension

Original: Module 3 Music Recommender Simulation, 20 synthetic songs, one genre/mood/energy profile and terminal output. New foundation: 1,200 real tracks, 775 artists, 113 represented genre labels, multiple genres, exclusions, required bounds, six optional attributes, and a browser review step. Show the README comparison. This is a capability/coverage comparison, not a measured improvement in enjoyment.

## 1:30–2:15 — Architecture

Show `diagrams/architecture.mmd`. Walk through request -> specialized prompt/schema -> response validation -> human review -> required-condition filtering -> deterministic ranking -> source-backed output. Point out manual fallback, explicit fixture mode, provider errors, unsupported conditions, and the catalog audit. Explain that structured prompting specializes an existing model; model weights are not trained here.

## 2:15–3:45 — Demonstration

Start the local app:

```bash
source .venv/bin/activate
python -m streamlit run app.py
```

For current reproducible evidence, select **Offline demo (mock)** and state clearly that the interpretation is a predefined test reply. Select the acoustic evening example, click Interpret, review genre/energy/acousticness/tempo assumptions, then Recommend. Show actual track metadata, a factual explanation and source reference. Change a preference and submit again; no new interpretation call is needed.

Next select the lyric-safety example. Show that unsupported conditions block results until the user explicitly removes that condition or revises the request. Never describe the resulting tracks as verified clean lyrics. Switch requests and show that old results disappear.

When a valid key and free-tier access have been confirmed and live evidence has been captured, AI assistant mode can replace the fixture demo. Until then, identify live access as the remaining verification gap. Do not silently present a fixture as live AI.

Terminal evidence:

```bash
python -m src.cli --mode offline --request "Danceable electronic or pop, high energy, no experimental tracks." --yes --limit 3
python -m src.evaluate_assistant --mode offline
python -m pytest -q
```

## 3:45–4:45 — Reliability and evaluation

Show the observed test result and `evaluation/pass23/offline_evaluation.txt`. The harness runs 12 predefined requests and reports individual/aggregate results. Offline success establishes orchestration and guardrail behavior, not model interpretation quality. Explain the exclusion ablation from Pass 1 and the test where a deliberately incomplete model fixture misses a lyric condition: a local guard blocks it, while the evaluator still marks model understanding as failed.

The specialization comparison command is implemented but has not run live. Its design holds model, schema, vocabulary, settings, and requests constant while changing generic versus specialized prompting. Show actual differences only after real results exist; a prompt file alone does not establish bonus completion.

## 4:45–5:30 — Limitations and responsible design

Historical independent catalog; uneven labels; sparse subgenres; algorithmic attributes, not emotional certainty or lyric guarantees. Scores are similarities, not confidence. Provider errors remain explicit, no automatic retries occur, requests are not written to disk by the browser app, and manual mode works without credentials. Explain that schema validity cannot prove that the model understood every sentence.

## 5:30–6:00 — Reflection and close

Use the actual accepted/revised/rejected suggestions in `model_card.md`: accepted music assistant, revised catalog depth, rejected repeated LLM binary-search coaching. Alex adds a genuine personal testing observation after trying the app. Close with the usefulness criterion demonstrated by the project: language interpretation, adequate data, and enforceable constraints must work together. Point reviewers to README evidence, model card, and the verified repository URL. State any remaining live-access or review gap honestly.
