# Biodivine workspace

Biodivine is a family of libraries for systems biology, written in Rust and available in Python.
Each library is its own repository; this repository brings them together as git submodules, along
with the documentation that covers all of them.

| path | what it is |
| --- | --- |
| [`biodivine-lib-xml-dom`](https://github.com/sybila/biodivine-lib-xml-dom) | an XML DOM library: the `biodivine-lib-xml-dom` crate, plus its thin PyO3 wrapper crate |
| [`biodivine-py`](https://github.com/sybila/biodivine-py) | the Python bindings of every library: the `biodivine-sys` native extension and the `biodivine` package |
| [`biodivine-book`](biodivine-book) | the Biodivine book: tutorials for every library, with runnable examples in Rust and Python |

## How the repositories fit together

Every library repository contains two crates: the library itself, published on crates.io, and a
`_sys` crate of thin PyO3 wrappers, which is never published. `biodivine-py` links the `_sys` crates
of all libraries into one native Python extension (`biodivine-sys`), so that a Rust type has one
Python class no matter which library's bindings use it, and builds the documented `biodivine`
package on top of it, with one submodule per library. The book's chapter
[How the packages fit together](biodivine-book/src/packages.md) explains the layers in detail.

Repositories normally depend on each other through versions or git revisions. When a change spans
several of them, the dependencies can temporarily point at the submodules through `path`
dependencies. The book always uses the checked-out submodules, so it documents and tests exactly the
code in this workspace.

## Getting started

```sh
git clone --recurse-submodules git@github.com:sybila/biodivine.git
cd biodivine/biodivine-book
make python-env    # builds the Python packages from ../biodivine-py into .venv
make verify        # runs every example of the book and builds it
```

Each repository has its own `README.md` and `Makefile` with its development workflow.
