# Custom Agent Harness

> A provider-agnostic, extensible agentic framework built from scratch in Python.

A powerful AI agent harness — think Claude Code or OpenAI Codex CLI — but **fully provider-agnostic** and **fully open-source**. Every line is written from scratch so you understand exactly how it works.

## Features

- 🔄 **Provider-agnostic** — Works with OpenAI, Anthropic, Google, Ollama, and 100+ more via LiteLLM
- 🛠️ **Extensible tools** — File I/O, shell execution, search, git, and a plugin system for custom tools
- 🛡️ **Safety first** — Human-in-the-loop approval, permission modes, sandbox isolation, audit logging
- 🧠 **Smart context** — Token-aware context management, compaction, summarization, session persistence
- 💭 **Extended thinking** — Task decomposition, planning, scratchpad, self-reflection, replanning
- 🤝 **Multi-agent** — Delegate work to specialized sub-agents with isolated contexts, parallel execution
- 💾 **Persistent memory** — Episodic + semantic memory with embeddings, cross-session recall
- 🔌 **MCP support** — Connect to any Model Context Protocol server for infinite tool extensibility
- 🎯 **Skills system** — Reusable workflows (code review, refactoring, testing) that extend the agent
- 📊 **Observability** — Full tracing, cost tracking, evaluation framework, debug replay

## Quick Start

```bash
# Install
pip install -e ".[dev]"

# Configure your API keys
cp .env.example .env
# Edit .env with your API keys

# Run the agent
agent-harness --provider anthropic
```

## Programmatic Usage

```python
from agent_harness import Agent

# Create an agent with any provider
agent = Agent(provider="openai/gpt-4o")

# Run a simple query
response = agent.run("What is the capital of France?")

# Run with tools
agent = Agent(
    provider="anthropic/claude-sonnet-4-20250514",
    tools=["file_read", "file_write", "shell"],
)
response = agent.run("Create a hello.py script")
```

## Blog Series

This project is built as a 10-step learning journey. Each step adds one concrete capability and maps to a blog post:

| Step | Title | What You Build |
|------|-------|----------------|
| 1 | The Heartbeat | Agent execution loop, multi-provider abstraction, streaming, lifecycle state |
| 2 | Giving It Hands | Tool registry, JSON schemas, function calling, async execution |
| 3 | Making It a Code Agent | File read/write/edit, shell, grep/glob, workspace + git integration |
| 4 | Guardrails | Permission policies, approval modes, sandbox, pre/post hooks, audit |
| 5 | Memory Palace | Token accounting, context window, prompt assembly, compaction, session persistence |
| 6 | Inner Monologue | Task decomposition, planning, checkpoints, reflection, replanning |
| 7 | Team of Agents | Subagent spawning, isolated contexts, parallel execution, orchestration |
| 8 | Long-Term Memory | Episodic/semantic memory, embeddings, retrieval, consolidation |
| 9 | Universal Tools | MCP client, server discovery, auth, connection lifecycle |
| 10 | Dashboard & Skills | Skill discovery/loading, reusable workflows, tracing, cost tracking, evals |

See [PLAN.md](./PLAN.md) for the full architecture and step-by-step breakdown.

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with type checking
mypy src/

# Run with linting
ruff check src/
```

## Architecture

```
┌─────────────────────────────────────────────┐
│              CLI / Programmatic API          │
├─────────────────────────────────────────────┤
│              Agent Core Loop                 │
│     (Plan → Act → Observe → Reflect)        │
├──────────┬──────────┬───────────────────────┤
│ Provider │  Tools   │  Context Manager      │
│ Abstraction│ Registry│  + Memory             │
├──────────┴──────────┴───────────────────────┤
│         Safety & Approval Layer              │
├─────────────────────────────────────────────┤
│      Observability (traces, costs, evals)    │
└─────────────────────────────────────────────┘
```

## License

MIT
