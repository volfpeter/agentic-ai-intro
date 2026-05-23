---
name: make-python-skill
description: Create a reusable agent skill that bundles a Python script with PEP 723 dependencies
---

## What this does

Creates a complete skill directory under `.agents/skills/<name>/` containing:

- `SKILL.md` — tells the agent when/how to use the skill
- One or more Python scripts that implement the behavior

## When to use this skill

- The user asks you to create a skill that performs a specific task
- The user did not define the programming language to use for the skill script and Python is a good fit
- The user asked to use Python for the script part of the skill

## Structure

```
.agents/skills/<name>/
├── SKILL.md
└── <script>.py
```

If the script is complex, you can split them up into multiple Python files.

## SKILL.md conventions

Frontmatter must have `name` and `description`. The body should explain:

- **What this does** — the steps the script performs
- **When to use** — trigger phrases and input patterns
- **How to run** — the `uv run` command (paths relative to the skill folder)

Write the "How to run" section like this:

`````markdown
## How to run

````bash
uv run <script>.py <required-arg> --output-dir /absolute/path/to/output


## Python script conventions

- Place the PEP 723 dependency block at the **very top** of the file (before even the docstring):

```python
# /// script
# dependencies = [
#   "requests",
#   "pyyaml",
# ]
# ///
```

"""..."""
````
`````

- Run with `uv run`, which auto-installs dependencies from the PEP 723 block
- Do **not** hardcode output paths — accept them as required CLI arguments. The agent resolves the project root and passes absolute paths
- Keep it a single `.py` module unless the logic genuinely warrants splitting
- Use standard library + the declared dependencies; no imports from the host project
- **Pin dependency versions:** when the script has dependencies, always check the latest available version on PyPI and pin each dependency to that exact version (e.g. `"requests==2.32.3"`)

### Error handling

- Use `try`/`except` around operations that can actually fail.
- If the error is fatal: catch specific exceptions, print descriptive messages to **stderr**, and call `sys.exit(1)`.
- If the error is non-fatal: handle it and continue, print a message if it's important.

### Security

Always keep security in mind.

If the script creates temporary files or directories, always clean them up.

Scripts should be safe to re-run.
