---
name: changelog
description: Update the changelog from recent changes
---

## What to do

- Look at the git history (current branch vs its base)
- Collect all user-facing changes
- Update `CHANGELOG.md`

## When to use

- Use this skill when a feature or change is fully implemented
- Ask clarifying questions if the you're not absolutely sure

## Do NOT

- Do NOT commit anything!
- Do NOT change files other than `CHANGELOG.md`

## Changelog format

- New changes go under the `## [next]` section
- If there is no `## [next]` section, add it
- The `## [next]` section can have the following subsections: `Added`, `Changed`, and `Updated`
- The `Added`, `Changed`, and `Updated` sections can only contain a single, unordered list
- List items are separated by an empty line
- Each changelist item has exactly one new list item
- Descriptions are short (preferably 1 line, max 3), but informative
- Descriptions are full sentences.
- **Avoid**: bold and italic text, unnecessary hyphenation and punctuation, filler text and AI slop in general
- Max 80 chars per line
