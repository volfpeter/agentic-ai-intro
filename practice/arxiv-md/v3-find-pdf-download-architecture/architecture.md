# arxiv-md architecture

## Overview

CLI tool that searches arXiv, downloads LaTeX source, converts it to Markdown, and optionally downloads PDFs. Built with Typer, Rich, and the arXiv Python client.

## Module map

| Module | Responsibility |
|--------|---------------|
| `cli.py` | Typer app, command definitions (`search`, `find`, `download`), entry point |
| `interactive.py` | Interactive review loop: browse papers, accept/skip, trigger downloads |
| `search.py` | arXiv API search via `arxiv` library, returns `list[Paper]` |
| `download.py` | HTTP downloads: LaTeX source (tarball) and PDF binary |
| `convert.py` | LaTeX→Markdown conversion via `pylatexenc` |
| `storage.py` | File I/O: save/load markdown files, save PDFs, frontmatter parsing |
| `display.py` | Rich table and detail panel rendering |
| `filter.py` | Fuzzy filtering abstraction (uses `rapidfuzz`, falls back to substring) |
| `models.py` | `Paper` and `Settings` dataclasses |

## Data flow

```
search → interactive → download (LaTeX) → convert → save (.md)
                                           └→ download (PDF) → save (.pdf)
                              find → load_papers → filter → show_table
                              download <id> → download_pdf → save_pdf
```

## CLI commands

- **`search <keywords>`** — Search arXiv, enter interactive loop to accept/skip papers. Produces `.md` files.
- **`find [keywords]`** — List already-downloaded papers. With keywords, fuzzy-filter on title+abstract. Read-only, no API calls.
- **`download <id>...`** — Download PDFs by arXiv ID. No metadata API calls — uses existing `.md` filename if available, else `{id}.pdf`.

## File naming & storage

- **Pattern**: `{arxiv_id}-{sanitized_title}.md`
- **Sanitization**: lowercase, strip non-alphanumeric/non-space/non-hyphen, collapse whitespace to `-`, strip leading/trailing `-`
- **Frontmatter**: YAML with `title`, `arxiv_id`, `arxiv_url`, `authors`, `abstract`, `published`, `categories`
- **PDFs**: same stem as `.md` when a matching markdown exists; otherwise `{arxiv_id}.pdf`

## Deduplication (overwrite)

Since filenames are prefixed with the unique arXiv ID, **no collision resolution**. Writing to an existing path intentionally overwrites. This applies to both `.md` and `.pdf` files.

## Technical decisions

- **`filter.py` abstracts fuzzy search**: CLI never imports `rapidfuzz`. `filter_papers()` uses `rapidfuzz.process.extract` with `WRatio` scorer (cutoff 50). Falls back to substring matching if rapidfuzz is unavailable.
- **No metadata API calls in `download`**: PDF downloads derive filenames from existing `.md` files or fall back to `{id}.pdf`. No arXiv API requests for title/author lookup.
- **Frontmatter-only reads**: `load_papers()` parses only the YAML frontmatter (split on `---`), never reads the full markdown body. Keeps listing fast.
- **Overwrite semantics**: arXiv IDs are globally unique, so multiple downloads of the same ID are intentional updates, not collisions.

## Dependencies

- `arxiv` — arXiv API client
- `pylatexenc` — LaTeX→text conversion
- `pyyaml` — frontmatter serialization
- `rapidfuzz` — fuzzy string matching
- `rich` — terminal UI (tables, panels, console)
- `typer` — CLI framework

## Dev tooling

- **Lint**: `ruff`
- **Type checking**: `ty` (based on mypy)
- **Commands**: `uv run ruff check .`, `uv run ty check .`, `uv run ruff format . --check`
