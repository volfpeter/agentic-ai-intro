# Task: Data Models and Configuration

## Number
2

## Complexity
2

## Dependencies
1 (Project scaffolding)

## Description
Define a `Paper` dataclass (id, title, authors, abstract, url, published, categories) and a settings/config object for the output directory and search defaults.

## Details
- Create a `Paper` dataclass with the following fields:
  - `id`: str (arXiv ID)
  - `title`: str
  - `authors`: list of str
  - `abstract`: str
  - `url`: str
  - `published`: datetime or str
  - `categories`: list of str
- Create a settings/config object (e.g., using Pydantic BaseSettings or a simple dataclass) for:
  - Output directory path (default: `papers/`)
  - Search defaults (e.g., default date range, max results)
- Ensure models are importable by other modules

## Success Criteria
- `Paper` dataclass can be instantiated with all required fields
- Config object provides sensible defaults and can be overridden
- Other modules can import and use these models

## Acceptance Criteria
- [ ] `Paper` dataclass is defined with all specified fields
- [ ] Settings/config object is defined with output directory and search defaults
- [ ] Unit tests or simple validation scripts confirm model correctness
