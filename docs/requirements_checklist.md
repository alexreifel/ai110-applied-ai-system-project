# Requirements checklist

Planning date: November 14, 2026 (America/New_York).

The 21 criterion texts below are copied verbatim from Appendix B of `source/AI110_Final_Project_Codex_Prompt.md`. That complete verbatim document remains the source for all requirements, including both appendices and every handoff instruction. Later explicit user instructions take precedence over historical document instructions.

Status meanings: **Complete** = verified artifact and evidence exist; **Partial** = planned or incomplete; **Blocked** = specific unavailable prerequisite prevents that item; **Requires Alex review** = personal judgment, review, or delivery still needed. A plan is not completed implementation. No official grade is assigned.

## Required rubric: all 21 one-point rows

| # | Exact supplied criterion | Implemented artifact(s) | Required observed evidence / acceptance | Status |
| --- | --- | --- | --- | --- |
| 1 | Student identifies the original project they are extending. | README original scope; docs/baseline/README.md | Explicitly names Module 3 Music Recommender Simulation and links preserved baseline documentation. | Complete |
| 2 | Student provides a short description of the original system's goal and capabilities. | README original scope section | Accurate original 20-song, genre/mood/energy, CLI description; captured baseline in evaluation/baseline/. | Complete |
| 3 | Description is accurate and sets clear context for extensions. | README comparison table; evaluation/baseline/; preservation_check.json | Description checked against unchanged base files and observed baseline runs. | Complete |
| 4 | Student adds at least one substantial AI feature such as RAG, a multi-step agent or planning workflow, specialized behavior (mini fine-tune or structured prompting), or a reliability harness (evaluation loop, guardrails, self-checking). | prompts/specialized.txt; src/assistant.py; src/llm_client.py | Specialized interpreter and provider adapter implemented, offline plumbing verified. Actual model behavior pending usable key and user access/billing confirmation. | Partial — live verification blocked |
| 5 | Feature is integrated into the working system (not an isolated demo). | app.py; src/cli.py; tests/test_app.py; runtime_checks.json | Both entry points share interpretation/validation/review/ranking. Browser runtime and CLI fixtures work; live provider integration not yet verified. | Partial — integrated offline; live pending |
| 6 | Feature is functional and produces meaningful changes in system behavior. | evaluation/pass1/manual_sensitivity.json; evaluation/pass23/ | Data/ranking changes observed; actual new language interpretation and specialization differences remain unmeasured. | Partial — live model behavior unverified |
| 7 | Architecture diagram is submitted as a Mermaid source file (.mmd or embedded in a .md file); a PNG image alone is not sufficient. | diagrams/architecture.mmd | Editable Mermaid source includes actual assistant/client, human review, Explore without AI and CLI fixture modes, ranking, errors and evaluation. | Complete |
| 8 | Diagram clearly illustrates data flow (input, then processing steps, then output). | diagrams/architecture.mmd | Actual input -> prompt/client -> checks -> review -> filter/rank -> output flow is shown, including error paths. | Complete |
| 9 | Diagram matches actual project implementation (not theoretical). | diagram; src modules; app.py | Diagram matches implemented components; final audit checked the finished app and current runtime evidence. | Complete |
| 10 | Student provides a working script or UI that demonstrates full system workflow. | app.py; src/cli.py; evaluation/final/runtime_checks.json | Full offline/manual entry point demonstrated in actual runtime; live output requires usable access. | Partial — live verification pending |
| 11 | README includes example commands and sample outputs in code blocks showing the system running end-to-end. | README three assistant-workflow examples; evaluation/pass23/cli_runs.json | Actual captured commands/outputs are explicitly labeled offline fixtures. Three live examples remain outstanding. | Partial — live examples missing |
| 12 | System responds consistently to at least 2-3 example inputs. | 12-case offline harness; tests/test_app.py | Offline cases repeat successfully. No model interpretation consistency claim is made. | Partial — live consistency unmeasured |
| 13 | System includes a reliability mechanism such as input validation, output guardrails, self-critique or multi-model agreement, or an evaluation script that tests sample inputs. | src/assistant.py; src/preferences.py; src/llm_client.py; tests/ | Validated inputs/outputs, unsupported-condition checks, effective exclusions, safe provider errors, bounded requests and tested UI review. | Complete |
| 14 | Mechanism is functional and meaningfully improves reliability. | guardrail_ablation.json; overlooked-lyric test; tests/test_app.py | Exclusion ablation changes actual results; local lyric guard blocks an overlooked condition while evaluator still records model-understanding failure. | Complete |
| 15 | Student provides examples in markdown format (showing input, behavior, and result) demonstrating how the guardrail or evaluator behaves. | README guardrail table; evaluation/pass23/; tests/ | Parseable input/observed-behavior/result evidence, with mode and error categories clearly distinguished. | Complete |
| 16 | README clearly explains project goals and new features. | README goals/features/status | Explains base scope, expanded recommender, structured-prompting assistant and the actual remaining live-access gap. | Complete |
| 17 | README contains step-by-step instructions to install, run, and test the system. | README setup; .env.example; requirements files; clean_setup_pytest.txt | Browser/CLI setup, tests and type checks verified in two environments; live configuration is documented, with its separate access gap disclosed. | Complete |
| 18 | README includes sample input/output illustrating system behavior. | README sample interactions; evaluation/pass23/cli_runs.json | Three captured offline assistant workflows and separate reliability case are documented. No mock is labeled live. | Partial — live examples missing |
| 19 | Student explains how they used AI during development (prompting, debugging, design). | model_card.md; ai_interactions.md | Actual prompting, implementation, debugging, type checks, UI/runtime tests, data and evaluation collaboration recorded. | Complete |
| 20 | Student identifies at least one AI suggestion they accepted and at least one they rejected or revised. | model_card.md accepted/revised/rejected suggestions | Actual user acceptance of option one, expanded-data revision and rejection of repetitive binary-search LLM coaching documented. | Complete |
| 21 | Student reflects on system limitations and future improvements. | model_card.md; docs/portfolio_draft.md | Current data/model limits, misuse mitigations, actual testing observations and future work described. Alex supplied his personal observation about recommendation variety. | Complete |

