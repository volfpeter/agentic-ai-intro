# Task: Storage and Frontmatter Module

## Number
6a (parallel with 6b)

## Complexity
4

## Dependencies
2 (Data models and configuration)

## Description
Implement `PaperStorage`: sanitize paper titles into hyphenated filenames, detect collisions and append an index, write YAML frontmatter plus Markdown body to `papers/`.

## Details
- `PaperStorage` class or module functions:
  - `sanitize_filename(title)`: Convert paper title to a hyphenated, lowercase, URL-safe filename
    - Remove special characters, replace spaces with hyphens
    - Example: "Attention Is All You Need" -> "attention-is-all-you-need"
  - `resolve_collision(filename)`: Check if `{filename}.md` exists in `papers/`
    - If yes, append `-2`, `-3`, etc. until a unique name is found
    - Example: "attention-is-all-you-need.md" exists -> use "attention-is-all-you-need-2.md"
  - `save(paper, markdown_body)`: Write the final `.md` file
    - Generate YAML frontmatter containing:
      - `title`: paper title
      - `arxiv_id`: paper ID
      - `arxiv_url`: paper URL
      - `authors`: list of authors
      - `published`: publication date
      - `categories`: list of categories
    - Append the Markdown body after the frontmatter
    - Write to `papers/{resolved-filename}.md`

## Success Criteria
- Filenames are sanitized correctly
- Collisions are resolved by appending an index
- Output files contain valid YAML frontmatter and the Markdown body
- Files are written to the configured `papers/` directory

## Acceptance Criteria
- [ ] Title sanitization produces clean hyphenated filenames
- [ ] Collision detection appends incrementing indices
- [ ] YAML frontmatter includes all required metadata fields
- [ ] Markdown body is appended after frontmatter
- [ ] Files are saved to the correct output directory
- [ ] Edge cases (empty title, all-special-characters title) are handled
