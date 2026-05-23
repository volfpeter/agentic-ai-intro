# Task: Interactive Selection Loop (Stubbed Pipeline)

## Number
5

## Complexity
4

## Dependencies
2 (Data models and configuration), 4 (Display module)

## Description
Build the `for paper in results` loop that shows the detail card and accepts Y/n/q input. Use stub functions for download/convert/save that only print what they would do. This validates the UX flow before the backend exists.

## Details
- Iterate over the list of `Paper` objects from the search module
- For each paper:
  1. Display the detail card view
  2. Prompt the user with "Accept? [Y/n/q]" (default: Y)
  3. Handle input:
     - `Y` or Enter: accept the paper
     - `n`: skip the paper
     - `q`: quit the loop and exit
- For accepted papers, call stub functions:
  - `download_source(paper.id)` -> prints "Would download source for {id}"
  - `convert_to_markdown(tex_files)` -> prints "Would convert LaTeX to Markdown"
  - `save_to_storage(paper, markdown)` -> prints "Would save {filename}.md"
- Ensure the loop handles invalid input gracefully (re-prompt)
- Track which papers were accepted, skipped, or quit

## Success Criteria
- Loop runs through all papers showing the detail card
- Y/n/q inputs are handled correctly
- Stub functions print expected messages for accepted papers
- Quit exits cleanly without processing remaining papers

## Acceptance Criteria
- [ ] Loop iterates over all search results
- [ ] Detail card is shown for each paper
- [ ] Y/Enter accepts, n skips, q quits
- [ ] Invalid input re-prompts
- [ ] Stub functions print what they would do
- [ ] Session summary is printed at the end (accepted/skipped counts)
