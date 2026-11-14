# Durable session handoff

Updated November 14, 2026 (America/New_York). **Pass 1: Recommender Foundation is complete.** Alex's latest request authorized the full Pass 1 only. Stop at this checkpoint; Passes 2–4 remain pending.

## Resume after compaction

1. Read `source/AI110_Final_Project_Codex_Prompt.md` in full, including both appendices. It remains the verbatim original, not a reconstructed summary.
2. Read this file, `pass1_report.md`, `requirements_checklist.md`, `execution_passes.md`, and the current README/model card.
3. Apply later user instructions over historical source statements. Project selection is complete; Alex also authorized the two selected bonuses. Do not ask to choose the base again or restart completed work.
4. Recheck actual Git state before mutations/commits/pushes. Never assume this recorded checkpoint is the latest working tree.
5. Keep Complete / Partial / Blocked / Requires Alex review statuses tied to real evidence. Re-read the full original at the final audit. Do not invent a grade, execution logs, live success, human evaluation, or personal experiences.

## Requirements and actual user decisions

- Original source: `/Users/alexreifel/Downloads/AI110_Final_Project_Codex_Prompt.md`.
- Preserved source: `docs/source/AI110_Final_Project_Codex_Prompt.md`; 36,532 bytes; SHA-256 `80499cf3ac233cf418596f1fa07d7531a9a35f7428439a8afc0fa57ecccbe0a0`.
- Checklist retains all 21 exact required rubric rows plus all four criterion statements in the two selected bonus categories.
- Alex selected Module 3 Music Recommender Simulation, revised the tiny fictional-catalog proposal to require real variety and richer preferences, accepted independent tracks with reliable metadata, and chose a local browser app plus CLI evidence.
- Alex rejected repeated LLM binary-search coaching because a deterministic algorithm suffices after one explanation. That is a real rejected AI suggestion. Alex's catalog revision is a real revised suggestion. Preserve this authorship record in the model card.
- Alex subsequently requested bonuses. Target evaluation harness (+2) and actual specialized-model comparison (+2); all 21 required points plus up to 4 bonus points is a target, not an awarded/guaranteed score. No RAG/agent bonus work is needed.
- Alex's current task is **full Pass 1**. The earlier general plan to continue across passes does not override that narrowed current request.

## Actual paths and repository history

- Actual course folder: `/Users/alexreifel/Coding Programs/CodePath AI 110`.
- The initially supplied `/Users/alexreifel/CodePath AI 110` path does not exist. Always pass the actual working directory explicitly. Available permission roots may still name the nonexistent path; necessary actual-project writes have succeeded through the escalation/auto-review mechanism. No approval rejection occurred.
- Final project: `/Users/alexreifel/Coding Programs/CodePath AI 110/ai110-applied-ai-system-project`.
- Dedicated origin: `https://github.com/alexreifel/ai110-applied-ai-system-project`. GitHub connector verified owner/login alexreifel, public visibility, and push permission during Pass 1. No other remote is retained.
- Base project: sibling `ai110-module3show-musicrecommendersimulation-starter`, original clean main at `46eaeb6abc72d10dafa895880a59945869610933`.
- History-preserving merge: `5901fa0321bbcac60f5b496e7f7c19b55dd24fe8`. Both original final initial commit `97724ce` and base head `46eaeb6` are ancestors. Used a local-path fetch, not a push-capable upstream. Resolved only the README add/add conflict using the base README at setup, then updated final docs separately. No history rewrite/reset/force push.
- Pass 1 feature checkpoint uses commit subject `Build audited real-track recommender foundation`; obtain its hash from `git log` after the commit. Setup merge is additional to coherent feature commits; adjust later grouping honestly rather than manufacture or rewrite commits.
- Original source repository remains clean and unchanged: all 18 original tracked-file hashes match the manifest. Its original source modules, synthetic CSV, and tests are also byte-identical in the final repo. See `evaluation/pass1/preservation_check.json`.
- No applicable AGENTS.md was found in checked ancestors/selected/base locations. Recheck if new instructions appear. Do not touch unrelated repositories, including BugHound remotes.

