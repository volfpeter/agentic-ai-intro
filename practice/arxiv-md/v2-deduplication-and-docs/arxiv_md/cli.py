import logging
import signal
import sys
from pathlib import Path

import typer

from arxiv_md.interactive import run_interactive
from arxiv_md.models import Settings
from arxiv_md.search import search_papers

app = typer.Typer()
OUTPUT_DIR = Path("papers")


@app.command()
def search(
    keywords: list[str] = typer.Argument(..., help="Keywords to search for"),
    max_results: int = typer.Option(
        Settings.default_max_results,
        "--max-results",
        "-m",
        help="Maximum number of results",
    ),
    days: int = typer.Option(
        Settings.default_date_range_days,
        "--days",
        "-d",
        help="Number of days back to search",
    ),
) -> None:
    logging.basicConfig(level=logging.WARNING)

    settings = Settings(
        output_dir=OUTPUT_DIR,
        default_max_results=max_results,
        default_date_range_days=days,
    )

    def handle_interrupt(sig: int, frame: object) -> None:
        typer.echo("\n\nInterrupted. Exiting.")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_interrupt)

    settings.output_dir.mkdir(parents=True, exist_ok=True)

    try:
        papers = search_papers(keywords, max_results=max_results, days=days)
    except Exception as exc:
        typer.echo(f"Search failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    if not papers:
        typer.echo("No papers found matching your criteria.")
        raise typer.Exit(code=0)

    run_interactive(papers, settings)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
