"""One interpretation call, deterministic checks, then explicit human review."""

from dataclasses import dataclass
import hashlib
import json
import logging
from pathlib import Path
import re
import time

from .catalog import FEATURES, Catalog, read_json
from .llm_client import ProviderError
from .preferences import Preferences


ROOT = Path(__file__).resolve().parents[1]
LOGGER = logging.getLogger(__name__)


def response_schema(vocabulary):
    genres = {"type": "array", "items": {"type": "string", "enum": sorted(vocabulary)}, "maxItems": 10}
    number_properties = {feature: {"type": "number"} for feature in FEATURES}
    interval = {"type": "object", "properties": {"minimum": {"type": "number"}, "maximum": {"type": "number"}}, "additionalProperties": False}
    prefs = {"type": "object", "properties": {
        "preferred_genres": genres, "required_genres": genres, "excluded_genres": genres,
        "targets": {"type": "object", "properties": number_properties, "additionalProperties": False},
        "bounds": {"type": "object", "properties": {f: interval for f in FEATURES}, "additionalProperties": False},
        "unsupported": {"type": "array", "items": {"type": "string"}, "maxItems": 10}},
        "additionalProperties": False}
    return {"type": "object", "properties": {"preferences": prefs,
        "summary": {"type": "string"}, "assumptions": {"type": "array", "items": {"type": "string"}, "maxItems": 10}},
        "required": ["preferences", "summary", "assumptions"], "additionalProperties": False}


def instructions_for(catalog, variant="specialized"):
    if variant not in ("generic", "specialized"):
        raise ValueError("Unknown prompt variant")
    instructions = (ROOT / "prompts" / f"{variant}.txt").read_text()
    # Same catalog vocabulary/schema in both experimental arms.
    return instructions + "\nSupported genre vocabulary: " + json.dumps(sorted(catalog.vocabulary))


def evidence_gaps(request):
    """Block a few unverifiable guarantees even if the model overlooks them."""
    checks = [
        (r"\b(explicit|profanity|clean lyrics|child.safe|kids.safe|no swearing|safe for (?:kids|children))\b", "Verified lyric safety is unavailable in this catalog."),
        (r"\b(no vocals|no singing|no voices|vocal.free|guaranteed instrumental)\b", "Absence of vocals cannot be guaranteed from an instrumentalness estimate."),
        (r"\b(cure|heal|medical treatment)\b", "Medical or therapeutic effects cannot be verified."),
    ]
    return [message for pattern, message in checks if re.search(pattern, request, re.I)]


@dataclass(frozen=True)
class Interpretation:
    preferences: Preferences
    model_preferences: dict
    summary: str
    assumptions: tuple[str, ...]
    mode: str
    model: str | None
    prompt_variant: str
    prompt_sha256: str
    elapsed_seconds: float

    def to_dict(self):
        return {"preferences": self.preferences.to_dict(), "summary": self.summary,
                "model_preferences_before_guardrails": self.model_preferences,
                "assumptions": list(self.assumptions), "mode": self.mode, "model": self.model,
                "prompt_variant": self.prompt_variant, "prompt_sha256": self.prompt_sha256,
                "elapsed_seconds": self.elapsed_seconds}


def interpret_request(request: str, catalog: Catalog, client, variant="specialized"):
    if not isinstance(request, str) or not request.strip():
        raise ValueError("Describe the music you want before interpreting it.")
    request = request.strip()
    if len(request) > 1200 or any(ord(char) < 32 and char not in "\n\t" for char in request):
        raise ValueError("Use at most 1,200 characters without control characters.")
    instructions = instructions_for(catalog, variant)
    started = time.monotonic()
    raw = client.generate(instructions, request, response_schema(catalog.vocabulary))
    try:
        if not isinstance(raw, str) or len(raw.encode()) > 16000:
            raise ValueError("Oversized or nontext model reply")
        data = read_json(raw)
        if not isinstance(data, dict) or set(data) != {"preferences", "summary", "assumptions"}:
            raise ValueError("Unexpected response contract")
        summary, assumptions = data["summary"], data["assumptions"]
        if not isinstance(summary, str) or not summary.strip() or len(summary) > 600:
            raise ValueError("Invalid summary")
        if not isinstance(assumptions, list) or len(assumptions) > 10 or any(not isinstance(v, str) or len(v) > 300 for v in assumptions):
            raise ValueError("Invalid assumptions")
        prefs = Preferences.from_dict(data["preferences"])
        prefs.validate_vocabulary(catalog.vocabulary)
        model_preferences = prefs.to_dict()
        gaps = evidence_gaps(request)
        if gaps:
            payload = prefs.to_dict()
            payload["unsupported"] = list(dict.fromkeys(payload["unsupported"] + gaps))[:10]
            prefs = Preferences.from_dict(payload)
    except (ValueError, TypeError, AttributeError):
        LOGGER.warning("interpretation rejected category=invalid_output mode=%s", client.mode)
        raise ProviderError("invalid_output", "The interpretation failed validation. No preferences were applied; try rephrasing or use manual mode.") from None
    elapsed = round(time.monotonic() - started, 4)
    LOGGER.info("interpretation mode=%s model=%s variant=%s elapsed=%s unsupported=%d", client.mode, client.model, variant, elapsed, len(prefs.unsupported))
    return Interpretation(prefs, model_preferences, summary.strip(), tuple(assumptions), client.mode, client.model, variant,
                          hashlib.sha256(instructions.encode()).hexdigest(), elapsed)
