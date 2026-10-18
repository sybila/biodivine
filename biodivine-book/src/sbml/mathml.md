# MathML formulas

The mathematics of a model - a kinetic law, a rule, an event assignment - is written in MathML.
SBML permits a *subset* of MathML, and this library models exactly that subset with typed nodes, so
a formula is navigated rather than parsed: a node knows what it is, which children it has, and how
to build the next node.

## Build a formula

An `apply` node holds its operator first and then the arguments, which is why a formula is
navigated by kind: the root is the application, and the operator is the kind of its first child. The
operators, constants and symbols of the subset are *closed* sets, so `MathOperator` names every
operator there is.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/mathml.rs
:language: rust
:start-after: ANCHOR: build
:end-before: ANCHOR_END: build
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/mathml.py
:language: python
:start-after: ANCHOR: build
:end-before: ANCHOR_END: build
:dedent:
```
:::
::::

## Attach it to the model

A `<math>` element is the child that holds a formula. A kinetic law has one, and so does a rule and
an event's delay; the typed accessor creates it if it is missing, and `set_expression` replaces what
it holds.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/mathml.rs
:language: rust
:start-after: ANCHOR: attach
:end-before: ANCHOR_END: attach
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/mathml.py
:language: python
:start-after: ANCHOR: attach
:end-before: ANCHOR_END: attach
:dedent:
```
:::
::::

## Read one back

Reading a formula back walks the same tree: the kinds come from the element names, and the payload
of a `cn` is the number the document spells. Text that the subset does not describe is not lost -
it stays in the document, reachable through the XML element of the node.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/mathml.rs
:language: rust
:start-after: ANCHOR: read
:end-before: ANCHOR_END: read
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/mathml.py
:language: python
:start-after: ANCHOR: read
:end-before: ANCHOR_END: read
:dedent:
```
:::
::::

## What the subset contains

The node kinds are the element kinds of the subset: `math`, `apply`, `ci`, `cn`, `csymbol`, `bvar`,
`lambda`, `piecewise`, `piece`, `otherwise`, `semantics`, `annotation`, `annotation-xml`, `sep`,
`degree` and `logbase`, plus one kind for an operator element and one for a constant element. An
operator element is one of the operators of the subset (`MathOperator`), and a constant element is
one of its constants (`MathConstant`); both sets know their element name, and an operator knows how
many arguments it takes.

SBML also adds four symbols of its own to MathML: `time`, `avogadro`, `rateOf` and `delay`. They are
the `MathSymbol` set, and a formula uses them through a `csymbol` node, which is what
`MathNode::csymbol` builds.
