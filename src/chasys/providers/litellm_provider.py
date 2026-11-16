"""LiteLLM-backed provider implementation."""

from collections.abc import AsyncIterator

import litellm

from chasys.providers.base import BaseProvider
from chasys.types import Message, Response


class LiteLLMProvider(BaseProvider):
    """Provider implementation using LiteLLM for multi-provider support."""

    def __init__(self, provider_prefix: str = "openai"):
        """Initialize the provider.

        Args:
            provider_prefix: Provider prefix (e.g., "openai", "anthropic", "ollama")
        """
        self._provider_prefix = provider_prefix

    @property
    def name(self) -> str:
        """Provider name."""
        return self._provider_prefix

    async def complete(
        self,
        messages: list[Message],
        model: str,
        **kwargs,
    ) -> Response:
        """Get a completion from the LLM via LiteLLM."""
        response = await litellm.acompletion(
            model=model,
            messages=[m.to_dict() for m in messages],
            **kwargs,
        )

        return Response(
            content=response.choices[0].message.content or "",
            model=response.model,
            provider=self.name,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            } if response.usage else None,
            finish_reason=response.choices[0].finish_reason,
        )

    async def stream(
        self,
        messages: list[Message],
        model: str,
        **kwargs,
    ) -> AsyncIterator[str]:
        """Stream a completion from the LLM via LiteLLM."""
        response = await litellm.acompletion(
            model=model,
            messages=[m.to_dict() for m in messages],
            stream=True,
            **kwargs,
        )

        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
