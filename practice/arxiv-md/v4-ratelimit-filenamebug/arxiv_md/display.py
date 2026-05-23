from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from arxiv_md.models import Paper

console = Console()


def show_table(papers: list[Paper], title: str = "arXiv Search Results") -> None:
    table = Table(title=title)
    table.add_column("#", style="dim")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="bold")
    table.add_column("Authors", style="green")
    table.add_column("Date", style="yellow")
    table.add_column("Categories", style="magenta")

    for i, paper in enumerate(papers, 1):
        authors = ", ".join(paper.authors[:3])
        if len(paper.authors) > 3:
            authors += " et al."
        title = paper.title[:80] + "..." if len(paper.title) > 80 else paper.title
        categories = ", ".join(paper.categories[:3])

        table.add_row(
            str(i),
            paper.id,
            title,
            authors,
            paper.published,
            categories,
        )

    console.print(table)


def show_detail(paper: Paper, index: int, total: int) -> None:
    authors = ", ".join(paper.authors)
    categories = ", ".join(paper.categories)

    content = (
        f"[bold]ID:[/bold] {paper.id}\n"
        f"[bold]URL:[/bold] {paper.url}\n"
        f"[bold]Authors:[/bold] {authors}\n"
        f"[bold]Published:[/bold] {paper.published}\n"
        f"[bold]Categories:[/bold] {categories}\n\n"
        f"[bold]Abstract:[/bold]\n{paper.abstract}"
    )

    panel = Panel(
        content,
        title=f"[bold]{paper.title}[/bold]",
        subtitle=f"Paper {index} of {total}",
        border_style="cyan",
        padding=(1, 2),
        width=80,
    )

    console.print(panel)
