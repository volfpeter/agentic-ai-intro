---
name: upgrade-python-deps
description: Update dependency versions in pyproject.toml to latest available on PyPI
---

## What this does

1. Reads `[project]dependencies` and `[dependency-groups]` from `pyproject.toml`
2. For each dependency, queries PyPI for the latest available version
3. Updates the version constraint in `pyproject.toml` to the latest version
4. Prints a summary of any "major" version changes (where the most significant non-zero version component changed)

## When to use

- The user asks to update/upgrade dependencies in `pyproject.toml`
- Trigger phrases: "update dependencies", "upgrade deps", "bump versions", "check for latest deps"
- The user wants to know which deps had a major version bump

## How to run

```bash
uv run update_deps.py [--skip PKG ...] [--pyproject PATH]
```

- `--skip`: Space-separated list of package names to leave unchanged
- `--pyproject`: Path to `pyproject.toml` (defaults to `./pyproject.toml`)
