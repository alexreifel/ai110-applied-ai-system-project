# Pass 1 completion report — Recommender Foundation

Completed November 14, 2026 (America/New_York). This checkpoint covers Pass 1 only. Browser UI, LLM interpretation, bonus evaluation, final audit, and publication remain for later passes.

## Delivered and verified

| Pass 1 requirement | Observed result | Evidence |
| --- | --- | --- |
| Preserve original submission | Original tracked-file hashes and Git head/status unchanged | `evaluation/baseline/manifest.json`, final preservation check |
| Retain both histories | Merge `5901fa0` has both original final initial commit `97724ce` and base head `46eaeb6` as ancestors | `git log --graph`; no history reset/force push |
| Project environment | Python 3.11.18, pytest 8.4.2, Streamlit 1.67.0; exact constraints recorded | `requirements.txt`, `requirements-lock.txt`, `evaluation/pass1/verification.json` |
| Real baseline before changes | 52 tests passed; original demo/evaluation matched committed reports | `evaluation/baseline/` |
| Audit actual data | 13,129 feature records, 13,128 valid candidates, one blank-title rejection | `data/catalog_report.json` |
| Varied real snapshot | 1,200 tracks, 775 artists, 113 genre labels; 15 broad genres >=20 tracks | `data/catalog.jsonl`, report; spoken remains sparse at 7 |
| Reproducible preparation | Catalog, report, and hierarchy rebuilt byte-for-byte identically | `python -m scripts.prepare_catalog`; `verification.json` |
| Rich manual preferences | Genre alternatives/exclusions, hard bounds, six optional numeric targets | `src/preferences.py`, `src/ranking.py`, examples |
| Source-backed explanations | Per-feature contributions, required-condition evidence, IDs/source URLs | Captured CLI outputs |
| Effective guardrail | Excluding rock returns none; bypassing guard returns 3 prohibited tracks | `evaluation/pass1/guardrail_ablation.json`, unit test |
| Honest unsupported/no-result paths | Lyric guarantee blocked; impossible jazz tempo returns no results, exit 3 | `unsupported_lyrics.txt`, `no_results.txt` |
| Changed attributes matter | Same folk catalog/energy target, changing acousticness changes all top-three IDs | `evaluation/pass1/manual_sensitivity.json` |
| Full regression/behavior suite | 127 passed; all 52 inherited plus 75 new checks | `evaluation/pass1/pytest.txt` |
| Clean setup | Fresh environment installed constrained dependencies; pip check and 127 tests pass | `clean_setup_pytest.txt`, `dependency_check.txt` |
| Baseline compatibility | Original src/main/recommender/evaluate, CSV and original tests unchanged; reports still exact | File hashes and inherited CI comparisons |
| Source references | Top reference from each demo returned HTTP 200 in HEAD checks | `evaluation/pass1/source_reference_checks.json`; playback not verified |

## Run the delivered foundation

```bash
cd "/Users/alexreifel/Coding Programs/CodePath AI 110/ai110-applied-ai-system-project"
source .venv/bin/activate
python -m src.cli --preferences examples/acoustic_folk.json
python -m src.cli --preferences examples/evening_jazz.json
python -m src.cli --preferences examples/dance_pop.json
python -m src.cli --preferences examples/unsupported_lyrics.json
python -m src.cli --preferences examples/no_results.json
python -m pytest -q
```

The last two recommendation examples intentionally exit 3, representing clarification/no-results. They do not crash. Successful examples are manual mode, not live AI.

## Architectural choices

The original interface is preserved for fair baseline comparisons. The richer manual pipeline lives in small independent modules so the future interpreter and browser use the same validation/ranking code. Genre matching follows source ancestors; multiple requested genres mean alternatives. Hard conditions are checked before scoring. Missing requested evidence excludes a candidate. Omitted soft dimensions do not affect the score. No missing attribute is filled with a plausible-looking zero.

Catalog stratification and an artist cap of three improve coverage without claiming representativeness. Match thresholds, feature weights, and tempo distance scaling are explicit heuristics. A sensitivity comparison verifies changed behavior, not objective recommendation quality. HTML entities and whitespace in track/artist labels are normalized, while identity, numeric features, and genre ancestry remain source-backed.

## Remaining boundaries and next pass

No browser app, provider adapter, language interpretation, live model evidence, prompt comparison, or bonus harness has been implemented. The original README/model card/checklist/interaction notes are archived under `docs/baseline`; root documents now describe the final-project checkpoint accurately. The current Mermaid describes actual Pass 1 components and must expand when Pass 2 is implemented.

Source requirements remain verbatim at `docs/source/AI110_Final_Project_Codex_Prompt.md`; the exact 21 core rows and selected +4 bonus target remain tracked in `docs/requirements_checklist.md`. No official grade or full-project completion is claimed. Personal testing reflection, portfolio/presentation preparation, provider access, final audit, and remote CI verification remain outstanding.

The first Pass 2 work should define the specialized interpreter/provider contract using this validated schema, verify usable access/cost without enabling billing, and build the browser review/edit flow plus a shared assistant CLI. Do not replace manual/fixture evidence with a live-success label. The user's current request is Pass 1; do not proceed into Pass 2 in this turn.

## Commit and publication policy

The history-preserving setup merge is `5901fa0321bbcac60f5b496e7f7c19b55dd24fe8`. The coherent Pass 1 feature checkpoint uses commit subject `Build audited real-track recommender foundation`; use `git log -1 --format='%H %s'` to obtain its final hash after commit. Subsequent feature/evaluation/documentation commits should remain coherent; do not manufacture commits or rewrite history to force a count. Publication and checking the real Actions run remain scheduled for Pass 4. No push or CodePath submission was performed in Pass 1.
