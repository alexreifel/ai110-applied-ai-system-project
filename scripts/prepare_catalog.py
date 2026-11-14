"""Build an attributed FMA snapshot from the checksum-verified metadata ZIP."""

import argparse
import ast
from collections import Counter, defaultdict
import csv
import hashlib
import html
import io
import json
from pathlib import Path
import zipfile

from src.catalog import FEATURES, Track, number


SOURCE_URL = "https://os.unil.cloud.switch.ch/fma/fma_metadata.zip"
EXPECTED_SHA1 = "f0df49ffe5f2a6008d7dc83c6915b31835dfe733"
SELECTION_VERSION = "ai110-fma-v1"


def digest(path, algorithm="sha256"):
    result = hashlib.new(algorithm)
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def genre_ancestors(genre_id, genres):
    """Include the given genre and follow only explicit source parent edges."""
    chain = []
    while genre_id:
        if genre_id in chain or genre_id not in genres:
            raise ValueError("Genre hierarchy contains an unknown ID or cycle")
        chain.append(genre_id)
        genre_id = genres[genre_id]["parent"]
    return chain


def select_tracks(candidates, roots_by_track, size):
    """Sample deterministically across broad genres, with at most 3 per artist."""
    buckets = defaultdict(list)
    for track in candidates:
        for root in roots_by_track[track.id]:
            buckets[root].append(track)
    for bucket in buckets.values():
        bucket.sort(key=lambda t: hashlib.sha256(f"{SELECTION_VERSION}:{t.id}".encode()).hexdigest(), reverse=True)
    selected, artist_counts = {}, Counter()
    while len(selected) < size:
        changed = False
        for root in sorted(buckets):
            bucket = buckets[root]
            while bucket:
                track = bucket.pop()
                if track.id in selected or artist_counts[track.artist_id] >= 3:
                    continue
                selected[track.id] = track
                artist_counts[track.artist_id] += 1
                changed = True
                break
            if len(selected) == size:
                break
        if not changed:
            break
    return sorted(selected.values(), key=lambda t: t.id)


