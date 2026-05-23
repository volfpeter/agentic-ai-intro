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
    filename = f"{paper.id}-{sanitize_filename(paper.title)}"
    filepath = (output_dir / filename).with_suffix(".md")

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
