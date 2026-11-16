"""Tests for provider registry."""

import pytest

from chasys.providers.litellm_provider import LiteLLMProvider
from chasys.providers.registry import ProviderRegistry


def test_registry_get_provider_with_prefix():
    """Test getting a provider with explicit prefix."""
    registry = ProviderRegistry()
    provider, model = registry.get_provider("openai/gpt-4o")
    assert isinstance(provider, LiteLLMProvider)
    assert provider.name == "openai"
    assert model == "gpt-4o"


def test_registry_get_provider_anthropic():
    """Test getting an Anthropic provider."""
    registry = ProviderRegistry()
    provider, model = registry.get_provider("anthropic/claude-3-5-sonnet-20241022")
    assert isinstance(provider, LiteLLMProvider)
    assert provider.name == "anthropic"
    assert model == "claude-3-5-sonnet-20241022"


def test_registry_get_provider_without_prefix():
    """Test getting a provider without prefix defaults to openai."""
    registry = ProviderRegistry()
    provider, model = registry.get_provider("gpt-4o")
    assert isinstance(provider, LiteLLMProvider)
    assert provider.name == "openai"
    assert model == "gpt-4o"


def test_registry_unknown_provider():
    """Test that unknown provider raises ValueError."""
    registry = ProviderRegistry()
    with pytest.raises(ValueError, match="Unknown provider"):
        registry.get_provider("unknown/model")
