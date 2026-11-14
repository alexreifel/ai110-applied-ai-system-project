# Four implementation passes and final acceptance audit

Updated November 14, 2026, America/New_York. This is an execution plan, not a claim that implementation or evaluation has run.

## Target and scope

Target all **21 required points**, plus two selected bonus categories worth **up to 4 additional points**: Test Harness or Evaluation Script and Fine-Tuning or Specialization Behavior. Alex explicitly requested bonuses after approving the core plan. This supersedes the original handoff's restriction on unsolicited bonus work for these selected categories. Course credit depends on the grader; do not assign an official grade.

The complete source remains unchanged at `source/AI110_Final_Project_Codex_Prompt.md`. Read it with the implementation plan, session handoff, and requirements checklist. Every one of its non-rubric requirements still applies. No agent or RAG component is necessary for the selected design or bonuses. Specialization uses structured prompting and examples, not training model weights.

Each pass is a coherent implementation batch with working behavior, relevant tests, and a recorded checkpoint. It is not a separate permission gate or a requirement for another user message. Once implementation is underway, continue through authorized passes, incorporating Alex's feedback. Pause only for an actual missing decision, unavailable access that blocks dependent work, or an action beyond authorization. Complete independent work when live access is unavailable.

## Pass 1 — establish the base and build the expanded recommender

**Outcome:** a tested recommender over varied real tracks that works without an LLM.

1. Recheck actual paths, applicable instructions, source and target Git state, authentication, and repository identity. Preserve the base submission. Import its history into the final repository while retaining the existing README-only history; never reset or force push.
2. Create a project-local Python 3.11 environment and install compatible dependencies. Rerun Streamlit skill discovery against that environment and read its version-matched documentation. Run inherited tests and the original CLI/evaluation before modifying behavior. Record actual baseline output and pre-existing failures.
3. Download and audit source metadata. FMA is the first candidate; the final catalog size and coverage depend on actual usable records. Produce a compact versioned snapshot, deterministic preparation recipe, source/checksum/attribution, and coverage/cleaning report. Retain the original synthetic catalog as the baseline.
4. Implement validated catalog records, multiple genre preferences, explicit exclusions, optional numeric preferences, hard conditions, and soft scoring. Unspecified preferences remain unset. Use metadata actually present rather than inventing song attributes.
5. Build a manual-preference CLI path through the new ranker. Show factual explanations, compromises, and explicit no-result behavior. Test meaningful ranking differences, exclusion enforcement, numeric bounds, unknown/missing metadata, and deterministic ordering.

**Exit checks:** inherited behavior is reproducible; actual catalog variety is documented; several different manual preferences produce sensible, traceable results; a prohibited candidate cannot enter the results; original files and history are preserved. If dataset coverage is inadequate, fix that before building an assistant on top.

## Pass 2 — integrate the assistant, browser app, and shared CLI

**Outcome:** a user can describe music, review/edit the interpretation, and obtain real catalog recommendations.

1. Implement a typed preference schema and one provider adapter with configured model, bounded request size, timeout, and explicit error categories. Verify current access/model/cost constraints before live calls; never print secrets or enable billing. No automatic retry by default.
2. Add the specialized prompt with a compact supported vocabulary and examples illustrating mixed genres, exclusions, numeric characteristics, unsupported conditions, and ambiguity. The provider returns preferences, not invented song facts or arbitrary actions.
3. Connect interpretation -> validation -> human review/edit -> filtering -> ranking -> output through shared Python services. Expose unverified assumptions and unsupported conditions. A required unsupported condition must be resolved or explicitly revised by the user.
4. Implement the local Streamlit app with explicit Interpret and Recommend actions. Use state correctly: rerendering does not repeat network calls, and changing request/interpretation cannot leave stale recommendations presented as current. Editing preferences reranks locally. Include manual mode.
5. Connect the terminal assistant entry point to exactly the same service. Allow explicit noninteractive confirmation for reproducible demonstrations. Clearly label live, manual, and fixture modes.
6. Test the actual CLI and critical browser workflow in addition to backend behavior. Verify missing configuration, quota/auth failure, timeout, malformed output, invalid preference, unsupported request, and legitimate no-results behavior.

**Exit checks:** browser and CLI both exercise the full workflow; the LLM interpretation affects recommendations meaningfully; manual mode works without credentials; provider failures do not become fabricated successful results. Capture initial live examples if usable authorized access is available. A live-access blocker is reported precisely, not disguised by mocks.

## Pass 3 — evaluate, demonstrate the bonuses, and prepare evidence

**Outcome:** reproducible measurements and execution evidence establish the app's behavior and both selected bonus claims.

### Evaluation harness (+2 target)

Implement `src/evaluate_assistant.py` with committed predefined cases and explicit modes. Planned commands are illustrative until implemented and verified:

```bash
python -m src.evaluate_assistant --mode offline
python -m src.evaluate_assistant --mode live
python -m src.evaluate_assistant --mode live --compare-prompts
```

Use roughly 12 representative cases covering varied genres/attributes, multiple acceptable genres, exclusions, missing metadata/coverage, contradictory requirements, unsupported lyric guarantees, blank input, and attempts to override the intended response contract. Add provider and malformed-output fixtures for failure paths. Final case count is recorded from actual runs.

For each case, print the relevant expected condition, observed behavior, pass/fail, and aggregate totals. Save structured JSON results and mode/model/settings/catalog/prompt identifiers. Use meaningful invariant checks: appropriate interpretation, required-condition preservation, result catalog membership, exclusion satisfaction, and honest handling of unsupported conditions. A successful schema check alone is insufficient.

