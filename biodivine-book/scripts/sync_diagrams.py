#!/usr/bin/env python3
"""Copies the diagrams of the libraries into the chapters that show them.

    python3 scripts/sync_diagrams.py            # write the diagrams into the chapters
    python3 scripts/sync_diagrams.py --check    # fail if a chapter is out of date

A diagram that the book shares with a library's own documentation lives in that library's
repository (under `docs/assets/`), which is its single source of truth. The chapters carry the SVG
inline, between markers, so that the same markup renders in the book and in the library's rustdoc:

    <!-- diagram: model.svg -->
    <svg ...>...</svg>
    <!-- /diagram -->

This script keeps the inline copies in step with the files; `--check` reports a chapter that has
drifted from its source.
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = ROOT.parent

#: chapter (relative to `src/`) -> the diagrams it shows, as paths relative to the workspace.
CHAPTERS = {
    "xml-dom/building-documents.md": ["biodivine-lib-xml-dom/docs/assets/model.svg"],
    "xml-dom/python-usage.md": ["biodivine-lib-xml-dom/docs/assets/layers.svg"],
}

BEGIN = "<!-- diagram: {name} -->"
END = "<!-- /diagram -->"


def rendered(chapter: str, diagrams: list[str]) -> str:
    """The chapter with every diagram block filled in from its source file."""
    text = (ROOT / "src" / chapter).read_text(encoding="utf-8")
    for source in diagrams:
        path = WORKSPACE / source
        svg = path.read_text(encoding="utf-8").strip()
        begin = BEGIN.format(name=path.name)
        if begin not in text:
            sys.exit(f"{chapter} has no `{begin}` marker")
        pattern = re.compile(re.escape(begin) + r".*?" + re.escape(END), re.S)
        text = pattern.sub(lambda _: f"{begin}\n{svg}\n{END}", text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail instead of writing")
    arguments = parser.parse_args()
    stale = 0
    for chapter, diagrams in CHAPTERS.items():
        path = ROOT / "src" / chapter
        current = path.read_text(encoding="utf-8")
        expected = rendered(chapter, diagrams)
        if current == expected:
            continue
        if arguments.check:
            stale += 1
            print(f"{chapter} is out of date with its diagrams:")
            sys.stdout.writelines(
                difflib.unified_diff(
                    current.splitlines(keepends=True), expected.splitlines(keepends=True), n=1
                )
            )
        else:
            path.write_text(expected, encoding="utf-8")
            print(f"updated {chapter}")
    if stale:
        print(f"\n{stale} chapter(s) out of date; run scripts/sync_diagrams.py")
        return 1
    print("diagrams: every chapter matches its sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
