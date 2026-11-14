"""Strict, reusable preferences for manual input and the AI interpreter."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from .catalog import FEATURES, number, text


@dataclass(frozen=True)
class FeatureRange:
    """A required inclusive interval; either endpoint may be left unset."""

    minimum: float | None = None
    maximum: float | None = None


@dataclass(frozen=True)
class Preferences:
    """Separate soft targets from conditions that must never be relaxed."""

    preferred_genres: tuple[str, ...] = ()
    required_genres: tuple[str, ...] = ()
    excluded_genres: tuple[str, ...] = ()
    targets: Mapping[str, float] = field(default_factory=dict)
    bounds: Mapping[str, FeatureRange] = field(default_factory=dict)
    unsupported: tuple[str, ...] = ()

    def __post_init__(self):
        for key in ("preferred_genres", "required_genres", "excluded_genres", "unsupported"):
            values = getattr(self, key)
            if not isinstance(values, (tuple, list)) or len(values) > 10:
                raise ValueError(f"{key} must be a list with at most 10 entries")
            clean = []
            for value in values:
                value = text(value, key)
                if len(value) > 200:
                    raise ValueError(f"{key} entries must be at most 200 characters")
                value = value if key == "unsupported" else value.casefold()
                if value not in clean:
                    clean.append(value)
            object.__setattr__(self, key, tuple(clean))
        overlap = (set(self.preferred_genres) | set(self.required_genres)) & set(self.excluded_genres)
        if overlap:
            raise ValueError(f"Genres cannot be requested and excluded: {', '.join(sorted(overlap))}")
        if not isinstance(self.targets, Mapping) or not isinstance(self.bounds, Mapping):
            raise ValueError("targets and bounds must be JSON objects")
        targets, bounds = {}, {}
        for feature, value in self.targets.items():
            _feature(feature)
            targets[feature] = number(value, feature, tempo=feature == "tempo_bpm")
        for feature, interval in self.bounds.items():
            _feature(feature)
            if not isinstance(interval, FeatureRange):
                raise ValueError(f"{feature} bounds must be FeatureRange objects")
            low, high = interval.minimum, interval.maximum
            if low is None and high is None:
                raise ValueError(f"{feature} bounds require minimum or maximum")
            if low is not None:
                low = number(low, feature, tempo=feature == "tempo_bpm")
            if high is not None:
                high = number(high, feature, tempo=feature == "tempo_bpm")
            if low is not None and high is not None and low > high:
                raise ValueError(f"{feature} minimum cannot exceed maximum")
            target = targets.get(feature)
            if target is not None and ((low is not None and target < low)
                                       or (high is not None and target > high)):
                raise ValueError(f"{feature} target contradicts required bounds")
            bounds[feature] = FeatureRange(low, high)
        object.__setattr__(self, "targets", MappingProxyType(targets))
        object.__setattr__(self, "bounds", MappingProxyType(bounds))
        if not any((self.preferred_genres, self.required_genres, self.excluded_genres,
                    self.targets, self.bounds, self.unsupported)):
            raise ValueError("Specify at least one preference or required condition")

    @classmethod
    def from_dict(cls, payload):
        if not isinstance(payload, dict):
            raise ValueError("Preferences must be a JSON object")
        if set(payload) - set(cls.__dataclass_fields__):
            raise ValueError("Unknown preference fields: " + ", ".join(sorted(set(payload) - set(cls.__dataclass_fields__))))
        data = dict(payload)
        if "bounds" in data:
            if not isinstance(data["bounds"], dict):
                raise ValueError("bounds must be a JSON object")
            bounds = {}
            for key, value in data["bounds"].items():
                if not isinstance(value, dict) or set(value) - {"minimum", "maximum"}:
                    raise ValueError(f"{key} bounds accept only minimum and maximum")
                bounds[key] = FeatureRange(**value)
            data["bounds"] = bounds
        return cls(**data)

    def validate_vocabulary(self, vocabulary):
        requested = set(self.preferred_genres + self.required_genres + self.excluded_genres)
        unknown = requested - set(vocabulary)
        if unknown:
            raise ValueError("Genres absent from this catalog: " + ", ".join(sorted(unknown)))

    def to_dict(self):
        return {
            "preferred_genres": list(self.preferred_genres),
            "required_genres": list(self.required_genres),
            "excluded_genres": list(self.excluded_genres),
            "targets": dict(self.targets),
            "bounds": {key: {"minimum": value.minimum, "maximum": value.maximum}
                       for key, value in self.bounds.items()},
            "unsupported": list(self.unsupported),
        }


def _feature(name):
    if name not in FEATURES:
        raise ValueError(f"Unsupported musical attribute: {name}")
