# Practice

This folder contains:

- A pre-configured Python project environment with `uv`, `ruff`, `ty`, and related `poethepoet` tasks.
- An example harness configuration.
- Coding challenges, project descriptions, example sessions and project implementations.

## Python setup

If you're not familiar with `uv`, `ruff`, and `ty`, these are the essentials:

- `uv`: Python package and project manager.
- `ruff`: Python code formatter and linter.
- `ty`: Python type checker and language server.

Useful commands:

- `uv run python`: Start the Python virtual environment with all dependencies (both standard and dev) installed.
- `uv add`: Add new dependencies.

`pyproject.toml` defines a couple of useful `poethepoet` tasks in the `[tool.poe.tasks]` section, which can be run with `uv run poe <task-name> [arguments]`:

- `check`: Runs the formatting, linting, and type checks.
- `format-fix`: Reformats the codebase, fixing formatting issues.
- `lint-fix`: Fixes automatically fixable linter issues.

## Harness/OpenCode configuration

- `AGENTS.md`: General instructions for agents.
- `.agents/`: Various skills in a format that's recognized by both OpenCode and other harnesses
- `.opencode/`: OpenCode config with custom agents, commands, and local provider config matching the llama.cpp example from the slides.

## Experimentation and examples

- `challenges/`: Coding challenges for experimenting with different agents (e.g. `teacher`), commands (e.g. `/explain`), and skills.
- `projects/`: More complex project ideas for experimentation. Complex enough to try the `/learn`, `/grill-me`, `/checkpoint`, `/to-plan`, `/what-went-wrong` commands and the `review` or `changelog` skills.
- `ai/`: Memory, prompts can go here, and agents can also store plans, task lists, etc. in this folder. It is normally git ignored.
- `sessions/`: A couple of example sessions.
- `arxiv-md/`: Different implementation milestones of the `arxiv-markdown-download.md` project (in `projects/`). Every folder contains the OpenCode session (`opencode-session.md`) that implemented the given milestone.

## `.gitignore` and agents

Well-behaved harnesses don't allow agent's to access files that are ignored by git. This can be a problem for if you need files for agents (prompts, memory, task lists) that you don't want to commit.

Harnesses offer different features or settings to work around this. Some examples:

- OpenCode: `.ignore` file can be added to repo, it is merged with `.gitignore` for the agent, allowing overrides.
- Zed: `file_scan_inclusions` and `file_scan_exclusions` settings.
