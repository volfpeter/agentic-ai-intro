I want you to write a skill that collects the dependencies of the current project from `pyproject.toml`, checks the latest available version of each dependency, and updates the dependency versions in `pyproject.toml`.
The user should be able to provide a list of dependency names which shouldn't be upgraded.
If any of the dependencies had a "major" version change (major meaning the most significant non-zero version number), output the names of these dependencies after completing the upgrade.
