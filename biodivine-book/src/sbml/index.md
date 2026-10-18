# Biodivine SBML

SBML (the *Systems Biology Markup Language*) is the file format models of biological systems are
exchanged in: compartments, species, reactions, rules, events, and the mathematics that connects
them. Biodivine SBML reads such a document, exposes it as typed objects you can inspect and edit,
validates it against the rules of the specification, and writes it back.

The library is a Rust crate (`biodivine-lib-sbml`) with a Python package on top of it
(`biodivine.sbml`). Every chapter shows the two side by side, so you can read whichever you use and
see what the other one does.

## What the library gives you

* **The object model of the specification.** A document is a tree of typed objects: a `Model` has
  `species`, a `Reaction` has a `kinetic_law`, a `Species` has an identifier, a compartment and a
  concentration. The types follow the specification's class hierarchy, so a value knows whether it
  is an `SBase`, a `Reaction` or a `FunctionDefinition`.
* **Validation.** Every rule of the specification the library implements is one function with a
  rule id, a severity and a message, and validation returns the report rather than throwing it away.
  It also reports what it could *not* check (see [Validating a document](validation.md)).
* **MathML.** The formulas of a model (a kinetic law, a rule, an event assignment) are typed trees,
  with the operators, constants and symbols of the subset SBML permits.
* **The packages.** FBC, Layout and Qual are modelled as part of the same object model, and the
  mechanisms a package needs are public: see [Writing an SBML extension](extensions.md).
* **The older levels.** Level 3 (every version) and Level 2 resolve a model; a document of a level
  the library does not model is still readable and says so. [Levels, packages and
  versions](levels-and-packages.md) has the details, and
  [Known limitations](limitations.md) states the contract in one place.

## A first look

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

## How the two layers fit together

The Python package is a thin, idiomatic layer over the Rust library, and the boundary is worth
knowing because error messages and stack traces cross it:

```text
biodivine-lib-sbml          the Rust library: the object model, validation, MathML
biodivine-lib-sbml-py-sys   a mirror of the Rust API, one Python class per type
biodivine-sys               the native extension that links the mirrors together
biodivine.sbml              the Pythonic layer: properties, sequences, exceptions
```

The middle layer is generated from the Rust library and mirrors it exactly (`Species.id` is a
property in Python, and it is the same accessor as `Species::id()` in Rust); the outer layer adds
what Python expects - a list is a sequence, a failure is an exception, a name is spelled the way
Python spells it. You never see the middle layer from the outside: every value the package hands you
is a class of `biodivine`.

## Where to go next

* [Getting started](getting-started.md) - read, inspect, edit, validate and write.
* [Levels, packages and versions](levels-and-packages.md) - which documents resolve a model.
* [The object model](object-model.md) - the typed wrappers and how to walk a document.
* [Validating a document](validation.md) - rules, severities and the report.
* [MathML formulas](mathml.md) - the formula layer.
* [Writing an SBML extension](extensions.md) - add a package of your own.
* [Using the Python package](python-usage.md) - the Python entry point.
* [Known limitations](limitations.md) - what the library does not do, stated plainly.
* [Design notes](design-notes.md) - why the layers look the way they do.

```{toctree}
:maxdepth: 1
:hidden:
getting-started
levels-and-packages
object-model
validation
mathml
extensions
python-usage
limitations
design-notes
```
