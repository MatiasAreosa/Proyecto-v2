from __future__ import annotations
import json
import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text

from agent.prompts import SYSTEM_PROMPT
from agent.tools import TOOL_DEFINITIONS, TOOL_FUNCTIONS

MODEL = "claude-opus-4-7"


class AirlineAgent:
    def __init__(self, api_key: str) -> None:
        self.client = anthropic.Anthropic(api_key=api_key)
        self.messages: list[dict] = []
        self.console = Console()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def chat(self, user_input: str) -> None:
        self.messages.append({"role": "user", "content": user_input})

        while True:
            response = self._stream_and_collect()
            self.messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                break

            tool_results = self._execute_tools(response.content)
            self.messages.append({"role": "user", "content": tool_results})

    # ------------------------------------------------------------------
    # Streaming call
    # ------------------------------------------------------------------

    def _stream_and_collect(self) -> anthropic.types.Message:
        system_with_cache = [
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ]

        self.console.print()
        self.console.rule("[dim]AERO-IA[/dim]", style="blue")

        with self.client.messages.stream(
            model=MODEL,
            max_tokens=4096,
            thinking={"type": "adaptive"},
            system=system_with_cache,
            tools=TOOL_DEFINITIONS,
            messages=self.messages,
        ) as stream:
            in_text = False
            for event in stream:
                self._handle_event(event, in_text_ref=lambda v: None)
                # Track whether we've started printing text
                if hasattr(event, "type"):
                    if event.type == "content_block_start":
                        block = getattr(event, "content_block", None)
                        if block and block.type == "text":
                            in_text = True
                    elif event.type == "content_block_stop":
                        if in_text:
                            in_text = False
                            self.console.print()

            return stream.get_final_message()

    def _handle_event(self, event, in_text_ref) -> None:
        if not hasattr(event, "type"):
            return
        t = event.type

        if t == "content_block_start":
            block = getattr(event, "content_block", None)
            if block and block.type == "tool_use":
                self.console.print(
                    f"\n[yellow]⚙ Ejecutando herramienta:[/yellow] [bold]{block.name}[/bold]"
                )
        elif t == "content_block_delta":
            delta = getattr(event, "delta", None)
            if delta is None:
                return
            if delta.type == "text_delta":
                self.console.print(delta.text, end="", markup=False)
            elif delta.type == "input_json_delta":
                pass  # tool input building, no display needed

    # ------------------------------------------------------------------
    # Tool execution
    # ------------------------------------------------------------------

    def _execute_tools(self, content: list) -> list[dict]:
        results = []
        for block in content:
            if block.type != "tool_use":
                continue
            output = self._run_tool(block.name, block.input)
            self.console.print(
                Panel(
                    Text(output, style="dim"),
                    title=f"[cyan]Resultado: {block.name}[/cyan]",
                    border_style="cyan",
                    expand=False,
                )
            )
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                }
            )
        return results

    def _run_tool(self, name: str, inputs: dict) -> str:
        fn = TOOL_FUNCTIONS.get(name)
        if fn is None:
            return f"Error: herramienta '{name}' no encontrada."
        try:
            return fn(inputs)
        except Exception as exc:  # noqa: BLE001
            return f"Error ejecutando {name}: {exc}"
