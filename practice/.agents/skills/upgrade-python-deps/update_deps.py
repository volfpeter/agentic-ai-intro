# /// script
# dependencies = [
#   "packaging",
# ]
# ///

"""
Update dependency versions in pyproject.toml to latest available on PyPI.

Usage:
    uv run update_deps.py [--skip PKG [PKG ...]] [--pyproject PATH]
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from packaging.requirements import Requirement
from packaging.version import Version


PYPI_URL = "https://pypi.org/pypi/{name}/json"
VERSION_IN_SPEC_RE = re.compile(r"\d+(?:\.\d+)*")


def fetch_latest_version(package_name: str) -> str | None:
    url = PYPI_URL.format(name=package_name)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data["info"]["version"]
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError) as exc:
        print(f"  WARNING: Failed to fetch {package_name}: {exc}", file=sys.stderr)
        return None


def major_component(version_str: str) -> int:
    parts = tuple(int(p) for p in version_str.split("."))
    for p in parts:
        if p != 0:
            return p
    return 0


def update_dep_specifier(dep_text: str, old_ver: str, new_ver: str) -> str:
    return dep_text.replace(old_ver, new_ver)


def process_pyproject(pyproject_path: Path, skip_packages: set[str]) -> dict[str, tuple[str, str, str]]:
    import tomllib

    text = pyproject_path.read_text(encoding="utf-8")
    data = tomllib.loads(text)

    updated: dict[str, tuple[str, str, str]] = {}

    dep_sources: dict[str, list[str]] = {}

    if "project" in data and "dependencies" in data["project"]:
        dep_sources["project.dependencies"] = data["project"]["dependencies"]
    if "dependency-groups" in data:
        for group_name, deps in data["dependency-groups"].items():
            dep_sources[f"dependency-groups.{group_name}"] = deps

    for source_name, deps in dep_sources.items():
        print(f"\n[{source_name}]")
        for dep in deps:
            try:
                req = Requirement(dep)
            except Exception as exc:
                print(f"  Skipping unparseable dep '{dep}': {exc}")
                continue

            name = req.name
            if name in skip_packages:
                print(f"  Skipping {name} (--skip)")
                continue

            specifier = str(req.specifier)
            if not specifier:
                print(f"  Skipping {name} (no version constraint)")
                continue

            ver_match = VERSION_IN_SPEC_RE.search(specifier)
            if not ver_match:
                print(f"  Skipping {name} (no version number in specifier)")
                continue

            old_ver = ver_match.group()
            latest = fetch_latest_version(name)
            if latest is None:
                continue

            if Version(latest) == Version(old_ver):
                print(f"  {name} == {latest}")
                continue

            new_spec = update_dep_specifier(specifier, old_ver, latest)
            old_dep_str = f"{name}{specifier}"
            new_dep_str = f"{name}{new_spec}"

            if old_dep_str in text:
                text = text.replace(old_dep_str, new_dep_str, 1)
                updated[name] = (source_name, old_ver, latest)
                print(f"  {name}: {old_ver} -> {latest}")
            else:
                print(f"  WARNING: Could not locate '{old_dep_str}' in file", file=sys.stderr)

    pyproject_path.write_text(text, encoding="utf-8")
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Update pyproject.toml dependency versions to latest on PyPI")
    parser.add_argument("--skip", nargs="*", default=[], help="Package names to skip")
    parser.add_argument(
        "--pyproject",
        type=Path,
        default=Path("pyproject.toml"),
        help="Path to pyproject.toml",
    )
    args = parser.parse_args()

    skip_set = set(args.skip)
    pyproject_path = args.pyproject

    if not pyproject_path.exists():
        print(f"Error: {pyproject_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Updating dependencies in {pyproject_path} ...")
    updated = process_pyproject(pyproject_path, skip_set)

    if not updated:
        print("\nNo dependencies were updated.")
        return

    major_changes = []
    for name, (source, old_ver, new_ver) in updated.items():
        if major_component(old_ver) != major_component(new_ver):
            major_changes.append(name)

    if major_changes:
        print("\nMajor version changes (most significant non-zero component changed):")
        for name in major_changes:
            source, old_ver, new_ver = updated[name]
            print(f"  {name}: {old_ver} -> {new_ver}")
    else:
        print("\nNo major version changes.")


if __name__ == "__main__":
    main()
