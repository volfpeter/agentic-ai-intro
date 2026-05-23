import re
from pathlib import Path

import yaml

from arxiv_md.models import Paper


def sanitize_filename(title: str) -> str:
    name = title.lower()
    name = re.sub(r"[^a-z0-9\s-]", "", name)
    name = re.sub(r"[\s-]+", "-", name)
    return name.strip("-")


def resolve_collision(output_dir: Path, filename: str) -> Path:
    base = output_dir / filename
    if not base.with_suffix(".md").exists():
        return base.with_suffix(".md")
    index = 2
    while True:
        candidate = output_dir / f"{filename}-{index}.md"
        if not candidate.exists():
            return candidate
        index += 1


def save(paper: Paper, markdown_body: str, output_dir: Path) -> Path:
    filename = sanitize_filename(paper.title)
    filepath = resolve_collision(output_dir, filename)

    frontmatter = {
        "title": paper.title,
        "arxiv_id": paper.id,
        "arxiv_url": paper.url,
        "authors": paper.authors,
        "published": paper.published,
        "categories": paper.categories,
    }

    content = f"---\n{yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True).strip()}\n---\n\n{markdown_body}"
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    return filepath
