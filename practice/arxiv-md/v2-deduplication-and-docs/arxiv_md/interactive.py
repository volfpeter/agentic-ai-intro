import logging
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

from arxiv_md.convert import PaperConverter, PylatexencConverter
from arxiv_md.display import show_detail, show_table
from arxiv_md.download import cleanup, download_and_extract
from arxiv_md.models import Paper, Settings
from arxiv_md.storage import save

logger = logging.getLogger(__name__)
console = Console()


class SessionSummary:
    def __init__(self) -> None:
        self.total: int = 0
        self.accepted: int = 0
        self.skipped_by_user: int = 0
        self.skipped_by_error: int = 0
        self.failed_ids: list[str] = []

    def print(self) -> None:
        console.print("\n[bold]Session Summary[/bold]")
        console.print(f"  Total papers found:   {self.total}")
        console.print(f"  Accepted and saved:   {self.accepted}")
        console.print(f"  Skipped by user:      {self.skipped_by_user}")
        console.print(f"  Skipped due to error: {self.skipped_by_error}")
        if self.failed_ids:
            console.print(f"  Failed paper IDs:     {', '.join(self.failed_ids)}")


def run_interactive(papers: list[Paper], settings: Settings) -> SessionSummary:
    summary = SessionSummary()
    summary.total = len(papers)

    converter: PaperConverter = PylatexencConverter()

    show_table(papers)

    for i, paper in enumerate(papers, 1):
        show_detail(paper, i, len(papers))

        answer = Prompt.ask(
            "Accept?",
            choices=["Y", "n", "q"],
            default="Y",
            show_choices=False,
        )

        if answer == "q":
            break
        elif answer == "n":
            summary.skipped_by_user += 1
            continue

        try:
            all_tex, main_tex = download_and_extract(paper.id)

            if main_tex is None:
                if not all_tex:
                    logger.warning(
                        "No LaTeX source available for %s, skipping.", paper.id
                    )
                    console.print(
                        f"[yellow]No LaTeX source available for {paper.id}, skipping.[/yellow]"
                    )
                    summary.skipped_by_error += 1
                    summary.failed_ids.append(paper.id)
                    continue
                main_tex = all_tex[0]

            markdown = converter.convert(all_tex, main_tex)
            filepath = save(paper, markdown, settings.output_dir)
            console.print(f"[green]Saved: {filepath}[/green]")
            summary.accepted += 1
        except Exception as exc:
            logger.exception("Error processing %s", paper.id)
            console.print(f"[red]Error processing {paper.id}: {exc}, skipping.[/red]")
            summary.skipped_by_error += 1
            summary.failed_ids.append(paper.id)
        finally:
            if "all_tex" in locals() and all_tex:
                temp_parent = Path(all_tex[0]).parent.parent
                cleanup(temp_parent)

    summary.print()
    return summary
