# Blog Series: Building an AI Agent from Scratch

> A 10-part series documenting the journey of building a provider-agnostic agentic harness from zero.

---

## Series Overview

In this series, we build a complete AI agent harness from scratch — no frameworks, no magic. By the end, we have a tool as capable as Claude Code or OpenAI Codex CLI, but fully open-source and provider-agnostic.

Each post covers one concrete step: what we're building, why it matters, the key concepts, and the implementation. Every post ends with a working system you can run.

**Target audience:** Developers who want to understand how AI agents actually work under the hood.

---

## Post 1: The Heartbeat — Agent Execution Loop + Provider Abstraction

**Hook:** Every agent starts with a single heartbeat — the loop that sends a message to an LLM and gets a response back. But what if you want to switch between OpenAI, Anthropic, and local models without rewriting your code?

**What we build:**
- Provider abstraction layer (unified interface for any LLM)
- Basic agent loop: message → LLM → response
- Streaming responses (real-time token delivery)
- Lifecycle state management (initializing, running, waiting, stopped)
- Interactive CLI REPL
- OpenAI + Anthropic support via LiteLLM

**Key concepts:** Provider protocol, unified message format, async LLM calls, streaming, agent lifecycle.

**Code diff:** ~300 lines. Core files: `agent.py`, `providers/`, `types.py`, `cli.py`.

**Demo:** Terminal screenshot showing a conversation with `--provider anthropic` and `--provider openai`.

---

## Post 2: Giving It Hands — Tool System + First Tools

**Hook:** An LLM that can only chat is like a brain in a jar. Let's give it hands — the ability to call tools, get results, and act on the world.

**What we build:**
- Tool definition system (decorators, JSON Schema generation)
- Tool registry and execution engine
- First tools: calculator, datetime, echo
- Provider-agnostic tool calling (works with OpenAI function calling, Anthropic tool use)

**Key concepts:** Function calling protocols, JSON Schema, tool result formatting, error handling.

**Code diff:** ~400 lines. Core files: `tools/`, updates to `agent.py` for tool loop.

**Demo:** Agent solving "what is 234 * 567 + 891?" by calling the calculator tool.

---

## Post 3: Making It a Code Agent — File & Shell Tools

**Hook:** Now that our agent has hands, let's make it a coder. We'll give it the ability to read files, write code, search codebases, run shell commands, and even use git — turning it into a full coding agent.

**What we build:**
- File tools: read, write, edit, list, search
- Shell tool with timeout and output truncation
- Grep/glob search (regex content search, pattern file discovery)
- Git integration (status, diff, commit, branch operations)
- Workspace management (working directory tracking, path safety)
- Path safety (no escaping working directory)

**Key concepts:** Code agent tool design, filesystem safety, output management, git workflows, workspace isolation.

**Code diff:** ~500 lines. Core files: `tools/builtin/`, `safety.py`.

**Demo:** Agent creating a Python project from scratch — writes files, runs tests, commits changes, fixes bugs.

---

## Post 4: Guardrails — Safety & Approval System

**Hook:** An agent that can run shell commands and edit files is powerful — and dangerous. Let's add guardrails: permission policies, sandbox isolation, pre/post-tool hooks, approval modes, and audit logs.

**What we build:**
- Permission policies (per-tool, per-path, per-command rules)
- Approval modes: yolo, normal, strict
- Sandbox isolation (restricted execution environment)
- Pre-tool hooks (validate inputs, block dangerous operations)
- Post-tool hooks (log results, trigger notifications)
- Human-in-the-loop prompts with diff preview
- Audit log of all tool executions

**Key concepts:** Human-in-the-loop AI, permission models, sandbox isolation, hook patterns, audit trails.

**Code diff:** ~400 lines. Core files: `safety/`.

**Demo:** Agent trying to `rm -rf /` and getting blocked. Approval prompt showing a file diff.

---

## Post 5: Memory Palace — Context Management

**Hook:** LLMs have limited context windows. Have a long conversation and they forget everything. Let's build a memory palace — token accounting, prompt assembly, compaction, summarization, and session persistence that keeps the agent sharp no matter how long the conversation.

**What we build:**
- Token accounting (per-provider token counting and tracking)
- Context window management (sliding window, priority-based dropping)
- Prompt assembly (dynamic system prompt construction)
- Message compaction (truncate, summarize, or drop low-priority messages)
- Conversation summarization (LLM-based)
- Session persistence (save/restore conversation state to disk)

**Key concepts:** Token economics, prompt assembly, message compaction, summarization strategies, session persistence.

**Code diff:** ~450 lines. Core files: `context/`.

**Demo:** 50+ turn conversation where the agent still remembers early context via summarization. Restart the agent and it picks up where it left off.

---

## Post 6: Inner Monologue — Extended Thinking & Planning

**Hook:** Most agents just react. Ours will think. We'll add task decomposition, planning with checkpoints, a scratchpad for notes, self-reflection, and replanning — giving it an inner monologue that adapts when things go wrong.

**What we build:**
- Task decomposition (break complex tasks into subtasks)
- Plan-and-execute pattern with execution checkpoints
- Scratchpad tool (agent writes notes to itself)
- Self-reflection loop (evaluate + retry)
- Replanning (adjust plan when steps fail or new info emerges)
- Goal tracking
- Extended thinking integration (Anthropic thinking, OpenAI reasoning)

