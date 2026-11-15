# Durable session handoff

Updated November 14, 2026 (America/New_York). **Submission recheck complete offline: 176 tests pass in both environments, harness 12/12, browser 14 states and exact catalog rebuild pass. Alex explicitly chose offline-only; live examples/comparison remain blocked. See docs/final_audit.md and evaluation/submission_check/.**

## Resume after compaction

1. Read `source/AI110_Final_Project_Codex_Prompt.md` in full, including both appendices. It is the word-for-word source, not a reconstructed summary. Later user instructions take precedence over its historical unselected-project/no-bonus wording.
2. Read this file, `pass23_report.md`, `requirements_checklist.md`, current README/model card, and `execution_passes.md`.
3. Do not repeat completed foundation/app/harness work. Recheck Git and actual files before changes. Never invent logs, live success, grades, human evaluation, or Alex personal experiences.
4. Latest user revisions: merge the redundant manual/offline browser modes, shorten the specified UI copy, perform the full final audit, and include Alex’s supplied reflection. The UI now has AI assistant and Explore without AI. The latter offers custom preferences or immediately loaded example settings, all editable, with no mock Interpret action. CLI/evaluation fixture modes remain for honest reproducibility. These UI changes are ready to include with the final audit/documentation commit. Previously, Alex requested combining Pass 2 and Pass 3 consecutively. Those passes' independent app, tests, harness, evidence, presentation/portfolio preparation and docs are done. Pass 4 local source/rubric/code audit and final verification are complete; see docs/final_audit.md and evaluation/final/. Publication and actual CI status are reported at delivery after the final commit.
5. **Live-call restriction:** Alex explicitly said to keep content generation offline until access and billing are confirmed, and will configure a valid key locally and confirm when ready. A new .env file or valid-looking key is NOT permission. Wait for explicit confirmation before generation. No billing changes or unapproved charges.

## Source integrity and confirmed decisions

- Original `/Users/alexreifel/Downloads/AI110_Final_Project_Codex_Prompt.md`; preserved at `docs/source/AI110_Final_Project_Codex_Prompt.md` (36,532 bytes).
- SHA-256 `80499cf3ac233cf418596f1fa07d7531a9a35f7428439a8afc0fa57ecccbe0a0` remains unchanged.
- Checklist retains all 21 exact required rubric rows plus the four exact criterion statements for the selected two bonus categories.
- Alex chose Module 3 Music Recommender Simulation, revised the tiny fictional catalog to real variety/richer preferences, accepted independent tracks with reliable metadata, and chose a local browser app plus CLI.
- Alex rejected repeated LLM binary-search coaching because the algorithm suffices after one explanation. Actual accepted/revised/rejected decisions are recorded in model_card.md and ai_interactions.md; do not attribute agent implementation choices to Alex.
- Alex authorized some bonuses after the original handoff: target evaluation harness (+2) and demonstrated specialization (+2). The harness has observed offline evidence. Specialization has no observed live model behavior/differences yet. Target all 21 plus up to 4, never assign/guarantee a grade. No RAG/agent bonus scope is needed.

## Paths, history, and publication

