# The Biodivine book

The tutorial documentation of the Biodivine libraries. It teaches each library by example, and every
example is shown in Rust and in Python with a switch between the two. Every example is also a real
program that `make test` runs, so the book cannot show code that no longer works.

The book documents the libraries as they are checked out in this workspace: the Rust examples
depend on the library crates through `path` dependencies on the submodules next to the book, and
the Python examples run against the `biodivine` package built from the `biodivine-py` submodule.

## Contents

| path | what it is |
| --- | --- |
| [`src/index.md`](src/index.md) | the landing page: what Biodivine is and how to read the book |
| [`src/installation.md`](src/installation.md), [`src/packages.md`](src/packages.md) | installing the libraries, and how the crates and Python packages fit together |
| [`src/xml-dom/`](src/xml-dom) | the XML DOM part (`biodivine-lib-xml-dom`, `biodivine.xml_dom`): a getting-started tour, one chapter per topic, the known limitations and the design notes |
| [`examples/<library>/`](examples) | the examples the chapters include: `<name>.rs` (the Cargo example `<library>_<name>`) and its Python twin `<name>.py` |
| [`tests/test_examples.py`](tests/test_examples.py) | runs every Python example, and the Python code blocks of the book-level pages and the library READMEs |
| [`scripts/check_book.py`](scripts/check_book.py) | checks the structure: chapters, Rust/Python tab pairs, anchored includes, the code-width budget, the example registry in `Cargo.toml`, and (with `--built`) the generated HTML |
| [`scripts/sync_diagrams.py`](scripts/sync_diagrams.py) | keeps the diagrams the book shares with a library's own documentation in step with the library's copy |

## Building and checking

```sh
make python-env   # .venv with the book toolchain and biodivine built from ../biodivine-py
make test         # every Rust example (cargo test) and every Python example (pytest)
make check        # the source checks, the diagrams, cargo fmt and clippy
make book         # build the HTML into _build/ (warnings are errors) and check the result
make verify       # all of the above
```

`make python-env` needs a Rust toolchain, because it builds the `biodivine-sys` extension. Run it
again after changing a library or its Python bindings.

## Writing a chapter

* A chapter lives in the directory of its library and starts with its title; add it to the
  library's `index.md` toctree and to `CHAPTERS` in `scripts/check_book.py`.
* Every example is a `tab-set` with exactly two `tab-item` blocks, Rust and Python, in the sync
  groups `rust` and `python`, so choosing a language switches every example on the page.
* Examples are included from files with `literalinclude`, always as a named region
  (`:start-after: ANCHOR: <name>` / `:end-before: ANCHOR_END: <name>`) with `:dedent:`. An anchor
  that no chapter uses is reported.
* A new Rust example file is registered in `Cargo.toml` as `[[example]]` named
  `<library>_<file>`, with `test = true` and `harness = false`, so `cargo test` runs it.
* Code lines in the book fit 88 characters; `.rustfmt.toml` formats the Rust examples to that width.

## Adding a library

Create `src/<library>/index.md` and its chapters, add the part to the toctree of `src/index.md`
and to the table of libraries there, put the examples under `examples/<library_name>/`, add the
library crate to `[dependencies]` in `Cargo.toml`, and list its chapters in `scripts/check_book.py`.
