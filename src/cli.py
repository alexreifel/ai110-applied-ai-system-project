"""Run reviewed manual or AI-assisted real-track recommendations."""

import argparse
import json
import logging
from pathlib import Path
import sys

from .catalog import CATALOG_PATH, load_catalog, read_json
from .preferences import Preferences
from .ranking import recommend
from .assistant import interpret_request
from .llm_client import FixtureClient, GeminiClient, ProviderError


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--preferences", type=Path, help="JSON preferences file")
    group.add_argument("--preferences-json", help="JSON preferences object")
    group.add_argument("--request", help="Natural-language music request")
    parser.add_argument("--mode", choices=["live", "offline"], default="live")
    parser.add_argument("--yes", action="store_true", help="Explicitly accept the displayed interpretation without an interactive prompt")
    parser.add_argument("--list-genres", action="store_true")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)
    try:
        catalog = load_catalog(args.catalog)
        if args.list_genres:
            print("\n".join(sorted(catalog.vocabulary)))
            return 0
        interpretation = None
        if args.request is not None:
            if not args.yes and not sys.stdin.isatty():
                raise ValueError("Noninteractive --request requires --yes; use the browser app for editable review")
            client = FixtureClient() if args.mode == "offline" else GeminiClient()
            interpretation = interpret_request(args.request, catalog, client)
            preferences = interpretation.preferences
            if not args.yes:
                print(json.dumps(interpretation.to_dict(), indent=2), file=sys.stderr)
                if not sys.stdin.isatty():
                    raise ValueError("Review the interpretation, then rerun with --yes to accept it explicitly")
                if input("Use these interpreted preferences? [y/N] ").strip().casefold() != "y":
                    return 3
        elif args.preferences is None and args.preferences_json is None:
            raise ValueError("Provide --request, --preferences FILE, or --preferences-json OBJECT")
        if args.preferences is not None and args.preferences.stat().st_size > 64000:
            raise ValueError("Preferences file must be at most 64,000 bytes")
        if args.request is None:
            raw = args.preferences.read_text(encoding="utf-8") if args.preferences is not None else args.preferences_json
            if len(raw.encode("utf-8")) > 64000:
                raise ValueError("Preferences must be at most 64,000 bytes")
            preferences = Preferences.from_dict(read_json(raw))
        result = recommend(catalog, preferences, args.limit)
        if args.json:
            print(json.dumps({"mode": interpretation.mode if interpretation else "manual",
                              "interpretation": interpretation.to_dict() if interpretation else None,
                              "preferences": preferences.to_dict(), **result.to_dict()}, indent=2, allow_nan=False))
        else:
            print("Mode: " + (interpretation.mode if interpretation else "manual (no LLM calls)"))
            if interpretation:
                print("Interpretation: " + interpretation.summary)
                print("Model: " + (interpretation.model or "none (predefined fixture)"))
                for assumption in interpretation.assumptions:
                    print("Assumption: " + assumption)
            print("Preferences: " + json.dumps(preferences.to_dict(), sort_keys=True))
            print(f"Catalog: {result.catalog_count}; eligible: {result.eligible_count}; returned: {len(result.recommendations)}")
            print(result.message)
            for index, item in enumerate(result.recommendations, 1):
                score = f"{item.score:.3f}" if item.score is not None else "not scored"
                print(f"{index}. {item.track.title} — {item.track.artist} | Match: {score} | FMA {item.track.id}")
                print("   Genres: " + ", ".join(item.track.direct_genres))
                for reason in item.explanations:
                    print("   " + reason)
                for compromise in item.compromises:
                    print("   Compromise: " + compromise)
                print("   Source: " + item.track.source_url)
        return 0 if result.status == "ok" else 3
    except ProviderError as exc:
        print(f"Error [{exc.kind}]: {exc}", file=sys.stderr)
        return 2
    except (OSError, ValueError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
