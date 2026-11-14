"""Provider boundaries, semantic guardrails, and real assistant CLI coverage."""

import io
import json
from pathlib import Path
import socket
import subprocess
import sys
import urllib.error

import pytest

from src.assistant import interpret_request, response_schema
from src.catalog import load_catalog
from src.evaluate_assistant import evaluate_case, run_evaluation
from src.llm_client import FixtureClient, GeminiClient, ProviderError, Settings, settings_from_environment


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def catalog():
    return load_catalog()


class ReplyClient:
    mode = "test_fixture"
    model = None

    def __init__(self, reply):
        self.reply = reply
        self.calls = 0

    def generate(self, instructions, request, schema):
        self.calls += 1
        return self.reply


def reply(preferences=None):
    return json.dumps({"preferences": preferences or {"targets": {"energy": .3}},
                       "summary": "Lower energy.", "assumptions": ["Energy target is approximate."]})


def provider_reply(text=None, finish="STOP"):
    return json.dumps({"candidates": [{"finishReason": finish, "content": {"parts": [
        {"text": "Private reasoning must not be returned", "thought": True},
        {"text": text or reply()}]}}]}).encode()


def test_provider_uses_header_schema_fixed_settings_and_one_request():
    requests = []
    def opener(req, timeout):
        requests.append((req, timeout))
        return io.BytesIO(provider_reply())
    client = GeminiClient(Settings("local-test-key"), opener)
    result = client.generate("instructions", "request", {"type": "object"})
    assert result == reply() and "Private reasoning" not in result
    assert len(requests) == 1
    req, timeout = requests[0]
    assert "local-test-key" not in req.full_url
    assert req.get_header("X-goog-api-key") == "local-test-key"
    payload = json.loads(req.data)
    assert payload["generationConfig"]["temperature"] == 0
    assert payload["generationConfig"]["responseJsonSchema"] == {"type": "object"}
    assert timeout == 20


@pytest.mark.parametrize("code,reason,kind", [(400,"API_KEY_INVALID","authentication"),(401,"","authentication"),(403,"","authentication"),(404,"","model_access"),(429,"","quota"),(500,"","provider")])
def test_provider_errors_are_safe_categorized_and_not_retried(code, reason, kind):
    calls = []
    def opener(req, timeout):
        calls.append(1)
        body = json.dumps({"error":{"message":"local-test-key private content", "details":[{"reason":reason}]}}).encode()
        raise urllib.error.HTTPError(req.full_url,code,"private detail",{},io.BytesIO(body))
    with pytest.raises(ProviderError) as caught:
        GeminiClient(Settings("local-test-key"),opener).generate("i","r",{})
    assert caught.value.kind == kind
    assert "local-test-key" not in str(caught.value)
    assert len(calls) == 1


@pytest.mark.parametrize("error,kind", [(socket.timeout(),"timeout"),(urllib.error.URLError("offline"),"network"),(urllib.error.URLError(socket.timeout()),"timeout")])
def test_network_failures_are_bounded(error,kind):
    def opener(req,timeout):
        raise error
    with pytest.raises(ProviderError) as caught:
        GeminiClient(Settings("local-test-key"),opener).generate("i","r",{})
    assert caught.value.kind == kind


@pytest.mark.parametrize("raw", [b"not json",b"{}",b"[]",provider_reply(finish="MAX_TOKENS"),b"x"*65537])
def test_provider_rejects_incomplete_malformed_and_oversized_output(raw):
    with pytest.raises(ProviderError) as caught:
        GeminiClient(Settings("local-test-key"),lambda req,timeout:io.BytesIO(raw)).generate("i","r",{})
    assert caught.value.kind == "invalid_output"


def test_missing_key_never_calls_network():
    def forbidden(*args,**kwargs):
        pytest.fail("Network must not be called")
    with pytest.raises(ProviderError) as caught:
        GeminiClient(Settings(""),forbidden).generate("i","r",{})
    assert caught.value.kind == "missing_credentials"


def test_settings_local_key_overrides_old_google_alias_without_exposing_it(tmp_path):
    path=tmp_path/".env"
    path.write_text('GEMINI_API_KEY="new-local-key"\nGEMINI_TIMEOUT_SECONDS=12\n')
    settings=settings_from_environment({"GOOGLE_API_KEY":"old-key"},path)
    assert settings.api_key == "new-local-key" and settings.timeout == 12
    assert "new-local-key" not in repr(settings)
    assert settings_from_environment({"GEMINI_API_KEY":"explicit-key"},path).api_key == "explicit-key"


