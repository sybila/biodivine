# Biodivine XML DOM

Biodivine XML DOM is an XML DOM library with full namespace support, whole-document validation and
thread-safe documents, in Rust with an idiomatic Python interface on top.

The library is designed for **document manipulation**: you build, edit, traverse, validate and
serialize XML trees. In code it is spelled `biodivine-lib-xml-dom` (the Rust crate) and
`biodivine.xml_dom` (the Python module). It is not a streaming parser, but it gets the awkward parts right —
expanded names instead of prefix juggling, one lock per document so a tree can be shared between
threads, and a validation pass that reports everything at once instead of failing on the first
problem.

## What it looks like

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/getting_started.rs
:language: rust
:start-after: ANCHOR: document
:end-before: ANCHOR_END: document
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/getting_started.py
:language: python
:start-after: ANCHOR: document
:end-before: ANCHOR_END: document
:dedent:
```
:::
::::

## The layers

| layer | what it is | who uses it |
| --- | --- | --- |
| `biodivine-lib-xml-dom` | the Rust library; no PyO3 anywhere | Rust programs |
| `biodivine-lib-xml-dom-py-sys` | a thin PyO3 mirror of the Rust API, compiled into the `biodivine-sys` extension as `biodivine_sys.xml_dom` | the layer below |
| `biodivine.xml_dom` | the Python module: argument coercion, Pythonic protocols, conveniences | Python programs |

The mapping between the Rust API and the Python one is itemised on the `documentation::bindings`
page of the crate documentation, and the design notes ship with the rustdoc as well.
[How the packages fit together](../packages.md) explains why the native layer of every Biodivine
library lives in one shared extension.

## Running the examples

The examples of this part are in `examples/xml_dom/` of the book: each chapter's Rust example is a
Cargo example called `xml_dom_<file name>`, and its Python counterpart is the `.py` file of the same
name.

```sh
cargo run --example xml_dom_getting_started              # Rust
.venv/bin/python examples/xml_dom/getting_started.py     # Python
```

## Chapters

```{toctree}
:maxdepth: 1
getting-started
building-documents
traversing-and-editing
namespaces
parsing-and-serializing
validation
thread-safety
python-usage
limitations
design-notes
```
