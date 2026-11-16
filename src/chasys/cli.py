"""CLI interface for Chasys."""

import asyncio

import click
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel

from chasys.config import settings
from chasys.core import Chasys

console = Console()


@click.command()
@click.option(
    "--provider",
    "-p",
    default=settings.default_provider,
    help="Provider string (e.g., 'openai/gpt-4o', 'anthropic/claude-3-5-sonnet-20241022')",
)
@click.option(
    "--system",
    "-s",
    default=None,
    help="System prompt",
)
@click.option(
    "--no-stream",
    is_flag=True,
    default=False,
    help="Disable streaming output",
)
def main(provider: str, system: str | None, no_stream: bool) -> None:
    """Chasys — The chassis for AI applications.

    Interactive CLI for chatting with LLMs.
    """
    console.print(Panel.fit(
        "[bold cyan]Chasys[/bold cyan] — The chassis for AI applications\n"
        f"Provider: [green]{provider}[/green]\n"
        "Type [bold]/help[/bold] for commands, [bold]/quit[/bold] to exit",
        border_style="cyan",
    ))

    harness = Chasys(provider=provider, system_prompt=system)

    # REPL loop
    while True:
        try:
            # Get user input
            console.print()
            user_input = console.input("[bold green]You>[/bold green] ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.startswith("/"):
                if user_input in ("/quit", "/exit"):
                    console.print("[cyan]Goodbye![/cyan]")
                    break
                elif user_input == "/help":
                    _print_help()
                    continue
                elif user_input == "/reset":
                    harness.reset()
                    console.print("[yellow]Conversation reset.[/yellow]")
                    continue
                elif user_input == "/messages":
                    _print_messages(harness.messages)
                    continue
                else:
                    console.print(f"[red]Unknown command: {user_input}[/red]")
                    continue

            # Get response
            if no_stream:
                response = harness.run(user_input)
                console.print()
                console.print(Panel(
                    Markdown(response.content),
                    title=f"[bold blue]{provider}[/bold blue]",
                    border_style="blue",
                ))
                if response.usage:
                    console.print(
                        f"[dim]Tokens: {response.usage.get('prompt_tokens', 0)} prompt + "
                        f"{response.usage.get('completion_tokens', 0)} completion = "
                        f"{response.usage.get('total_tokens', 0)} total[/dim]"
                    )
            else:
                console.print()
                console.print(f"[bold blue]{provider}>[/bold blue]")
                full_response = ""
                with Live("", console=console, refresh_per_second=10) as live:
                    async def stream_and_display():
                        nonlocal full_response
                        async for chunk in harness.astream(user_input):
                            full_response += chunk
                            live.update(Markdown(full_response))

                    asyncio.run(stream_and_display())

                # Final display with panel
                console.print()
                console.print(Panel(
                    Markdown(full_response),
                    title=f"[bold blue]{provider}[/bold blue]",
                    border_style="blue",
                ))

        except KeyboardInterrupt:
            console.print("\n[cyan]Interrupted. Type /quit to exit.[/cyan]")
            continue
        except EOFError:
            console.print("\n[cyan]Goodbye![/cyan]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            continue


def _print_help() -> None:
    """Print help message."""
    help_text = """
[bold]Commands:[/bold]
  /help      Show this help message
  /reset     Reset conversation history
  /messages  Show conversation history
  /quit      Exit the CLI
  /exit      Exit the CLI

[bold]Tips:[/bold]
  - Use --provider to switch LLM providers
  - Use --system to set a system prompt
  - Use --no-stream to disable streaming output
"""
    console.print(Panel(help_text, title="Help", border_style="cyan"))


def _print_messages(messages: list) -> None:
    """Print conversation history."""
    for i, msg in enumerate(messages):
        role_color = {
            "system": "yellow",
            "user": "green",
            "assistant": "blue",
        }.get(msg.role.value, "white")

        console.print(f"[{role_color}]{msg.role.value}[/{role_color}]: {msg.content[:100]}...")


if __name__ == "__main__":
    main()
