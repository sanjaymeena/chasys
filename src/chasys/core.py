"""Core harness execution loop."""

from collections.abc import AsyncIterator
from enum import StrEnum

from chasys.providers.base import BaseProvider
from chasys.providers.registry import registry
from chasys.types import Message, Response, Role


class HarnessState(StrEnum):
    """Harness lifecycle states."""
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    STOPPED = "stopped"


class Chasys:
    """Core harness for LLM interactions.

    The harness manages the execution loop: send messages → get responses → return results.
    It provides both synchronous and streaming interfaces.

    Example:
        harness = Chasys(provider="openai/gpt-4o")
        response = harness.run("Hello!")
        print(response.content)
    """

    def __init__(
        self,
        provider: str = "openai/gpt-4o",
        system_prompt: str | None = None,
    ):
        """Initialize the harness.

        Args:
            provider: Provider string in format "provider/model" (e.g., "openai/gpt-4o")
            system_prompt: Optional system prompt to set context
        """
        self._state = HarnessState.INITIALIZING
        self._provider: BaseProvider
        self._model: str
        self._messages: list[Message] = []
        self._system_prompt = system_prompt

        # Set up provider
        self._provider, self._model = registry.get_provider(provider)

        # Add system prompt if provided
        if self._system_prompt:
            self._messages.append(Message(role=Role.SYSTEM, content=self._system_prompt))

        self._state = HarnessState.READY

    @property
    def state(self) -> HarnessState:
        """Current harness state."""
        return self._state

    @property
    def messages(self) -> list[Message]:
        """Current conversation history."""
        return self._messages.copy()

    def run(self, user_input: str, **kwargs) -> Response:
        """Run a synchronous completion.

        Args:
            user_input: User message
            **kwargs: Additional arguments passed to the provider

        Returns:
            Response from the LLM
        """
        import asyncio
        return asyncio.run(self.arun(user_input, **kwargs))

    async def arun(self, user_input: str, **kwargs) -> Response:
        """Run an async completion.

        Args:
            user_input: User message
            **kwargs: Additional arguments passed to the provider

        Returns:
            Response from the LLM
        """
        self._state = HarnessState.RUNNING

        # Add user message
        self._messages.append(Message(role=Role.USER, content=user_input))

        # Get response
        response = await self._provider.complete(
            messages=self._messages,
            model=self._model,
            **kwargs,
        )

        # Add assistant response to history
        self._messages.append(Message(role=Role.ASSISTANT, content=response.content))

        self._state = HarnessState.READY
        return response

    async def astream(self, user_input: str, **kwargs) -> AsyncIterator[str]:
        """Stream a completion asynchronously.

        Args:
            user_input: User message
            **kwargs: Additional arguments passed to the provider

        Yields:
            Text chunks as they arrive
        """
        self._state = HarnessState.RUNNING

        # Add user message
        self._messages.append(Message(role=Role.USER, content=user_input))

        # Stream response
        full_content = ""
        async for chunk in self._provider.stream(
            messages=self._messages,
            model=self._model,
            **kwargs,
        ):
            full_content += chunk
            yield chunk

        # Add complete assistant response to history
        self._messages.append(Message(role=Role.ASSISTANT, content=full_content))

        self._state = HarnessState.READY

    def reset(self) -> None:
        """Reset conversation history."""
        self._messages.clear()
        if self._system_prompt:
            self._messages.append(Message(role=Role.SYSTEM, content=self._system_prompt))

    def stop(self) -> None:
        """Stop the harness."""
        self._state = HarnessState.STOPPED
