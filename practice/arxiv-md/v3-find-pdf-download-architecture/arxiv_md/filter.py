from arxiv_md.models import Paper

try:
    from rapidfuzz import fuzz, process

    _FUZZY_AVAILABLE = True
except ImportError:
    _FUZZY_AVAILABLE = False


_SCORE_CUTOFF = 50


def filter_papers(papers: list[Paper], query: str) -> list[Paper]:
    if not query:
        return list(papers)

    if _FUZZY_AVAILABLE:
        texts = [f"{p.title} {p.abstract}" for p in papers]
        results = process.extract(
            query,
            texts,
            scorer=fuzz.WRatio,
            score_cutoff=_SCORE_CUTOFF,
        )
        return [papers[idx] for _, _, idx in results]

    query_lower = query.lower()
    return [
        p
        for p in papers
        if query_lower in p.title.lower() or query_lower in p.abstract.lower()
    ]
