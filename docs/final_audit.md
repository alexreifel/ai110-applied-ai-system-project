# Final assignment and implementation audit

Audit date: November 14, 2026, America/New_York. This is an evidence assessment, not an official grade. The local final pass is complete. Live Gemini verification remains blocked by the user's explicit instruction to wait for access and billing confirmation. Zero content-generation calls were made.

## Scope and source integrity

Codex reread the complete supplied handoff, Appendix A and Appendix B, then checked the finished application, tests, current running-app states, documentation, history and evidence against them. The complete source remains verbatim at [source/AI110_Final_Project_Codex_Prompt.md](source/AI110_Final_Project_Codex_Prompt.md): 36,532 bytes; SHA-256 `80499cf3ac233cf418596f1fa07d7531a9a35f7428439a8afc0fa57ecccbe0a0`. Final verification compared it byte-for-byte to the Downloads original. Later user choices authorize the music assistant, expanded independent-track catalog, browser plus CLI, two selected bonuses, and merged Explore without AI mode.

The final browser copy matches Alex's requested text: “Choose an example or set your own preferences below. All settings are editable.” and “Built on historical FMA metadata.” The separate requests-to-Gemini sidebar sentence was removed. Catalog/AI limitations remain documented in the model card and README. Custom settings and examples share one editable flow; examples load preferences directly. CLI fixtures remain explicitly identified.

## Every required criterion

The criterion column below is copied verbatim from the source, as in the [maintained checklist](requirements_checklist.md). Complete means the specified artifact and observed supporting evidence exist. Partial identifies actual missing evidence, including an unverified live interpreter. Conservative live-related statuses are retained even where offline reliability evidence is substantial.

| # | Exact supplied criterion | Implemented artifact(s) | Observed evidence / remaining gap | Status |
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

Fourteen rows have complete local artifact/evidence coverage; seven retain a live-verification gap (4–6, 10–12, 18). These counts are checklist statuses, not predicted course points. In particular, passing deterministic tests does not establish that Gemini understands arbitrary requests. The selected AI feature has not been silently relabeled to claim completion.

## Selected bonus criteria

| Category | Exact supplied criterion | Implemented artifact / observed evidence | Status |
| --- | --- | --- | --- |
| Fine-Tuning or Specialization Behavior (+2 per category) | Specialized model behavior (few-shot patterns, synthetic datasets, or constrained tone/style) is demonstrated. | Actual prompt/examples and live comparison machinery exist; no actual live model outputs or measurable differences collected. | Blocked — usable key and user access/billing confirmation pending |
| Fine-Tuning or Specialization Behavior (+2 per category) | `model_card.md` includes a comparison of baseline vs. specialized output showing measurable differences. | Actual prompt/examples and live comparison machinery exist; no actual live model outputs or measurable differences collected. | Blocked — usable key and user access/billing confirmation pending |
| Test Harness or Evaluation Script (+2 per category) | A script that evaluates the system on multiple predefined inputs is built and runs successfully. | Actual 12-case offline harness traverses interpretation, guards and ranking; evaluation/final/offline_evaluation.json and .txt. | Complete — evidence supports this category; no awarded grade claimed |
| Test Harness or Evaluation Script (+2 per category) | The script prints a summary of results (pass/fail score, confidence, or similar). | Printed per-case results and aggregate specialized: 12/12 passed, explicitly labeled fixtures/model none. | Complete — evidence supports this category; no awarded grade claimed |

The two harness statements support the **+2 evaluation category**, subject to grading. They are not +2 each. The two specialization statements remain blocked: prompt files, schemas and a comparison command do not establish measured specialized behavior. RAG and agentic bonuses remain outside scope. No bonus award or 100% result is guaranteed.

## Observed final verification

All outputs below are captured under [evaluation/final](../evaluation/final/verification.json), with commands and exit codes. Earlier checkpoints are retained as historical evidence; their three-mode browser snapshots do not describe the final UI.