## Additional handoff and course instructions

| Requirement | Status | Evidence / remaining action |
| --- | --- | --- |
| Verbatim preservation across compaction | Complete | Source copy is byte-identical; SHA-256 is recorded in SESSION_HANDOFF.md. Re-read it after compaction and at the final audit. |
| Project selection | Complete | Alex chose Module 3 plus an expanded real-track recommender and language assistant; independent tracks and browser UI + CLI confirmed. |
| Authorized bonus scope | Partial — one verified category; one blocked | Evaluation harness has 12/12 offline evidence; specialization needs actual live behavior and measurable differences. No credit awarded by this audit. |
| Dedicated final project and original preservation | Complete | Base head, clean status, all 18 original tracked-file hashes unchanged; core inherited application/tests identical. evaluation/pass1/preservation_check.json. |
| Public repository identity | Complete | Reverified public owner alexreifel and push permission during final audit; exact dedicated URL in docs/final_audit.md. |
| Retain both existing histories | Complete | History-preserving merge 5901fa0 retains 97724ce and base 46eaeb6 as ancestors. No reset or force push; setup merge is additional to feature commits. |
| Authentication and safe push destinations | Complete | Final audit verified authenticated alexreifel, sole origin fetch/push URL, main tracking, and no pushDefault/pushRemote/extra mappings. Publication uses explicit HEAD:refs/heads/main, without force. |
| Any retained upstream is fetch-only | Complete | Used a local-path fetch via FETCH_HEAD; no upstream remote was retained. Dedicated origin is the only remote. |
| Secrets, unrelated material, and visibility | Complete | Final publication gate scans staged files and every reachable history blob, verifies ignored credential paths, and checks unrelated content. See final audit; no credentials or visibility changes authorized. |
| Project-local supported Python environment | Complete | Project .venv uses Python 3.11.18; pinned constraints install in a fresh environment; Streamlit 1.67.0 skill discovery succeeded. Shared environment unchanged. |
| Baseline tests before changes | Complete | 52 tests passed before changes, no pre-existing failures; original demo/evaluation match committed reports. See evaluation/baseline/. |
| Preserve and explain original behavior | Complete | Original code, CSV and tests retained; original demo/evaluation still byte-identical; original docs archived. README explains the extension. |
| Required directories | Complete | assets/README.md and diagrams/architecture.mmd present; final diagram reflects actual merged browser modes and CLI evaluation. |
| Real catalog variety and source provenance | Complete | 1,200 real tracks, 775 artists, 113 labels; audited source/checksums/cleaning and byte-identical rebuild. data/README.md and catalog_report.json. |
| Substantial integrated specialization | Partial | Document actual prompt/schema/model; verify natural-language interpretation affects the actual workflow. No fine-tuning or RAG claims for this design. |
| Deterministic validation and bounded execution | Complete | Tests cover blank/malformed/oversized inputs, unsupported conditions, schema/types/values/vocabulary, contradictions, provider errors, and timeouts. One call, no retries, bounded output. |
| User-facing errors and safe useful logs | Complete | Provider/category tests distinguish configuration, auth/model access, quota/provider/network/timeout/invalid output from legitimate clarification/no-result. Logs omit credentials and private requests. |
| Live versus offline integrity | Partial — live blocked | All fixture captures are labeled offline_fixture/model none. No generation until explicit key/access/billing confirmation. No model-quality or live-success claim. |
| No unapproved charges | Complete | Zero content-generation calls; no billing changes. Explicit user access/billing confirmation remains required before any live generation. |
| Meaningful new/regression tests and checks | Complete | 171 tests pass in project and clean environments, including the added successful AI review test with an injected fixture. Mypy, compileall, pip check and original report comparisons pass; evaluation/final/. |
| Reproducible setup and actual user entry points | Complete | Clean dependency installation and full tests verified; actual localhost browser and captured CLI exercised. Live provider behavior is separately blocked. |
| Three successful end-to-end examples plus errors | Partial | Capture actual commands/input/output/mode/model for three varied normal requests and separate guardrail/provider/no-result behavior. |
| Fair before/after comparison | Partial — live comparison blocked | Preserved original outputs and controlled fixed-catalog sensitivity/guardrail ablation isolate deterministic changes. Same-model/settings/schema/cases live prompt comparison is implemented but unmeasured; no invented listening scores. |
| Parseable execution evidence | Complete | README fenced commands/outputs and committed text/JSON evidence, including evaluation/final/. No screenshot/video substituted. |
| Retained and updated offline CI | Partial — inspect remote run after publication | Workflow retains baseline checks and adds offline harness/type checking for Python 3.11/3.12. Local equivalents pass. Actual post-push run/status must be reported separately; see final audit. |
| README all required content | Partial — three live AI outputs missing | All requested sections and three actual labeled fixture examples exist. Actual live Gemini example outputs remain unavailable and are not fabricated. |
| Final Mermaid matches implementation | Complete | Source diagram checked against final modules: explicit interpretation, human review, unified Explore without AI, CLI fixtures, catalog/ranking, errors and evaluation. |
| Model card all ethics/reflection questions | Complete | Clearly labeled sections answer every Appendix A question and rubric reflection criterion. Includes actual Alex feedback, accepted/rejected/revised suggestions and technical findings; live comparison remains separately blocked. |
| Honest authorship and personal experience | Complete | Actual session decisions and verbatim Alex variety/discovery observation are attributed accurately; no fabricated surprise, human scores or live evaluation. |
| 5–7 minute presentation outline | Complete — prepared, not delivered | docs/presentation_outline.md provides a six-minute structure, exact demo commands, evidence, limitations and reflection. |
| Presentation delivery | Requires Alex review | Actual delivery is a future human action; prepared outline is not evidence of delivery. |
| Portfolio summary and reflection | Requires Alex review | Prepared summary/reflection and verified public repo link in docs/portfolio_draft.md. Personal wording remains for review; nothing published elsewhere. |
| Multiple meaningful new commits | Complete in final audit checkpoint | Foundation, assistant/reliability, and final interface/audit/evidence changes form three substantive new commits, in addition to the history-preserving setup merge. No empty commits or rewrites. |
| Final source and rubric audit | Complete | Re-read full source/both appendices; docs/final_audit.md evaluates every required/selected-bonus row and all additional handoff instructions. Exact source SHA verified again. |
| Final report contents | Complete at delivery | Final delivery reports local path, public repo, actual commits, commands/results, real CI status/link, rubric assessment and exact live/review gaps. No official grade or submission claim. |
| No course submission or external messaging | Complete | None performed; continue to avoid submission, messages, video recording/upload, or publication outside authorized final repo. |
| Deadline and Demo Day timing | Partial | Official pages inaccessible. Prior observed deadline Nov 16, 2026 2:59 a.m. New York and Demo Day Nov 18 8 p.m. remain unverified; do not claim on-time submission. |
| Combined Passes 2–3 checkpoint | Partial — live verification blocked | Independent implementation and Pass 4 local audit complete. Actual live outputs and generic-versus-specialized measurements await explicit access/billing confirmation. |