## Pass 1 delivered code and data

- `src/catalog.py`: immutable real-track records, strict JSON, validated identity/source/features, represented vocabulary, local snapshot loading.
- `src/preferences.py`: manual/future-model contract with `preferred_genres`, `required_genres`, `excluded_genres`, optional numeric `targets`, inclusive hard `bounds`, and `unsupported` conditions. Genre lists mean alternatives, not all-at-once requirements. Unknown fields/genres, invalid values, duplicate keys, contradictory conditions, and oversized inputs are rejected.
- `src/ranking.py`: hard-filter first, then weighted mean over requested soft preferences only. Genre weight 2, numeric weight 1; tempo gap scale 100 BPM. Threshold 0.6; compromise indicator below 0.75 per feature; these are explicit uncalibrated heuristics. Required-only results are unscored; ties use source ID. Missing requested evidence excludes a track. Never relax conditions to fill results.
- `src/cli.py`: manual entry point, text/JSON output, supported-genre listing, safe aggregate logs. Exit 0 results; 2 invalid input/file/configuration; 3 no-results/clarification. No LLM calls. Examples in `examples/`.
- `scripts/prepare_catalog.py`: checksum-verified metadata ZIP reader (CSV only; never deserialize pickle), deterministic artist-capped round-robin selection, audit/provenance and exact rebuild. Audio is not downloaded.
- FMA metadata rc1 source ZIP is temporarily at `/private/tmp/ai110-fma-metadata.zip` (342 MiB). Published SHA-1 verified: `f0df49ffe5f2a6008d7dc83c6915b31835dfe733`. Actual SHA-256: `d9527a5297a65da31c5676484d5047c3e2b8a8060ce72a46e26158be736bf265`. Rebuild instructions/attribution in `data/README.md`.
- 106,574 source metadata tracks; 13,129 feature records; 13,128 usable candidates. Track 26620 rejected for missing title.
- Snapshot: **1,200 real tracks, 775 artists, 113 represented genre labels**. Six numeric estimates present for all selected tracks. All 16 broad genres represented; 15 have at least 20 tracks, spoken is sparse at 7. Genre counts overlap.
- Selected source IDs, exact checksums, feature ranges/coverage, cleaning, and limitations in `data/catalog_report.json`. Titles/artists have HTML entities decoded and whitespace collapsed; genres casefolded with source-derived ancestry; tempo renamed; HTTP FMA references upgraded to HTTPS. No track identity, feature, or genre is invented by an LLM.
- Catalog/report/hierarchy rebuild byte-for-byte identically. Original 20-song synthetic catalog is retained as `data/songs.csv`.

## Verified tests, evidence, and environment

- Project-local `.venv`: Python **3.11.18**, pytest **8.4.2**, Streamlit **1.67.0**. `requirements.txt` pins direct dependencies; `requirements-lock.txt` supplies exact transitive constraints. Install with `python -m pip install -r requirements.txt -c requirements-lock.txt`.
- Original baseline before changes: **52 passed**, no pre-existing failures; original demo/evaluation match committed reports. Captured in `evaluation/baseline/` with original tracked-file hashes.
- After Pass 1: **127 passed** (52 inherited + 75 new behavior checks), also **127 passed in a freshly installed temporary environment**. `pip check`, syntax compilation, baseline output comparisons all pass. Evidence in `evaluation/pass1/`.
- Three captured successful manual examples: acoustic_folk, evening_jazz, dance_pop. Separate unsupported_lyrics and no_results examples exit 3 intentionally. They are **manual, model none**, not live AI.
- Real controlled exclusion ablation: fixed catalog and energy target; guard on returns 0 excluded rock tracks, bypass returns 3. JSON contains exact IDs/preferences and matching catalog hash. Unit test also proves the effect with controlled fixtures.
- Same-catalog sensitivity: changing only acousticness target (fixed folk condition and energy target) changes all top-three IDs. `manual_sensitivity.json` records actual attributes/scores. This is not a listener-quality or LLM-specialization comparison.
- Three top demo source references returned HTTP 200 in HEAD checks; playback/content identity and all other URLs remain unverified. `source_reference_checks.json` records exactly what was checked.
- Inherited offline CI retained, dependency constraints added, syntax check expanded to scripts. **No Pass 1 push or new Actions run** has occurred. Publication is scheduled for Pass 4.

