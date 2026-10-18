# Levels, packages and versions

SBML is not one language but a family of them. A document declares which member of the family it is
written in with two attributes of its root element - the *level* and the *version* - and, when it
uses a package, with one namespace declaration per package.

This chapter says what that means for reading a document: which documents this library resolves a
model for, what it does with the others, and how the packages are modelled.

## The container and the model

The specification's own figure shows the two elements every document has: the document element (the
one that declares the level and the version) and the model it contains.

<!-- diagram: uml-sbml-container.svg -->
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!--
  Redrawn from the SBML Level 3 Version 2 Core specification's `figs/sbml-uml.tex` (the TikZ source
  that `components.tex` inputs): the same two boxes, the same attributes and the same composition
  from `SBML` to `Model`. The specification draws this figure with TikZ rather than shipping an SVG,
  so this file is a redraw, not a copy of a specification file. See `docs-images/README.md`.
-->
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 900 300" width="900pt" height="300pt">
  <defs>
    <marker id="open-triangle" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto">
      <path d="M 1 1 L 11 6 L 1 11 z" fill="#ffffff" stroke="#000000" stroke-width="1.1"/>
    </marker>
    <marker id="diamond" viewBox="0 0 12 12" refX="6" refY="6" markerWidth="13" markerHeight="13" orient="auto">
      <path d="M 6 0 L 12 6 L 6 12 L 0 6 z" fill="#ffffff" stroke="#000000" stroke-width="1.1"/>
    </marker>
  </defs>

  <style>
    .box { fill: #ffffff; stroke: #000000; stroke-width: 1.4; }
    .classname { font-family: "DejaVu Sans", Helvetica, Arial, sans-serif; font-size: 16px; font-style: italic; text-anchor: middle; }
    .attr { font-family: "DejaVu Sans Mono", monospace; font-size: 10px; }
    .label { font-family: "DejaVu Sans", Helvetica, Arial, sans-serif; font-size: 13px; }
  </style>

  <!-- SBase: the root of the object model -->
  <rect class="box" x="340" y="14" width="170" height="42"/>
  <text class="classname" x="425" y="41">SBase</text>

  <!-- the two children of SBase in this figure: the document element itself, and Model -->
  <path d="M 425 56 L 425 76 L 245 76 L 245 98" fill="none" stroke="#000000" stroke-width="1.4" marker-end="url(#open-triangle)"/>
  <path d="M 425 56 L 425 76 L 725 76 L 725 98" fill="none" stroke="#000000" stroke-width="1.4" marker-end="url(#open-triangle)"/>

  <!-- SBML: the document element, with the attributes the specification fixes -->
  <rect class="box" x="10" y="98" width="470" height="152"/>
  <path d="M 10 128 L 480 128" stroke="#000000" stroke-width="1.4"/>
  <text class="classname" x="245" y="121">SBML</text>
  <text class="attr" x="24" y="152">xmlns: string { use = "required" fixed =</text>
  <text class="attr" x="36" y="168">"http://www.sbml.org/sbml/level3/version2/core" }</text>
  <text class="attr" x="24" y="192">level: positiveInteger { use = "required" fixed = "3" }</text>
  <text class="attr" x="24" y="214">version: positiveInteger { use = "required" fixed = "2" }</text>
  <text class="attr" x="24" y="238">{ Additional attributes permitted. }</text>

  <!-- Model -->
  <rect class="box" x="650" y="98" width="150" height="46"/>
  <text class="classname" x="725" y="126">Model</text>

  <!-- the composition from the document element to its model -->
  <path d="M 480 174 L 570 174 L 570 121 L 640 121" fill="none" stroke="#000000" stroke-width="1.4" marker-start="url(#diamond)"/>
  <text class="label" x="492" y="166">model</text>
  <text class="label" x="546" y="152">0..1</text>
</svg>
<!-- /diagram -->

The figure is the specification's, used with the permission of the SBML Editors;
`biodivine-lib-sbml/docs-images/README.md` names where each figure comes from and whether it was
changed.

## The three axes

* **Level** - a major revision. Level 1, Level 2 and Level 3 are different languages: Level 1 has no
  identifiers but names, Level 2 adds identifiers and the `listOf*` containers, Level 3 rewrites
  units, reactions and events. A document declares its level as `level="1"`, `"2"` or `"3"`.
* **Version** - a revision *within* a level. The differences are small and local: an attribute that
  becomes optional, a rule that changes, a type that is added. A document declares it as
  `version="1"`, `"2"`, ...
* **Package** - an extension to the core language, with its own namespace and its own specification:
  FBC (flux balance constraints), Layout (diagrams), Qual (qualitative models), and others. A
  package adds elements to the object model and can add attributes to the objects of the core.

The namespace of the core language encodes the level and the version:
`http://www.sbml.org/sbml/level3/version2/core` is Level 3 Version 2. A package's namespace has the
same shape with its own name in place of `core`, which is what makes a package's content
distinguishable from the core's at a glance - and what the library's validation checks.

## Which documents resolve a model

The examples read three documents, one per case:

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/levels.rs
:language: rust
:start-after: ANCHOR: documents
:end-before: ANCHOR_END: documents
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/levels.py
:language: python
:start-after: ANCHOR: documents
:end-before: ANCHOR_END: documents
:dedent:
```
:::
::::

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/levels.rs
:language: rust
:start-after: ANCHOR: resolve
:end-before: ANCHOR_END: resolve
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/levels.py
:language: python
:start-after: ANCHOR: resolve
:end-before: ANCHOR_END: resolve
:dedent:
```
:::
::::

The exact contract is:

| level | versions | a model resolves? |
| --- | --- | --- |
| Level 3 | 1, 2 | yes, every version the library knows |
| Level 2 | 2, 3, 4, 5 | yes |
| Level 1 | any | **no** - the document is readable, the model is not modelled |
| anything else | any | no |

"Resolves a model" means that `document.model` hands you a `Model` and the typed accessors work as
they do for Level 3 Version 2. The library reads the older levels into the *same* object model: a
Level 2 `compartment` is a `Compartment`, with the accessors of the specification revision it
belongs to, so code written against Level 3 reads a Level 2 model without a special case.

## What happens to a document that does not resolve

Reading such a document *succeeds*, and that is deliberate: the XML tree is there, the container
reports the level and version it declares, the MathML of the document is typed, and an editor can
still work with it. What the library reports is that it did not model the model, as a lint of the
validation report:

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/levels.rs
:language: rust
:start-after: ANCHOR: unmodelled
:end-before: ANCHOR_END: unmodelled
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/levels.py
:language: python
:start-after: ANCHOR: unmodelled
:end-before: ANCHOR_END: unmodelled
:dedent:
```
:::
::::

The lint is called `unmodelled-level`, it is a `LibraryLint` rather than a specification rule, and it
is a `Warning`: the document is not wrong, it is just not a document this library models. A program
that needs a model should therefore treat it as fatal, which is what the exception hierarchy makes
easy - the lint is in the report, and the report is in the exception:

```python
issues = document.validate()
if document.model is None:
    raise ValueError("this document has no model this library can model")
```

## Packages

A package is modelled in the same object model: FBC's flux bounds are typed accessors of
`FbcReaction`, Layout's diagram is a `Layout` child of the model, and Qual's transitions are
`Transition` objects with typed inputs and outputs. Their namespaces are checked by validation like
the core's, and the accessors that create package content introduce the namespace declaration the
package needs.

What a package *adds to the core* is reachable even when the library does not know the package: the
XML layer has dynamic accessors for an attribute or a child by name, so a document of an unknown
package can be read, edited and written. See [Writing an SBML extension](extensions.md) for the
typed version of the same idea, which is what a package you implement yourself wants.
