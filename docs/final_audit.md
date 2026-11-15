# Final assignment audit and submission recheck

Reviewed November 14, 2026, America/New_York, starting from commit `791b1db67477c7e8ca69b4026444f6c8bcabc924`. Alex explicitly selected **“Keep live calls off; run everything offline.”** This recheck made no Gemini requests. It completed all independent offline verification and reviewed every required rubric criterion, both selected bonus categories and the complete handoff. This is an evidence assessment, not an official grade.

**Readiness:** the offline implementation and documentation checks pass. Full submission readiness remains unverified because three successful live AI examples and actual model-behavior evidence are missing. The specialization bonus also lacks measured generic-versus-specialized outputs. No fixture result is treated as live AI, and the selected feature remains structured prompting/specialization.

## Source and user instructions

The full supplied handoff and both appendices were reread. The complete source is preserved at [source/AI110_Final_Project_Codex_Prompt.md](source/AI110_Final_Project_Codex_Prompt.md), 36,532 bytes, SHA-256 `80499cf3ac233cf418596f1fa07d7531a9a35f7428439a8afc0fa57ecccbe0a0`. It matches the original hash recorded before implementation. The Downloads original is no longer present during this recheck; the verbatim archived source remains available and unchanged.

Later instructions select Module 3 Music Recommender Simulation, a broad independent-track catalog, a local browser app plus CLI, evaluation/specialization bonuses, and the merged Explore without AI mode. Alex's exact requested copy remains installed. The personal variety/discovery reflection is quoted verbatim in the model card. The original base and unrelated user work remain preserved.

## Observed execution results

Fresh evidence: [evaluation/submission_check/verification.json](../evaluation/submission_check/verification.json).

| Check | Actual result |
| --- | --- |
| `.venv/bin/python -m pytest -q` | 176 passed, including all 52 original tests |
| `/private/tmp/ai110-pass1-clean-env/bin/python -m pytest -q` | 176 passed in the separately installed environment |
| `.venv/bin/python -m src.evaluate_assistant --mode offline --output evaluation/submission_check/offline_evaluation.json` | 12/12 predefined cases passed; offline_fixture, model none |
| `.venv/bin/python -m mypy app.py --follow-imports=silent --ignore-missing-imports` | Success, no issues |
| `.venv/bin/python -m compileall -q src tests scripts app.py` | Exit 0 |
| `.venv/bin/python -m pip check` | No broken requirements |
| `python -m src.main` and `python -m src.evaluate` | Both byte-identical to committed original reports |
| Actual CLI entry point | Six captured cases passed: three normal fixture requests, unsupported lyric guarantee, manual acoustic request and strict no-results case |
| Actual running browser entry point | 14 states passed: custom preferences, three varied examples, source cards, unsupported blocking and explicit revision, mode-change clearing, blank AI request rejection and exact requested copy |
| Exact catalog rebuild | Catalog, report and genre hierarchy byte-identical after archive checksum verification |
| Base preservation | All 18 tracked baseline hashes unchanged; original sibling clean |
| Source preservation | Archived assignment byte count and original recorded SHA-256 unchanged |

The temporary test server used a separate localhost port and was stopped afterward; Alex's existing app server was untouched. The AI success path is covered offline by an explicitly injected fixture, including review/edit/rerank without repeated interpretation. Browser fixtures and CLI fixtures do not establish real language understanding. The README contains three actual captured fixture examples with outputs; [fresh CLI captures](../evaluation/submission_check/cli_runs.json) reproduce them, but live versions remain missing.

The fixed-catalog sensitivity and exclusion ablation in evaluation/pass1/ still demonstrate deterministic changes. The evaluator checks original model preferences before local semantic corrections so a guardrail rescue cannot inflate model-understanding scores. No confidence calibration or numerical listening-quality claim is made.

## All 21 exact required rubric criteria

The wording below is copied verbatim from Appendix B, as in the [maintained checklist](requirements_checklist.md). Complete means observed supporting evidence exists. Partial retains the specific live evidence gap rather than predicting a score.

