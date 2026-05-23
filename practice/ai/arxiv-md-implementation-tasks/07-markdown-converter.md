# Task: Markdown Converter

## Number
7

## Complexity
5

## Dependencies
2 (Data models and configuration)

## Description
Define a `PaperConverter` protocol/ABC and a concrete `PylatexencConverter`. The implementation should accept the set of `.tex` files and the main file from the downloader, use `pylatexenc` to extract plain text from the main file, and return a single Markdown string. Design the interface so a future `PandocConverter` or `LLMConverter` can be swapped in without changing callers.

## Details
- Define an abstract base class or protocol `PaperConverter` with a single method:
  - `convert(tex_files: list[Path], main_file: Path) -> str`
- Implement `PylatexencConverter`:
  - Read the main `.tex` file content
  - Use `pylatexenc.latex2text` to convert LaTeX to plain text
  - Perform minimal cleanup to produce Markdown-like output:
    - Convert section headers to Markdown `#` style (or keep as-is if pylatexenc handles it)
    - Preserve paragraph breaks
    - Strip or simplify LaTeX environments that don't convert well
  - Return the resulting string
- The interface should be pluggable:
  - Callers should depend only on `PaperConverter`, not `PylatexencConverter` directly
  - Future implementations (`PandocConverter`, `LLMConverter`) should satisfy the same interface

## Success Criteria
- `PaperConverter` ABC/protocol is defined with a clear interface
- `PylatexencConverter` converts a main `.tex` file to a readable Markdown-like string
- The conversion is lossy but produces readable text
- Callers can use any `PaperConverter` implementation interchangeably

## Acceptance Criteria
- [ ] `PaperConverter` ABC or protocol is defined with `convert()` method
- [ ] `PylatexencConverter` implements the interface
- [ ] Converter reads the main `.tex` file
- [ ] `pylatexenc.latex2text` is used for conversion
- [ ] Output is a single string in Markdown-ish format
- [ ] Interface is designed for future converter swap without caller changes
- [ ] Conversion errors are caught and handled gracefully
