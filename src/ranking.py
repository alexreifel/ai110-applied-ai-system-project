"""Filter hard conditions before scoring supported soft preferences."""

from dataclasses import dataclass
import logging

from .catalog import Catalog, Track
from .preferences import Preferences


LOGGER = logging.getLogger(__name__)
MIN_MATCH_SCORE = 0.6
TEMPO_DISTANCE_BPM = 100.0


@dataclass(frozen=True)
class Recommendation:
    track: Track
    score: float | None
    explanations: tuple[str, ...]
    compromises: tuple[str, ...]

    def to_dict(self):
        return {"track": self.track.to_dict(), "match_score": self.score,
                "explanations": list(self.explanations), "compromises": list(self.compromises)}


@dataclass(frozen=True)
class RankingResult:
    status: str
    message: str
    catalog_count: int
    eligible_count: int
    recommendations: tuple[Recommendation, ...]

    def to_dict(self):
        return {"status": self.status, "message": self.message,
                "catalog_count": self.catalog_count, "eligible_count": self.eligible_count,
                "recommendations": [item.to_dict() for item in self.recommendations]}


def rejection_reason(track, preferences):
    """Return a hard-condition/missing-evidence reason, or None if eligible."""
    if set(track.genres) & set(preferences.excluded_genres):
        return "excluded genre"
    if preferences.required_genres and not set(track.genres) & set(preferences.required_genres):
        return "required genre absent"
    for name in set(preferences.targets) | set(preferences.bounds):
        if getattr(track, name) is None:
            return f"missing {name} evidence"
    for name, interval in preferences.bounds.items():
        value = getattr(track, name)
        if ((interval.minimum is not None and value < interval.minimum)
                or (interval.maximum is not None and value > interval.maximum)):
            return f"outside required {name} bounds"
    return None


def score_track(track, preferences):
    """Return a weighted mean similarity with matching per-feature explanations."""
    points, weights, reasons, compromises = [], [], [], []
    if preferences.preferred_genres:
        matches = sorted(set(track.genres) & set(preferences.preferred_genres))
        similarity = float(bool(matches))
        points.append(2 * similarity)
        weights.append(2.0)
        reasons.append(f"genre: matched {', '.join(matches) if matches else 'none'}; similarity {similarity:.3f}, weight 2")
        if not matches:
            compromises.append("Does not match a preferred genre")
    for feature, target in sorted(preferences.targets.items()):
        value = getattr(track, feature)
        if value is None:
            raise ValueError(f"Cannot score missing {feature}; filter candidates first")
        scale = TEMPO_DISTANCE_BPM if feature == "tempo_bpm" else 1.0
        similarity = max(0.0, 1.0 - abs(value - target) / scale)
        points.append(similarity)
        weights.append(1.0)
        reasons.append(f"{feature}: observed {value:.4f}, target {target:.4f}; similarity {similarity:.4f}, weight 1")
        if similarity < 0.75:
            compromises.append(f"{feature} differs substantially from target")
    for feature, interval in sorted(preferences.bounds.items()):
        if interval.minimum is None:
            condition = f"at most {interval.maximum}"
        elif interval.maximum is None:
            condition = f"at least {interval.minimum}"
        else:
            condition = f"between {interval.minimum} and {interval.maximum}"
        reasons.append(f"required {feature}: {condition}; observed {getattr(track, feature):.4f}")
    if preferences.required_genres:
        reasons.append("required genre matched: " + ", ".join(sorted(set(track.genres) & set(preferences.required_genres))))
    if preferences.excluded_genres:
        reasons.append("excluded genres absent: " + ", ".join(preferences.excluded_genres))
    score = round(sum(points) / sum(weights), 12) if weights else None
    if score is None:
        reasons.append("Eligible by required conditions; no soft preferences to score")
    return Recommendation(track, score, tuple(reasons), tuple(compromises))


def recommend(catalog: Catalog, preferences: Preferences, limit=5):
    """Rank validated preferences; never relax a hard condition to fill results."""
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError("limit must be an integer between 1 and 20")
    preferences.validate_vocabulary(catalog.vocabulary)
    total = len(catalog.tracks)
    if preferences.unsupported:
        return RankingResult("needs_clarification", "Cannot verify: " + "; ".join(preferences.unsupported), total, 0, ())
    eligible = [track for track in catalog.tracks if rejection_reason(track, preferences) is None]
    scored = [score_track(track, preferences) for track in eligible]
    suitable = [item for item in scored if item.score is None or item.score >= MIN_MATCH_SCORE]
    ordered = sorted(suitable, key=lambda item: (-(item.score or 0), item.track.id))
    chosen = tuple(ordered[:limit])
    status = "ok" if chosen else "no_results"
    if chosen:
        message = "Recommendations from catalog metadata; scores are similarities, not probabilities."
    elif not eligible:
        message = "No tracks satisfy every required condition with sufficient metadata. Conditions were not relaxed."
    else:
        message = f"No eligible tracks reach the documented {MIN_MATCH_SCORE:.2f} soft-match threshold. Revise your preferences."
    LOGGER.info("ranking status=%s catalog=%d eligible=%d returned=%d", status, total, len(eligible), len(chosen))
    return RankingResult(status, message, total, len(eligible), chosen)