## Documentation and skills

- Root README describes current/future behavior accurately and includes setup, design, three actual manual examples, error/guardrail table, test results, provenance/limitations, and links.
- `model_card.md` answers current technical/ethical/collaboration sections, with honest pending live-specialization and Alex personal-reflection markers. Original docs archived verbatim under `docs/baseline/`; root uppercase checklist points to final checklist.
- `diagrams/architecture.mmd` matches implemented Pass 1; add actual LLM/browser/human-review components in Pass 2. `assets/README.md` retains the required directory.
- Read engineering:system-design and developing-with-streamlit skills during planning. Project environment discovery now succeeds: `.venv/lib/python3.11/site-packages/streamlit/.agents/skills/developing-with-streamlit/SKILL.md`. Read task-specific version-matched references before UI implementation, especially state, forms, layout, testing, and environment. No UI was built in Pass 1.
- Current Streamlit skill says to verify edited UI in the running app and type-check edited UI code; agent API can drive local tests. It also asks before starting a user-facing app or actions with external side effects. Apply actual user authorization and developer instructions, and do not invent a new approval gate. Live paid API access still requires approved cost scope.

## Remaining access and review constraints

- A `GOOGLE_API_KEY` variable NAME was previously observed; no secret value printed. Usable key, provider/model access, quotas, billing/free use remain unverified. **No live model calls made.** Never enable billing or incur unapproved charges. Never commit `.env`/secrets; ignore rules are present. Use placeholder configuration in Pass 2.
- Official course pages were inaccessible. Prior deadline November 16, 2026, 2:59 a.m. New York and Demo Day November 18, 8 p.m. New York remain unverified. No submission/timeliness claim.
- Do not fabricate Alex's testing surprise, listening satisfaction, human evaluations, or personal experiences. Actual accepted/rejected/revised suggestions are grounded in chat; Alex reviews personal reflection after trying the app.
- Final presentation outline and portfolio draft are not yet written; do not claim a presentation delivered or portfolio published.

## Next passes and final obligations

Pass 2: integrate one specialized structured-preference interpreter/provider with bounded errors, honest unsupported conditions, a browser review/edit flow, and the shared assistant CLI. Reuse the existing schema/ranker and preserve manual fallback. Verify live access/cost early without changing billing; finish independent work if access is unavailable.

Pass 3: add the explicitly requested runnable evaluation harness with per-case/aggregate summaries. Demonstrate specialization through actual generic-vs-specialized prompt outputs using the same model/settings/schema/vocabulary/requests; fixtures cannot establish live-model behavior. Capture at least three actual live end-to-end examples plus separate guardrail/errors when access permits. Document differences/regressions/ties honestly in model_card.md.

Pass 4: re-read the entire source and check all 21 required rows, four selected bonus criterion statements, and every additional instruction against the finished app/evidence. Fix gaps, verify clean setup and entry points, finish README/model card/architecture/presentation/portfolio/checklist/final audit, and mark personal-review/live gaps accurately.

Before any push: inspect actual Git authentication, owner, all fetch/push URLs/mappings/tracking, remote.pushDefault, branch-specific push remotes, staged content and inherited history for secrets/unrelated material. Push only to the dedicated public final repository; never change an existing private repository's visibility. Inspect real CI run and report its URL/status. Do not change account-wide security settings.

Do not submit to CodePath, message anyone, record/upload a video, or publish elsewhere. Final implementation report includes absolute local path, verified repo URL, actual commit hashes/purposes, exact commands/results, CI URL/status, rubric/bonus evidence assessment, and outstanding live/personal-review items. No official grade is assigned.
