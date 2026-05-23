# /// script
# dependencies = [
#   "arxiv",
#   "pylatexenc",
#   "pyyaml",
#   "requests",
# ]
# ///

"""Download an arXiv paper as Markdown + PDF.

Usage:
    uv run arxiv_paper.py <arxiv_id_or_url> [--output-dir <dir>]
"""

import argparse
import re
import shutil
import tarfile
import tempfile
import time
from pathlib import Path

import arxiv
import requests
import yaml
from pylatexenc.latex2text import LatexNodes2Text


ARXIV_ID_PATTERN = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/)?(\d{4}\.\d{4,5})(?:v\d+)?")


def parse_arxiv_id(text: str) -> str | None:
    m = ARXIV_ID_PATTERN.search(text.strip())
    return m.group(1) if m else None


def fetch_metadata(arxiv_id: str) -> dict | None:
    client = arxiv.Client(num_retries=50, delay_seconds=5)
    results = list(client.results(arxiv.Search(id_list=[arxiv_id], max_results=1)))
    if not results:
        return None
    r = results[0]
    return {
        "id": r.entry_id.split("/")[-1].split("v")[0],
        "title": r.title,
        "authors": [a.name for a in r.authors],
        "abstract": r.summary,
        "url": r.entry_id,
        "published": r.published.date().isoformat(),
        "categories": r.categories,
    }


def sanitize_filename(title: str) -> str:
    name = title.lower()
    name = re.sub(r"[^a-z0-9\s-]", "", name)
    name = re.sub(r"[\s-]+", "-", name)
    return name.strip("-")


def _request_with_retry(url: str, **kwargs) -> requests.Response:
    for attempt in range(5):
        try:
            resp = requests.get(url, timeout=30, **kwargs)
            if resp.status_code == 429:
                delay = min(5.0 * (2 ** attempt), 120.0)
                print(f"Rate limited. Retrying in {delay:.0f}s ...")
                time.sleep(delay)
                continue
            resp.raise_for_status()
            return resp
        except (requests.ConnectionError, requests.Timeout) as exc:
            if attempt == 4:
                raise
            delay = min(5.0 * (2 ** attempt), 120.0)
            print(f"Connection error: {exc}. Retrying in {delay:.0f}s ...")
            time.sleep(delay)
    raise RuntimeError(f"Failed to fetch {url}")


def _resolve_inputs(content: str, tex_dir: Path) -> str:
    def _replace_input(match: re.Match) -> str:
        name = match.group(1)
        for ext in ("", ".tex"):
            candidate = tex_dir / f"{name}{ext}"
            if candidate.exists():
                nested = candidate.read_text(encoding="utf-8", errors="replace")
                return _resolve_inputs(nested, tex_dir)
        return f"% missing input: {name}"

    content = re.sub(
        r"\\(?:input|include)\{([^}]+)\}",
        _replace_input,
        content,
    )
    return content


def download_latex_source(arxiv_id: str) -> str | None:
    url = f"https://arxiv.org/e-print/{arxiv_id}"
    resp = _request_with_retry(url)
    if "pdf" in resp.headers.get("Content-Type", ""):
        return None
    tmp = Path(tempfile.mkdtemp(prefix=f"arxiv_{arxiv_id}_"))
    tar_path = tmp / f"{arxiv_id}.tar.gz"
    tar_path.write_bytes(resp.content)
    extract_dir = tmp / "extracted"
    extract_dir.mkdir()
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=extract_dir, filter="data")
    tex_files = sorted(extract_dir.rglob("*.tex"))
    if not tex_files:
        return None
    main = _find_main(tex_files)
    content = main.read_text(encoding="utf-8", errors="replace")
    content = _resolve_inputs(content, main.parent)
    converter = LatexNodes2Text()
    plain = converter.latex_to_text(content)
    lines = [l.strip() for l in plain.split("\n")]
    body = "\n".join("" if not l else l for l in lines)
    body = re.sub(r"\n{3,}", "\n\n", body)
    shutil.rmtree(tmp, ignore_errors=True)
    return body


def _find_main(tex_files: list[Path]) -> Path:
    for tex in tex_files:
        if "\\documentclass" in tex.read_text(encoding="utf-8", errors="replace"):
            return tex
    return max(tex_files, key=lambda p: p.stat().st_size)


def download_pdf(arxiv_id: str) -> bytes:
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    resp = _request_with_retry(url)
    return resp.content


def save_markdown(meta: dict, body: str, output_dir: Path) -> Path:
    frontmatter = {
        "title": meta["title"],
        "arxiv_id": meta["id"],
        "arxiv_url": meta["url"],
        "authors": meta["authors"],
        "abstract": meta["abstract"],
        "published": meta["published"],
        "categories": meta["categories"],
    }
    filename = f"{meta['id']}-{sanitize_filename(meta['title'])}.md"
    filepath = output_dir / filename
    output_dir.mkdir(parents=True, exist_ok=True)
    content = (
        f"---\n"
        f"{yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True).strip()}\n"
        f"---\n\n"
        f"{body}"
    )
    filepath.write_text(content, encoding="utf-8")
    return filepath


def save_pdf(arxiv_id: str, pdf_data: bytes, output_dir: Path) -> Path:
    for f in output_dir.glob(f"{arxiv_id}-*.md"):
        filepath = f.with_suffix(".pdf")
        filepath.write_bytes(pdf_data)
        return filepath
    filepath = output_dir / f"{arxiv_id}.pdf"
    filepath.write_bytes(pdf_data)
    return filepath


def process(arxiv_id_or_url: str, output_dir: Path) -> dict:
    arxiv_id = parse_arxiv_id(arxiv_id_or_url)
    if not arxiv_id:
        raise ValueError(f"Could not extract arXiv ID from: {arxiv_id_or_url}")

    meta = fetch_metadata(arxiv_id)
    if not meta:
        raise RuntimeError(f"No metadata found for ID: {arxiv_id}")

    print(f"Title: {meta['title']}")
    print(f"Authors: {', '.join(meta['authors'])}")

    markdown = download_latex_source(arxiv_id)
    if markdown is None:
        print("No LaTeX source available; PDF only.")
    else:
        md_path = save_markdown(meta, markdown, output_dir)
        print(f"Saved: {md_path}")

    pdf_data = download_pdf(arxiv_id)
    pdf_path = save_pdf(arxiv_id, pdf_data, output_dir)
    print(f"Saved: {pdf_path}")

    return {"markdown": str(md_path) if markdown else None, "pdf": str(pdf_path)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download arXiv paper as Markdown + PDF")
    parser.add_argument("arxiv_id", help="arXiv ID or URL (e.g. 1706.03762 or https://arxiv.org/abs/1706.03762)")
    parser.add_argument("--output-dir", "-o", type=Path, required=True, help="Output directory")
    args = parser.parse_args()
    process(args.arxiv_id, args.output_dir)


if __name__ == "__main__":
    main()
