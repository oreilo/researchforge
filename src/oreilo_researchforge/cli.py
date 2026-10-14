from __future__ import annotations
from pathlib import Path
import typer
from rich.console import Console
from .models import ResearchConfig
from .pipeline import ResearchEngine
from .export import export_report

app = typer.Typer(help="OREiLO ResearchForge - evidence-first web research")
console = Console()

@app.command()
def research(topic: str = typer.Argument(..., help="Research topic"),
             question: list[str] = typer.Option([], "--question", "-q", help="Research question (repeatable)"),
             output: Path = typer.Option(Path("report.md"), "--output", "-o"),
             backend: str = typer.Option("searxng", "--backend"),
             searxng_url: str = typer.Option("http://localhost:8080", "--searxng-url"),
             max_pages: int = typer.Option(10, "--max-pages"),
             allow_domain: list[str] = typer.Option([], "--allow-domain"),
             block_domain: list[str] = typer.Option([], "--block-domain"),
             ai_model: str | None = typer.Option(None, "--ai-model")):
    """Search the web, gather evidence and produce a sourced report."""
    config = ResearchConfig(topic=topic, questions=question, search_backend=backend,
                            searxng_url=searxng_url, max_pages=max_pages,
                            allow_domains=allow_domain, block_domains=block_domain,
                            ai_model=ai_model)
    report = ResearchEngine(config).run()
    export_report(report, output)
    console.print(f"[green]Report saved:[/green] {output} | sources={len(report.sources)} errors={len(report.errors)}")
    if not report.sources:
        raise typer.Exit(code=2)

@app.command()
def version():
    from . import __version__
    console.print(__version__)

from .cli_plus import app as extra_app  # noqa: E402
for command in extra_app.registered_commands:
    app.registered_commands.append(command)

if __name__ == "__main__":
    app()
