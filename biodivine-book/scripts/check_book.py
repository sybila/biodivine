#!/usr/bin/env python3
"""Checks the Biodivine book: structure, examples, and the built HTML.

Run from anywhere (paths are resolved relative to the book):

    python3 scripts/check_book.py            # source-level checks
    python3 scripts/check_book.py --built    # additionally inspects _build

The book shows every example twice, once in Rust and once in Python, and it includes the examples
from real files so that a chapter cannot show code that no longer runs. Two properties of those
includes are checked rather than promised:

* every include is a *named region* of the example file (`:start-after:`/`:end-before:` around an
  ``ANCHOR`` comment) with `:dedent:` on, so a region can neither start nor end in the middle of a
  statement and never carries the example's own indentation;
* every line of every included region fits the book's code column, measured in the built HTML as the
  longest line of any highlighted code block (the budget is `CODE_LINE_BUDGET`, which is the same
  number `.rustfmt.toml` uses, so `cargo fmt` cannot reflow an example past it);
* every Rust example file is registered in `Cargo.toml` as an example named `<library>_<file>`
  that `cargo test` runs (`test = true`, `harness = false`), so no example is silently skipped.

Every example of the book is available in both Rust and Python with a switch between them. That is a
structural property, so it is checked rather than promised:

* every ``tab-set`` in the book contains exactly two ``tab-item`` blocks, one labelled Rust and one
  Python, each in its own sync group (so choosing a language in one example switches all of them);
* every example is included with ``literalinclude`` from a real file, the two members point at
  *different* files, and the Rust member is a ``.rs`` file while the Python member is a ``.py`` file;
* every chapter the book promises exists, and the book contains at least one example pair (a
  mis-globbed directory would otherwise make all of the above vacuous);
* with ``--built``, the generated HTML contains the chapters and sphinx-design tab markup.
"""

from __future__ import annotations

import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
MANIFEST = ROOT / "Cargo.toml"

BOOK = ROOT / "src"
BUILD = ROOT / "_build"

#: The name the book is presented under.
DISPLAY_NAME = "The Biodivine book"

#: Chapters the book promises, relative to `src/` (the titles are also searched for in the built
#: HTML). Each library is a directory with its own `index.md`.
CHAPTERS = {
    "index.md": DISPLAY_NAME,
    "installation.md": "Installation",
    "packages.md": "How the packages fit together",
    "xml-dom/index.md": "Biodivine XML DOM",
    "xml-dom/getting-started.md": "Getting started",
    "xml-dom/building-documents.md": "Building documents",
    "xml-dom/traversing-and-editing.md": "Traversing and editing",
    "xml-dom/namespaces.md": "Namespaces",
    "xml-dom/parsing-and-serializing.md": "Parsing and serializing",
    "xml-dom/validation.md": "Validating a document",
    "xml-dom/thread-safety.md": "Thread safety",
    "xml-dom/python-usage.md": "Using the Python package",
    "xml-dom/limitations.md": "Known limitations and gotchas",
    "xml-dom/design-notes.md": "Design notes",
    "sbml/index.md": "Biodivine SBML",
    "sbml/getting-started.md": "Getting started",
    "sbml/levels-and-packages.md": "Levels, packages and versions",
    "sbml/object-model.md": "The object model",
    "sbml/validation.md": "Validating a document",
    "sbml/mathml.md": "MathML formulas",
    "sbml/extensions.md": "Writing an SBML extension",
    "sbml/python-usage.md": "Using the Python package",
    "sbml/limitations.md": "Known limitations",
    "sbml/design-notes.md": "Design notes",
}

#: Maximum number of characters on a line of an included example, and of a rendered code line.
#: Shibuya's content column is about 800 pixels wide and its monospace font is 13 pixels, so a line
#: of 88 characters is roughly 690 pixels: it fits without horizontal scrolling.
CODE_LINE_BUDGET = 88

#: The theme the built book must use.
THEME = "shibuya"

