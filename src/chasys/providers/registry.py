"""Provider registry for discovery and instantiation."""

from chasys.providers.base import BaseProvider
from chasys.providers.litellm_provider import LiteLLMProvider


class ProviderRegistry:
    """Registry for LLM providers."""

    def __init__(self):
        self._providers: dict[str, type[BaseProvider]] = {
            "openai": LiteLLMProvider,
            "anthropic": LiteLLMProvider,
            "ollama": LiteLLMProvider,
            "google": LiteLLMProvider,
        }

    def get_provider(self, model_string: str) -> tuple[BaseProvider, str]:
        """Get a provider instance for the given model string.

        Args:
            model_string: Model string in format "provider/model" (e.g., "openai/gpt-4o")

        Returns:
            Tuple of (provider instance, model name)
        """
        if "/" in model_string:
            provider_name, model = model_string.split("/", 1)
        else:
            provider_name = "openai"
            model = model_string

        provider_class = self._providers.get(provider_name)
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_name}")

        return provider_class(provider_prefix=provider_name), model


# Global registry instance
registry = ProviderRegistry()