- Actual course folder `/Users/alexreifel/Coding Programs/CodePath AI 110`. Initially supplied `/Users/alexreifel/CodePath AI 110` does not exist; always pass the actual cwd explicitly.
- Final project `/Users/alexreifel/Coding Programs/CodePath AI 110/ai110-applied-ai-system-project`.
- Actual-project writes have succeeded through escalation/automatic review because permission roots may still name the nonexistent path. No approval rejection occurred. Explain any future actual rejection precisely; do not invent an approval requirement.
- Only retained remote is dedicated origin `https://github.com/alexreifel/ai110-applied-ai-system-project`. GitHub connector reverified alexreifel ownership, public visibility, and push permission during combined passes. At the pre-publication audit, no push had occurred and the remote was README-only. Final delivery reports the subsequently observed push and CI; recheck the remote instead of treating this historical checkpoint as current state.
- Original base is sibling `ai110-module3show-musicrecommendersimulation-starter`, clean main at `46eaeb6abc72d10dafa895880a59945869610933`. All 18 original tracked-file hashes still match and original CLI/evaluation reports remain byte-identical.
- History-preserving setup merge `5901fa0321bbcac60f5b496e7f7c19b55dd24fe8` retains both original final initial commit `97724ce` and base history. Used a local fetch; no upstream remote remains; no reset/rebase/force push.
- Pass 1 feature commit `5fd73684d51e170ff9fdb3d0a43c38a1b7960658` (`Build audited real-track recommender foundation`). Combined feature/evaluation checkpoint uses subject `Integrate music assistant, browser review, and evaluation harness`; actual hash e6da65ce5748e5fac0dd430fef434a6178d2ec95.
- Setup merge is additional to coherent feature commits; adjust final documentation/evidence grouping honestly without empty commits or history rewriting.
- Original source, synthetic CSV and tests remain unchanged. `docs/baseline/` archives original docs; `docs/pass1_README.md` archives the Pass 1 README.
- No applicable AGENTS.md found in checked ancestors/selected/base locations; recheck if new files appear. Do not alter unrelated repositories or BugHound remotes.

## Implemented application

- Project .venv: Python 3.11.18, Streamlit 1.67.0, pytest 8.4.2. Runtime requirements pinned in requirements.txt, optional development mypy 2.4.1 in requirements-dev.txt, exact transitive constraints in requirements-lock.txt. Install development setup with `python -m pip install -r requirements-dev.txt -c requirements-lock.txt`.
- `src/catalog.py`, `src/preferences.py`, `src/ranking.py`: Pass 1 validated catalog, immutable typed preferences, hard-condition filtering, factual scoring/explanations and stable ID ties. Multiple genre labels mean alternatives. Missing requested evidence excludes candidates, never becomes fabricated zero. Hard conditions are never relaxed.
- Numeric targets: energy, tempo_bpm, valence, acousticness, danceability, instrumentalness. Preferred-genre weight 2, requested numeric weight 1; tempo gap scale 100 BPM; soft match threshold .6 and compromise indicator .75 are uncalibrated heuristics, not probabilities. Required-only results are unscored.
- `src/llm_client.py`: standard-library Gemini generateContent adapter. Default configurable `gemini-2.5-flash-lite`; JSON response schema, temperature 0, maxOutputTokens 2048, network timeout configurable 1–45 seconds (default 20), one request, no retries/tools. Key goes only in header, is excluded from repr, and malformed format is rejected before header construction. Safe separate error categories: config/missing credentials/auth/model access/quota/timeout/network/provider/invalid output. Raw error bodies and keys are not displayed/logged. Model thought parts are excluded, no hidden chain-of-thought requested/saved.
- Simple ignored .env config (no shell execution/interpolation). Priority: environment GEMINI_API_KEY, local GEMINI_API_KEY, environment GOOGLE_API_KEY, local GOOGLE_API_KEY. Other matching environment settings override file. .env.example has placeholders only.
- `prompts/specialized.txt`: rules/four examples for alternatives/exclusions, hard bounds, unrequested dimensions, assumptions, unsupported conditions, prompt override. `generic.txt`: minimal extraction baseline. Same vocabulary/schema supplied to both.
- `src/assistant.py`: bounded input, single interpretation call, strict wrapper/preferences/vocabulary checks, visible summary/assumptions, small deterministic evidence-gap rules (lyric guarantees, guaranteed no vocals, medical effects). The model can still misunderstand requests; keyword rules are not exhaustive semantic validation. Original validated model preferences are stored separately BEFORE local corrections for honest evaluation.
- `app.py`: cached source catalog; AI assistant and unified Explore without AI modes; explicit Interpret button only in AI mode; review/edit form with optional target selection and required bounds; unsupported conditions block until user explicitly revises; source-backed cards/explanations. No API calls on initial load, rerenders, or preference edits. New request/mode clears stale review/results. Forms submit edits together; outputs reflect last submitted preferences.
- `src/cli.py`: same backend; manual JSON inputs preserved. `--request`, `--mode live|offline`, `--yes` batch confirmation; --json provenance. Noninteractive requests without --yes fail BEFORE generation. Exit 0 results, 2 invalid/provider/configuration, 3 no-results/clarification. The CLI offline fixture mode accepts exact predefined requests only and is explicitly labeled offline_fixture/model none.
- Browser requests are kept only in session memory, not written to disk. Evaluation intentionally records predefined nonpersonal requests/replies; provider retention is governed by provider terms. Catalog facts are never model-generated.