@pytest.mark.parametrize("model,timeout", [("../../bad",20),("valid",0),("valid",float("nan")),("valid",46)])
def test_invalid_settings_rejected(model,timeout):
    with pytest.raises(ProviderError):
        Settings("",model,timeout)


@pytest.mark.parametrize("music_request", ["", "  ", "x"*1201, "music\x00"])
def test_bad_input_rejected_before_provider_call(catalog,music_request):
    client=ReplyClient(reply())
    with pytest.raises(ValueError):
        interpret_request(music_request,catalog,client)
    assert client.calls == 0


@pytest.mark.parametrize("raw", ["{}","[]","not json",reply({"targets":{"energy":True}}),reply({"preferred_genres":["imaginary nonexistent genre"]}),json.dumps({"preferences":{"targets":{"energy":.3}},"summary":"x","assumptions":[],"execute":"do things"})])
def test_invalid_model_interpretations_never_reach_ranker(catalog,raw):
    with pytest.raises(ProviderError) as caught:
        interpret_request("Music please",catalog,ReplyClient(raw))
    assert caught.value.kind == "invalid_output"


def test_lyric_guard_changes_overlooked_model_condition_but_preserves_raw_evidence(catalog):
    client=ReplyClient(reply({"preferred_genres":["pop"]}))
    interpretation=interpret_request("Pop with guaranteed no explicit lyrics",catalog,client)
    assert interpretation.preferences.unsupported
    assert interpretation.model_preferences["unsupported"] == []
    case={"id":"guard","request":"Pop with guaranteed no explicit lyrics","expected":{"unsupported":True}}
    evaluated=evaluate_case(case,catalog,client)
    assert not evaluated["checks"]["unsupported_identified_by_model"]
    assert evaluated["checks"]["clarification_blocks_results"]
    assert not evaluated["passed"]  # local guard must not inflate model-quality metrics


def test_fixture_mode_is_labeled_and_does_not_guess_for_new_requests(catalog):
    client=FixtureClient()
    case=json.loads((ROOT/"evaluation/cases.json").read_text())[0]
    result=interpret_request(case["request"],catalog,client)
    assert result.mode == "offline_fixture" and result.model is None
    with pytest.raises(ProviderError,match="only"):
        interpret_request("A completely new music request",catalog,client)


def test_schema_uses_only_actual_catalog_vocabulary(catalog):
    schema=response_schema(catalog.vocabulary)
    actual=schema["properties"]["preferences"]["properties"]["preferred_genres"]["items"]["enum"]
    assert set(actual) == catalog.vocabulary


def test_offline_harness_runs_real_backend_and_cannot_claim_specialization():
    report=run_evaluation()
    assert report["summary"]["specialized"] == {"passed":12,"total":12}
    assert report["mode"] == "offline_fixture" and report["model"] is None
    assert "no measured model behavior" in report["claim_scope"]
    with pytest.raises(ValueError,match="live"):
        run_evaluation(compare=True)


def test_harness_stops_on_unavailable_access(catalog):
    class Unavailable(ReplyClient):
        mode="live"
        def generate(self,*args):
            self.calls+=1
            raise ProviderError("authentication","Invalid access")
    client=Unavailable("")
    report=run_evaluation(mode="live",compare=True,client=client)
    assert client.calls == 1 and len(report["records"]) == 1
    assert report["summary"]["specialized"]["total"] == 0


def test_actual_cli_interprets_fixture_and_requires_explicit_batch_acceptance():
    case=json.loads((ROOT/"evaluation/cases.json").read_text())[0]
    args=[sys.executable,"-m","src.cli","--mode","offline","--request",case["request"],"--json"]
    rejected=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
    assert rejected.returncode == 2 and "--yes" in rejected.stderr
    result=subprocess.run(args+["--yes"],cwd=ROOT,text=True,capture_output=True)
    assert result.returncode == 0,result.stderr
    payload=json.loads(result.stdout)
    assert payload["mode"] == "offline_fixture" and payload["status"] == "ok"
    assert payload["interpretation"]["model"] is None


def test_invalid_key_cannot_leak_through_a_header_exception():
    secret="private key with\nnewline"
    with pytest.raises(ProviderError) as caught:
        Settings(secret)
    assert caught.value.kind=="configuration"
    assert secret not in str(caught.value)