| # | Exact supplied criterion | Implemented artifact(s) | Observed evidence / remaining gap | Status |
| --- | --- | --- | --- | --- |
| 1 | Student identifies the original project they are extending. | README original scope; docs/baseline/README.md | Explicitly names Module 3 Music Recommender Simulation and links preserved baseline documentation. | Complete |
| 2 | Student provides a short description of the original system's goal and capabilities. | README original scope section | Accurate original 20-song, genre/mood/energy, CLI description; captured baseline in evaluation/baseline/. | Complete |
| 3 | Description is accurate and sets clear context for extensions. | README comparison table; evaluation/baseline/; preservation_check.json | Description checked against unchanged base files and observed baseline runs. | Complete |
| 4 | Student adds at least one substantial AI feature such as RAG, a multi-step agent or planning workflow, specialized behavior (mini fine-tune or structured prompting), or a reliability harness (evaluation loop, guardrails, self-checking). | prompts/specialized.txt; src/assistant.py; src/llm_client.py | Specialized interpreter and provider adapter implemented, offline plumbing verified. Current key loads and read-only metadata succeeded; the one previously approved generation attempt returned 403. Live behavior remains unverified, and Alex requested offline-only testing for this pass. | Partial — live verification blocked |
| 5 | Feature is integrated into the working system (not an isolated demo). | app.py; src/cli.py; tests/test_app.py; runtime_checks.json | Both entry points share interpretation/validation/review/ranking. Browser runtime and CLI fixtures work; live provider integration not yet verified. | Partial — integrated offline; live pending |
| 6 | Feature is functional and produces meaningful changes in system behavior. | evaluation/pass1/manual_sensitivity.json; evaluation/pass23/ | Data/ranking changes observed; actual new language interpretation and specialization differences remain unmeasured. | Partial — live model behavior unverified |
| 7 | Architecture diagram is submitted as a Mermaid source file (.mmd or embedded in a .md file); a PNG image alone is not sufficient. | diagrams/architecture.mmd | Editable Mermaid source includes actual assistant/client, human review, Explore without AI and CLI fixture modes, ranking, errors and evaluation. | Complete |
| 8 | Diagram clearly illustrates data flow (input, then processing steps, then output). | diagrams/architecture.mmd | Actual input -> prompt/client -> checks -> review -> filter/rank -> output flow is shown, including error paths. | Complete |
| 9 | Diagram matches actual project implementation (not theoretical). | diagram; src modules; app.py | Diagram matches implemented components; final audit checked the finished app and current runtime evidence. | Complete |
| 10 | Student provides a working script or UI that demonstrates full system workflow. | app.py; src/cli.py; evaluation/submission_check/runtime_checks.json | Full offline/manual entry point demonstrated in actual runtime; live output requires usable access. | Partial — live verification pending |
| 11 | README includes example commands and sample outputs in code blocks showing the system running end-to-end. | README three assistant-workflow examples; evaluation/submission_check/cli_runs.json | Actual captured commands/outputs are explicitly labeled offline fixtures. Three live examples remain outstanding. | Partial — live examples missing |
| 12 | System responds consistently to at least 2-3 example inputs. | 12-case offline harness; tests/test_app.py | Offline cases repeat successfully. No model interpretation consistency claim is made. | Partial — live consistency unmeasured |
| 13 | System includes a reliability mechanism such as input validation, output guardrails, self-critique or multi-model agreement, or an evaluation script that tests sample inputs. | src/assistant.py; src/preferences.py; src/llm_client.py; tests/ | Validated inputs/outputs, unsupported-condition checks, effective exclusions, safe provider errors, bounded requests and tested UI review. | Complete |
| 14 | Mechanism is functional and meaningfully improves reliability. | guardrail_ablation.json; overlooked-lyric test; tests/test_app.py | Exclusion ablation changes actual results; local lyric guard blocks an overlooked condition while evaluator still records model-understanding failure. | Complete |
| 15 | Student provides examples in markdown format (showing input, behavior, and result) demonstrating how the guardrail or evaluator behaves. | README guardrail table; evaluation/pass23/; tests/ | Parseable input/observed-behavior/result evidence, with mode and error categories clearly distinguished. | Complete |
| 16 | README clearly explains project goals and new features. | README goals/features/status | Explains base scope, expanded recommender, structured-prompting assistant and the actual remaining live-access gap. | Complete |
| 17 | README contains step-by-step instructions to install, run, and test the system. | README setup; .env.example; requirements files; clean_setup_pytest.txt | Browser/CLI setup, tests and type checks verified in two environments; live configuration is documented, with its separate access gap disclosed. | Complete |
| 18 | README includes sample input/output illustrating system behavior. | README sample interactions; evaluation/submission_check/cli_runs.json | Three captured offline assistant workflows and separate reliability case are documented. No mock is labeled live. | Partial — live examples missing |
| 19 | Student explains how they used AI during development (prompting, debugging, design). | model_card.md; ai_interactions.md | Actual prompting, implementation, debugging, type checks, UI/runtime tests, data and evaluation collaboration recorded. | Complete |
| 20 | Student identifies at least one AI suggestion they accepted and at least one they rejected or revised. | model_card.md accepted/revised/rejected suggestions | Actual user acceptance of option one, expanded-data revision and rejection of repetitive binary-search LLM coaching documented. | Complete |
| 21 | Student reflects on system limitations and future improvements. | model_card.md; docs/portfolio_draft.md | Current data/model limits, misuse mitigations, actual testing observations and future work described. Alex supplied his personal observation about recommendation variety. | Complete |