## Catalog and source

- 1,200 real FMA tracks; 775 artists; 113 represented genre labels. All 16 broad genres represented; 15 have >=20 tracks, spoken only 7. Six numeric estimates present for all selected tracks. Genre counts overlap.
- FMA metadata rc1: 106,574 metadata records, 13,129 feature rows, 13,128 usable candidates; one blank-title track 26620 rejected.
- scripts/prepare_catalog.py verifies the ZIP and reads only CSVs (never pickle); deterministic SHA-256 ordering, round-robin broad genre selection, max 3 per artist, output sorted IDs. Snapshot/report/hierarchy rebuild byte-identically. No audio downloaded or model-imputed data.
- Source ZIP temporarily `/private/tmp/ai110-fma-metadata.zip`; published SHA-1 `f0df49ffe5f2a6008d7dc83c6915b31835dfe733`, actual SHA-256 `d9527a5297a65da31c5676484d5047c3e2b8a8060ce72a46e26158be736bf265`. Attribution/license/rebuild in data/README.md; IDs, feature ranges, transformations/checksums in catalog_report.json.
- Historical independent catalog, not current mainstream coverage. Features are estimates, not verified moods/lyrics/instruments/no vocals or listening satisfaction. Three demo source references returned HTTP 200 in HEAD checks; playback/all URLs not guaranteed.

## Evaluation and observed results

- Before changes: 52 original tests passed, no pre-existing failures, original outputs exact; evidence evaluation/baseline/.
- Pass 1: 127 passed (52 inherited +75 new), fresh environment also passed; exclusion ablation and fixed-catalog acousticness sensitivity in evaluation/pass1/.
- Combined passes: **170 passed** in project and separate clean environments; mypy checks app.py with imported modules followed silently; compileall/pip check pass. Evidence evaluation/pass23/verification.json and stdout files.
- Five AppTest flows cover no initial generation, full fixture review/results/edit without reinterpreting, stale-state clearing, manual fallback, unsupported-condition revision, and safe provider failure (some covered together).
- Actual localhost Streamlit agent runtime checked page load, offline Interpret/Recommend (five real-track cards), request-change clearing and manual recommendations, with no exceptions. The temporary test server was stopped afterward. Runtime evidence is compact actual snapshots, not a human visual/listening review.
- `src/evaluate_assistant.py`: twelve predefined requests in evaluation/cases.json, per-case checks and aggregate summary, JSON output with model/mode/prompt/schema/case/catalog hashes and settings. Offline run **12/12 passed**, labeled fixture plumbing/guardrails only; no measured model quality. Checks compare original model preferences before semantic corrections, then downstream conditions and catalog membership. A controlled omitted-lyric fixture shows guard success but model-semantic failure.
- Comparison mode requires live; offline comparison is refused. Same model/settings/schema/vocabulary/catalog/cases across generic/specialized arms, only instructions/examples change. Default twelve cases × two arms = at most 24 generation calls. Stops on access/quota/network/provider failures. Actual live outputs/differences remain missing.
- Three normal assistant CLI examples plus separate unsupported case captured in evaluation/pass23/cli_runs.json and README. All are offline fixtures/model none. Do not relabel as live.
- CI retains original Python 3.11/3.12 pytest/baseline comparisons, adds offline harness and UI type check, and uses development requirements with constraints. No secrets required. Corresponding commands pass locally; no new remote Actions run claimed.