**Key concepts:** Task decomposition, plan-and-execute, execution checkpoints, self-reflection, replanning, meta-cognition.

**Code diff:** ~500 lines. Core files: `thinking/`.

**Demo:** Agent refactoring a module — first decomposes the task, writes a plan, executes step by step, catches its own mistake, replans, and fixes it.

---

## Post 7: Team of Agents — Sub-Agent Delegation

**Hook:** One agent is good. A team is better. Let's build a multi-agent system where the main agent can spawn specialists with isolated contexts, delegate work in parallel, orchestrate workflows, and merge results.

**What we build:**
- Subagent spawning with specific roles
- Isolated contexts (each agent has its own conversation history)
- Task delegation patterns
- Parallel execution
- Orchestration (sequential, parallel, hierarchical)
- Result aggregation
- Git worktree isolation for code changes

**Key concepts:** Multi-agent systems, delegation patterns, isolated contexts, parallel execution, orchestration.

**Code diff:** ~600 lines. Core files: `agents/`.

**Demo:** "Research HTTP libraries, write a comparison, and create a benchmark script" — three sub-agents working in parallel with isolated contexts, results merged by the orchestrator.

---

## Post 8: Long-Term Memory — Persistent Knowledge

**Hook:** Every conversation starts from zero. Not anymore. We'll add persistent memory with episodic and semantic storage, embedding-based retrieval, and memory consolidation — the agent remembers your preferences, project decisions, and key facts across sessions.

**What we build:**
- Episodic memory (specific events, decisions, conversation highlights)
- Semantic memory (general knowledge, user preferences, project facts)
- Embedding-based retrieval (vector search for relevant memories)
- Memory consolidation (merge duplicates, update outdated info, prune)
- Auto-memory (agent decides what to remember)
- Storage: local SQLite + vector index

**Key concepts:** Episodic vs semantic memory, embeddings, vector retrieval, memory consolidation, cross-session persistence.

**Code diff:** ~500 lines. Core files: `memory/`.

**Demo:** Tell the agent "I prefer TypeScript" in session 1. In session 2, it suggests TypeScript without being asked. It remembers project decisions and deadlines.

---

## Post 9: Universal Tools — MCP Integration

**Hook:** Our agent has a fixed set of tools. But what if it could connect to *any* tool server and instantly gain new capabilities? Enter the Model Context Protocol — infinite extensibility with proper authentication and connection lifecycle management.

**What we build:**
- MCP client implementation (Model Context Protocol)
- Server discovery (auto-discover available MCP servers)
- Dynamic tool discovery at runtime
- Tool call translation (our format ↔ MCP format)
- Resource access (read resources from MCP servers)
- Authentication handling (API keys, OAuth, etc.)
- Connection lifecycle (connect, reconnect, health checks, disconnect)
- Built-in MCP server configs

**Key concepts:** Model Context Protocol, tool interoperability, dynamic loading, protocol translation, connection lifecycle.

**Code diff:** ~550 lines. Core files: `mcp/`.

**Demo:** Connect a Postgres MCP server — agent can now query databases. Connect GitHub — it can create PRs. Authentication handled automatically. Infinite tools.

---

## Post 10: Dashboard & Skills — Observability, Evaluation + Reusable Workflows

**Hook:** We've built a powerful agent. But can we see what it's doing? How much does it cost? How well does it perform? And can we package useful workflows as reusable skills? Let's add full observability, evaluation, and a skills system.

**What we build:**
- **Skills system:**
  - Skill discovery (find skills in local directories or registries)
  - Skill loading (load parameterized workflows as reusable commands)
  - Skill composition (combine skills into larger workflows)
  - Built-in skills: code review, refactoring, testing, documentation
- **Observability:**
  - Execution tracing (every LLM call, tool call, decision)
  - Cost tracking (per-call and cumulative)
  - Performance metrics (latency, tokens, tool counts)
  - Trace export and debug replay
- **Evaluation:**
  - Evaluation framework (define tasks, run agent, score results)
  - Benchmark suites (compare providers, prompts, strategies)
  - Summary dashboard

**Key concepts:** Skill systems, reusable workflows, observability, cost optimization, evaluation-driven design, tracing.

**Code diff:** ~600 lines. Core files: `skills/`, `observability/`.

**Demo:** Dashboard showing a trace of a complex task. Cost breakdown by provider. Run a code review skill. Eval scores comparing GPT-4o vs Claude on coding tasks.

---

## Writing Guidelines

- **Code-first:** Show the code, explain the key parts, skip the boilerplate
- **Progressive disclosure:** Each post builds on the last. Reference previous posts.
- **Honest about tradeoffs:** Discuss what we gained and what we gave up
- **Terminal screenshots:** Every post has a demo section with real output
- **Open source:** Link to the git diff for each step

## Publishing Plan

- **Platform:** Personal blog / Dev.to / Hashnode
- **Format:** Markdown with code blocks, diagrams, terminal output
- **Code:** Each step is a git tag (`step-1`, `step-2`, ...) so readers can check out any step
- **Cadence:** One post per week (or as completed)