Fourteen rows have complete local evidence; seven retain the same live-verification gap (4–6, 10–12, 18). This counts checklist statuses, not awarded or predicted points. Passing 176 offline tests does not establish successful Gemini generation, interpretation quality or full end-to-end live operation.

## All selected bonus statements

| Category | Exact supplied criterion | Implemented artifact / observed evidence | Status |
| --- | --- | --- | --- |
| Fine-Tuning or Specialization Behavior (+2 per category) | Specialized model behavior (few-shot patterns, synthetic datasets, or constrained tone/style) is demonstrated. | Actual prompt/examples and live comparison machinery exist; no actual live model outputs or measurable differences collected. | Blocked — usable key and user access/billing confirmation pending |
| Fine-Tuning or Specialization Behavior (+2 per category) | `model_card.md` includes a comparison of baseline vs. specialized output showing measurable differences. | Actual prompt/examples and live comparison machinery exist; no actual live model outputs or measurable differences collected. | Blocked — usable key and user access/billing confirmation pending |
| Test Harness or Evaluation Script (+2 per category) | A script that evaluates the system on multiple predefined inputs is built and runs successfully. | Actual 12-case offline harness traverses interpretation, guards and ranking; evaluation/submission_check/offline_evaluation.json and .txt. | Complete — evidence supports this category; no awarded grade claimed |
| Test Harness or Evaluation Script (+2 per category) | The script prints a summary of results (pass/fail score, confidence, or similar). | Printed per-case results and aggregate specialized: 12/12 passed, explicitly labeled fixtures/model none. | Complete — evidence supports this category; no awarded grade claimed |

The two harness statements support the **+2 evaluation-harness category**, subject to grading; they are not +2 each. The specialization category remains blocked until real model behavior and measurable baseline differences are captured. RAG/agentic bonuses are outside the selected scope. No bonus award or 100% result is guaranteed.

## Code and documentation review

The engineering code-review skill was used for correctness, security, performance and maintainability. No unresolved critical/high code defect was found in this scoped offline review. This is not an exhaustive security audit or live model certification.