## Live access: actual blocker and next steps

- Existing key read-only model-list check: HTTP 400 / INVALID_ARGUMENT / API_KEY_INVALID; no secret printed. See evaluation/pass23/access_status.json.
- Alex said: keep model calls offline until access and billing are confirmed; will configure the key locally and confirm when ready. **Zero content-generation requests made.** Neither a new file nor elapsed time is confirmation.
- After explicit confirmation and usable access, run the bounded live comparison, inspect actual outputs/semantics and fix actual failures. Save model identifiers/settings and baseline/specialized differences/ties/regressions in model_card.md. Use specialized records from the first three normal cases as examples to avoid unnecessary extra calls. Do not assume a free quota or enable billing.
- If live remains unavailable, finish independent work and report the precise missing evidence; do not claim complete core/live or specialization-bonus verification.

## Documentation, reflection and skills

- README has actual current setup/run/test commands, original scope, architecture, captured offline examples, guardrails/evaluation, design, limitations and clear live gap. Mermaid describes actual code, assets/ retained.
- model_card.md covers limitations/bias, misuse/mitigation, actual tests/collaboration, accepted/revised/rejected suggestions, future work and comparison status. Alex supplied his actual variety/discovery observation; quoted verbatim in model_card.md. No scored listening evaluation invented.
- docs/presentation_outline.md is a six-minute outline with honest demo modes. docs/portfolio_draft.md has verified public repository link and personal text grounded in actual chat decisions. Neither delivered/published. Writing-style skill was used for the draft; its wording remains for Alex's review.
- Read engineering:system-design, developing-with-streamlit, and Alex writing-style skills. Current Streamlit skill is in .venv/lib/python3.11/site-packages/streamlit/.agents/skills/developing-with-streamlit/; read relevant version-matched references before UI edits. UI changes were type-checked and verified in AppTest and actual runtime. Do not introduce permission gates from inferred skill requirements; honor actual authorization and the explicit no-live-until-confirmed instruction.

## Pass 4 and final obligations

Re-read the complete original handoff and both appendices; explicitly check all 21 required rows, four selected bonus criteria, and all additional instructions against finished code/app/logs/docs. Fix gaps and verify affected behavior. Write docs/final_audit.md and update exact-criterion checklist. Alex supplied the personal reflection; live comparison still cannot be completed by invention. Prepared presentation is not delivered; draft portfolio is not published.

Before pushing, inspect actual Git auth/owner, all fetch/push URLs/mappings/tracking, remote.pushDefault and branch push remotes; scan staged content and inherited history for credentials/unrelated data. Push only dedicated public final repository, never original submission/CodePath; no force push/history rewrite, no visibility change of an existing private repo, no account-wide security changes. Inspect actual CI run and report URL/status after push.

Do not submit to CodePath, message anyone, record/upload a video, or publish elsewhere. Final report includes absolute local path, verified repo URL, actual commits/purposes, exact commands/results, real CI URL/status, rubric/bonus evidence assessment and live/personal-review gaps. Official course pages remain inaccessible: prior Nov 16, 2026 2:59 a.m. New York deadline and Nov 18 8 p.m. Demo Day are unverified; do not claim timeliness or submission. Never assign an official grade.

## UI consolidation verification

Alex requested merging manual preferences and offline demo as redundant. The browser now loads example preferences directly or starts custom controls in one Explore without AI mode. Existing UI tests verify that neither GeminiClient nor FixtureClient is called by that mode; edits rerank, changing examples clears prior results and loads the new settings, unsupported conditions still require explicit revision. All 171 tests pass in project and clean environments, including a restored successful AI review/edit test with an injected offline client. App type check passes. Latest ten-state running-app evidence is evaluation/final/runtime_checks.json, including the exact requested copy; evaluation/ui_merge/ and Pass 2/3 are historical snapshots. Live-call restriction is unchanged.

