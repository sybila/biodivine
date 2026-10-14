# Using the Python package

This chapter covers what the Python module `biodivine.xml_dom` adds to the Rust API, which Pythonic protocols it
supports, how errors and validation surface, and what identity and equality mean for handles. The
Rust API is described in the rest of this book and in its rustdoc; the item-by-item mapping between
the two is the `documentation::bindings` page of that rustdoc.

## Three layers, one behaviour

`biodivine.xml_dom` is a thin Pythonic layer over the native `biodivine_sys.xml_dom` module,
which mirrors the Rust API. There is no XML logic in Python, so the behaviour is the
Rust behaviour:

* names are accepted as a `str` (no namespace), a `(local_name, namespace_or_uri)` tuple, or a
  `QualifiedName`;
* a `Namespace` may be given anywhere a namespace is expected, or a URI string;
* any `PathLike` is accepted for file paths;
* parsing and writing are `Document` methods, as in Rust: `Document.parse` (a `str` or bytes),
  `Document.parse_file`, `document.write()` and `document.write_file(path)`;
* values that Rust reads with a method are properties (`document.root`, `node.parent`,
  `element.attributes`, ...), and the enums are `enum.Enum` classes;
* a failure raises one of the `XmlError` subclasses rather than returning an error value, because
  Python has no `Result` type.

<!-- diagram: layers.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="720" height="220" viewBox="0 0 720 220" role="img" aria-label="Three layers: the Rust library, its native PyO3 mirror in the biodivine_sys extension, and the biodivine.xml_dom Python module that wraps it.">
  <style>
    .box { fill: #f8fafc; stroke: #475569; stroke-width: 1.2; }
    .label { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 13px; fill: #0f172a; }
    .small { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 11px; fill: #475569; }
    .title { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 14px; font-weight: 600; fill: #0f172a; }
    .edge { stroke: #4b5563; stroke-width: 1.4; fill: none; }
  </style>
  <text class="title" x="24" y="26">Your program</text>
  <rect class="box" x="24" y="40" width="320" height="70" rx="8"/>
  <text class="label" x="40" y="66">biodivine.xml_dom</text>
  <text class="small" x="40" y="86">the Python module: coercion, protocols, conveniences</text>
  <rect class="box" x="24" y="130" width="320" height="70" rx="8"/>
  <text class="label" x="40" y="156">biodivine_sys.xml_dom</text>
  <text class="small" x="40" y="176">the native extension: a one-to-one mirror of the Rust API</text>
  <rect class="box" x="380" y="85" width="316" height="70" rx="8"/>
  <text class="label" x="396" y="111">biodivine-lib-xml-dom</text>
  <text class="small" x="396" y="131">the Rust library: the implementation, with no Python in it</text>
  <path class="edge" d="M 184 110 L 184 130"/>
  <path class="edge" d="M 184 165 L 184 180"/>
  <path class="edge" d="M 344 165 L 378 140"/>
  <path class="edge" d="M 344 75 L 378 105"/>
  <text class="small" x="24" y="216">Only the top box is the documented API; the two below it are implementation layers.</text>
</svg>
<!-- /diagram -->

## What is Pythonic rather than mirrored

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/pythonic.rs
:language: rust
:start-after: ANCHOR: mapping
:end-before: ANCHOR_END: mapping
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/pythonic.py
:language: python
:start-after: ANCHOR: mapping
:end-before: ANCHOR_END: mapping
:dedent:
```
:::
::::

The extras are conveniences, not a second API: `node.attributes` is a `dict` instead of a list of
pairs, `Element.get(name, default=None)` reads an attribute with the same name spellings as
`Element.attribute`, `validation_errors()` returns a `list` so `if document.validation_errors():`
works, and `Document.create_element_tree(name, *children)` builds a parent and its children in one
call.

## Indexing and iteration

Python has protocols Rust does not: `len(node)`, `node[i]` and `for child in node`.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/pythonic.rs
:language: rust
:start-after: ANCHOR: indexing
:end-before: ANCHOR_END: indexing
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/pythonic.py
:language: python
:start-after: ANCHOR: indexing
:end-before: ANCHOR_END: indexing
:dedent:
```
:::
::::

## Handles

A handle refers to one node in both languages: it can be used as a dictionary key, and it knows its
document, its parent and its id.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/pythonic.rs
:language: rust
:start-after: ANCHOR: handles
:end-before: ANCHOR_END: handles
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/pythonic.py
:language: python
:start-after: ANCHOR: handles
:end-before: ANCHOR_END: handles
:dedent:
```
:::
::::

## Validation

Validation is a whole-document call in both languages; in Python it raises by default and has a
non-raising form for collecting the list.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/pythonic.rs
:language: rust
:start-after: ANCHOR: validation
:end-before: ANCHOR_END: validation
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/pythonic.py
:language: python
:start-after: ANCHOR: validation
:end-before: ANCHOR_END: validation
:dedent:
```
:::
::::

## Errors

```python
try:
    document.validate()
except xml.XmlValidationError as error:
    for problem in error.errors:
        print(problem.kind, problem.node, problem.message, problem.rule)
```

The exceptions of this library derive from `XmlError`; the subclasses are `XmlSyntaxError` (the
input is not well-formed), `XmlNamespaceError`, `XmlDocumentError` (an operation on the tree itself:
foreign document, cycle, bad index), `XmlIoError` and `XmlValidationError`.

A long operation (parsing, writing, validating, a deep copy or a garbage collection) started on the
main thread can be interrupted by Ctrl+C or by any other Python signal handler that raises. The
handler's exception (`KeyboardInterrupt` for Ctrl+C) is raised as soon as the operation has stopped,
and the document is left as it was.

## Identity and equality

`==` on two handles compares the *node* they refer to (document identity plus arena index), and
`hash` follows, so handles work as dictionary keys. `is` compares Python objects, which are created
on demand, so two handles to the same node are `==` but usually not `is`. `a.ptr_eq(b)` is the
explicit spelling of `a == b`.

## A note on types

The `biodivine` package ships a `py.typed` marker and full annotations, so type checkers see
`Document`, `Element`, `Node`, `Namespace`, `QualifiedName`, `ValidationErrors`, the option types and
the exception hierarchy. The native `biodivine_sys.xml_dom` module is importable but is not the
documented surface — a test of the `biodivine` package enumerates its public names and checks that
no native object ever leaks out of it.

Next: [Known limitations and gotchas](limitations.md) collects what the library deliberately does
not do.
