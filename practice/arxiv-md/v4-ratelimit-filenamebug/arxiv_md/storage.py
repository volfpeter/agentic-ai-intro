import re
from pathlib import Path

import yaml

from arxiv_md.models import Paper


def sanitize_filename(title: str) -> str:
    name = title.lower()
    name = re.sub(r"[^a-z0-9\s-]", "", name)
    name = re.sub(r"[\s-]+", "-", name)
    return name.strip("-")


def save(paper: Paper, markdown_body: str, output_dir: Path) -> Path:
    filename = f"{paper.id}-{sanitize_filename(paper.title)}.md"
    filepath = output_dir / filename

    frontmatter = {
        "title": paper.title,
        "arxiv_id": paper.id,
        "arxiv_url": paper.url,
        "authors": paper.authors,
        "abstract": paper.abstract,
        "published": paper.published,
        "categories": paper.categories,
    }

    content = f"---\n{yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True).strip()}\n---\n\n{markdown_body}"
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    return filepath


def _parse_frontmatter(content: str) -> dict | None:
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None


def load_papers(output_dir: Path) -> list[Paper]:
    papers: list[Paper] = []
    for md_file in sorted(output_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        fm = _parse_frontmatter(content)
        if fm is None:
            continue
        papers.append(
            Paper(
                id=fm.get("arxiv_id", ""),
                title=fm.get("title", ""),
                authors=fm.get("authors", []),
                abstract=fm.get("abstract", ""),
                url=fm.get("arxiv_url", ""),
                published=fm.get("published", ""),
                categories=fm.get("categories", []),
            )
        )
    return papers


def find_md_for_id(arxiv_id: str, output_dir: Path) -> Path | None:
    for f in output_dir.glob(f"{arxiv_id}-*.md"):
        return f
    return None


def save_pdf(arxiv_id: str, pdf_data: bytes, output_dir: Path) -> Path:
    existing_md = find_md_for_id(arxiv_id, output_dir)
    if existing_md:
        filepath = existing_md.with_suffix(".pdf")
    else:
        filepath = output_dir / f"{arxiv_id}.pdf"
    filepath.write_bytes(pdf_data)
    return filepath