## Final local audit checkpoint — supersedes historical pending notes above

- Exact requested UI copy installed and verified in actual runtime. Two browser modes remain: AI assistant and Explore without AI. CLI fixture mode remains honest.
- Complete source and both appendices reread; exact21 core/four bonus statements retained. docs/final_audit.md maps each row and full additional obligations. Fourteen complete local rows, seven partial for live evidence (4–6,10–12,18); not predicted points. Harness evidence supports selected +2 category, specialization +2 remains blocked. No official grade or 100% guarantee.
- Final verification: 171 passed in project and separately installed environment; offline harness 12/12; mypy, compileall, pip check passed; original CLI/evaluator byte-identical; all18 base tracked-file hashes unchanged and base clean; source36532bytes and SHA unchanged. Evidence evaluation/final/.
- Added meaningful UI success regression using explicit injected fixture: Interpret -> review -> recommend -> edited rerank, one interpretation call, changed request clears state. No Gemini content calls.
- Final localhost check covered10states: exactcopy, default AI page without generation, custom results, acoustic/jazz example results, unsupported condition blocking, mode clearing. Server stopped.
- Alex's actual feedback is quoted in model_card.md: “I really liked how the recommendations were so diverse, most of the songs it recommended I had never heard before. Some of the perks of upgrading to such a large dataset.” This is qualitative feedback about discovery, not a quantitative listening study. Portfolio wording still for Alex review.
- Review fixed obsolete fallback names, a broken bonus Markdown-table separator, and missing successful AI review test coverage. README/model card/presentation/portfolio updated. No unrelated features added.
- Publication checks reverified authenticated alexreifel, public final repository ownership/push permission, sole correct origin URL, main tracking, no pushDefault/pushRemote/extra mappings. Recognized-secret scan covers candidate files, staged content and every reachable inherited blob; credential paths ignored. Final delivery must report the actual push and real Actions run, never assume local tests mean CI passed.
- Third coherent feature/audit commit follows 5fd7368 foundation and e6da65c assistant/reliability. Obtain exact final hash from git log. Normal explicit push only to origin HEAD:refs/heads/main; no force/rewrite. No original submission/CodePath push.
- Live restriction unchanged: wait for explicit key/access/billing confirmation even if .env exists. Three live examples and measured generic-vs-specialized comparison remain missing. Run at most24 approved small generation calls after confirmation, stop on access/quota/network failure, inspect actual results before claiming complete.
- No course submission, external message, recorded/uploaded video or outside publication. Course timing unverified. Actual remote publication/CI status is supplied in final delivery; do not repeat historical “remote README-only” notes after a successful observed push.

## Actual publication and CI correction — supersedes earlier checkpoint

- Three planned substantive commits were published to the verified final repository: 5fd7368, e6da65c, 2abd669. Published main was verified identical to local HEAD; worktree clean at that checkpoint.
- Real CI run https://github.com/alexreifel/ai110-applied-ai-system-project/actions/runs/43653019071: Python3.11 all steps passed; Python3.12 pytest had1failure/170passes and skipped later steps. Actual logs showed1,500 nested arrays did not raise ValueError.
- Cause: relying on json.loads RecursionError for depth; Python3.12 has different recursion behavior. Fixed src/catalog.py read_json with explicit MAX_JSON_DEPTH32 iterative container traversal; retains duplicate/nonfinite rejection and catches parser recursion. Added array/object boundary and string escaping coverage, descriptive case IDs.
- Final refreshed checks:174passed per local environment, harness 12/12, mypy/compileall/pipcheck and byte-identical original output. evaluation/final/ci_followup.json records actual failure/correction. Final actual rerun still must be inspected/reported at delivery.
- Fourth meaningful commit is necessary for the observed CI fix; do not rewrite already published commits merely to reach the source's preferred2–3 grouping. Final delivery includes this extra fix hash, actual latest CI URL/status and remaining live gap. All live restrictions and no-submission rules remain unchanged.

## Latest key-format fix