| Check | Actual result |
| --- | --- |
| `.venv/bin/python -m pytest -q` | 174 passed, including all 52 inherited tests |
| `/private/tmp/ai110-pass1-clean-env/bin/python -m pytest -q` | 174 passed in the separately installed environment |
| `.venv/bin/python -m src.evaluate_assistant --mode offline --output evaluation/final/offline_evaluation.json` | 12/12 predefined cases passed; offline_fixture, model none |
| `.venv/bin/python -m mypy app.py --follow-imports=silent --ignore-missing-imports` | Success, no issues |
| `.venv/bin/python -m compileall -q src tests scripts app.py` | Exit 0 |
| `.venv/bin/python -m pip check` | No broken requirements |
| Original `python -m src.main` / `python -m src.evaluate` | Byte-identical to committed original reports |
| Final running Streamlit app | Ten actual localhost states passed: copy, initial AI screen without generation, custom settings, two examples, five result cards, unsupported blocking and cleared results |
| Original project preservation | Original sibling clean at `46eaeb6abc72d10dafa895880a59945869610933`; all 18 tracked hashes match baseline |
| Assignment source | Exact byte/hash match to original |

The new AI-UI success-path regression injects an explicitly offline test client, exercises Interpret -> review -> Recommend -> edited rerank, and verifies exactly one interpretation call and request-change clearing. It complements provider-failure and non-AI tests; it does not represent a live Gemini result. Final runtime server was stopped after checks. No provider generation occurred.

The README's three normal assistant examples and separate unsupported example are actual captured CLI fixture executions from `evaluation/pass23/cli_runs.json`; they remain reproducible and honestly labeled. A real live-output requirement remains open rather than being filled with fabricated samples. Fixed-catalog sensitivity and an exclusion-guard ablation in `evaluation/pass1/` isolate deterministic behavior changes; listener quality and model superiority are not inferred from them.

## Code review findings and resolutions

The engineering code-review skill was applied to the final change and relevant surrounding modules. No unresolved critical/high defect was found in this scoped review; it is not an exhaustive security assurance.

| Review area | Evidence and judgment |
| --- | --- |
| Correctness | Strict finite typed values, catalog-backed identities, genre ancestry, hard filtering before scoring, stable ties, genuine no-result/clarification states. Current success/error/review/state transitions tested. Live semantic correctness remains unmeasured. |
| Security | Fixed provider endpoint; key in header and excluded from repr; safe error categories; no model code/tools or pickle loading; source URL validation; ignored secrets; no private request text in app logs. Publication pattern scan covers candidates and inherited blobs, with limitations stated in its report. |
| Performance | Cached 1,200-track catalog; local filtering/scoring; bounded request/output sizes and timeout; one generation call, no automatic retries. No large-scale performance claim. |
| Maintainability | Shared browser/CLI backend, separate schema/provider/ranker, immutable validated preferences, explicit fixture provenance and repeatable evidence. Current diagram and instructions match implementation. |

Resolved during this pass: explicit JSON depth validation now works independently of interpreter recursion, with array/object boundaries and quoted-string coverage; obsolete fallback names now refer to Explore without AI; the bonus table's blank row was removed so it renders as one table; successful AI review coverage was restored after the mode consolidation. The requested copy was verified in the actual running app. Useful existing design choices retained include original model preferences before guardrail corrections, factual score explanations, and explicit human review.

## Full handoff and Appendix A coverage

