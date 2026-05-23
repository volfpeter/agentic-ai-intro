# Task: LaTeX Source Downloader and Extractor

## Number
6b (parallel with 6a)

## Complexity
4

## Dependencies
2 (Data models and configuration)

## Description
Implement `SourceDownloader`: given an arXiv ID, download the `.tar.gz` source to a temp directory, extract it with `tarfile`, identify the main `.tex` file, return the paths of all `.tex` files and the main file.

## Details
- `SourceDownloader` class or module functions:
  - `download(arxiv_id)`: Download the LaTeX source `.tar.gz` from arXiv
    - Use arXiv's source URL pattern (e.g., `https://arxiv.org/e-print/{id}`)
    - Save to a temporary directory (use `tempfile` module)
  - `extract(tar_path)`: Extract the `.tar.gz` using `tarfile`
    - Handle nested directories within the archive
  - `find_main_tex(extracted_dir)`: Identify the main `.tex` file
    - Strategy 1: Find the largest `.tex` file by size
    - Strategy 2: Find a `.tex` file containing `\documentclass`
    - Use Strategy 2 as primary, fallback to Strategy 1
  - Return:
    - `all_tex_files`: list of paths to all `.tex` files
    - `main_tex_file`: path to the identified main file
- Clean up temp files after processing (or use context managers)

## Success Criteria
- Source `.tar.gz` is downloaded successfully for papers that have LaTeX sources
- Archive is extracted correctly
- Main `.tex` file is identified accurately
- All `.tex` file paths are returned
- Network and extraction errors are handled gracefully

## Acceptance Criteria
- [ ] `.tar.gz` source is downloaded to a temp directory
- [ ] Archive is extracted with `tarfile`
- [ ] Main `.tex` file is found via `\documentclass` search
- [ ] Fallback to largest `.tex` file if no `\documentclass` found
- [ ] Returns all `.tex` paths and the main file path
- [ ] Network errors are caught and reported
- [ ] Missing LaTeX source is handled gracefully (no crash)
