"""Behavioral contracts for the expanded catalog, constraints, and real CLI."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

from src.catalog import CATALOG_PATH, FEATURES, Catalog, Track, load_catalog, read_json
from src.preferences import FeatureRange, Preferences
from src.ranking import recommend, rejection_reason, score_track


ROOT = Path(__file__).resolve().parents[1]


def track(id=1, genre="rock", energy=.9, **changes):
    record = dict(id=id, artist_id=id, title=f"Fixture {id}", artist=f"Artist {id}",
                  direct_genres=(genre,), genres=(genre,),
                  source_url=f"https://freemusicarchive.org/music/fixture/album/{id}",
                  energy=energy, tempo_bpm=120, acousticness=.2, danceability=.8,
                  valence=.7, instrumentalness=.1)
    record.update(changes)
    return Track(**record)


@pytest.fixture
def catalog():
    return Catalog((track(1), track(2, "folk", .2, acousticness=.95, tempo_bpm=75),
                    track(3, "electronic", .8, danceability=.95),
                    track(4, "jazz", .4, acousticness=.8)))


@pytest.mark.parametrize("payload", [
    None, [], {}, {"preferred_genres": "folk"}, {"preferred_genres": [""]},
    {"preferred_genres": [1]}, {"preferred_genres": ["rock"] * 11},
    {"targets": []}, {"targets": {"energy": True}}, {"targets": {"energy": "0.5"}},
    {"targets": {"energy": float("nan")}}, {"targets": {"energy": float("inf")}},
    {"targets": {"energy": -1}}, {"targets": {"energy": 1.1}},
    {"targets": {"tempo_bpm": 0}}, {"targets": {"lyrics": .5}},
    {"bounds": {"energy": {}}}, {"bounds": {"energy": {"minimum": .9, "maximum": .1}}},
    {"bounds": {"energy": {"maximum": True}}}, {"bounds": []},
    {"bounds": {"energy": {"min": 0}}}, {"bounds": {"energy": 1}},
    {"targets": {"energy": .8}, "bounds": {"energy": {"maximum": .2}}},
    {"preferred_genres": ["folk"], "excluded_genres": ["Folk"]},
    {"required_genres": ["rock"], "excluded_genres": ["rock"]},
    {"unsupported": "lyrics"}, {"unsupported": ["x" * 201]},
    {"preferred_genres": ["rock"], "execute": "anything"},
])
def test_rejects_invalid_or_contradictory_preferences(payload):
    with pytest.raises(ValueError):
        Preferences.from_dict(payload)


def test_preferences_are_normalized_immutable_and_round_trip():
    source = {"preferred_genres": [" Folk ", "folk"], "targets": {"energy": .3},
              "bounds": {"acousticness": {"minimum": .6}}}
    prefs = Preferences.from_dict(source)
    source["targets"]["energy"] = 1
    assert prefs.preferred_genres == ("folk",)
    assert prefs.targets["energy"] == .3
    assert Preferences.from_dict(prefs.to_dict()) == prefs
    with pytest.raises(TypeError):
        prefs.targets["energy"] = .9


@pytest.mark.parametrize("value", [True, "0.3", float("nan"), float("inf"), -1, 1.01, 10**1000])
def test_track_features_are_not_fabricated_or_coerced(value):
    with pytest.raises(ValueError):
        track(energy=value)


@pytest.mark.parametrize("changes", [
    {"id": True}, {"artist_id": 0}, {"title": " "}, {"genres": "rock"},
    {"genres": []}, {"genres": ["folk"]}, {"tempo_bpm": 0},
    {"source_url": "https://example.org/music/record"},
    {"source_url": "https://user:pass@freemusicarchive.org/music/x"},
    {"source_url": "https://freemusicarchive.org:443/music/x"},
])
def test_invalid_catalog_records_are_rejected(changes):
    with pytest.raises(ValueError):
        track(**changes)


def test_catalog_rejects_duplicate_ids_and_empty_data():
    with pytest.raises(ValueError, match="unique"):
        Catalog((track(), track()))
    with pytest.raises(ValueError, match="at least one"):
        Catalog(())


def test_catalog_loader_reports_line_and_rejects_duplicate_keys(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text(json.dumps(track().to_dict()) + '\n{"id":2,"id":3}\n')
    with pytest.raises(ValueError, match="line 2.*Duplicate JSON key"):
        load_catalog(path)
    with pytest.raises(ValueError, match="Duplicate"):
        read_json('{"targets":{"energy":0.2,"energy":0.9}}')


@pytest.mark.parametrize("value", ['{"energy":NaN}', '{"energy":Infinity}', '[' * 1500 + '0' + ']' * 1500])
def test_nonstandard_or_excessively_nested_json_is_rejected(value):
    with pytest.raises(ValueError):
        read_json(value)


def test_genre_alternatives_are_or_not_an_impossible_and(catalog):
    prefs = Preferences(required_genres=("folk", "rock"))
    result = recommend(catalog, prefs)
    assert {r.track.id for r in result.recommendations} == {1, 2}
    assert all(r.score is None for r in result.recommendations)


def test_parent_genre_exclusion_also_removes_subgenres():
    child = track(genres=("rock", "indie-rock"), direct_genres=("indie-rock",))
    catalog = Catalog((child, track(2, "folk")))
    assert recommend(catalog, Preferences(excluded_genres=("rock",))).recommendations[0].track.id == 2
    assert recommend(catalog, Preferences(required_genres=("rock",))).recommendations[0].track.id == 1


def test_guardrail_blocks_candidate_that_would_otherwise_rank_first(catalog, monkeypatch):
    prefs = Preferences(excluded_genres=("rock",), targets={"energy": .9})
    guarded = recommend(catalog, prefs)
    assert guarded.recommendations[0].track.id == 3
    assert all("rock" not in r.track.genres for r in guarded.recommendations)
    # Controlled ablation: all else equal, bypass the candidate rejection guard.
    monkeypatch.setattr("src.ranking.rejection_reason", lambda track, preferences: None)
    unguarded = recommend(catalog, prefs)
    assert unguarded.recommendations[0].track.id == 1


def test_targets_change_order_and_explanations_reconcile(catalog):
    low = recommend(catalog, Preferences(targets={"energy": .2}))
    high = recommend(catalog, Preferences(targets={"energy": .9}))
    assert low.recommendations[0].track.id == 2
    assert high.recommendations[0].track.id == 1
    assert high.recommendations[0].score == 1
    assert "observed 0.9000, target 0.9000" in high.recommendations[0].explanations[0]
    mixed = score_track(catalog.tracks[1], Preferences(preferred_genres=("folk",), targets={"energy": .9}))
    assert mixed.score == pytest.approx((2 + .3) / 3)
    assert mixed.compromises


def test_numeric_hard_bounds_are_inclusive_and_never_relaxed(catalog):
    prefs = Preferences(bounds={"energy": FeatureRange(.2, .4)})
    result = recommend(catalog, prefs, limit=20)
    assert {r.track.id for r in result.recommendations} == {2, 4}
    assert len(result.recommendations) < 20
    impossible = Preferences(bounds={"energy": FeatureRange(.01, .02)})
    assert recommend(catalog, impossible).status == "no_results"


def test_unknown_feature_evidence_is_not_treated_as_zero():
    unknown = track(energy=None)
    catalog = Catalog((unknown, track(2, energy=.3)))
    result = recommend(catalog, Preferences(targets={"energy": 0}))
    assert [r.track.id for r in result.recommendations] == [2]
    assert rejection_reason(unknown, Preferences(bounds={"energy": FeatureRange(maximum=.5)}))
    assert recommend(catalog, Preferences(required_genres=("rock",))).eligible_count == 2


def test_weak_soft_matches_produce_honest_empty_result(catalog):
    prefs = Preferences(required_genres=("rock",), targets={"energy": 0})
    result = recommend(catalog, prefs)
    assert result.status == "no_results" and result.eligible_count == 1
    assert "threshold" in result.message


def test_unsupported_conditions_block_instead_of_being_silently_dropped(catalog):
    result = recommend(catalog, Preferences(preferred_genres=("rock",), unsupported=("verified clean lyrics",)))
    assert result.status == "needs_clarification"
    assert result.recommendations == ()
    assert "clean lyrics" in result.message


def test_unknown_genre_is_rejected_instead_of_being_mapped_to_a_preset(catalog):
    with pytest.raises(ValueError, match="absent"):
        recommend(catalog, Preferences(required_genres=("nonexistent genre",)))


def test_ties_sort_by_stable_id_without_reordering_catalog():
    values = (track(3), track(2), track(1))
    catalog = Catalog(values)
    result = recommend(catalog, Preferences(targets={"energy": .9}))
    assert [r.track.id for r in result.recommendations] == [1, 2, 3]
    assert catalog.tracks == values


@pytest.mark.parametrize("limit", [True, 0, -1, 21, 1.5])
def test_invalid_result_limit_rejected(catalog, limit):
    with pytest.raises(ValueError):
        recommend(catalog, Preferences(targets={"energy": .5}), limit)


def test_snapshot_has_observed_depth_and_matches_its_provenance_report():
    catalog = load_catalog()
    report = json.loads((ROOT / "data/catalog_report.json").read_text())
    assert len(catalog.tracks) == report["selected_tracks"] == 1200
    assert len({t.artist_id for t in catalog.tracks}) == report["selected_artists"]
    assert sum(n >= 20 for n in report["broad_genre_counts"].values()) >= 10
    assert len(catalog.vocabulary) == len(report["all_genre_counts"])
    assert hashlib.sha256(CATALOG_PATH.read_bytes()).hexdigest() == report["selection"]["catalog_sha256"]
    assert [t.id for t in catalog.tracks] == report["selection"]["selected_track_ids"]
    assert all(getattr(t, f) is not None for t in catalog.tracks for f in FEATURES)


@pytest.mark.parametrize("example", ["acoustic_folk", "evening_jazz", "dance_pop"])
def test_real_cli_examples_satisfy_required_conditions(example):
    command = [sys.executable, "-m", "src.cli", "--preferences", f"examples/{example}.json", "--json"]
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout)
    assert result["mode"] == "manual" and result["status"] == "ok"
    prefs = Preferences.from_dict(result["preferences"])
    assert len(result["recommendations"]) == 5
    for item in result["recommendations"]:
        assert rejection_reason(Track(**item["track"]), prefs) is None
        assert item["match_score"] >= .6


@pytest.mark.parametrize("example,status", [("unsupported_lyrics", "needs_clarification"), ("no_results", "no_results")])
def test_real_cli_reliability_cases(example, status):
    proc = subprocess.run([sys.executable, "-m", "src.cli", "--preferences", f"examples/{example}.json", "--json"], cwd=ROOT, text=True, capture_output=True)
    assert proc.returncode == 3
    assert json.loads(proc.stdout)["status"] == status


def test_cli_invalid_input_and_genre_listing():
    proc = subprocess.run([sys.executable, "-m", "src.cli", "--preferences-json", '{"targets":{"energy":true}}'], cwd=ROOT, text=True, capture_output=True)
    assert proc.returncode == 2 and "must be a number" in proc.stderr
    assert "Traceback" not in proc.stderr
    listing = subprocess.run([sys.executable, "-m", "src.cli", "--list-genres"], cwd=ROOT, text=True, capture_output=True)
    assert listing.returncode == 0 and "folk" in listing.stdout.splitlines()


def test_preparation_checks_source_integrity_before_processing(tmp_path):
    from scripts.prepare_catalog import prepare
    archive = tmp_path / "wrong.zip"
    archive.write_bytes(b"not verified metadata")
    with pytest.raises(ValueError, match="checksum"):
        prepare(archive, tmp_path / "output")
    assert not (tmp_path / "output").exists()


def test_preparation_hierarchy_rejects_unknown_parents_and_cycles():
    from scripts.prepare_catalog import genre_ancestors
    with pytest.raises(ValueError):
        genre_ancestors(1, {1: {"parent": 2}, 2: {"parent": 1}})
    with pytest.raises(ValueError):
        genre_ancestors(1, {1: {"parent": 2}})
