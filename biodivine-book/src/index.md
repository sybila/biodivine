# The Biodivine book

Biodivine is a family of libraries for working with the models and file formats of systems biology.
Every library is written in Rust, published as its own crate, and available in Python as a submodule
of the `biodivine` package. This book teaches the libraries by example: every example is shown in
both languages, with a switch between them, and every example is a real program that is run when
the book is checked.

## What it looks like

The following builds a small XML document with a namespace and serializes it. The tabs switch every
example in the book between Rust and Python:

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../examples/xml_dom/getting_started.rs
:language: rust
:start-after: ANCHOR: document
:end-before: ANCHOR_END: document
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../examples/xml_dom/getting_started.py
:language: python
:start-after: ANCHOR: document
:end-before: ANCHOR_END: document
:dedent:
```
:::
::::

## The libraries

| library | Rust crate | Python module | what it does |
| --- | --- | --- | --- |
| [XML DOM](xml-dom/index.md) | `biodivine-lib-xml-dom` | `biodivine.xml_dom` | build, parse, edit, validate and serialize XML documents, with full namespace support and thread-safe documents |
| [SBML](sbml/index.md) | `biodivine-lib-sbml` | `biodivine.sbml` | read, edit and validate SBML models, including their MathML formulas and the SBML packages |

## How to read this book

* [Installation](installation.md) shows how to add the libraries to a Rust or a Python project.
* [How the packages fit together](packages.md) explains the crates and Python packages that make up
  Biodivine, and why the Python bindings of all libraries share one native extension. Read it if
  you want to know what `biodivine-sys` is, or if you are writing bindings yourself.
* Each library then has its own part, which starts with a "Getting started" tour and continues
  with chapters on specific topics, ending with its known limitations and pointers to the design
  documentation.

The API references are the documentation of each Rust crate (on [docs.rs](https://docs.rs)) and the
API reference of the `biodivine` Python package.

```{toctree}
:maxdepth: 1
:caption: Biodivine
installation
packages
```

```{toctree}
:maxdepth: 2
:caption: XML DOM
xml-dom/index
```

```{toctree}
:maxdepth: 2
:caption: SBML
sbml/index
```
