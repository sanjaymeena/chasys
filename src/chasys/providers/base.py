"""Base provider protocol."""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from chasys.types import Message, Response


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""
        ...

    @abstractmethod
    async def complete(
        self,
        messages: list[Message],
        model: str,
        **kwargs,
    ) -> Response:
        """Get a completion from the LLM.

        Args:
            messages: List of messages in the conversation
            model: Model identifier (e.g., "gpt-4o", "claude-3-5-sonnet-20241022")
            **kwargs: Additional provider-specific arguments

        Returns:
            Response from the LLM
        """
        ...

    @abstractmethod
    async def stream(
        self,
        messages: list[Message],
        model: str,
        **kwargs,
    ) -> AsyncIterator[str]:
        """Stream a completion from the LLM.

        Args:
            messages: List of messages in the conversation
            model: Model identifier
            **kwargs: Additional provider-specific arguments

        Yields:
            Text chunks as they arrive
        """
        ...
