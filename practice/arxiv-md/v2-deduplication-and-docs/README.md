# arXiv-to-Markdown CLI

Search recent arXiv papers by keyword and download them as Markdown files.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Quick start

```bash
uv run arxiv-md "attention mechanism"
```

You'll see a list of recent papers. For each one, choose `Y` to download, `n` to skip, or `q` to quit.

## Options

```bash
# Limit how many results to show
uv run arxiv-md "transformer" --max-results 10

# Narrow the search to the last 7 days
uv run arxiv-md "reinforcement learning" --days 7

# Combine options
uv run arxiv-md "nlp" "reasoning" --max-results 5 --days 14

# Full help
uv run arxiv-md --help
```

## Where files go

Papers are saved to the `papers/` folder. Each filename looks like this:

```
papers/2401.12345-attention-is-all-you-need.md
```

The arXiv ID is at the front, so files are easy to find and sort.

## What's inside

Each file starts with YAML frontmatter containing the paper's metadata:

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
