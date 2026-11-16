# Custom Agentic Harness — Master Plan

> A provider-agnostic, extensible agentic framework built from scratch in Python.
> Designed as a 10-step learning journey, each step producing a working system and a blog post.

---

## Vision

Build an agentic harness **as powerful as Claude Code / OpenAI Codex CLI** — but fully provider-agnostic, fully open-source, and fully understood (every line written by you, no black-box frameworks).

**Dual-mode**: CLI agent for interactive use + importable Python library for programmatic use in other projects.

---

## Design Principles

1. **Provider-agnostic** — Unified interface for any LLM (OpenAI, Anthropic, Google, local via Ollama, etc.). Swap providers with a config change.
2. **From scratch** — No LangChain, no CrewAI. We build the core loop ourselves so we understand every piece. (We *do* use `litellm` for provider normalization — that's infrastructure, not a framework.)
3. **Incremental** — Each step adds one concrete capability. Every step ends with a working, testable system.
4. **Blog-friendly** — Each step maps to one blog post. The code diffs tell the story.
5. **Production-quality** — Proper error handling, logging, testing. Not a toy — something you'd actually use.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    CLI Interface                      │
│              (Rich terminal UI, REPL)                 │
├─────────────────────────────────────────────────────┤
│                  Agent Core Loop                      │
│    (Plan → Act → Observe → Reflect → Repeat)        │
├──────────────┬──────────────┬───────────────────────┤
│   Provider   │    Tool      │    Context             │
│   Abstraction│    Registry  │    Manager             │
│              │              │                        │
│  ┌─────────┐ │ ┌──────────┐ │ ┌──────────────────┐  │
│  │ OpenAI  │ │ │ file_read│ │ │ Message History  │  │
│  │Anthropic│ │ │ shell    │ │ │ Token Counter    │  │
│  │ Ollama  │ │ │ search   │ │ │ Summarizer       │  │
│  │ Gemini  │ │ │ custom.. │ │ │ Memory Store     │  │
│  └─────────┘ │ └──────────┘ │ └──────────────────┘  │
├──────────────┴──────────────┴───────────────────────┤
│              Safety & Approval Layer                  │
│         (Permission modes, sandboxing, audit)        │
├─────────────────────────────────────────────────────┤
│           Observability (traces, costs, evals)        │
└─────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Language | Python 3.11+ | Richest LLM ecosystem, fast iteration |
| LLM calls | `litellm` | Unified interface for 100+ providers |
| CLI UI | `rich` + `prompt_toolkit` | Beautiful terminal output + input handling |
| Config | `pydantic-settings` + `.env` | Type-safe config with env overrides |
| Testing | `pytest` + `pytest-asyncio` | Standard, async support |
| Logging | `structlog` | Structured JSON logs, great for observability |
| Packaging | `pyproject.toml` + `uv` | Modern Python packaging |
| Type hints | Strict `mypy` | Catch bugs early |

---

## The 10 Steps

### Step 1: The Heartbeat — Agent Execution Loop + Provider Abstraction
**Blog Title**: *"Building an AI Agent from Scratch — Step 1: The Heartbeat"*

**Core Technical Capabilities:**
- Agent execution loop (send → receive → process cycle)
- Multi-provider LLM abstraction (unified interface for any LLM)
- Streaming responses (real-time token delivery)
- Message handling (unified message format across providers)
- CLI/REPL interface (interactive terminal chat)
- Lifecycle state management (initializing, running, waiting, stopped)

**What we build:**
- Provider abstraction layer (protocol/interface for any LLM)
- Basic agent loop: send message → get response → print it
- Interactive REPL (chat with the model in terminal)
- Support for OpenAI + Anthropic (via litellm)
- Programmatic API: `agent = Agent(provider="anthropic/claude-sonnet-4-20250514"); agent.run("Hello")`

**Key concepts:** Provider protocol, unified message format, async LLM calls, streaming responses, agent lifecycle.

**Deliverable:** A chat REPL that works with any provider. Type a message, get a response. Switch providers with `--provider anthropic`.

**Files:**
```
src/agent_harness/
├── __init__.py
├── cli.py              # CLI entry point
├── agent.py            # Core agent loop
├── providers/
│   ├── __init__.py
│   ├── base.py         # Provider protocol (ABC)
│   ├── litellm_provider.py  # litellm-backed provider
│   └── registry.py     # Provider discovery
├── types.py            # Message, Role, Response types
└── config.py           # Settings (API keys, defaults)
```

---

### Step 2: Hands — Tool System + First Tools
**Blog Title**: *"Building an AI Agent from Scratch — Step 2: Giving It Hands"*

**Core Technical Capabilities:**
- Tool registry (centralized tool discovery and management)
- JSON Schema generation (automatic schema from tool definitions)
- Function calling protocol (provider-agnostic tool invocation)
- Tool dispatch (match LLM tool calls → execute → return results)
- Input validation (validate tool arguments against schemas)
- Async execution (concurrent tool calls)
- Error handling (graceful failure, error reporting to LLM)

**What we build:**
- Tool definition system (decorators or dataclasses to define tools)
- Tool registry (discover, validate, serialize tool schemas)
- Tool execution engine (match LLM tool calls → execute → return results)
- First tools: `calculator`, `current_time`, `echo`
- JSON Schema generation for tool definitions (so any provider can use them)

**Key concepts:** Function calling / tool use protocol, JSON Schema, tool result formatting, async execution, error handling.

**Deliverable:** Agent can now use tools. Ask it "what is 234 * 567?" and it calls the calculator. The tool system is provider-agnostic — works with OpenAI function calling, Anthropic tool use, etc.

**Files added:**
```
src/agent_harness/
├── tools/
│   ├── __init__.py
│   ├── base.py         # Tool protocol, ToolResult
│   ├── registry.py     # Tool registration + lookup
│   ├── executor.py     # Tool execution engine
│   └── builtin/
│       ├── calculator.py
│       ├── datetime_tool.py
│       └── echo.py
```

---

### Step 3: Code Agent — File & Shell Tools
**Blog Title**: *"Building an AI Agent from Scratch — Step 3: Making It a Code Agent"*

**Core Technical Capabilities:**
- File read/write/edit tools (with line numbers, targeted replacement)
- Shell execution (bash commands with timeout, output capture)
- Grep/glob search (regex content search, pattern file discovery)
- Workspace management (working directory tracking, path safety)
- Git integration (status, diff, commit, branch operations)

**What we build:**
- `read_file` tool — read file contents with line numbers
- `write_file` tool — create/overwrite files
- `edit_file` tool — targeted string replacement in files
- `shell` tool — execute bash commands with timeout
- `list_files` / `glob` tool — discover files by pattern
- `grep_search` tool — search file contents with regex
- `git_*` tools — basic git operations (status, diff, commit)
- Safety: path validation (no escaping working directory)

**Key concepts:** Code agent tool design, filesystem safety, command execution, output truncation, git workflows.

**Deliverable:** Agent can now read, write, and search files, and run shell commands. Ask it to "create a Python script that fetches weather" and it does.

**Files added:**
```
src/agent_harness/tools/builtin/
├── file_read.py
├── file_write.py
├── file_edit.py
├── shell.py
├── file_search.py     # glob + grep
└── safety.py          # Path validation, sandboxing
```

---

### Step 4: Guardrails — Safety & Approval System
**Blog Title**: *"Building an AI Agent from Scratch — Step 4: Guardrails"*

**Core Technical Capabilities:**
- Permission policies (per-tool, per-path, per-command rules)
- Approval modes (yolo, normal, strict — configurable autonomy)
- Sandbox isolation (restricted execution environment)
- Pre/post-tool hooks (intercept and validate before/after execution)
- Audit logging (complete execution trail with inputs/outputs)

**What we build:**
- Permission levels: `auto`, `suggest`, `approve` per tool
- Human-in-the-loop approval prompts (show diff, approve/deny/edit)
- Approval modes: `yolo` (auto-approve all), `normal` (approve writes/shell), `strict` (approve everything)
- Sandbox isolation (configurable allowed/denied paths, command blocklist)
- Pre-tool hooks (validate inputs, block dangerous operations)
- Post-tool hooks (log results, trigger notifications)
- Audit log of all tool executions with inputs/outputs
- Dangerous command detection (rm -rf, force push, etc.)

**Key concepts:** Human-in-the-loop AI, permission models, sandbox isolation, hook patterns, audit trails.

**Deliverable:** Agent asks before doing dangerous things. You can set `--approval strict` for maximum safety or `--approval yolo` for full autonomy. Every action is logged.

**Files added:**
```
src/agent_harness/
├── safety/
│   ├── __init__.py
│   ├── permissions.py   # Permission levels, modes
│   ├── approval.py      # Human approval prompts
│   ├── audit.py         # Execution audit log
│   └── guards.py        # Dangerous command detection
```

---

### Step 5: Memory Palace — Context Management
**Blog Title**: *"Building an AI Agent from Scratch — Step 5: Memory Palace"*

**Core Technical Capabilities:**
- Token accounting (per-provider token counting and tracking)
- Context window management (sliding window, priority-based dropping)
- Prompt assembly (dynamic system prompt construction)
- Compaction (compress old messages to free tokens)
- Summarization (LLM-based conversation summarization)
- Session persistence (save/restore conversation state)

**What we build:**
- Token counting (per-provider tokenizer awareness)
- Context window management (sliding window, drop oldest messages)
- Conversation summarization (summarize old messages to free tokens)
- Prompt assembly (dynamic system prompts with context injection)
- Message compaction (truncate, summarize, or drop low-priority messages)
- Session persistence (save/restore conversation state to disk)
- Message role management (user, assistant, tool, system)
- Multi-turn tool call chains (tool call → result → continue)

**Key concepts:** Context windows, token economics, prompt assembly, message compaction, summarization strategies, session persistence.

**Deliverable:** Agent can have long conversations without hitting context limits. Old messages get summarized. System prompt adapts to the current task.

**Files added:**
```
src/agent_harness/
├── context/
│   ├── __init__.py
│   ├── token_counter.py  # Per-provider token counting
│   ├── window.py         # Context window management
│   ├── summarizer.py     # Message summarization
│   └── system_prompt.py  # Dynamic system prompt builder
```

---

### Step 6: Inner Monologue — Extended Thinking & Planning
**Blog Title**: *"Building an AI Agent from Scratch — Step 6: Inner Monologue"*

**Core Technical Capabilities:**
- Task decomposition (break complex tasks into subtasks)
- Planning (generate execution plans with steps)
- Scratchpad (agent's notebook for notes and intermediate results)
- Goal tracking (set goals, track progress, report completion)
- Execution checkpoints (save/restore execution state)
- Reflection (evaluate own output, identify mistakes)
- Replanning (adjust plan based on new information or failures)

**What we build:**
- Scratchpad / thinking tool (agent can write notes to itself)
- Plan-and-execute pattern (make a plan, then execute steps)
- Task decomposition (break complex requests into manageable subtasks)
- Execution checkpoints (save progress, resume after failures)
- Self-reflection loop (evaluate own output, retry if needed)
- Replanning (adjust plan when steps fail or new info emerges)
- Goal tracking (set goals, track progress, report completion)
- Extended thinking integration (Anthropic thinking, OpenAI reasoning)
- Structured output parsing (get JSON responses reliably)

**Key concepts:** Task decomposition, plan-and-execute, execution checkpoints, self-reflection, replanning, meta-cognition patterns.

**Deliverable:** Agent can now plan before acting, reflect on its work, and correct mistakes. Ask it to "refactor the auth module" and it makes a plan first, then executes step by step.

**Files added:**
```
src/agent_harness/
├── thinking/
│   ├── __init__.py
│   ├── scratchpad.py    # Agent's notebook
│   ├── planner.py       # Plan generation + execution
│   ├── reflection.py    # Self-evaluation loop
│   ├── goals.py         # Goal tracking
│   └── structured.py    # Structured output parsing
```

---

### Step 7: Team of Agents — Sub-Agent Delegation
**Blog Title**: *"Building an AI Agent from Scratch — Step 7: Team of Agents"*

**Core Technical Capabilities:**
- Subagent spawning (create child agents with specific roles)
- Task delegation (assign work to specialized agents)
- Isolated contexts (each agent has its own conversation history)
- Parallel execution (run multiple sub-agents concurrently)
- Orchestration (coordinate multi-agent workflows)
- Result aggregation (collect and merge sub-agent outputs)

**What we build:**
- Sub-agent spawning (create child agents with specific roles)
- Message passing between agents (parent ↔ child)
- Isolated contexts (each sub-agent has its own conversation)
- Parallel execution (run multiple sub-agents concurrently)
- Orchestration patterns (sequential, parallel, hierarchical)
- Result aggregation (collect and merge sub-agent outputs)
- Agent roles/specializations (researcher, coder, reviewer)
- Worktree isolation (each sub-agent gets its own git worktree for code changes)

**Key concepts:** Multi-agent systems, delegation patterns, isolated contexts, parallel execution, orchestration, result merging.

**Deliverable:** Main agent can delegate work to specialized sub-agents. "Research the best Python HTTP libraries, then write a comparison script" — one agent researches, another codes, results merge.

**Files added:**
```
src/agent_harness/
├── agents/
│   ├── __init__.py
│   ├── base.py          # Base agent class (refactored from Step 1)
│   ├── spawner.py       # Sub-agent creation
│   ├── messenger.py     # Inter-agent communication
│   ├── pool.py          # Parallel execution pool
│   └── roles.py         # Predefined agent roles
```

---

### Step 8: Long-Term Memory — Persistent Knowledge
**Blog Title**: *"Building an AI Agent from Scratch — Step 8: Long-Term Memory"*

**Core Technical Capabilities:**
- Persistent memory storage (save/load facts across sessions)
- Episodic memory (specific events, conversations, decisions)
- Semantic memory (general knowledge, facts, preferences)
- Embeddings (vector representations for semantic search)
- Retrieval (find relevant memories for current context)
- Memory consolidation (merge, update, and prune memories)
- Cross-session recall (access memories from any session)

**What we build:**
- Persistent memory store (save/load facts across sessions)
- Episodic memory (specific events, decisions, conversation highlights)
- Semantic memory (general knowledge, user preferences, project facts)
- Embedding-based retrieval (vector search for relevant memories)
- Memory types: facts, preferences, decisions, references, events
- Memory consolidation (merge duplicates, update outdated info, prune irrelevant)
- Auto-memory (agent decides what to remember)
- Storage: local SQLite + vector index, no external DB needed

**Key concepts:** Episodic vs semantic memory, embeddings, vector retrieval, memory consolidation, cross-session persistence.

**Deliverable:** Agent remembers things across sessions. Tell it "I prefer TypeScript" once, and it knows next time. It remembers project decisions, deadlines, and your preferences.

**Files added:**
```
src/agent_harness/
├── memory/
│   ├── __init__.py
│   ├── store.py         # Memory storage (JSON/SQLite)
│   ├── retriever.py     # Memory search + ranking
│   ├── types.py         # Memory types + schema
│   ├── auto_memory.py   # Auto-decide what to remember
│   └── inject.py        # Inject memories into context
```

---

### Step 9: Universal Tools — MCP Integration
**Blog Title**: *"Building an AI Agent from Scratch — Step 9: Universal Tools"*

**Core Technical Capabilities:**
- MCP client implementation (Model Context Protocol)
- Server discovery (find and connect to MCP servers)
- Tool/resource integration (use tools and read resources from servers)
- Authentication (handle auth for MCP servers)
- Connection lifecycle (connect, reconnect, disconnect gracefully)

**What we build:**
- MCP (Model Context Protocol) client implementation
- Server discovery (auto-discover available MCP servers)
- Connect to any MCP server (filesystem, databases, APIs, etc.)
- Dynamic tool discovery (list tools from MCP servers at runtime)
- Tool call translation (our tool format ↔ MCP tool format)
- Resource access (read resources from MCP servers)
- Authentication handling (API keys, OAuth, etc.)
- Connection lifecycle management (connect, reconnect, health checks)
- Built-in MCP servers: filesystem, GitHub, web fetch
- Configuration for MCP servers (JSON config file)

**Key concepts:** Model Context Protocol, tool interoperability, dynamic tool loading, protocol translation, connection lifecycle, ecosystem integration.

**Deliverable:** Agent can connect to any MCP server and instantly gain new tools. Want database access? Connect a Postgres MCP server. Want GitHub? Connect the GitHub MCP server. Infinite extensibility.

**Files added:**
```
src/agent_harness/
├── mcp/
│   ├── __init__.py
│   ├── client.py        # MCP client implementation
│   ├── transport.py     # stdio + SSE transport
│   ├── adapter.py       # MCP ↔ our tool format
│   ├── discovery.py     # Dynamic tool discovery
│   └── config.py        # MCP server configuration
```

---

### Step 10: Dashboard & Skills — Observability, Evaluation + Reusable Workflows
**Blog Title**: *"Building an AI Agent from Scratch — Step 10: Dashboard & Skills"*

**Core Technical Capabilities:**
- Skill discovery/loading (find and load reusable workflows)
- Reusable workflows (parameterized, composable agent workflows)
- Execution tracing (every LLM call, tool call, decision logged)
- Token/cost tracking (per-call and cumulative cost by provider/model)
- Evaluations (define tasks, run agent, score results)
- Debugging (trace replay, step-through execution)

**What we build:**
- **Skills system:**
  - Skill discovery (find skills in local directories or registries)
  - Skill loading (load parameterized workflows as reusable commands)
  - Skill composition (combine skills into larger workflows)
  - Built-in skills: code review, refactoring, testing, documentation
- **Observability:**
  - Execution tracing (every LLM call, tool call, decision logged)
  - Cost tracking (per-call and cumulative cost by provider/model)
  - Performance metrics (latency, token usage, tool call counts)
  - Trace export (JSON, or export to LangSmith/Arize/etc.)
  - Debug replay (replay a trace to see what the agent did)
- **Evaluation:**
  - Evaluation framework (define tasks, run agent, score results)
  - Benchmark suites (compare providers, prompts, strategies)
  - Summary dashboard (terminal-based or simple web UI)

**Key concepts:** Skill systems, reusable workflows, observability, cost optimization, evaluation-driven design, tracing, benchmarking.

**Deliverable:** Full visibility into what the agent is doing, how much it costs, and how well it performs. Plus a library of reusable skills that extend the agent's capabilities. Run eval suites to compare providers, prompts, and strategies.

**Files added:**
```
src/agent_harness/
├── skills/
│   ├── __init__.py
│   ├── discovery.py   # Skill discovery
│   ├── loader.py      # Skill loading + execution
│   ├── registry.py    # Skill registration
│   └── builtin/       # Built-in skills
│       ├── code_review.py
│       ├── refactor.py
│       └── test_gen.py
├── observability/
│   ├── __init__.py
│   ├── tracer.py        # Execution tracing
│   ├── costs.py         # Cost tracking
│   ├── metrics.py       # Performance metrics
│   ├── eval/
│   │   ├── runner.py    # Eval suite runner
│   │   ├── tasks.py     # Task definitions
│   │   └── scorers.py   # Result scoring
│   └── export.py        # Trace export
```

---

## Project Structure (Final)

```
custom-agent-harness/
├── PLAN.md                    # This file
├── README.md                  # Project overview + quickstart
├── pyproject.toml             # Project config + dependencies
├── .env.example               # Environment variables template
├── src/
│   └── agent_harness/
│       ├── __init__.py        # Public API exports
│       ├── cli.py             # CLI entry point (Rich + prompt_toolkit)
│       ├── agent.py           # Core agent loop
│       ├── types.py           # Shared types (Message, Role, etc.)
│       ├── config.py          # Settings management
│       ├── providers/         # Step 1: LLM provider abstraction
│       ├── tools/             # Step 2-3: Tool system + built-in tools
│       ├── safety/            # Step 4: Permissions + approval
│       ├── context/           # Step 5: Context window management
│       ├── thinking/          # Step 6: Planning + reflection
│       ├── agents/            # Step 7: Multi-agent delegation
│       ├── memory/            # Step 8: Persistent memory
│       ├── mcp/               # Step 9: MCP integration
│       ├── skills/            # Step 10: Reusable workflows
│       └── observability/     # Step 10: Tracing + evals
├── tests/
│   ├── unit/                  # Unit tests per module
│   ├── integration/           # Integration tests (real LLM calls)
│   └── evals/                 # Evaluation tasks
└── docs/
    ├── blog/                  # Blog post drafts
    └── api/                   # API documentation
```

---

## Blog Series Structure

Each blog post follows this template:

1. **Hook** — What we're building and why (1 paragraph)
2. **Context** — What we built in the previous step (2-3 sentences)
3. **Concept** — The key idea behind this step (explained simply)
4. **Implementation** — Code walkthrough with explanations
5. **Demo** — Screenshots/terminal output showing it working
6. **What's Next** — Teaser for the next step

**Posting cadence:** One post per step, published as each step is completed.

---

## Getting Started (After Step 1)

```bash
# Install
git clone https://github.com/yourusername/custom-agent-harness.git
cd custom-agent-harness
pip install -e ".[dev]"

# Configure
cp .env.example .env
# Add your API keys to .env

# Run (CLI mode)
agent-harness --provider anthropic

# Use (programmatic)
from agent_harness import Agent

agent = Agent(provider="openai/gpt-4o")
response = agent.run("Hello, world!")
print(response)
```

---

## Success Criteria

By the end of Step 10, the harness should:

- [ ] Work with any LLM provider (OpenAI, Anthropic, Google, local)
- [ ] Read/write files, run commands, search code, use git
- [ ] Ask before doing dangerous things (approval modes, sandbox)
- [ ] Handle long conversations without losing context (compaction, summarization)
- [ ] Plan, reflect, replan, and self-correct
- [ ] Delegate work to sub-agents with isolated contexts
- [ ] Remember things across sessions (episodic + semantic memory)
- [ ] Connect to any MCP server for infinite tool extensibility
- [ ] Load and run reusable skills (code review, refactoring, testing)
- [ ] Show exactly what it's doing and how much it costs (tracing, evals)
- [ ] Be usable as both a CLI tool and a Python library
- [ ] Have 10 blog posts explaining every decision

---

## References & Inspiration

- **Claude Code** — Anthropic's agentic coding tool (architecture, tool design, approval modes)
- **OpenAI Codex CLI** — OpenAI's terminal agent (provider patterns, tool execution)
- **Aider** — Open-source coding agent (file editing patterns, git integration)
- **LiteLLM** — Provider normalization library (we use this, not build it)
- **Model Context Protocol** — Anthropic's open protocol for tool interoperability
- **OpenAI Agents SDK** — Multi-agent patterns (handoffs, guardrails)
- **LangGraph** — State machine agent patterns (we build simpler, but learn from it)

---

## Next Action

**Start with Step 1**: Set up the project structure, implement the provider abstraction, build the basic agent loop, and create the CLI REPL.
