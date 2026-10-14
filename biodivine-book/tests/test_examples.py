"""Runs every Python example of the book, and the Python code blocks of the pages around them.

The chapters include the example files verbatim, so running them is what makes "the examples
work" a checked property: a chapter cannot show a snippet that no longer runs. The READMEs of the
libraries carry a Python example too; they are run here because the book is where the libraries'
Python interface is exercised against the checked-out sources.
"""

from __future__ import annotations

import re
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
EXAMPLES = sorted((ROOT / "examples").glob("*/*.py"))

#: Markdown pages whose ```python blocks are runnable programs (one namespace per page): the
#: book-level pages and the library READMEs. The chapters of a library show their examples with
#: `literalinclude` from the example files; an inline block in a chapter is a fragment.
PAGES = sorted((ROOT / "src").glob("*.md")) + [WORKSPACE / "biodivine-lib-xml-dom" / "README.md"]


def _python_blocks(page: Path) -> list[str]:
    return re.findall(r"```python\n(.*?)```", page.read_text(encoding="utf-8"), flags=re.DOTALL)


def test_the_book_has_python_examples() -> None:
    """A mis-globbed directory would silently run nothing, so the count is asserted."""
    assert len(EXAMPLES) >= 8, f"expected the Python examples under {ROOT / 'examples'}"
    assert all(path.with_suffix(".rs").is_file() for path in EXAMPLES), (
        "every Python example has a Rust counterpart of the same name"
    )


@pytest.mark.parametrize("example", EXAMPLES, ids=lambda path: f"{path.parent.name}/{path.stem}")
def test_example_runs(example: Path) -> None:
    runpy.run_path(str(example), run_name="__main__")


@pytest.mark.parametrize(
    "page",
    [page for page in PAGES if _python_blocks(page)],
    ids=lambda page: page.relative_to(WORKSPACE).as_posix(),
)
def test_page_code_blocks_run(page: Path) -> None:
    namespace: dict[str, object] = {"__name__": "__main__"}
    for index, block in enumerate(_python_blocks(page)):
        exec(compile(block, f"{page.name}[{index}]", "exec"), namespace)