TAB_SET = re.compile(r"^(?P<fence>:{3,})\{tab-set\}\s*$")
TAB_ITEM = re.compile(r"^(?P<fence>:{3,})\{tab-item\}\s*(?P<label>.*?)\s*$")
COLON_ONLY = re.compile(r"^(?P<fence>:{3,})\s*$")
SYNC = re.compile(r"^\s*:sync:\s*(\S+)\s*$")
INCLUDE = re.compile(r"literalinclude\}\s+(\S+)")
START_AFTER = re.compile(r"^\s*:start-after:\s*(?P<marker>.+?)\s*$")
END_BEFORE = re.compile(r"^\s*:end-before:\s*(?P<marker>.+?)\s*$")
LINES_OPTION = re.compile(r"^\s*:lines:")
DEDENT_OPTION = re.compile(r"^\s*:dedent:")
ANCHOR = re.compile(r"^(?P<indent>\s*)(?P<prefix>//|#) ANCHOR: (?P<name>[a-z0-9_]+)\s*$")


def include_blocks(lines: list[str]) -> list[dict[str, object]]:
    """Every `literalinclude` block, with the options it carries."""
    blocks: list[dict[str, object]] = []
    index = 0
    while index < len(lines):
        if not INCLUDE.search(lines[index]):
            index += 1
            continue
        block = {
            "file": INCLUDE.search(lines[index]).group(1),
            "line": index + 1,
            "start": "",
            "end": "",
            "lines": False,
            "dedent": False,
        }
        index += 1
        while index < len(lines) and lines[index].startswith(":"):
            if found := START_AFTER.match(lines[index]):
                block["start"] = found.group("marker")
            if found := END_BEFORE.match(lines[index]):
                block["end"] = found.group("marker")
            if LINES_OPTION.match(lines[index]):
                block["lines"] = True
            if DEDENT_OPTION.match(lines[index]):
                block["dedent"] = True
            index += 1
        blocks.append(block)
    return blocks


def anchor_name(marker: str) -> str:
    """The anchor name in `[//|#] ANCHOR: name`, or the marker itself when it is already a name."""
    found = re.search(r"ANCHOR: ([a-z0-9_]+)", marker)
    return f"ANCHOR: {found.group(1)}" if found else marker


def region(text: str, start_marker: str, end_marker: str) -> list[str] | None:
    """The lines between two anchor comments, or `None` if they are missing or out of order."""
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if start_marker in line), None)
    end = next((i for i, line in enumerate(lines) if end_marker in line and (start is None or i > start)), None)
    if start is None or end is None:
        return None
    return lines[start + 1 : end]


def parse_tab_sets(lines: list[str]) -> list[list[tuple[str, str, str]]]:
    """Every tab set in `lines`, as a list of `(label, sync_group, included_file)` items.

    The fence lengths disambiguate the nesting: a tab item closes with a shorter colon-only line
    than the tab set that contains it (``:::`` versus ``::::``).
    """
    sets: list[list[tuple[str, str, str]]] = []
    index = 0
    while index < len(lines):
        opening = TAB_SET.match(lines[index])
        if not opening:
            index += 1
            continue
        set_fence = len(opening.group("fence"))
        index += 1
        items: list[tuple[str, str, str]] = []
        while index < len(lines):
            closer = COLON_ONLY.match(lines[index])
            if closer and len(closer.group("fence")) >= set_fence:
                index += 1
                break
            item = TAB_ITEM.match(lines[index])
            if not item:
                index += 1
                continue
            label = item.group("label")
            sync = ""
            include = ""
            index += 1
            while index < len(lines):
                closer = COLON_ONLY.match(lines[index])
                if closer and len(closer.group("fence")) < set_fence:
                    index += 1
                    break
                if not sync and (found := SYNC.match(lines[index])):
                    sync = found.group(1)
                if not include and (found := INCLUDE.search(lines[index])):
                    include = found.group(1)
                index += 1
            items.append((label, sync, include))
        sets.append(items)
    return sets