Offline fixtures test orchestration, ranking, and rejection behavior reproducibly; label their interpretation as mocked. Live cases test actual interpretation when access permits. A skipped live run is a reported gap, not a pass. Return a failure status when checks fail, so CI can catch regressions. Separate evaluation output from inherited `src/evaluate.py` baseline experiments.

### Demonstrated specialization (+2 target)

Compare a minimal generic preference-extraction prompt with the specialized prompt on the same semantically challenging requests. Keep model, response schema, available vocabulary, generation settings, token budget, and catalog snapshot constant. Vary task-specific instructions/examples only. This comparison isolates prompt specialization; it must not compare different catalogs or ranking algorithms.

Measure schema validity, genre/exclusion handling, supported attribute extraction, unsupported-condition handling, and downstream constraint satisfaction, using cases with predefined expected behavior. Show representative baseline and specialized outputs and aggregate results in `model_card.md`. Record actual observed differences, including regressions or ties. Do not assert improvement in advance, cherry-pick favorable outputs, equate scores with confidence, or claim fine-tuning. Report uncertainty from a small case set and possible variation between calls.

Only actual model runs substantiate the live specialization comparison. Fixtures can test that the comparison machinery works, but do not prove model behavior. If the observed comparison does not substantiate the bonus, revise the prompt using documented development cases and verify again on separate cases when access permits, or report the remaining gap. Avoid unapproved charges.

### Required evidence and documentation preparation

- Capture at least three distinct successful end-to-end inputs/outputs through the actual entry point, plus separate guardrail and error examples. Record exact commands, mode, model, and observed output.
- Compare original system, expanded manual recommender, and AI-assisted system while isolating the effect being evaluated.
- Demonstrate a guardrail rejects a high-scoring but excluded candidate; show a controlled failure without the guardrail where feasible.
- Run inherited and substantive new tests, browser/CLI checks, and a clean setup. Retain/update offline GitHub Actions without API secrets; include the offline harness.
- Draft the README, actual architecture Mermaid, model card, presentation outline, portfolio text, source attribution, and evidence tables from observed results. Preserve truthful authorship and mark personal reflection for Alex's review.

**Exit checks:** the evaluation command runs and prints a real summary; both exact bonus criteria per category have direct evidence or an explicitly recorded gap; README examples are captured rather than invented; ordinary CI requires no live credentials.

## Pass 4 — audit the finished app, fix gaps, and verify publication

**Outcome:** an evidence-backed final project ready for Alex's review and course submission.

1. Re-read the complete original handoff and both appendices. Inspect the finished code, browser flow, CLI, tests, actual logs, and documentation. Check all 21 required rows individually, all four criterion statements in the two selected bonus categories, and every additional source instruction. A plan, placeholder, or test count alone is not proof of completion.
2. Create `docs/final_audit.md` with criterion, concrete file/location, actual observed evidence, status, and any corrective action. Cross-check `docs/requirements_checklist.md`. Use Complete / Partial / Blocked / Requires Alex review; do not assign an official grade.
3. Fix implementation or documentation gaps. Verify affected behavior after fixes. Confirm the Mermaid matches actual code, README setup works, three examples include actual output, source attribution exists, and all ethics/reflection questions are answered in `model_card.md`.
4. Give Alex a short browser review checklist and request only personal reflection/judgment not grounded in the actual session. Do not invent testing surprise, listening satisfaction, human evaluations, or presentation delivery.
5. Verify clean-install instructions, tests, harness, and browser/CLI entry points. Summarize actual results; do not repeat expensive checks without a change or unresolved concern.
6. Make the planned meaningful commits, inspect staged material and inherited history for secrets/unrelated content, and verify all fetch/push/tracking destinations. Push only to the dedicated public final repository. Inspect the real GitHub Actions run, address failures within scope, and record its URL/status. Never force push, change unrelated remotes/settings, or submit the course assignment.
7. Update the final audit with publication and CI evidence. Report local path, repository URL, commit hashes/purposes, exact commands/results, core and bonus evidence coverage, and remaining live-access or Alex-review items. Keep presentation preparation distinct from actual delivery.

**Completion standard:** no required row is marked Complete without corresponding evidence. The selected bonuses are claimed only to the extent actual results support their exact criteria. Any external-access or personal-review gap remains visible. Alex receives a runnable app and a traceable final review package.

## Commit grouping and pass boundaries

Aim for three coherent feature commits on top of the imported history: (1) data/recommender/assistant/UI; (2) reliability/evaluation/CI; (3) final documentation/evidence/audit. An additional nonempty history-merge/setup commit may be needed to preserve the target's existing initial commit. Pass checkpoints can be working-tree artifacts; do not manufacture empty commits or rewrite history to force a count.

## First implementation actions

Recheck Git and instructions, create the project environment, run the original baseline, integrate history safely, and audit actual source metadata. Resolve dataset/access issues early so the browser app and evidence use real supported capabilities.

## Current checkpoint

Pass 1 is complete: see [pass1_report.md](pass1_report.md), the recorded 127-test result, and the catalog report. Alex requested the full Pass 1 only in the latest turn; stop at that checkpoint and leave Passes 2–4 pending. The initial general continuation language above does not expand that later scope. No browser app, LLM calls, bonus harness/comparison, push, or course submission has occurred.
