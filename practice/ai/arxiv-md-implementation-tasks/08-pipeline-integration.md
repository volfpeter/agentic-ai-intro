# Task: Pipeline Integration

## Number
8

## Complexity
4

## Dependencies
5 (Interactive selection loop), 6a (Storage and frontmatter module), 6b (LaTeX source downloader), 7 (Markdown converter)

## Description
Replace the stub functions in the interactive loop with real calls to the downloader, converter, and storage modules. Ensure the flow is: user says Y -> download -> convert -> storage.save().

## Details
- In the interactive selection loop, replace stub calls with real implementations:
  - When user accepts a paper (`Y` or Enter):
    1. Call `SourceDownloader.download_and_extract(paper.id)`
    2. Call `PylatexencConverter.convert(tex_files, main_file)`
    3. Call `PaperStorage.save(paper, markdown_body)`
- If any step fails (download error, conversion error, storage error):
  - Print an informative error message
  - Skip to the next paper (do not crash the session)
- Maintain the session summary (accepted/skipped counts)
- Ensure the UX flow remains smooth and responsive

## Success Criteria
- Accepted papers trigger the full pipeline: download -> convert -> save
- Each step uses the real module implementations
- Failures in any step skip the paper and continue the session
- Session summary accurately reflects successes and skips

## Acceptance Criteria
- [ ] Stub functions are replaced with real module calls
- [ ] Pipeline flow is: download -> convert -> storage.save()
- [ ] Download errors are caught and reported; paper is skipped
- [ ] Conversion errors are caught and reported; paper is skipped
- [ ] Storage errors are caught and reported; paper is skipped
- [ ] Session summary shows correct accepted/skipped counts
- [ ] User experience remains interactive and responsive
