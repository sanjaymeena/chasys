"""Tests for core harness."""

from unittest.mock import AsyncMock

import pytest

from chasys.core import Chasys, HarnessState
from chasys.types import Message, Response, Role


def test_harness_initialization():
    """Test harness initializes correctly."""
    harness = Chasys(provider="openai/gpt-4o")
    assert harness.state == HarnessState.READY
    assert len(harness.messages) == 0


def test_harness_with_system_prompt():
    """Test harness with system prompt."""
    harness = Chasys(provider="openai/gpt-4o", system_prompt="You are helpful.")
    assert harness.state == HarnessState.READY
    assert len(harness.messages) == 1
    assert harness.messages[0].role == Role.SYSTEM
    assert harness.messages[0].content == "You are helpful."


def test_harness_reset():
    """Test resetting conversation history."""
    harness = Chasys(provider="openai/gpt-4o", system_prompt="You are helpful.")
    harness._messages.append(Message(role=Role.USER, content="Hello"))
    assert len(harness.messages) == 2

    harness.reset()
    assert len(harness.messages) == 1
    assert harness.messages[0].role == Role.SYSTEM


def test_harness_stop():
    """Test stopping the harness."""
    harness = Chasys(provider="openai/gpt-4o")
    assert harness.state == HarnessState.READY

    harness.stop()
    assert harness.state == HarnessState.STOPPED


@pytest.mark.asyncio
async def test_harness_arun():
    """Test async run with mocked provider."""
    harness = Chasys(provider="openai/gpt-4o")

    # Mock the provider
    mock_response = Response(
        content="Hello!",
        model="gpt-4o",
        provider="openai",
        usage={"prompt_tokens": 5, "completion_tokens": 2, "total_tokens": 7},
    )
    harness._provider.complete = AsyncMock(return_value=mock_response)

    response = await harness.arun("Hi")

    assert response.content == "Hello!"
    assert len(harness.messages) == 2  # user + assistant
    assert harness.messages[0].role == Role.USER
    assert harness.messages[1].role == Role.ASSISTANT
    assert harness.state == HarnessState.READY


@pytest.mark.asyncio
async def test_harness_astream():
    """Test async streaming with mocked provider."""
    harness = Chasys(provider="openai/gpt-4o")

    # Mock the provider stream
    async def mock_stream(*args, **kwargs):
        for chunk in ["Hello", " ", "world", "!"]:
            yield chunk

    harness._provider.stream = mock_stream

    chunks = []
    async for chunk in harness.astream("Hi"):
        chunks.append(chunk)

    assert chunks == ["Hello", " ", "world", "!"]
    assert len(harness.messages) == 2
    assert harness.messages[1].content == "Hello world!"
