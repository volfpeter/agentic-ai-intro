---
name: arxiv-paper
description: Download an arXiv paper as Markdown + PDF when the user provides an arXiv ID or URL
---

## What this does

Takes an arXiv paper ID or URL (e.g. `1706.03762` or `https://arxiv.org/abs/1706.03762`) and:
1. Fetches metadata (title, authors, abstract) from the arXiv API
2. Downloads the LaTeX source, converts it to Markdown, and saves as `{arxiv_id}-{sanitized_title}.md`
3. Downloads the PDF and saves alongside with the same filename stem

## When to use

- The user pastes an arXiv URL (`arxiv.org/abs/...` or `arxiv.org/pdf/...`)
- The user mentions a raw arXiv ID like `1706.03762`
- Trigger phrases: "I want this arxiv paper", "download this paper", "arxiv link", etc.

## How to run

Run the companion script with `uv run` (dependencies are auto-installed from the embedded PEP 723 block). The `--output-dir` is required — always pass the **absolute path** to the `papers/` subdirectory of the project/workspace root:

```bash
uv run arxiv_paper.py <arxiv_id_or_url> --output-dir /absolute/path/to/project/papers
```


