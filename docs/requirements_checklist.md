# Requirements checklist

Planning date: November 14, 2026 (America/New_York).

The 21 criterion texts below are copied verbatim from Appendix B of `source/AI110_Final_Project_Codex_Prompt.md`. That complete verbatim document remains the source for all requirements, including both appendices and every handoff instruction. Later explicit user instructions take precedence over historical document instructions.

Status meanings: **Complete** = verified artifact and evidence exist; **Partial** = planned or incomplete; **Blocked** = specific unavailable prerequisite prevents that item; **Requires Alex review** = personal judgment, review, or delivery still needed. A plan is not completed implementation. No official grade is assigned.

## Required rubric: all 21 one-point rows

| # | Exact supplied criterion | Planned artifact(s) | Required observed evidence / acceptance | Status |
| --- | --- | --- | --- | --- |
| 1 | Student identifies the original project they are extending. | README original scope; docs/baseline/README.md | Explicitly names Module 3 Music Recommender Simulation and links preserved baseline documentation. | Complete |
| 2 | Student provides a short description of the original system's goal and capabilities. | README original scope section | Accurate original 20-song, genre/mood/energy, CLI description; captured baseline in evaluation/baseline/. | Complete |
| 3 | Description is accurate and sets clear context for extensions. | README comparison table; evaluation/baseline/; preservation_check.json | Description checked against unchanged base files and observed baseline runs. | Complete |
| 4 | Student adds at least one substantial AI feature such as RAG, a multi-step agent or planning workflow, specialized behavior (mini fine-tune or structured prompting), or a reliability harness (evaluation loop, guardrails, self-checking). | src/preferences.py; src/ranking.py; future assistant/prompt | Expanded foundation works; substantial specialized LLM interpretation is not implemented yet. | Partial — Pass 2 pending |
| 5 | Feature is integrated into the working system (not an isolated demo). | src/cli.py; future browser and assistant services | Manual CLI traverses real pipeline; AI/browser integration remains outstanding. | Partial — Pass 2 pending |
| 6 | Feature is functional and produces meaningful changes in system behavior. | evaluation/pass1/manual_sensitivity.json; future live examples | Changed catalog/ranking behavior verified; no live AI behavior is claimed. | Partial — Pass 2 pending |
| 7 | Architecture diagram is submitted as a Mermaid source file (.mmd or embedded in a .md file); a PNG image alone is not sufficient. | diagrams/architecture.mmd | Editable Mermaid source committed with implemented Pass 1 components; update after Pass 2. | Complete for current checkpoint |
| 8 | Diagram clearly illustrates data flow (input, then processing steps, then output). | diagrams/architecture.mmd | Current flow includes human JSON input, checks, filtering, scoring and output; AI/review browser flow awaits Pass 2. | Partial — final flow pending |
| 9 | Diagram matches actual project implementation (not theoretical). | diagrams/architecture.mmd; actual source modules | Diagram matches current foundation; verify final implementation again after AI integration. | Partial — final flow pending |
| 10 | Student provides a working script or UI that demonstrates full system workflow. | src/cli.py; examples/ | Working manual entry point demonstrated; final browser/AI workflow remains outstanding. | Partial — full AI workflow pending |
| 11 | README includes example commands and sample outputs in code blocks showing the system running end-to-end. | README; evaluation/pass1/cli_runs.json | Three actual manual commands/outputs captured; later capture live assistant commands/outputs separately. | Partial — live examples pending |
| 12 | System responds consistently to at least 2-3 example inputs. | tests/test_foundation.py; evaluation/pass1/ | Three varied manual examples repeat successfully; no AI interpretation consistency measured yet. | Partial — live examples pending |
| 13 | System includes a reliability mechanism such as input validation, output guardrails, self-critique or multi-model agreement, or an evaluation script that tests sample inputs. | src/catalog.py; src/preferences.py; src/ranking.py; tests/test_foundation.py | Validation, hard conditions, missing evidence and unsupported-condition checks tested; provider guardrails remain Pass 2 work. | Complete for foundation |
| 14 | Mechanism is functional and meaningfully improves reliability. | test_guardrail_blocks_candidate_that_would_otherwise_rank_first; evaluation/pass1/guardrail_ablation.json | Guard enabled returns zero excluded tracks; controlled bypass returns three excluded real tracks. | Complete for foundation |
| 15 | Student provides examples in markdown format (showing input, behavior, and result) demonstrating how the guardrail or evaluator behaves. | README reliability table; evaluation/pass1/guardrail_ablation.json | Inputs, observed behavior and actual results are parseable; unsupported/no-result examples include exit status. | Complete for foundation |
| 16 | README clearly explains project goals and new features. | README goals, comparison, remaining work | Explains original/new behavior and clearly marks the AI feature as pending. | Complete for current checkpoint |
| 17 | README contains step-by-step instructions to install, run, and test the system. | README install/run/test; requirements files; clean_setup_pytest.txt | Manual setup verified in a fresh environment; provider configuration and browser commands await Pass 2. | Partial — AI setup pending |
| 18 | README includes sample input/output illustrating system behavior. | README three manual examples | Actual current behavior illustrated; final AI input/output samples still needed. | Partial — live examples pending |
| 19 | Student explains how they used AI during development (prompting, debugging, design). | model_card.md collaboration; ai_interactions.md | Actual Codex and Alex contributions recorded; update as later passes proceed. | Complete for current checkpoint |
| 20 | Student identifies at least one AI suggestion they accepted and at least one they rejected or revised. | model_card.md accepted/rejected/revised suggestions | Actual acceptance of option one, revision of tiny catalog, and rejection of repeated LLM binary-search coaching documented. | Complete; wording for Alex review |
| 21 | Student reflects on system limitations and future improvements. | model_card.md limitations/future work | Current limitations, biases, future work and evidence described; final model-specific observations and Alex review remain. | Partial — final review pending |

