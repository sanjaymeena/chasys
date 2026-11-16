"""Tests for core types."""

from chasys.types import Message, Response, Role


def test_message_creation():
    """Test creating a message."""
    msg = Message(role=Role.USER, content="Hello!")
    assert msg.role == Role.USER
    assert msg.content == "Hello!"


def test_message_to_dict():
    """Test converting message to dictionary."""
    msg = Message(role=Role.ASSISTANT, content="Hi there!")
    d = msg.to_dict()
    assert d == {"role": "assistant", "content": "Hi there!"}


def test_response_creation():
    """Test creating a response."""
    response = Response(
        content="Hello!",
        model="gpt-4o",
        provider="openai",
        usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        finish_reason="stop",
    )
    assert response.content == "Hello!"
    assert response.model == "gpt-4o"
    assert response.provider == "openai"
    assert response.usage["total_tokens"] == 15


def test_role_enum():
    """Test Role enum values."""
    assert Role.SYSTEM.value == "system"
    assert Role.USER.value == "user"
    assert Role.ASSISTANT.value == "assistant"
