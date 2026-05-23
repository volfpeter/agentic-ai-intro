# Task: Display Module

## Number
4

## Complexity
3

## Dependencies
2 (Data models and configuration), 3 (arXiv search module)

## Description
Implement two Rich formatters: a table view for the initial overview of all results, and a detailed card view for the one-by-one interactive display.

## Details
- **Table View**:
  - Use `rich.table.Table` to display all search results
  - Columns: ID, Title, Authors (truncated), Published Date, Categories
  - Style the table with appropriate colors and formatting
  - Handle long titles/authors gracefully with truncation or wrapping
- **Detail Card View**:
  - Use `rich.panel.Panel` or similar to display a single paper's details
  - Show: Title, Authors (full list), Published Date, Categories, Abstract
  - Include a prompt hint (e.g., "[Y]es / [n]o / [q]uit")
  - Ensure the card is readable and well-formatted

## Success Criteria
- Table view renders a formatted overview of all search results
- Card view renders detailed information for a single paper with input hints
- Both views use Rich for styling and formatting

## Acceptance Criteria
- [ ] Table view displays all results with specified columns
- [ ] Long text is truncated or wrapped appropriately
- [ ] Detail card view shows all paper fields plus prompt hint
- [ ] Rich styling is applied consistently
- [ ] Views are tested with sample `Paper` objects
