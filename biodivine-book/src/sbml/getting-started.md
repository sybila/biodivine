# Getting started

This chapter is a tour of the library in the order you are likely to need it. Every section is a
short program, shown in Rust and in Python, that you can copy and extend; the assertions are what
makes each file runnable, and the book includes the files verbatim.

## Install

Rust:

```sh
cargo add biodivine-lib-sbml
```

Python (the library is the `sbml` module of the `biodivine` package):

```sh
pip install biodivine
```

[Installation](../installation.md) explains how to build the Python package from source.

## Read a document

The document the examples below use is this one - a cell with one species in it:

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/getting_started.rs
:language: rust
:start-after: ANCHOR: model
:end-before: ANCHOR_END: model
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/getting_started.py
:language: python
:start-after: ANCHOR: model
:end-before: ANCHOR_END: model
:dedent:
```
:::
::::

Reading parses the XML and checks that it is a document this library understands: the container
element, its level and version, and the well-formedness of the whole tree. A document of a
level/version the library does not model is still readable - see
[Levels, packages and versions](levels-and-packages.md) for what happens to its model.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/getting_started.rs
:language: rust
:start-after: ANCHOR: read
:end-before: ANCHOR_END: read
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/getting_started.py
:language: python
:start-after: ANCHOR: read
:end-before: ANCHOR_END: read
:dedent:
```
:::
::::

## Look at the model

The model is a tree of typed objects. An accessor reads one attribute or one child with the rules
of the specification: an identifier, a number, a boolean or an enumerated value. A child that the
specification makes optional reads as "nothing", which is what a document without a model, or
without a list of species, looks like.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/getting_started.rs
:language: rust
:start-after: ANCHOR: inspect
:end-before: ANCHOR_END: inspect
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/getting_started.py
:language: python
:start-after: ANCHOR: inspect
:end-before: ANCHOR_END: inspect
:dedent:
```
:::
::::

## Change it

An accessor is a *view* onto one attribute or one child of one element: writing through it changes
the document in place, and the element is still the element. A new object is created from the
document it will belong to (which is what ties it to that document's namespace declarations), then
added to a list.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/getting_started.rs
:language: rust
:start-after: ANCHOR: edit
:end-before: ANCHOR_END: edit
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/getting_started.py
:language: python
:start-after: ANCHOR: edit
:end-before: ANCHOR_END: edit
:dedent:
```
:::
::::

## Validate it

Validation returns a report: every finding names the rule that produced it, how serious it is, and
what is wrong. [Validating a document](validation.md) is the full story.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/getting_started.rs
:language: rust
:start-after: ANCHOR: validate
:end-before: ANCHOR_END: validate
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/getting_started.py
:language: python
:start-after: ANCHOR: validate
:end-before: ANCHOR_END: validate
:dedent:
```
:::
::::

## Write it back

Writing serializes the document that is in memory. Text the library does not interpret - a `notes`,
an `annotation`, the inside of a MathML element - is kept exactly as it was read; only what the
specification *interprets* as a value is read with its whitespace rules, so a read/edit/write cycle
does not rewrite the parts of a document the library does not understand.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/getting_started.rs
:language: rust
:start-after: ANCHOR: write
:end-before: ANCHOR_END: write
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/getting_started.py
:language: python
:start-after: ANCHOR: write
:end-before: ANCHOR_END: write
:dedent:
```
:::
::::

## If you know libSBML

The two libraries describe the same standard, and the names differ enough to be worth a table.
Everything on the right is covered in this book; the differences are Python's conventions (a
property instead of a getter, a sequence instead of a list object, an exception instead of a
return code).

| libSBML (C++/Python) | `biodivine.sbml` |
| --- | --- |
| `readSBML(path) -> SBMLDocument` | `sbml.read(path) -> Document` |
| `readSBMLFromString(text)` | `sbml.reads(text)` |
| `document.writeSBML(path)` / `toSBML()` | `document.write(path)` / `document.to_string()` |
| `document.getModel()` | `document.model` |
| `model.getSpecies()` / `getNumSpecies()` | `model.species` (a sequence: `len(model.species)`) |
| `model.createSpecies()` | `Species.new_empty(document)` + `model.species.append(...)` |
| `species.getId()` / `setId(x)` | `species.id` / `species.id = x` |
| `document.checkConsistency()` + error log | `document.validate()` (a report, not a log) |
| `SBase.getNotes()` / `getAnnotation()` | `object.notes` / `object.annotation` (XML elements) |
| `species.getLevel()` | `document.level` |
| `MathML` (`ASTNode`) | `MathNode` (typed, iterable) |
| packages (`FbcModelPlugin`, ...) | modelled in the core types, plus the extension mechanism |