def check_examples(problems: list[str]) -> None:
    """Every include is an anchored, dedented region whose lines fit the code column."""
    used: set[tuple[str, str]] = set()
    for chapter in sorted(CHAPTERS):
        path = BOOK / chapter
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8").split("\n")
        for block in include_blocks(lines):
            target = (path.parent / str(block["file"])).resolve()
            where = f"{chapter}:{block['line']}"
            if not target.is_file():
                continue  # reported by the tab-set check
            if block["lines"]:
                problems.append(
                    f"{where}: includes {block['file']} with `:lines:`, which can cut a statement in "
                    f"half; use an anchored region instead"
                )
                continue
            if not block["start"] or not block["end"]:
                problems.append(
                    f"{where}: includes {block['file']} without `:start-after:` and `:end-before:`"
                )
                continue
            if not block["dedent"]:
                problems.append(f"{where}: includes {block['file']} without `:dedent:`")
            body = region(target.read_text(encoding="utf-8"), str(block["start"]), str(block["end"]))
            if body is None:
                problems.append(
                    f"{where}: the anchors {block['start']!r} / {block['end']!r} are missing from "
                    f"{block['file']} or out of order"
                )
                continue
            if not any(line.strip() for line in body):
                problems.append(f"{where}: the anchored region of {block['file']} is empty")
            for number, line in enumerate(body, 1):
                if len(line.rstrip()) > CODE_LINE_BUDGET:
                    problems.append(
                        f"{where}: line {number} of the region in {block['file']} is "
                        f"{len(line.rstrip())} characters, over the {CODE_LINE_BUDGET} budget"
                    )
            used.add((target, anchor_name(str(block["start"]))))
            used.add((target, anchor_name(str(block["end"]))))

    # An anchor that no chapter uses is dead weight in the example; report it so it cannot rot.
    for path in example_files():
        for line in path.read_text(encoding="utf-8").split("\n"):
            found = ANCHOR.match(line)
            if found and "ANCHOR_END" not in line:
                if (path, f"ANCHOR: {found.group('name')}") not in used:
                    problems.append(
                        f"{path.relative_to(ROOT)}: the anchor `{found.group('name')}` is not "
                        f"used by the book"
                    )
    print(f"book sources: {len(used) // 2} anchored example regions")


def example_files() -> list[Path]:
    """Every example of the book: `examples/<library>/<name>.rs` and `.py`."""
    return sorted(EXAMPLES.glob("*/*.rs")) + sorted(EXAMPLES.glob("*/*.py"))


def check_manifest(problems: list[str]) -> None:
    """Every Rust example is a Cargo example that `cargo test` runs, under its canonical name."""
    manifest = MANIFEST.read_text(encoding="utf-8")
    registered: dict[str, dict[str, str]] = {}
    for entry in manifest.split("[[example]]")[1:]:
        fields = dict(re.findall(r'^(\w+)\s*=\s*"?([^"\n]*)"?\s*$', entry, flags=re.M))
        registered[fields.get("path", "")] = fields
    rust_examples = [path for path in example_files() if path.suffix == ".rs"]
    for path in rust_examples:
        relative = path.relative_to(ROOT).as_posix()
        fields = registered.pop(relative, None)
        if fields is None:
            problems.append(f"{relative} is not an `[[example]]` of Cargo.toml")
            continue
        expected = f"{path.parent.name}_{path.stem}"
        if fields.get("name") != expected:
            problems.append(f"{relative} is registered as `{fields.get('name')}`, not `{expected}`")
        if fields.get("test") != "true" or fields.get("harness") != "false":
            problems.append(f"{relative} needs `test = true` and `harness = false`")
    for relative in registered:
        problems.append(f"Cargo.toml registers {relative}, which does not exist")
    if not rust_examples:
        problems.append("the book has no Rust examples at all — is the layout right?")
    print(f"examples: {len(rust_examples)} Rust examples registered in Cargo.toml")