## Selected bonus rubric: up to +4 targeted

Alex's later request to pursue bonuses authorizes these two categories. The original source remains unchanged. These are targets subject to observed evidence and the course grader's judgment.

| Category | Exact supplied criterion | Implemented artifact / observed evidence | Status |
| --- | --- | --- | --- |
| Fine-Tuning or Specialization Behavior (+2 per category) | Specialized model behavior (few-shot patterns, synthetic datasets, or constrained tone/style) is demonstrated. | Actual prompt/examples and live comparison machinery exist; no actual live model outputs or measurable differences collected. | Blocked — usable key and user access/billing confirmation pending |
| Fine-Tuning or Specialization Behavior (+2 per category) | `model_card.md` includes a comparison of baseline vs. specialized output showing measurable differences. | Actual prompt/examples and live comparison machinery exist; no actual live model outputs or measurable differences collected. | Blocked — usable key and user access/billing confirmation pending |
| Test Harness or Evaluation Script (+2 per category) | A script that evaluates the system on multiple predefined inputs is built and runs successfully. | Actual 12-case offline harness traverses interpretation, guards and ranking; evaluation/final/offline_evaluation.json and .txt. | Complete — evidence supports this category; no awarded grade claimed |
| Test Harness or Evaluation Script (+2 per category) | The script prints a summary of results (pass/fail score, confidence, or similar). | Printed per-case results and aggregate specialized: 12/12 passed, explicitly labeled fixtures/model none. | Complete — evidence supports this category; no awarded grade claimed |

RAG Enhancement and Agentic Workflow Enhancement remain outside the selected scope. Do not report bonus completion based only on the existence of tests or a specialized prompt; verify the exact criteria and observed behavior.

## Evidence update rule

Replace planned paths with real paths as code is implemented. Mark Complete only when the artifact and supporting observed result exist. Record blockers specifically and preserve mock/live distinctions. Review all 21 rows and additional instructions against the full source before final reporting.
