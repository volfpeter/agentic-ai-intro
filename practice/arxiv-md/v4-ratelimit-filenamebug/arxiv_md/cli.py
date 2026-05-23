import logging
import signal
import sys
from pathlib import Path

import typer

from arxiv_md.display import show_table
from arxiv_md.download import download_pdf_binary
from arxiv_md.filter import filter_papers
from arxiv_md.interactive import run_interactive
from arxiv_md.models import Settings
from arxiv_md.search import search_papers
from arxiv_md.storage import load_papers, save_pdf

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
    """Search arXiv for recent papers and download them as Markdown (optionally PDF)."""
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

    typer.echo(f"Searching arXiv for: {' '.join(keywords)}")
    try:
        papers = search_papers(keywords, max_results=max_results, days=days)
    except Exception as exc:
        typer.echo(f"Search failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    if not papers:
        typer.echo("No papers found matching your criteria.")
        raise typer.Exit(code=0)

    run_interactive(papers, settings)


@app.command()
def find(
    keywords: list[str] = typer.Argument(
        None, help="Keywords to fuzzy-filter downloaded papers by"
    ),
    output_dir: Path = typer.Option(
        OUTPUT_DIR, "--output-dir", "-o", help="Output directory"
    ),
) -> None:
    """List and fuzzy-filter already downloaded papers."""
    papers = load_papers(output_dir)
    if keywords:
        papers = filter_papers(papers, " ".join(keywords))
    if not papers:
        typer.echo("No papers found.")
        raise typer.Exit(code=0)
    show_table(papers, title="Downloaded Papers")


@app.command()
def download(
    arxiv_ids: list[str] = typer.Argument(..., help="arXiv IDs to download PDFs for"),
    output_dir: Path = typer.Option(
        OUTPUT_DIR, "--output-dir", "-o", help="Output directory"
    ),
) -> None:
    """Download PDFs for one or more arXiv IDs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    success = 0
    for arxiv_id in arxiv_ids:
        typer.echo(f"Downloading PDF for {arxiv_id}...")
        try:
            pdf_data = download_pdf_binary(arxiv_id)
            filepath = save_pdf(arxiv_id, pdf_data, output_dir)
            typer.echo(f"Saved: {filepath}")
            success += 1
        except Exception as exc:
            typer.echo(f"Error downloading {arxiv_id}: {exc}", err=True)
    typer.echo(f"\nDownloaded: {success}, Failed: {len(arxiv_ids) - success}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