def check_sources() -> list[str]:
    problems: list[str] = []
    pairs = 0
    for chapter, title in CHAPTERS.items():
        path = BOOK / chapter
        if not path.is_file():
            problems.append(f"missing chapter {chapter} (expected to be about `{title}`)")
            continue
        lines = path.read_text(encoding="utf-8").split("\n")
        if title not in "\n".join(lines[:6]):
            problems.append(f"{chapter}: does not start with the title `{title}`")

        for items in parse_tab_sets(lines):
            pairs += 1
            if len(items) != 2:
                problems.append(
                    f"{chapter}: a tab-set has {len(items)} tab(s); every example needs exactly "
                    f"two (Rust and Python)"
                )
                continue
            labels = {label.lower() for label, _, _ in items}
            if labels != {"rust", "python"}:
                problems.append(f"{chapter}: a tab-set is labelled {sorted(labels)}, not Rust/Python")
            syncs = {sync for _, sync, _ in items}
            if syncs != {"rust", "python"}:
                problems.append(
                    f"{chapter}: a tab-set uses sync groups {sorted(syncs)}; both members must be in "
                    f"their own group (`rust` / `python`) so the switch is linked"
                )
            paths = {}
            for label, _, include in items:
                if not include:
                    problems.append(f"{chapter}: the {label} tab has no `literalinclude`")
                    continue
                target = (path.parent / include).resolve()
                if not target.is_file():
                    problems.append(f"{chapter}: the {label} tab includes {include}, which is missing")
                    continue
                paths[label.lower()] = target
            if len(paths) == 2:
                rust, python = paths.get("rust"), paths.get("python")
                if rust == python:
                    problems.append(f"{chapter}: both tabs include the same file ({rust})")
                elif rust is not None and rust.suffix != ".rs":
                    problems.append(f"{chapter}: the Rust tab includes {rust.name}, not a `.rs` file")
                elif python is not None and python.suffix != ".py":
                    problems.append(f"{chapter}: the Python tab includes {python.name}, not a `.py` file")
    if pairs == 0:
        problems.append("the book contains no example pair at all — is the layout right?")
    print(f"book sources: {len(CHAPTERS)} chapters, {pairs} language pairs")
    check_examples(problems)
    check_manifest(problems)
    return problems


def check_built() -> list[str]:
    problems: list[str] = []
    if not BUILD.is_dir():
        return [f"{BUILD} does not exist; build the book before using --built"]
    pages = {
        path.relative_to(BUILD).with_suffix("").as_posix(): path for path in BUILD.rglob("*.html")
    }
    for chapter, title in CHAPTERS.items():
        stem = Path(chapter).with_suffix("").as_posix()
        if stem not in pages:
            problems.append(f"the built book has no page for {chapter}")
            continue
        html = unescape(pages[stem].read_text(encoding="utf-8", errors="ignore"))
        if title not in html:
            problems.append(f"the built page {stem}.html does not contain the title `{title}`")
    # The language switch is sphinx-design's, so the markup has to be there.
    tab_sets = sum(
        page.read_text(encoding="utf-8", errors="ignore").count("sd-tab-set")
        for page in pages.values()
    )
    if tab_sets == 0:
        problems.append("the built book contains no sphinx-design tab sets")
    if not any(THEME in page.read_text(encoding="utf-8", errors="ignore").lower() for page in pages.values()):
        problems.append(f"the built book does not look like it uses the {THEME} theme")
    if not any(
        DISPLAY_NAME in page.read_text(encoding="utf-8", errors="ignore") for page in pages.values()
    ):
        problems.append(f"the built book never mentions the display name `{DISPLAY_NAME}`")
    longest, where = longest_code_line(pages)
    if longest > CODE_LINE_BUDGET:
        problems.append(
            f"the longest rendered code line has {longest} characters (in {where}), over the "
            f"{CODE_LINE_BUDGET} budget: it would need horizontal scrolling"
        )
    print(
        f"built book: {len(pages)} pages, {tab_sets} tab-set occurrences, "
        f"longest code line {longest} characters"
    )
    return problems


def longest_code_line(pages: dict[str, Path]) -> tuple[int, str]:
    """The longest line of any highlighted code block in the built book."""
    longest, where = 0, ""
    for stem, page in sorted(pages.items()):
        html = page.read_text(encoding="utf-8", errors="ignore")
        for block in re.findall(r"<pre>(.*?)</pre>", html, re.S):
            text = unescape(re.sub(r"<[^>]+>", "", block))
            for line in text.split("\n"):
                if len(line.rstrip()) > longest:
                    longest, where = len(line.rstrip()), f"{stem}.html"
    return longest, where


def main() -> int:
    problems = check_sources()
    if "--built" in sys.argv:
        problems += check_built()
    if problems:
        print(f"\n{len(problems)} problem(s):", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print("the book is well-formed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