| Dimension | Rating | Evidence and observations |
| --- | --- | --- |
| Correctness | Pass offline; live interpretation unverified | Strict typed finite values, duplicate/nonfinite/depth rejection, catalog-backed identities, hard filtering before ranking, stable ties and honest clarification/no-result states. Provider, review, edit and stale-state paths are tested. |
| Security | Pass for scoped checks | Fixed provider URL, secret-safe errors, header-only key transport, repr exclusion, validated source links, no model tools/code execution and no pickle deserialization. Credential paths remain ignored; candidate/history scans are publication gates. |
| Performance | Appropriate for documented local catalog | Cached 1,200-track catalog; bounded input/output and timeout; one call with no automatic retries. No large-scale benchmark claim. |
| Maintainability | Pass after documentation corrections | Shared browser/CLI backend, immutable preferences, clear provider/schema/ranking modules, honest fixture provenance and updated evidence links. |

Findings resolved in this recheck:

- The 403 message incorrectly led with a rejected-key diagnosis. It now identifies HTTP 403 and directs the user to project Status, Billing Tier and key restrictions. The existing provider test verifies that message, one attempt and secret-safe output. The category remains compatible with the evaluator's early-stop behavior. See [src/llm_client.py:100](../src/llm_client.py#L100) and [tests/test_assistant.py:82](../tests/test_assistant.py#L82).
- Current README/model card/checklist still contained historical “no generation attempts” and old invalid-key status. They now distinguish the earlier invalid key, the later successful metadata lookups, the single approved generation diagnostic returning 403, and this explicitly offline recheck.
- Current portfolio/checklist test counts and runtime links were stale. They now point to the fresh 176-test, six-CLI-case, 14-state browser and exact-rebuild evidence. Historical checkpoint logs are preserved.

Earlier resolved compatibility findings remain documented in evaluation/final/ci_followup.json and evaluation/key_compatibility/: explicit JSON depth independent of Python recursion, authorization-key periods, merged browser modes and successful AI-review regression coverage. Good choices retained include actual source facts, explicit review, visible assumptions, effective hard conditions and separate model-versus-guardrail evaluation.

## Every additional handoff obligation