Alex configured a key but has not confirmed free-tier/billing scope. Do not infer permission for live calls. Safe format-only inspection found a dotted key with no whitespace, rejected by the old app regex. src/llm_client.py now accepts periods; existing header safety protections remain.176 tests pass in project and clean environments; mypy and offline harness 12/12pass. Evidence evaluation/key_compatibility/. The actual configured key passes local Settings validation with no value printed and zero model calls. No key rewriting/recreation needed for the local-format error; provider authentication remains untested.

## Latest access diagnosis and billing screenshot — not resolved

Alex reported provider rejection after the format fix. Read-only model listing and configured-model GET both returned200 using the project .env key; configured gemini-2.5-flash-lite exists and advertises generateContent. Alex explicitly confirmed seeing Free Tier and authorized ONE tiny generation diagnostic. That single POST, maxOutputTokens32, returned403 PERMISSION_DENIED (no structured reason); see untracked evaluation/access_diagnostic.json. No successful generation, billing change, payment or full evaluation occurred. This supersedes historical zero-attempt statements but does not establish working live access.

The first diagnostic omitted Google's explanatory message, so Codex asked for one additional tiny diagnostic; no approval was received before Alex sent a screenshot of a billing page requiring a one-time payment of at least30USD to activate service, showing Postpay, zero balance/no amount due,100USD payment threshold available. Screenshot alone does not prove that this billing account is linked to the Gemini project or that the project is free-tier ineligible. No further generation requests are authorized or needed until the account/billing path and approved spend are clarified. Do not treat the screenshot or any future payment as permission for24calls.

Official troubleshooting https://aistudio.google.com/docs/troubleshooting#free-tier-unavailable states some projects are ineligible for Free Tier, attaching paid billing does not unlock Free Tier quota, and metadata GET200 does not establish inference eligibility/billing. Cloud Billing payment threshold determines collection timing, not a spending cap. Explain these distinctions without assuming payment is required for every Free Tier account. Preserve unrelated user .vscode/ files untracked and untouched.

## Latest submission recheck — authoritative over historical checkpoints

Alex requested all tests and one final complete rubric/assignment audit, then explicitly answered “Keep live calls off; run everything offline.” No Gemini requests were made during this recheck. Do not infer live permission from the earlier one-test approval, his billing screenshot, a key file, or this submission-readiness request.

Full source and both appendices reread. Archived source remains 36,532 bytes with original SHA-256 80499cf3ac233cf418596f1fa07d7531a9a35f7428439a8afc0fa57ecccbe0a0; Downloads original is no longer present, so do not require that path to run verification. Base 18 files unchanged and original sibling clean.176 tests passed in each environment, offline evaluator12/12, mypy/compileall/pipcheck passed, original demo/evaluator byte-identical. Six actual CLIcases and14 actual local browser states passed, catalog/report/hierarchy rebuilt byte-identically. Temporary server stopped; user's port 8501 server untouched. Evidence evaluation/submission_check/.

Corrected403message to identify HTTP403 and suggest checking project Status, Billing Tier and API key restrictions, with an assertion in the existing safe/no-retry provider test. All176 tests rerun after that correction. No other application behavior changed. Updated stale zero-attempt/old-key statements and current counts/links in README/model card/checklist/portfolio. docs/final_audit.md now maps all 21 exact core criteria, all 4 selected bonus statements, every handoff obligation and the four code-review dimensions.14core rows complete evidence,7partial because live evidence missing; harness +2 supported subject to grading, specialization +2 blocked. No official grade or 100% guarantee.

Latest approved generation history remains one earlier 32-token diagnostic returning403; metadata GETs succeeded then. No successful live AI outputs. Billing linkage/eligibility remains unresolved. Required three live examples, actual live flow verification and generic-vs-specialized measurements remain missing. Final delivery reports the new audit commit/push/realCI status. Prior verified published checkpoint791b1db had CI success on both Python versions. Preserve user-committed .vscode settings; .env untracked. Never submit to CodePath or change billing.
