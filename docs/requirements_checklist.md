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
| 4 | Student adds at least one substantial AI feature such as RAG, a multi-step agent or planning workflow, specialized behavior (mini fine-tune or structured prompting), or a reliability harness (evaluation loop, guardrails, self-checking). | prompts/specialized.txt; src/assistant.py; src/llm_client.py | Specialized interpreter and provider adapter implemented, offline plumbing verified. Actual model behavior pending usable key and user access/billing confirmation. | Partial — live verification blocked |
| 5 | Feature is integrated into the working system (not an isolated demo). | app.py; src/cli.py; tests/test_app.py; runtime_checks.json | Both entry points share interpretation/validation/review/ranking. Browser runtime and CLI fixtures work; live provider integration not yet verified. | Partial — integrated offline; live pending |
| 6 | Feature is functional and produces meaningful changes in system behavior. | evaluation/pass1/manual_sensitivity.json; evaluation/pass23/ | Data/ranking changes observed; actual new language interpretation and specialization differences remain unmeasured. | Partial — live model behavior unverified |
| 7 | Architecture diagram is submitted as a Mermaid source file (.mmd or embedded in a .md file); a PNG image alone is not sufficient. | diagrams/architecture.mmd | Editable Mermaid source includes actual assistant/client, human review, manual/fixture modes, ranking, errors and evaluation. | Complete |
| 8 | Diagram clearly illustrates data flow (input, then processing steps, then output). | diagrams/architecture.mmd | Actual input -> prompt/client -> checks -> review -> filter/rank -> output flow is shown, including error paths. | Complete |
| 9 | Diagram matches actual project implementation (not theoretical). | diagram; src modules; app.py | Diagram matches implemented components; final Pass 4 audit still rechecks the finished app. | Complete for current implementation |
| 10 | Student provides a working script or UI that demonstrates full system workflow. | app.py; src/cli.py; evaluation/pass23/runtime_checks.json | Full offline/manual entry point demonstrated in actual runtime; live output requires usable access. | Partial — live verification pending |
| 11 | README includes example commands and sample outputs in code blocks showing the system running end-to-end. | README three assistant-workflow examples; evaluation/pass23/cli_runs.json | Actual captured commands/outputs are explicitly labeled offline fixtures. Three live examples remain outstanding. | Partial — live examples missing |
| 12 | System responds consistently to at least 2-3 example inputs. | 12-case offline harness; tests/test_app.py | Offline cases repeat successfully. No model interpretation consistency claim is made. | Partial — live consistency unmeasured |
| 13 | System includes a reliability mechanism such as input validation, output guardrails, self-critique or multi-model agreement, or an evaluation script that tests sample inputs. | src/assistant.py; src/preferences.py; src/llm_client.py; tests/ | Validated inputs/outputs, unsupported-condition checks, effective exclusions, safe provider errors, bounded requests and tested UI review. | Complete |
| 14 | Mechanism is functional and meaningfully improves reliability. | guardrail_ablation.json; overlooked-lyric test; tests/test_app.py | Exclusion ablation changes actual results; local lyric guard blocks an overlooked condition while evaluator still records model-understanding failure. | Complete |
| 15 | Student provides examples in markdown format (showing input, behavior, and result) demonstrating how the guardrail or evaluator behaves. | README guardrail table; evaluation/pass23/; tests/ | Parseable input/observed-behavior/result evidence, with mode and error categories clearly distinguished. | Complete |
| 16 | README clearly explains project goals and new features. | README goals/features/status | Explains base scope, expanded recommender, structured-prompting assistant and the actual remaining live-access gap. | Complete |
| 17 | README contains step-by-step instructions to install, run, and test the system. | README setup; .env.example; requirements files; clean_setup_pytest.txt | Browser/manual/offline setup, tests and type checks verified in two environments; live configuration instructions supplied but model access unverified. | Partial — provider access unverified |
| 18 | README includes sample input/output illustrating system behavior. | README sample interactions; evaluation/pass23/cli_runs.json | Three captured offline assistant workflows and separate reliability case are documented. No mock is labeled live. | Partial — live examples missing |
| 19 | Student explains how they used AI during development (prompting, debugging, design). | model_card.md; ai_interactions.md | Actual prompting, implementation, debugging, type checks, UI/runtime tests, data and evaluation collaboration recorded. | Complete; final wording for Alex review |
| 20 | Student identifies at least one AI suggestion they accepted and at least one they rejected or revised. | model_card.md accepted/revised/rejected suggestions | Actual user acceptance of option one, expanded-data revision and rejection of repetitive binary-search LLM coaching documented. | Complete; wording for Alex review |
| 21 | Student reflects on system limitations and future improvements. | model_card.md; docs/portfolio_draft.md | Current data/model limits, misuse mitigations, testing observations and future work described. Alex personal testing reflection remains for review. | Partial — personal/final review pending |

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
| Live versus offline integrity | Partial — live blocked | All captured assistant cases are labeled offline_fixture/model none. Existing key rejected with API_KEY_INVALID; user instructed no generation until confirmation. No live success claimed. |
| No unapproved charges | Partial | Confirm usable access/cost before live calls; never enable billing or assume course quotas remain current. |
| Meaningful new/regression tests and checks | Complete for current implementation | 170 tests pass in project and clean environments, including UI/provider failures and effective guardrails. Mypy, compileall, pip check and original report comparisons pass. |
| Reproducible setup and actual user entry points | Partial | Verify documented install/run/test from clean setup; test browser and CLI behavior, not only helpers. |
| Three successful end-to-end examples plus errors | Partial | Capture actual commands/input/output/mode/model for three varied normal requests and separate guardrail/provider/no-result behavior. |
| Fair before/after comparison | Partial | Isolate catalog/ranker and LLM effects; numeric match scores are not probabilities; no invented listener evaluation. |
| Parseable execution evidence | Partial | Use README fenced blocks/tables and committed text/JSON logs; screenshots/video do not replace evidence. |
| Retained and updated offline CI | Partial — remote run pending Pass 4 | Workflow retains inherited checks and adds offline harness and app type checking, with no secrets. All corresponding commands pass locally; no push/new Actions run claimed. |
| README all required content | Partial | Name/describe base, goals, architecture, design tradeoffs, setup/prerequisites/configuration, three real examples, reliability, limitations/live gap, and brief reflection. |
| Final Mermaid matches implementation | Complete for current implementation | diagrams/architecture.mmd includes actual interpreter/provider, review, fixtures/manual fallback, catalog/ranker, errors and evaluator. Recheck during final audit. |
| Model card all ethics/reflection questions | Requires Alex review | All technical ethics/collaboration/limitation sections are drafted in model_card.md; personal testing surprise still needs Alex. Live specialization result remains blocked. |
| Honest authorship and personal experience | Requires Alex review | Record actual decisions from chat; do not fabricate Alex surprise, human evaluation, or personal experiences. Personal reflection reviewed after real tests. |
| 5–7 minute presentation outline | Complete — prepared, not delivered | docs/presentation_outline.md provides a six-minute structure, exact demo commands, evidence, limitations and reflection. |
| Presentation delivery | Requires Alex review | Actual delivery is a future human action; prepared outline is not evidence of delivery. |
| Portfolio summary and reflection | Requires Alex review | docs/portfolio_draft.md includes verified public repository URL, factual status and a draft grounded in actual user decisions. Not published elsewhere. |
| Multiple meaningful new commits | Partial | Aim for three coherent feature/test/documentation commits atop imported base history; no empty commits or unrelated changes. |
| Final source and rubric audit | Partial | Re-read full handoff and both appendices; replace planned targets with actual files, evidence, and precise remaining gaps. |
| Final report contents | Partial | Absolute local path, verified repo URL, actual commit hashes/purposes, exact commands/results, real CI URL/status, rubric assessment, live/personal-review items. |
| No course submission or external messaging | Complete | None performed; continue to avoid submission, messages, video recording/upload, or publication outside authorized final repo. |
| Deadline and Demo Day timing | Partial | Official pages inaccessible. Prior observed deadline Nov 16, 2026 2:59 a.m. New York and Demo Day Nov 18 8 p.m. remain unverified; do not claim on-time submission. |
| Combined Passes 2–3 checkpoint | Partial — live verification blocked | App, provider/interpreter, review flow, offline harness, tests, evidence and documentation implemented. User requested combined passes. Live outputs/comparison and Pass 4 audit/publication remain outstanding. |

