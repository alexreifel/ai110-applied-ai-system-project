"""A bounded Gemini REST adapter; no SDK, tools, retries, or secret logging."""

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
import socket
import urllib.error
import urllib.request

from .catalog import read_json


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gemini-2.5-flash-lite"


class ProviderError(Exception):
    """Expose a stable, safe category and message, never a raw provider body."""

    def __init__(self, kind, message):
        self.kind = kind
        super().__init__(message)


@dataclass(frozen=True)
class Settings:
    api_key: str = field(default="", repr=False)
    model: str = DEFAULT_MODEL
    timeout: float = 20

    def __post_init__(self):
        if not isinstance(self.api_key, str) or (self.api_key and not re.fullmatch(r"[A-Za-z0-9_-]{10,256}", self.api_key)):
            raise ProviderError("configuration", "API key format is invalid. Check the local value; it must not contain whitespace or control characters.")
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", self.model):
            raise ProviderError("configuration", "GEMINI_MODEL must be a plain model identifier.")
        if not 1 <= self.timeout <= 45:
            raise ProviderError("configuration", "GEMINI_TIMEOUT_SECONDS must be between 1 and 45.")


def settings_from_environment(env=None, env_path=None):
    """Read simple KEY=value settings; do not execute/interpolate a .env file."""
    env = os.environ if env is None else env
    path = ROOT / ".env" if env_path is None else Path(env_path)
    local = {}
    allowed = {"GEMINI_API_KEY", "GOOGLE_API_KEY", "GEMINI_MODEL", "GEMINI_TIMEOUT_SECONDS"}
    if path.is_file():
        if path.stat().st_size > 16000:
            raise ProviderError("configuration", "The local .env file is too large.")
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, separator, value = line.partition("=")
                if separator and key.strip() in allowed:
                    local[key.strip()] = value.strip().strip("\"'")
        except (OSError, UnicodeError):
            raise ProviderError("configuration", "Could not read the local .env configuration.") from None
    key = env.get("GEMINI_API_KEY") or local.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY") or local.get("GOOGLE_API_KEY", "")
    model = env.get("GEMINI_MODEL") or local.get("GEMINI_MODEL", DEFAULT_MODEL)
    try:
        timeout = float(env.get("GEMINI_TIMEOUT_SECONDS") or local.get("GEMINI_TIMEOUT_SECONDS", "20"))
    except ValueError:
        raise ProviderError("configuration", "GEMINI_TIMEOUT_SECONDS must be a number.") from None
    return Settings(key, model, timeout)


class GeminiClient:
    mode = "live"

    def __init__(self, settings=None, opener=None):
        self.settings = settings or settings_from_environment()
        self.model = self.settings.model
        self.opener = opener or urllib.request.urlopen

    def generate(self, instructions, request, schema):
        if not self.settings.api_key:
            raise ProviderError("missing_credentials", "Set GEMINI_API_KEY in the ignored .env file, or use manual mode/offline demo.")
        payload = {"systemInstruction": {"parts": [{"text": instructions}]},
                   "contents": [{"role": "user", "parts": [{"text": request}]}],
                   "generationConfig": {"temperature": 0, "maxOutputTokens": 2048,
                                        "responseMimeType": "application/json", "responseJsonSchema": schema}}
        req = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent",
            data=json.dumps(payload).encode(), method="POST",
            headers={"Content-Type": "application/json", "x-goog-api-key": self.settings.api_key},
        )
        try:
            with self.opener(req, timeout=self.settings.timeout) as response:
                raw = response.read(65537)
        except urllib.error.HTTPError as exc:
            reason = ""
            try:
                error = json.loads(exc.read(16000)).get("error", {})
                reason = " ".join(str(item.get("reason", "")) for item in error.get("details", []) if isinstance(item, dict))
            except (ValueError, TypeError, AttributeError, OSError):
                pass
            if exc.code in (401, 403) or "API_KEY_INVALID" in reason:
                kind, message = "authentication", "Gemini rejected the key or its access. Check the local key and API restrictions."
            elif exc.code == 404:
                kind, message = "model_access", "The configured Gemini model is unavailable. Check GEMINI_MODEL and account access."
            elif exc.code == 429:
                kind, message = "quota", "Gemini quota/rate limit reached. Try later or use manual mode; billing was not changed."
            else:
                kind, message = "provider", f"Gemini request failed (HTTP {exc.code}). Use manual mode or try again later."
            raise ProviderError(kind, message) from None
        except (TimeoutError, socket.timeout):
            raise ProviderError("timeout", "Gemini timed out. No automatic retry was made; manual mode is available.") from None
        except urllib.error.URLError as exc:
            if isinstance(exc.reason, (TimeoutError, socket.timeout)):
                raise ProviderError("timeout", "Gemini timed out. No automatic retry was made.") from None
            raise ProviderError("network", "Could not reach Gemini. Check the connection or use manual mode.") from None
        if len(raw) > 65536:
            raise ProviderError("invalid_output", "Gemini returned an oversized response; it was not used.")
        try:
            data = read_json(raw.decode("utf-8"))
            candidate = data.get("candidates", [])[0]
            if candidate.get("finishReason") != "STOP":
                raise ValueError("Incomplete or blocked response")
            result = "".join(part["text"] for part in candidate["content"]["parts"]
                             if isinstance(part, dict) and "text" in part and not part.get("thought"))
            if not result:
                raise ValueError("No usable output")
            return result
        except (ValueError, UnicodeError, TypeError, KeyError, IndexError, AttributeError):
            raise ProviderError("invalid_output", "Gemini returned an incomplete, blocked, or malformed response; it was not used.") from None


class FixtureClient:
    """Exact predefined test replies, explicitly not a natural-language model."""

    mode = "offline_fixture"
    model = None

    def __init__(self, cases=None):
        if cases is None:
            cases = json.loads((ROOT / "evaluation/cases.json").read_text())
        self.replies = {case["request"]: case["fixture"] for case in cases if case.get("fixture")}

    def generate(self, instructions, request, schema):
        if request not in self.replies:
            raise ProviderError("fixture_unavailable", "Offline demo recognizes only its listed examples. Use AI mode for other requests or edit preferences manually.")
        return json.dumps(self.replies[request])