## Additional handoff and course instructions

| Requirement | Status | Evidence / remaining action |
| --- | --- | --- |
| Verbatim preservation across compaction | Complete | Source copy is byte-identical; SHA-256 is recorded in SESSION_HANDOFF.md. Re-read it after compaction and at the final audit. |
| Project selection | Complete | Alex chose Module 3 plus an expanded real-track recommender and language assistant; independent tracks and browser UI + CLI confirmed. |
| Authorized bonus scope | Partial | Alex now requests bonuses. Target evaluation harness (+2) and demonstrated specialization (+2); preserve required work and avoid unrelated stretch categories. |
| Dedicated final project and original preservation | Complete | Base head, clean status, all 18 original tracked-file hashes unchanged; core inherited application/tests identical. evaluation/pass1/preservation_check.json. |
| Public repository identity | Complete | GitHub connector verified alexreifel/ai110-applied-ai-system-project is public during planning; recheck before publication. |
| Retain both existing histories | Complete | History-preserving merge 5901fa0 retains 97724ce and base 46eaeb6 as ancestors. No reset or force push; setup merge is additional to feature commits. |
| Authentication and safe push destinations | Partial | Before pushing inspect auth, fetch/push URLs, tracking, remote.pushDefault, branch pushRemote and push mappings; publish only to final repo. |
| Any retained upstream is fetch-only | Complete | Used a local-path fetch via FETCH_HEAD; no upstream remote was retained. Dedicated origin is the only remote. |
| Secrets, unrelated material, and visibility | Partial | Scan staged content and inherited history; never publish credentials/.env or unrelated files, enable billing, or change an existing private repo to public. |
| Project-local supported Python environment | Complete | Project .venv uses Python 3.11.18; pinned constraints install in a fresh environment; Streamlit 1.67.0 skill discovery succeeded. Shared environment unchanged. |
| Baseline tests before changes | Complete | 52 tests passed before changes, no pre-existing failures; original demo/evaluation match committed reports. See evaluation/baseline/. |
| Preserve and explain original behavior | Complete | Original code, CSV and tests retained; original demo/evaluation still byte-identical; original docs archived. README explains the extension. |
| Required directories | Complete | assets/README.md and diagrams/architecture.mmd present; diagram reflects actual Pass 1 implementation. |
| Real catalog variety and source provenance | Complete | 1,200 real tracks, 775 artists, 113 labels; audited source/checksums/cleaning and byte-identical rebuild. data/README.md and catalog_report.json. |
| Substantial integrated specialization | Partial | Document actual prompt/schema/model; verify natural-language interpretation affects the actual workflow. No fine-tuning or RAG claims for this design. |
| Deterministic validation and bounded execution | Partial | Cover blank/malformed/oversized input, unsupported conditions, bad schema, invalid values, contradictions, provider errors, and timeouts. Justify any bounded retry. |
| User-facing errors and safe useful logs | Partial | Separate missing config, auth/model access, provider/quota failure, timeout, invalid response, legitimate no-result; avoid secret/raw private request logs. |
| Live versus offline integrity | Partial | Use labeled mock/fixture clients for repeatable tests; actual live access/cost/model remain unverified. Never label mocks as live success. |
| No unapproved charges | Partial | Confirm usable access/cost before live calls; never enable billing or assume course quotas remain current. |
| Meaningful new/regression tests and checks | Partial | Run pytest and inherited applicable checks; include effective guardrail test and comparison with it disabled when feasible. |
| Reproducible setup and actual user entry points | Partial | Verify documented install/run/test from clean setup; test browser and CLI behavior, not only helpers. |
| Three successful end-to-end examples plus errors | Partial | Capture actual commands/input/output/mode/model for three varied normal requests and separate guardrail/provider/no-result behavior. |
| Fair before/after comparison | Partial | Isolate catalog/ranker and LLM effects; numeric match scores are not probabilities; no invented listener evaluation. |
| Parseable execution evidence | Partial | Use README fenced blocks/tables and committed text/JSON logs; screenshots/video do not replace evidence. |
| Retained and updated offline CI | Partial | Retain inherited workflow, regression evidence comparisons, and mock tests without API secrets; inspect actual run URL/status after push. |
| README all required content | Partial | Name/describe base, goals, architecture, design tradeoffs, setup/prerequisites/configuration, three real examples, reliability, limitations/live gap, and brief reflection. |
| Final Mermaid matches implementation | Partial | Source in diagrams/ shows actual components, flow, checks, and human review; PNG alone is insufficient. |
| Model card all ethics/reflection questions | Partial | Include biases/limitations, misuse/mitigations, testing observations/surprise, collaboration, accepted and rejected/revised suggestion, future improvements. README-only reflection does not satisfy this. |
| Honest authorship and personal experience | Requires Alex review | Record actual decisions from chat; do not fabricate Alex surprise, human evaluation, or personal experiences. Personal reflection reviewed after real tests. |
| 5–7 minute presentation outline | Partial | Prepare docs/presentation_outline.md covering problem, base vs extension, architecture, demo, reliability, limits, and reflection; do not claim delivered. |
| Presentation delivery | Requires Alex review | Actual delivery is a future human action; prepared outline is not evidence of delivery. |
| Portfolio summary and reflection | Requires Alex review | Draft docs/portfolio_draft.md with verified GitHub URL and personal wording for Alex review; do not publish elsewhere. |
| Multiple meaningful new commits | Partial | Aim for three coherent feature/test/documentation commits atop imported base history; no empty commits or unrelated changes. |
| Final source and rubric audit | Partial | Re-read full handoff and both appendices; replace planned targets with actual files, evidence, and precise remaining gaps. |
| Final report contents | Partial | Absolute local path, verified repo URL, actual commit hashes/purposes, exact commands/results, real CI URL/status, rubric assessment, live/personal-review items. |
| No course submission or external messaging | Complete | None performed; continue to avoid submission, messages, video recording/upload, or publication outside authorized final repo. |
| Deadline and Demo Day timing | Partial | Official pages inaccessible. Prior observed deadline Nov 16, 2026 2:59 a.m. New York and Demo Day Nov 18 8 p.m. remain unverified; do not claim on-time submission. |
| Pass 1 checkpoint | Complete | Foundation implemented and verified; user requested Pass 1 only. Browser/LLM, bonus harness/comparison, final audit and publication remain for later passes. |