| Additional obligation | Verification / status |
| --- | --- |
| Original project choice and context | Module 3 named accurately; archived original docs, unchanged source/data/tests and captured baseline. No unrelated project touched. |
| Dedicated public final repository and history | Verified public `alexreifel/ai110-applied-ai-system-project`, owner/push permission and authenticated account. Both initial final-repo and base histories preserved with merge `5901fa0`; no force push/rewrite. |
| Safe publication | Sole origin fetch/push URL is the dedicated final repo, main tracks origin/main, no extra push mappings/default/branch overrides. Candidate paths/diff and staged content reviewed; credential files ignored, reachable history scanned. Publication uses explicit regular push to main. Actual remote verification follows the final commit. |
| Supported local environment | Project .venv Python 3.11.18; pinned requirements/constraints; separate clean installation verified. No shared dependency changes. |
| Architecture assets | `assets/README.md`, actual `diagrams/architecture.mmd`, README source link. Flow includes request, prompt/client, validation, review, unified explore, fixture CLI, catalog/ranking, errors and evaluator. No PNG substituted. |
| Real variety/provenance | 1,200 FMA tracks, 775 artists, 113 labels; exact archive checksums and deterministic cleaning/rebuild in data docs/report. Historical, uneven coverage and estimated features disclosed; no audio downloaded. |
| Bounded reliable implementation | Input/schema/vocabulary/contradiction checks; unsupported conditions; no invented scores/tracks; safe provider categories; no retries or hidden chain-of-thought. Tests and controlled guards have observed effects. |
| Reproducible human entry points | Browser actual runtime plus AppTest; shared CLI and three fenced observed examples; missing live interpretation explicitly disclosed. |
| Required README | Goals, original scope, architecture, setup/prerequisites/config, modes, commands/results, design tradeoffs, reliability, limitations/reflection. Three actual live AI outputs remain missing. |
| Required model card | All four Appendix A ethics/reflection questions and all three rubric reflection statements answered under labeled sections. Limitations/bias, misuse/mitigation, testing observations, collaboration, accepted and rejected/revised suggestions, future work and comparison status included. |
| Honest personal reflection | Alex's actual variety/discovery feedback quoted verbatim. Agent-selected implementation details attributed to Codex. No scored listening study, personal authorship claim or live success invented. |
| Presentation preparation | Six-minute outline covers problem, old/new, architecture, demo, reliability, limitations and actual reflection. Prepared, not delivered. |
| Portfolio preparation | Verified repository link, short summary and grounded personal paragraph in `docs/portfolio_draft.md`; requires Alex's wording review, not published elsewhere. |
| Parseable evidence | Committed text/JSON outputs plus README/model-card tables and blocks. No screenshot or video replaces execution evidence. |
| Selected extras only | Evaluation harness and specialization comparison; no unrelated RAG/agent or app expansion. |
| Multiple meaningful commits | Three planned commits: foundation; assistant/reliability; final merged interface/audit/evidence. One additional necessary CI correction preserves published history and fixes the observed Python 3.12 failure. Setup merge is additional; no empty commits. Actual hashes reported at delivery. |
| Retained CI | Offline workflow includes inherited baseline checks, full tests, syntax, evaluator and app type checking on Python 3.11/3.12. No API key. Local checks do not establish remote success. |
| Deadline, delivery and submission | Course pages inaccessible; prior deadline/Demo Day timing remains unverified. No on-time submission claim, CodePath submission, video upload, outside portfolio publication or external message. |
| Compaction/source discipline | Complete source retained word-for-word; current handoff preserves decisions, blockers and obligations with a hash and source link. |

## Publication and actual CI verification

Repository: [alexreifel/ai110-applied-ai-system-project](https://github.com/alexreifel/ai110-applied-ai-system-project). The final commit is published only after staged/history scanning and destination review. [Actual Actions runs](https://github.com/alexreifel/ai110-applied-ai-system-project/actions/workflows/ci.yml) provide the remote result. The first observed [remote run](https://github.com/alexreifel/ai110-applied-ai-system-project/actions/runs/43653019071) passed all Python 3.11 steps but failed one Python 3.12 test (170 passed). Python 3.12 parsed 1,500 nested arrays without the recursion error used by the earlier guard. The correction enforces a version-independent maximum of 32 container levels and adds boundary/quoted-string tests; local suites now pass 174 tests. See evaluation/final/ci_followup.json. A fourth necessary commit carries this actual CI correction without rewriting the three published implementation commits. The delivery report supplies the latest observed rerun URL/status and exact pushed commit; this document does not predeclare that rerun successful.

## Remaining actions and review order

1. Alex confirms a usable locally configured Gemini key and approved access/billing scope. An .env appearing is not confirmation; no secret should be pasted into chat.
2. Run the implemented bounded comparison (12 cases, two arms, at most 24 calls; stop on access/quota/network failure), inspect original model interpretation and downstream checks separately, and fix actual failures. Capture three successful live cases from that run to avoid extra calls.
3. Replace missing live evidence with actual model/settings/outputs, report ties/regressions as well as improvements, and re-audit the seven partial core rows and specialization category. Do not assume a specialized prompt beats the baseline.
4. Alex reviews the app, personal portfolio wording and six-minute outline before any course submission/presentation. Required presentation delivery remains a human action.

Review the [README](../README.md) first, run `python -m streamlit run app.py` and use Explore without AI, then inspect the [model card](../model_card.md) and exact checklist. All independent local work is complete; the specific live prerequisites above remain open.

## Subsequent key-compatibility correction

Alex configured a key, then reported a local format error. Safe metadata-only inspection found no whitespace; the app's regular expression incorrectly excluded periods used by Google AI Studio authorization keys. The correction accepts periods while retaining length/character, whitespace/control protections and secret-safe errors. Offline regression coverage checks both standard and dotted keys through .env precedence and header construction. Latest verification:176tests in both local environments, mypy success and offline harness12/12; evidence evaluation/key_compatibility/. The configured local key now passes formatting, without revealing its value or making an API/model call. This does not resolve the separate live access/billing confirmation or specialization-evidence gap.
