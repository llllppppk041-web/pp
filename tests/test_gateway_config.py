import os
from unittest.mock import patch

import pytest

from backend.app.services.provider_gateway import (
    LocalBrainUnavailable,
    _openai_config,
    provider_runtime_status,
)


def test_loopback_http_is_allowed_without_api_key():
    with patch.dict(os.environ, {
        "OMNI_OPENAI_BASE_URL": "http://127.0.0.1:8080/v1",
        "OMNI_OPENAI_API_KEY": "",
        "OMNI_OPENAI_MODEL": "bitnet-local",
    }, clear=False):
        config = _openai_config()
    assert config["is_loopback"] == "true"
    assert config["model"] == "bitnet-local"
    assert config["api_key"] == ""


@pytest.mark.parametrize("url", [
    "http://example.com/v1",
    "http://192.168.1.2:8080/v1",
    "http://example.org/v1",
])
def test_non_loopback_http_is_rejected(url):
    with patch.dict(os.environ, {
        "OMNI_OPENAI_BASE_URL": url,
        "OMNI_OPENAI_API_KEY": "test-only-not-a-real-key",
    }, clear=False):
        with pytest.raises(LocalBrainUnavailable):
            _openai_config()


def test_remote_https_requires_server_side_key():
    with patch.dict(os.environ, {
        "OMNI_OPENAI_BASE_URL": "https://provider.example/v1",
        "OMNI_OPENAI_API_KEY": "",
    }, clear=False):
        with pytest.raises(LocalBrainUnavailable):
            _openai_config()


def test_remote_https_is_allowed_with_key():
    with patch.dict(os.environ, {
        "OMNI_OPENAI_BASE_URL": "https://provider.example/v1",
        "OMNI_OPENAI_API_KEY": "test-only-not-a-real-key",
        "OMNI_OPENAI_MODEL": "test-model",
    }, clear=False):
        config = _openai_config()
    assert config["is_loopback"] == "false"
    assert config["base_url"] == "https://provider.example/v1"


def test_status_never_returns_secret_or_complete_url():
    with patch.dict(os.environ, {
        "OMNI_AI_PROVIDER": "openai_compatible",
        "OMNI_OPENAI_BASE_URL": "https://provider.example/private-path/v1",
        "OMNI_OPENAI_API_KEY": "test-only-secret-value",
        "OMNI_OPENAI_MODEL": "test-model",
    }, clear=False):
        status = provider_runtime_status()
    rendered = repr(status)
    assert "test-only-secret-value" not in rendered
    assert "provider.example" not in rendered
    assert status["secrets_exposed"] is False
