"""Read a small, versioned real-track catalog without network access."""

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
from urllib.parse import urlparse


CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "catalog.jsonl"
FEATURES = ("energy", "tempo_bpm", "valence", "acousticness", "danceability",
            "instrumentalness")


def number(value, name, *, tempo=False):
    """Require a finite JSON number; never coerce booleans or numeric strings."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite or (tempo and value <= 0) or (not tempo and not 0 <= value <= 1):
        interval = "positive and finite" if tempo else "finite and between 0 and 1"
        raise ValueError(f"{name} must be {interval}")
    return float(value)


def text(value, name):
    """Require nonblank text and retain the source's spelling."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonblank text")
    return value.strip()


@dataclass(frozen=True)
class Track:
    """Imported identity and genre metadata plus optional algorithmic estimates."""

    id: int
    artist_id: int
    title: str
    artist: str
    direct_genres: tuple[str, ...]
    genres: tuple[str, ...]
    source_url: str
    energy: float | None = None
    tempo_bpm: float | None = None
    valence: float | None = None
    acousticness: float | None = None
    danceability: float | None = None
    instrumentalness: float | None = None

    def __post_init__(self):
        for name in ("id", "artist_id"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        for name in ("title", "artist", "source_url"):
            object.__setattr__(self, name, text(getattr(self, name), name))
        parsed = urlparse(self.source_url)
        if parsed.scheme != "https" or parsed.hostname != "freemusicarchive.org":
            raise ValueError("source_url must reference https://freemusicarchive.org")
        if parsed.username or parsed.password or parsed.port or not parsed.path.startswith("/music/"):
            raise ValueError("source_url must be an FMA track reference")
        for name in ("genres", "direct_genres"):
            values = getattr(self, name)
            if not isinstance(values, (list, tuple)) or not values:
                raise ValueError(f"{name} must be a nonempty list of genre labels")
            clean = tuple(sorted({text(v, name).casefold() for v in values}))
            object.__setattr__(self, name, clean)
        if not set(self.direct_genres) <= set(self.genres):
            raise ValueError("direct_genres must be included in genres")
        for name in FEATURES:
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, number(value, name, tempo=name == "tempo_bpm"))

    def to_dict(self):
        """Return JSON-compatible values, without any generated song facts."""
        result = asdict(self)
        for key in ("genres", "direct_genres"):
            result[key] = list(result[key])
        return result


@dataclass(frozen=True)
class Catalog:
    """Hold unique tracks and the vocabulary actually represented in them."""

    tracks: tuple[Track, ...]

    def __post_init__(self):
        object.__setattr__(self, "tracks", tuple(self.tracks))
        if not self.tracks:
            raise ValueError("Catalog must contain at least one track")
        if not all(isinstance(track, Track) for track in self.tracks):
            raise ValueError("Catalog entries must be validated Track objects")
        ids = [track.id for track in self.tracks]
        if len(ids) != len(set(ids)):
            raise ValueError("Catalog track IDs must be unique")

    @property
    def vocabulary(self):
        return frozenset(genre for track in self.tracks for genre in track.genres)


def reject_duplicates(pairs):
    """Reject duplicate JSON keys instead of silently using the last value."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(value):
    """Reject duplicate keys, non-JSON constants, and excessive nesting."""
    def invalid_constant(value):
        raise ValueError(f"Invalid JSON constant: {value}")
    try:
        return json.loads(value, object_pairs_hook=reject_duplicates,
                          parse_constant=invalid_constant)
    except RecursionError as exc:
        raise ValueError("JSON nesting exceeds the supported depth") from exc


def load_catalog(path=CATALOG_PATH):
    """Load JSONL records, reporting errors with a source line number."""
    tracks = []
    with Path(path).open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            try:
                row = read_json(line)
                if not isinstance(row, dict):
                    raise ValueError("Track must be a JSON object")
                tracks.append(Track(**row))
            except (ValueError, TypeError) as exc:
                raise ValueError(f"Catalog line {line_no}: {exc}") from exc
    return Catalog(tuple(tracks))