def prepare(archive, output, size=1200):
    """Validate source records and write a deterministic JSONL/report snapshot."""
    if type(size) is not int or size <= 0:
        raise ValueError("size must be a positive integer")
    if digest(archive, "sha1") != EXPECTED_SHA1:
        raise ValueError("FMA archive checksum mismatch; refusing unverified input")
    csv.field_size_limit(10_000_000)
    excluded, feature_rows, raw_rows = Counter(), {}, {}
    excluded_examples = []
    with zipfile.ZipFile(archive) as zipped:
        def reader(name):
            return csv.reader(io.TextIOWrapper(zipped.open("fma_metadata/" + name), encoding="utf-8", newline=""))

        genre_reader = reader("genres.csv")
        names = next(genre_reader)
        genres = {}
        for values in genre_reader:
            row = dict(zip(names, values))
            genre_id = int(row["genre_id"])
            if genre_id in genres:
                raise ValueError("Duplicate source genre ID")
            genres[genre_id] = {"title": row["title"].strip().casefold(), "parent": int(row["parent"])}
        for genre_id in genres:
            genre_ancestors(genre_id, genres)

        rows = reader("echonest.csv")
        next(rows)
        groups, columns = next(rows), next(rows)
        indices = {name: i for i, (group, name) in enumerate(zip(groups, columns)) if group == "audio_features"}
        next(rows)  # source index-name row
        echonest_count = 0
        for row in rows:
            echonest_count += 1
            track_id = int(row[0])
            if track_id in feature_rows:
                raise ValueError("Duplicate source feature ID")
            try:
                features = {}
                for feature in FEATURES:
                    source_name = "tempo" if feature == "tempo_bpm" else feature
                    value = row[indices[source_name]]
                    if not value:
                        raise ValueError("missing feature")
                    features[feature] = number(float(value), feature, tempo=feature == "tempo_bpm")
                feature_rows[track_id] = features
            except ValueError:
                excluded["missing_or_invalid_feature_record"] += 1

        rows = reader("raw_tracks.csv")
        names = next(rows)
        url_index, id_index = names.index("track_url"), names.index("track_id")
        for row in rows:
            track_id = int(row[id_index])
            if track_id in feature_rows:
                if track_id in raw_rows:
                    raise ValueError("Duplicate raw track ID")
                raw_rows[track_id] = row[url_index]

        rows = reader("tracks.csv")
        groups, columns = next(rows), next(rows)
        indices = {(group, name): i for i, (group, name) in enumerate(zip(groups, columns))}
        next(rows)
        candidates, roots_by_track = [], {}
        metadata_count, seen = 0, set()
        for row in rows:
            metadata_count += 1
            track_id = int(row[0])
            if track_id in seen:
                raise ValueError("Duplicate track metadata ID")
            seen.add(track_id)
            if track_id not in feature_rows:
                continue
            def value(group, name):
                return row[indices[group, name]]
            try:
                direct_ids = ast.literal_eval(value("track", "genres"))
                if not isinstance(direct_ids, list) or not direct_ids or any(type(g) is not int for g in direct_ids):
                    raise ValueError("missing genre labels")
                chains = [genre_ancestors(g, genres) for g in direct_ids]
                all_ids = {g for chain in chains for g in chain}
                raw_url = raw_rows.get(track_id, "")
                if raw_url.startswith("http://freemusicarchive.org/"):
                    raw_url = "https://" + raw_url[len("http://"):]
                track = Track(
                    id=track_id, artist_id=int(value("artist", "id")),
                    title=" ".join(html.unescape(value("track", "title")).split()),
                    artist=" ".join(html.unescape(value("artist", "name")).split()),
                    direct_genres=tuple(genres[g]["title"] for g in direct_ids),
                    genres=tuple(genres[g]["title"] for g in all_ids),
                    source_url=raw_url, **feature_rows[track_id],
                )
                candidates.append(track)
                roots_by_track[track_id] = sorted({genres[chain[-1]]["title"] for chain in chains})
            except (ValueError, TypeError, KeyError, SyntaxError) as exc:
                excluded["invalid_identity_genres_or_reference"] += 1
                if len(excluded_examples) < 20:
                    excluded_examples.append({"track_id": track_id, "reason": str(exc)})
        excluded["valid_features_missing_track_metadata"] = len(set(feature_rows) - seen)
    selected = select_tracks(candidates, roots_by_track, size)
    if not selected:
        raise ValueError("No usable tracks; no catalog was written")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    catalog_path = output / "catalog.jsonl"
    catalog_path.write_text("".join(json.dumps(track.to_dict(), sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n" for track in selected), encoding="utf-8")
    (output / "genres.json").write_text(json.dumps(genres, indent=2, sort_keys=True) + "\n")
    candidate_roots = Counter(g for t in candidates for g in roots_by_track[t.id])
    selected_roots = Counter(g for t in selected for g in roots_by_track[t.id])
    report = {
        "source": {"dataset": "FMA metadata rc1 (2017)", "url": SOURCE_URL,
                   "documentation": "https://github.com/mdeff/fma", "metadata_license": "CC BY 4.0",
                   "archive_sha1": EXPECTED_SHA1, "archive_sha256": digest(archive),
                   "members_used": ["genres.csv", "echonest.csv", "tracks.csv", "raw_tracks.csv"]},
        "selection": {"version": SELECTION_VERSION, "requested_size": size,
                      "method": "Round-robin broad genres; SHA-256 ordered track IDs; max 3 tracks per artist; output sorted by ID",
                      "selected_track_ids": [t.id for t in selected], "catalog_sha256": digest(catalog_path)},
        "source_metadata_tracks": metadata_count,
        "source_feature_tracks": echonest_count,
        "excluded_records": dict(sorted(excluded.items())),
        "excluded_examples": excluded_examples,
        "usable_candidates": len(candidates),
        "usable_candidate_broad_genres": dict(sorted(candidate_roots.items())),
        "selected_tracks": len(selected),
        "selected_artists": len({t.artist_id for t in selected}),
        "broad_genre_counts": dict(sorted(selected_roots.items())),
        "all_genre_counts": dict(sorted(Counter(g for t in selected for g in t.genres).items())),
        "direct_genre_counts": dict(sorted(Counter(g for t in selected for g in t.direct_genres).items())),
        "feature_coverage": {f: {"present": sum(getattr(t, f) is not None for t in selected),
                                  "minimum": min(getattr(t, f) for t in selected),
                                  "maximum": max(getattr(t, f) for t in selected)} for f in FEATURES},
        "attribute_combinations": {
            "low_energy_high_acousticness": sum(t.energy <= .35 and t.acousticness >= .7 for t in selected),
            "high_energy_high_danceability": sum(t.energy >= .7 and t.danceability >= .7 for t in selected),
            "slow_tempo": sum(t.tempo_bpm <= 85 for t in selected),
            "fast_tempo": sum(t.tempo_bpm >= 140 for t in selected),
            "high_instrumentalness_estimate": sum(t.instrumentalness >= .8 for t in selected),
        },
        "duplicates_in_snapshot": 0,
        "unselected_usable_candidates": len(candidates) - len(selected),
        "transformations": ["genre labels stripped and casefolded", "genre ancestors from source parent hierarchy",
                            "title/artist HTML entities decoded and whitespace collapsed",
                            "http FMA track references upgraded to https; no other URL invented",
                            "tempo renamed tempo_bpm; numeric values retained without imputation"],
        "limitations": ["Historical independent-music snapshot, not a current mainstream catalog",
                        "Genre labels overlap; counts can exceed track count and some categories remain sparse",
                        "Audio attributes are estimates, not verified mood, lyric, or no-vocals labels",
                        "Source references identify records; current playback/link availability is not guaranteed",
                        "Stratification and artist cap change source distribution; not representative sampling"],
    }
    (output / "catalog_report.json").write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data"))
    parser.add_argument("--size", type=int, default=1200)
    args = parser.parse_args()
    result = prepare(args.archive, args.output, args.size)
    print(json.dumps({key: result[key] for key in ("source_feature_tracks", "usable_candidates", "selected_tracks", "selected_artists", "broad_genre_counts", "excluded_records", "attribute_combinations")}, indent=2))
