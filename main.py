#!/usr/bin/env python3
"""AERO-IA — Agente de inteligencia artificial para la industria aérea."""
import os
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

load_dotenv()

console = Console()


def print_banner() -> None:
    banner = Text()
    banner.append("✈  AERO-IA\n", style="bold cyan")
    banner.append("Agente de Inteligencia Artificial Aeronáutico\n\n", style="bold white")
    banner.append("Especializado en:\n", style="dim")
    banner.append("  • Sabre GDS   ", style="green")
    banner.append("• Amadeus GDS\n", style="blue")
    banner.append("  • Análisis de datos   ", style="yellow")
    banner.append("• Reportes mensuales\n", style="magenta")
    banner.append("  • Tarifas & PNRs   ", style="cyan")
    banner.append("• Revenue Management\n\n", style="red")
    banner.append("Comandos: ", style="dim")
    banner.append("'salir'", style="bold red")
    banner.append(" o ", style="dim")
    banner.append("Ctrl+C", style="bold red")
    banner.append(" para terminar  |  ", style="dim")
    banner.append("'limpiar'", style="bold yellow")
    banner.append(" para nueva conversación", style="dim")

    console.print(
        Panel(banner, title="[bold blue]Bienvenido[/bold blue]",
              border_style="blue", padding=(1, 2))
    )


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key or not api_key.startswith("sk-ant-"):
        console.print(
            "[bold red]Error:[/bold red] ANTHROPIC_API_KEY no configurada o inválida.\n"
            "Copia [bold].env.example[/bold] a [bold].env[/bold] y agrega tu API key."
        )
        sys.exit(1)

    # Import here to avoid loading heavy modules before key check
    from agent.core import AirlineAgent  # noqa: PLC0415

    agent = AirlineAgent(api_key=api_key)
    print_banner()

    try:
        while True:
            try:
                user_input = Prompt.ask("\n[bold green]Tú[/bold green]").strip()
            except EOFError:
                break

            if not user_input:
                continue

            if user_input.lower() in ("salir", "exit", "quit", "q"):
                console.print("\n[dim]¡Hasta luego! Buen vuelo. ✈[/dim]")
                break

            if user_input.lower() in ("limpiar", "clear", "reset", "nueva"):
                agent.messages.clear()
                console.clear()
                print_banner()
                console.print("[dim]Conversación reiniciada.[/dim]")
                continue

            agent.chat(user_input)

    except KeyboardInterrupt:
        console.print("\n\n[dim]Sesión interrumpida. ¡Hasta pronto! ✈[/dim]")


if __name__ == "__main__":
    main()
