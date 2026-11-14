"""Run manual real-track recommendations; AI interpretation arrives in Pass 2."""

import argparse
import json
import logging
from pathlib import Path
import sys

from .catalog import CATALOG_PATH, load_catalog, read_json
from .preferences import Preferences
from .ranking import recommend


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--preferences", type=Path, help="JSON preferences file")
    group.add_argument("--preferences-json", help="JSON preferences object")
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
        if args.preferences is None and args.preferences_json is None:
            raise ValueError("Provide --preferences FILE or --preferences-json OBJECT; language input is planned for Pass 2")
        if args.preferences is not None and args.preferences.stat().st_size > 64000:
            raise ValueError("Preferences file must be at most 64,000 bytes")
        raw = args.preferences.read_text(encoding="utf-8") if args.preferences is not None else args.preferences_json
        if len(raw.encode("utf-8")) > 64000:
            raise ValueError("Preferences must be at most 64,000 bytes")
        preferences = Preferences.from_dict(read_json(raw))
        result = recommend(catalog, preferences, args.limit)
        if args.json:
            print(json.dumps({"mode": "manual", "preferences": preferences.to_dict(), **result.to_dict()}, indent=2, allow_nan=False))
        else:
            print("Mode: manual (no LLM calls)")
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
    except (OSError, ValueError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
