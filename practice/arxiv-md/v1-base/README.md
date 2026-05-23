# arXiv-to-Markdown CLI

Search recent arXiv papers by keyword and interactively download selected papers as Markdown files.

## Installation

```bash
uv sync
```

## Usage

```bash
# Search for papers matching keywords
uv run arxiv-md "attention mechanism"

# Limit results and date range
uv run arxiv-md "transformer" "nlp" --max-results 10 --days 7

# Get help
uv run arxiv-md --help
```

Papers are saved to `papers/` with YAML frontmatter (arXiv URL, authors, categories, etc.) and a lossy LaTeX-to-Markdown body.