| Requirement | Status | Evidence / remaining action |
| --- | --- | --- |
| Verbatim preservation across compaction | Complete | Complete source and both appendices reread. Archived36,532-byte source matches preserved SHA-256; the Downloads original is no longer present, so this recheck uses the archived copy and original recorded hash. |
| Project selection | Complete | Alex chose Module 3 plus an expanded real-track recommender and language assistant; independent tracks and browser UI + CLI confirmed. |
| Authorized bonus scope | Partial — one verified category; one blocked | Evaluation harness has 12/12 offline evidence; specialization needs actual live behavior and measurable differences. No credit awarded by this audit. |
| Dedicated final project and original preservation | Complete | Base head, clean status, all 18 original tracked-file hashes unchanged; core inherited application/tests identical. evaluation/pass1/preservation_check.json. |
| Public repository identity | Complete | GitHub connector reverified public visibility, alexreifel ownership and push permission during this submission recheck. |
| Retain both existing histories | Complete | History-preserving merge 5901fa0 retains 97724ce and base 46eaeb6 as ancestors. No reset or force push; setup merge is additional to feature commits. |
| Authentication and safe push destinations | Complete | Final audit verified authenticated alexreifel, sole origin fetch/push URL, main tracking, and no pushDefault/pushRemote/extra mappings. Publication uses explicit HEAD:refs/heads/main, without force. |
| Any retained upstream is fetch-only | Complete | Used a local-path fetch via FETCH_HEAD; no upstream remote was retained. Dedicated origin is the only remote. |
| Secrets, unrelated material, and visibility | Complete | Final publication gate scans staged files and every reachable history blob, verifies ignored credential paths, and checks unrelated content. See final audit; no credentials or visibility changes authorized. |
| Project-local supported Python environment | Complete | Project .venv uses Python 3.11.18; pinned constraints install in a fresh environment; Streamlit 1.67.0 skill discovery succeeded. Shared environment unchanged. |
| Baseline tests before changes | Complete | 52 tests passed before changes, no pre-existing failures; original demo/evaluation match committed reports. See evaluation/baseline/. |
| Preserve and explain original behavior | Complete | Original code, CSV and tests retained; original demo/evaluation still byte-identical; original docs archived. README explains the extension. |
| Required directories | Complete | assets/README.md and diagrams/architecture.mmd present; final diagram reflects actual merged browser modes and CLI evaluation. |
| Real catalog variety and source provenance | Complete | 1,200 tracks, 775 artists, 113 labels. Fresh source-archive checksum check and byte-identical catalog/report/hierarchy rebuild passed; evaluation/submission_check/catalog_rebuild.json. |
| Substantial integrated specialization | Partial | Document actual prompt/schema/model; verify natural-language interpretation affects the actual workflow. No fine-tuning or RAG claims for this design. |
| Deterministic validation and bounded execution | Complete | Tests cover blank/malformed/oversized inputs, unsupported conditions, schema/types/values/vocabulary, contradictions, provider errors, and timeouts. One call, no retries, bounded output. |
| User-facing errors and safe useful logs | Complete | Provider/category tests distinguish configuration, auth/model access, quota/provider/network/timeout/invalid output from legitimate clarification/no-result. Logs omit credentials and private requests. |
| Live versus offline integrity | Complete — evidence labeling; live behavior blocked | One earlier approved 32-token generation attempt returned 403; metadata GETs succeeded. Alex explicitly selected offline-only for this recheck. Fixtures remain labeled; no live-model quality claim. |
| No unapproved charges | Complete | The earlier single diagnostic was explicitly approved and denied with403. No billing changes or additional generation during this recheck; Alex instructed offline-only. |
| Meaningful new/regression tests and checks | Complete | 176 tests pass in both project and separately installed environments. Updated403-message test verifies useful account/billing guidance without exposing secrets. Mypy, compileall, pip check, original outputs all pass; evaluation/submission_check/. |
| Reproducible setup and actual user entry points | Complete | Both test environments pass. Fresh running app passed14 states, including3 different examples, unsupported blocking/revision and blank request; six fresh CLI cases passed. No Gemini calls during this recheck. |
| Three successful end-to-end examples plus errors | Partial | Capture actual commands/input/output/mode/model for three varied normal requests and separate guardrail/provider/no-result behavior. |
| Fair before/after comparison | Partial — live comparison blocked | Original behavior byte-identical; deterministic catalog/ranking sensitivity and guardrail ablation preserved. Actual same-model generic-vs-specialized comparison remains unmeasured; fixtures are not model-quality evidence. |
| Parseable execution evidence | Complete | Fresh text/JSON in evaluation/submission_check/, including176-test results,12-case evaluation,6 CLI cases,14 runtime states and exact catalog rebuild. README includes fenced observed results. |
| Retained and updated offline CI | Complete for verified published checkpoint; final push rechecked at delivery | Real CI run 43655455444 for 791b1db passed Python 3.11/3.12. Workflow retains baseline checks,176 tests, syntax, offline evaluator and mypy without secrets. Latest audit-commit run is inspected after publication. |
| README all required content | Partial — three live AI outputs missing | All requested sections and three actual labeled fixture examples exist. Actual live Gemini example outputs remain unavailable and are not fabricated. |
| Final Mermaid matches implementation | Complete | Source diagram checked against final modules: explicit interpretation, human review, unified Explore without AI, CLI fixtures, catalog/ranking, errors and evaluation. |
| Model card all ethics/reflection questions | Complete | Clearly labeled sections answer every Appendix A question and rubric reflection criterion. Includes actual Alex feedback, accepted/rejected/revised suggestions and technical findings; live comparison remains separately blocked. |
| Honest authorship and personal experience | Complete | Actual session decisions and verbatim Alex variety/discovery observation are attributed accurately; no fabricated surprise, human scores or live evaluation. |
| 5–7 minute presentation outline | Complete — prepared, not delivered | docs/presentation_outline.md provides a six-minute structure, exact demo commands, evidence, limitations and reflection. |
| Presentation delivery | Requires Alex review | Actual delivery is a future human action; prepared outline is not evidence of delivery. |
| Portfolio summary and reflection | Requires Alex review | Prepared summary/reflection and verified public repo link in docs/portfolio_draft.md. Personal wording remains for review; nothing published elsewhere. |
| Multiple meaningful new commits | Complete | Published history contains the foundation, assistant/reliability, interface/audit and necessary compatibility corrections plus Alex’s later commit. This recheck adds actual verification and documentation corrections; no history rewriting or empty commits. |
| Final source and rubric audit | Complete | Complete source/both appendices reread; all 21 exact required rows,4 selected bonus statements and additional handoff rules audited again. docs/final_audit.md records current evidence and remaining gaps. |
| Final report contents | Complete at delivery | Final delivery reports local path, public repo, actual commits, commands/results, real CI status/link, rubric assessment and exact live/review gaps. No official grade or submission claim. |
| No course submission or external messaging | Complete | None performed; continue to avoid submission, messages, video recording/upload, or publication outside authorized final repo. |
| Deadline and Demo Day timing | Partial | Official pages inaccessible. Prior observed deadline Nov 16, 2026 2:59 a.m. New York and Demo Day Nov 18 8 p.m. remain unverified; do not claim on-time submission. |
| Combined Passes 2–3 checkpoint | Partial — live verification blocked | Independent implementation and all offline rechecks complete. Actual live outputs and specialization measurements remain unavailable; this pass is explicitly offline-only. |

