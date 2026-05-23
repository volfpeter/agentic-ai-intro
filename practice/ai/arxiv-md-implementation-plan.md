# arXiv-to-Markdown CLI - Implementation Plan

## Context

A Python command-line application that searches recent arXiv papers by keyword, displays results, and interactively downloads selected papers as Markdown files. The application targets a flat `papers/` storage directory with hyphenated filenames, YAML frontmatter, and lossy LaTeX-to-Markdown conversion via pylatexenc. No system dependencies like pandoc are required.

## Goal

Build a pip-installable CLI tool that implements the following flow:

1. Accept keywords and date range via CLI arguments
2. Search arXiv and display results in a rich table
3. Present papers one-by-one for interactive Y/n/q selection
4. For accepted papers: download LaTeX source, convert to Markdown, save to `papers/` with frontmatter
5. Handle errors gracefully without crashing the session

## Success Criteria

- Running the tool with keywords produces a formatted table of recent results
- Each paper can be accepted or skipped via Y/Enter, n, or q
- Accepted papers result in a `.md` file in `papers/` with YAML frontmatter containing the arXiv URL and metadata, plus a lossy but readable body extracted from LaTeX source
- Filename collisions are resolved by appending an index
- Missing LaTeX sources or conversion errors are reported and skipped, not fatal
- The tool works after a single `pip install` with no external system dependencies

## Architecture

The tool is split into modules by concern:

- `search`: arXiv API client wrapper
- `display`: table and per-paper detail formatting (Rich-based)
- `download`: .tar.gz fetch and temp extraction
- `convert`: LaTeX-to-Markdown converter (pluggable abstraction)
- `storage`: filename generation and frontmatter writing
- `interactive`: user prompt loop
- `cli`: Typer entry point and orchestration

Dependencies: `arxiv`, `pylatexenc`, `pyyaml`, `rich`, `typer`

## Subtasks

Execute in order. Tasks 6, 7, and 8 are independent of each other and could theoretically be done in parallel; they are ordered by complexity (easiest first).

### 1. Project scaffolding
Complexity: 2
Dependencies: none
Create directory layout, `pyproject.toml` with dependencies, and a minimal CLI entry point that parses arguments. Define the `papers/` output path constant.

### 2. Data models and configuration
Complexity: 2
Dependencies: 1
Define a `Paper` dataclass (id, title, authors, abstract, url, published, categories) and a settings/config object for the output directory and search defaults.

### 3. arXiv search module
Complexity: 3
Dependencies: 2
Implement a search function using the `arxiv` library that takes keywords and a date range, returning a list of `Paper` objects.

### 4. Display module
Complexity: 3
Dependencies: 2, 3
Implement two Rich formatters:
- A table view for the initial overview of all results
- A detailed card view for the one-by-one interactive display

### 5. Interactive selection loop (stubbed pipeline)
Complexity: 4
Dependencies: 2, 4
Build the `for paper in results` loop that shows the detail card and accepts Y/n/q input. Use stub functions for download/convert/save that only print what they would do. This validates the UX flow before the backend exists.

### 6. Storage and frontmatter module
Complexity: 4
Dependencies: 2
Implement `PaperStorage`:
- Sanitize paper titles into hyphenated filenames
- Detect collisions and append an index (e.g. `-2`)
- Write YAML frontmatter plus Markdown body to `papers/`

### 7. LaTeX source downloader and extractor
Complexity: 4
Dependencies: 2
Implement `SourceDownloader`:
- Given an arXiv ID, download the `.tar.gz` source to a temp directory
- Extract it with `tarfile`
- Identify the main `.tex` file (largest `.tex` or one containing `\documentclass`)
- Returns the paths of all `.tex` files and the main file

### 8. Markdown converter
Complexity: 5
Dependencies: 2
Define a `PaperConverter` protocol/ABC and a concrete `PylatexencConverter`. The implementation should:
- Accept the set of `.tex` files and the main file from the downloader
- Use `pylatexenc` to extract plain text from the main file
- Return a single Markdown string
Design the interface so a future `PandocConverter` or `LLMConverter` can be swapped in without changing callers.

### 9. Pipeline integration
Complexity: 4
Dependencies: 5, 6, 7, 8
Replace the stub functions in the interactive loop with real calls to the downloader, converter, and storage modules. Ensure the flow is: user says Y -> download -> convert -> storage.save().

### 10. Error handling and polish
Complexity: 3
Dependencies: 9
Add graceful error handling for:
- Papers with no LaTeX source (skip with message)
- Network or tarfile errors (skip with message)
- Keyboard interrupt (Ctrl-C) caught to exit cleanly
- Informative logging of successes and skips at the end of the session
