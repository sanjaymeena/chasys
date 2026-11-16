"""Chasys — The chassis for AI applications.

A provider-agnostic, extensible harness for building AI applications.

Example:
    from chasys import Chasys

    harness = Chasys(provider="openai/gpt-4o")
    response = harness.run("Hello!")
    print(response.content)
"""

from chasys.config import settings
from chasys.core import Chasys, HarnessState
from chasys.types import Message, Response, Role

__version__ = "0.1.0"
__all__ = ["Chasys", "HarnessState", "Message", "Response", "Role", "settings"]