## Access and live-evidence status

The original model-list failure (`evaluation/pass23/access_status.json`) was historical. With Alex's replacement key, read-only listing and configured-model lookup returned 200. He approved one tiny diagnostic with a 32-token output cap; it returned 403 PERMISSION_DENIED (`evaluation/access_diagnostic.json`). No successful live output was captured. His later billing screenshot showed a payment-activation requirement for a Postpay account, but did not establish that account's linkage to this Gemini project or conclusively explain the 403. This pass respects his subsequent explicit offline-only instruction and made no additional Gemini calls or billing changes.

Remaining required evidence is three successful real AI inputs/outputs and verification of the actual live interpreter/review/ranking flow. A working key alone cannot prove those paths. The optional selected specialization comparison must hold model, settings, schema, vocabulary, catalog and cases constant, report actual differences/ties/regressions and remain within separately approved call/spend limits. A denied access probe is not a successful example, and preset outputs cannot fill the gap.

## Publication and CI

Dedicated public repository: [alexreifel/ai110-applied-ai-system-project](https://github.com/alexreifel/ai110-applied-ai-system-project). Identity/public visibility/push permission were rechecked through the GitHub connector. Both initial histories remain ancestors; no reset, rebase or force push is used. The last verified published review-base run, [43655455444](https://github.com/alexreifel/ai110-applied-ai-system-project/actions/runs/43655455444), passed Python 3.11 and 3.12 for 791b1db. The current audit change is committed/pushed after destination and secret checks; its actual new run URL/status is reported at delivery, never predeclared successful.

Original feature commits include 5fd7368 (foundation), e6da65c (assistant/evaluation), 2abd669 (interface/audit), e16e099 (Python depth correction), and 2e1a516 (authorization-key compatibility). Alex later committed 791b1db. This audit adds meaningful updated evidence and truthful documentation, preserving all published history and the original Module 3 submission.

## Review and remaining human actions

Review the README, model card and this checklist before submission. The six-minute presentation outline and portfolio summary/reflection are prepared; Alex still reviews personal wording and delivers the presentation. No CodePath submission, external message, video upload or outside publication has occurred. Course project/rubric/Demo Day pages were attempted again but remained inaccessible, so deadline and Demo Day times remain unverified.

Offline verification is complete. Full submission readiness and the specialization bonus remain unverified while live examples/comparison are unavailable. Future live work requires new explicit authorization after usable account/billing access is established; this pass's instruction is offline-only.