## Selected bonus rubric: up to +4 targeted

Alex's later request to pursue bonuses authorizes these two categories. The original source remains unchanged. These are targets subject to observed evidence and the course grader's judgment.

| Category | Exact supplied criterion | Planned artifact / acceptance evidence | Status |
| --- | --- | --- | --- |

| Fine-Tuning or Specialization Behavior (+2 per category) | Specialized model behavior (few-shot patterns, synthetic datasets, or constrained tone/style) is demonstrated. | Actual prompt/examples and live comparison machinery exist; no actual live model outputs or measurable differences collected. | Blocked — usable key and user access/billing confirmation pending |
| Fine-Tuning or Specialization Behavior (+2 per category) | `model_card.md` includes a comparison of baseline vs. specialized output showing measurable differences. | Actual prompt/examples and live comparison machinery exist; no actual live model outputs or measurable differences collected. | Blocked — usable key and user access/billing confirmation pending |
| Test Harness or Evaluation Script (+2 per category) | A script that evaluates the system on multiple predefined inputs is built and runs successfully. | Actual 12-case offline harness traverses interpretation, guards and ranking; evaluation/pass23/offline_evaluation.json and .txt. | Complete — evidence supports this category; no awarded grade claimed |
| Test Harness or Evaluation Script (+2 per category) | The script prints a summary of results (pass/fail score, confidence, or similar). | Printed per-case results and aggregate specialized: 12/12 passed, explicitly labeled fixtures/model none. | Complete — evidence supports this category; no awarded grade claimed |

RAG Enhancement and Agentic Workflow Enhancement remain outside the selected scope. Do not report bonus completion based only on the existence of tests or a specialized prompt; verify the exact criteria and observed behavior.

## Evidence update rule

Replace planned paths with real paths as code is implemented. Mark Complete only when the artifact and supporting observed result exist. Record blockers specifically and preserve mock/live distinctions. Review all 21 rows and additional instructions against the full source before final reporting.
