"""Core types for Chasys."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel


class Role(StrEnum):
    """Message roles."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    """A message in the conversation."""
    role: Role
    content: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API calls."""
        return {"role": self.role.value, "content": self.content}


class Response(BaseModel):
    """Response from the LLM."""
    content: str
    model: str
    provider: str
    usage: dict[str, int] | None = None
    finish_reason: str | None = None
