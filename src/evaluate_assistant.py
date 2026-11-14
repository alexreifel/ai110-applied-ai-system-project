"""Evaluate predefined requests; offline checks never claim live model quality."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from .assistant import interpret_request, response_schema
from .catalog import CATALOG_PATH, load_catalog
from .llm_client import FixtureClient, GeminiClient, ProviderError
from .preferences import Preferences
from .ranking import recommend, rejection_reason


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evaluation/cases.json"


def check_interpretation(payload, expected):
    """Check the model's preferences BEFORE local semantic corrections."""
    checks = {}
    for key in ("preferred_genres", "required_genres", "excluded_genres"):
        if key in expected:
            checks[key] = set(payload.get(key, [])) == set(expected[key])
    if expected.get("no_genre"):
        checks["no_invented_genre"] = not payload.get("preferred_genres") and not payload.get("required_genres")
    for feature, (low, high) in expected.get("targets", {}).items():
        value = payload.get("targets", {}).get(feature)
        checks["target_"+feature] = isinstance(value, (float, int)) and not isinstance(value, bool) and low <= value <= high
    for feature, interval in expected.get("bounds", {}).items():
        actual = payload.get("bounds", {}).get(feature, {})
        for endpoint, value in interval.items():
            checks[feature+"_"+endpoint] = actual.get(endpoint) == value
    if expected.get("unsupported"):
        checks["unsupported_identified_by_model"] = bool(payload.get("unsupported"))
    return checks


def evaluate_case(case, catalog, client, variant="specialized"):
    record = {"id": case["id"], "request": case["request"], "variant": variant, "mode": client.mode, "model": client.model}
    try:
        interpretation = interpret_request(case["request"], catalog, client, variant)
        result = recommend(catalog, interpretation.preferences)
        semantic = check_interpretation(interpretation.model_preferences, case["expected"])
        checks = {"valid_interpretation": True, **semantic,
                  "results_respect_conditions": all(rejection_reason(item.track, interpretation.preferences) is None for item in result.recommendations),
                  "catalog_membership": all(item.track.id in {t.id for t in catalog.tracks} for item in result.recommendations)}
        if case["expected"].get("results"):
            checks["nonempty_results"] = result.status == "ok" and bool(result.recommendations)
        if case["expected"].get("unsupported"):
            checks["clarification_blocks_results"] = result.status == "needs_clarification" and not result.recommendations
        record.update({"interpretation": interpretation.to_dict(), "result": result.to_dict(),
                       "checks": checks, "passed": all(checks.values())})
    except (ValueError, ProviderError) as exc:
        record.update({"passed": False, "error_category": exc.kind if isinstance(exc, ProviderError) else "input_validation",
                       "error": str(exc), "checks": {"valid_interpretation": False}})
    return record


def run_evaluation(mode="offline", compare=False, case_ids=None, client=None):
    if compare and mode != "live":
        raise ValueError("Prompt comparison requires live model runs; fixtures cannot establish specialization.")
    catalog = load_catalog()
    cases = json.loads(CASES_PATH.read_text())
    if case_ids:
        unknown = set(case_ids) - {case["id"] for case in cases}
        if unknown:
            raise ValueError("Unknown case IDs: " + ", ".join(sorted(unknown)))
        cases = [case for case in cases if case["id"] in case_ids]
    client = client or (FixtureClient() if mode == "offline" else GeminiClient())
    variants = ["generic", "specialized"] if compare else ["specialized"]
    records = []
    for case in cases:
        for variant in variants:
            record = evaluate_case(case, catalog, client, variant)
            records.append(record)
            # Stop on unavailable external access instead of issuing repeated doomed requests.
            if record.get("error_category") in {"missing_credentials", "authentication", "model_access", "quota", "network", "timeout", "provider"}:
                break
        if records[-1].get("error_category") in {"missing_credentials", "authentication", "model_access", "quota", "network", "timeout", "provider"}:
            break
    summary = {variant: {"passed": sum(r["passed"] for r in records if r["variant"] == variant),
                         "total": sum(r["variant"] == variant for r in records)} for variant in variants}
    return {"mode": client.mode, "model": client.model,
            "claim_scope": "offline orchestration/guardrail checks using predefined replies; no measured model behavior" if mode == "offline" else "observed live preference interpretation and downstream conditions; no listener-quality measurement",
            "created_at_utc": datetime.now(timezone.utc).isoformat(), "generation_settings": {"temperature": 0, "maxOutputTokens": 2048},
            "catalog_sha256": hashlib.sha256(CATALOG_PATH.read_bytes()).hexdigest(),
            "cases_sha256": hashlib.sha256(CASES_PATH.read_bytes()).hexdigest(),
            "response_schema_sha256": hashlib.sha256(json.dumps(response_schema(catalog.vocabulary), sort_keys=True).encode()).hexdigest(),
            "planned_cases": len(cases), "summary": summary, "records": records}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["offline", "live"], default="offline")
    parser.add_argument("--compare-prompts", action="store_true")
    parser.add_argument("--case", action="append", dest="case_ids")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = run_evaluation(args.mode, args.compare_prompts, args.case_ids)
    except (ValueError, ProviderError) as exc:
        parser.exit(2, str(exc)+"\n")
    print(f"Mode: {report['mode']}; model: {report['model'] or 'none'}")
    print(report["claim_scope"])
    for record in report["records"]:
        print(f"{'PASS' if record['passed'] else 'FAIL'} {record['variant']} {record['id']}")
    for variant, result in report["summary"].items():
        print(f"{variant}: {result['passed']}/{result['total']} passed")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False)+"\n")
    specialized = report["summary"]["specialized"]
    return 0 if specialized["total"] == report["planned_cases"] and specialized["passed"] == specialized["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