## Selected bonus rubric: up to +4 targeted

Alex's later request to pursue bonuses authorizes these two categories. The original source remains unchanged. These are targets subject to observed evidence and the course grader's judgment.

| Category | Exact supplied criterion | Planned artifact / acceptance evidence | Status |
| --- | --- | --- | --- |

| Fine-Tuning or Specialization Behavior (+2 per category) | Specialized model behavior (few-shot patterns, synthetic datasets, or constrained tone/style) is demonstrated. | Actual specialized prompt with task-specific examples and constrained output, integrated in the app; observed live model behavior. | Partial — planned; no observed bonus evidence yet |
| Fine-Tuning or Specialization Behavior (+2 per category) | `model_card.md` includes a comparison of baseline vs. specialized output showing measurable differences. | model_card.md includes a measured same-model, same-schema, same-vocabulary, same-request comparison of generic and specialized prompt outputs; record individual results, actual settings, and limitations. | Partial — planned; no observed bonus evidence yet |
| Test Harness or Evaluation Script (+2 per category) | A script that evaluates the system on multiple predefined inputs is built and runs successfully. | python -m src.evaluate_assistant runs predefined inputs through the real backend, with explicit offline/live modes, and exits successfully on recorded checks. | Partial — planned; no observed bonus evidence yet |
| Test Harness or Evaluation Script (+2 per category) | The script prints a summary of results (pass/fail score, confidence, or similar). | Print per-case pass/fail and aggregate counts; commit actual machine-readable results and a reproducible command. | Partial — planned; no observed bonus evidence yet |

RAG Enhancement and Agentic Workflow Enhancement remain outside the selected scope. Do not report bonus completion based only on the existence of tests or a specialized prompt; verify the exact criteria and observed behavior.

## Evidence update rule

Replace planned paths with real paths as code is implemented. Mark Complete only when the artifact and supporting observed result exist. Record blockers specifically and preserve mock/live distinctions. Review all 21 rows and additional instructions against the full source before final reporting.
