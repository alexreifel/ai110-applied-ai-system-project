# Actual AI collaboration — final project

Alex selected the music-assistant extension, rejected repetitive LLM binary-search coaching, and revised the initial tiny-catalog proposal. Alex confirmed independent real tracks and a local browser interface plus reproducible CLI. Alex subsequently authorized the evaluation-harness and specialization bonuses and requested the full Pass 1 foundation.

Codex inspected the actual repositories, preserved both histories, established the 52-test baseline, researched FMA, implemented the data preparation/schema/ranker/CLI, ran meaningful regression and error tests, and captured the observed results. Weights, thresholds, sampling and module choices are Codex implementation decisions for Alex to review. No hidden model chain-of-thought is requested or stored.

See [Pass 1 report](docs/pass1_report.md), [model card](model_card.md), and [session handoff](docs/SESSION_HANDOFF.md). Original Module 3 interaction notes are preserved verbatim in [docs/baseline/ai_interactions.md](docs/baseline/ai_interactions.md). No live LLM was called in Pass 1.

Combined Passes 2–3: Alex requested both passes in one run. Codex implemented the specialized/generic prompts, bounded Gemini adapter, editable Streamlit flow, shared assistant CLI, evaluation harness, provider/UI tests and captured offline evidence. A pytest reserved-parameter naming issue and UI type annotations were corrected during verification. Codex added a key-format check to prevent malformed header values leaking through errors and separated original model interpretation from deterministic corrections in evaluation.

Read-only model access returned API_KEY_INVALID. Alex explicitly directed that generation stay offline until access/billing are confirmed and plans to configure the key locally. No model generation was run. The offline harness passed 12/12 predefined cases; 170 tests passed in two environments, app type checks passed, and a temporary localhost runtime check returned real-track cards and cleared stale state. Specialization comparison is implemented but has no observed live results. Portfolio wording uses Alex's writing-style skill and remains for Alex's review.
