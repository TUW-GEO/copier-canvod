"""Check that a generated package's TOML, YAML, CITATION.cff and Markdown
front matter parse.

Usage: python tests/check_generated.py <generated package directory>
"""

from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

import yaml

SKIP = {".git", ".venv", "site", "node_modules"}


def files(root: Path, *suffixes: str) -> list[Path]:
    """Every file below ``root`` with one of ``suffixes``, outside ``SKIP``."""
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix in suffixes
        and not SKIP.intersection(path.relative_to(root).parts)
    )


def main(root: Path) -> int:
    errors = []
    for path in files(root, ".toml"):
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as error:
            errors.append(f"{path.relative_to(root)}: {error}")
    for path in files(root, ".yml", ".yaml", ".cff"):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            errors.append(f"{path.relative_to(root)}: {error}")
    for path in files(root, ".md"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        try:
            yaml.safe_load(text.split("---\n", 2)[1])
        except (yaml.YAMLError, IndexError) as error:
            errors.append(f"{path.relative_to(root)} (front matter): {error}")
    cff = subprocess.run(
        ["cffconvert", "--validate", "--infile", str(root / "CITATION.cff")],
        capture_output=True,
        text=True,
        check=False,
    )
    if cff.returncode:
        errors.append(f"CITATION.cff: {cff.stdout}{cff.stderr}".strip())
    for error in errors:
        print(error, file=sys.stderr)
    print(f"{root.name}: {len(errors)} files that do not parse")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
