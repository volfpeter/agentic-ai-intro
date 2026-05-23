# arXiv-to-Markdown CLI

Search recent arXiv papers by keyword, download them as Markdown files, and optionally grab the PDF too.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Commands

### `search` — find and download papers

```bash
uv run arxiv-md search "attention mechanism"
```

You'll see a list of recent papers. For each one, choose:

| Choice | Action |
|--------|--------|
| `Y` | Download LaTeX source, convert to Markdown, and save |
| `p` | Same as `Y`, plus also download the PDF |
| `n` | Skip this paper |
| `q` | Quit the session |

Options:

```bash
# Limit how many results to show
uv run arxiv-md search "transformer" --max-results 10

# Narrow the search to the last 7 days
uv run arxiv-md search "reinforcement learning" --days 7

# Combine options
uv run arxiv-md search "nlp" "reasoning" --max-results 5 --days 14
```

### `find` — list and filter downloaded papers

```bash
# List all downloaded papers
uv run arxiv-md find

# Fuzzy-filter by abstract content
uv run arxiv-md find "transformer" "attention"
```

Scans the `papers/` folder and shows results in the same table format as `search`. With keywords, fuzzy-matches against the abstract and title (via `rapidfuzz`). No API calls.

### `download` — download PDFs by arXiv ID

```bash
uv run arxiv-md download 2401.12345 2306.12345
```

Downloads the PDF for each ID. If a markdown file with that arXiv ID already exists, the PDF gets the same filename (just with `.pdf` extension). Otherwise it's saved as `{id}.pdf`.

## Where files go

Papers are saved to the `papers/` folder. Each filename looks like this:

```
papers/2401.12345-attention-is-all-you-need.md
papers/2401.12345-attention-is-all-you-need.pdf
```

The arXiv ID is at the front, so files are easy to find and sort.

## What's inside

Each markdown file starts with YAML frontmatter containing the paper's metadata:

```yaml
---
title: Attention Is All You Need
arxiv_id: 2401.12345
arxiv_url: https://arxiv.org/abs/2401.12345
authors:
  - Ashish Vaswani
  - ...
abstract: The dominant sequence transduction models are based on...
published: 2024-01-05
categories:
  - cs.CL
  - cs.LG
---
```

The rest of the file is the paper content, converted from LaTeX to Markdown.

## Re-downloading a paper

Downloading a paper that already exists will overwrite the existing file. The arXiv ID in the filename makes sure the same paper always maps to the same file.

## Help

```bash
uv run arxiv-md --help
```
