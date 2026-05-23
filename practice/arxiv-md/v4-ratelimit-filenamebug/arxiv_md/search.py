from datetime import date, timedelta

import arxiv

from arxiv_md.models import Paper


def search_papers(
    keywords: list[str],
    max_results: int = 30,
    days: int = 30,
) -> list[Paper]:
    query = " AND ".join(f"all:{kw}" for kw in keywords)
    client = arxiv.Client(num_retries=50, delay_seconds=5)

    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    results: list[Paper] = []
    for result in client.results(
        arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )
    ):
        published = result.published.date()
        if published < start_date or published > end_date:
            continue

        results.append(
            Paper(
                id=result.entry_id.split("/")[-1].split("v")[0],
                title=result.title,
                authors=[a.name for a in result.authors],
                abstract=result.summary,
                url=result.entry_id,
                published=published.isoformat(),
                categories=result.categories,
            )
        )

    return results
