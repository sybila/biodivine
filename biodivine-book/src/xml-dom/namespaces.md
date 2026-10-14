# Namespaces

Names are *expanded names* in this library, which is the single idea the rest of the API follows.
This chapter shows how a name is resolved while parsing, what is in scope where, how the reserved
`xml` prefix behaves, and why editing never repairs a namespace declaration for you. The validation
side is in [Validating a document](validation.md).

## Names are expanded, prefixes are decoration

Every element and attribute name in the tree is an *expanded* name: a local name plus, optionally, a
namespace that carries both a URI and the prefix it was written with. Two names are the same if
their local names and their *URIs* match; the prefix is presentation. That is what makes
`<p:x xmlns:p="u"/>` and `<q:x xmlns:q="u"/>` the same element — which is exactly what the XML
Namespaces specification means by an expanded name.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/namespaces.rs
:language: rust
:start-after: ANCHOR: parse
:end-before: ANCHOR_END: parse
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/namespaces.py
:language: python
:start-after: ANCHOR: parse
:end-before: ANCHOR_END: parse
:dedent:
```
:::
::::

## Scope

A declaration applies from the start tag that carries it to the end of the corresponding end tag, so
it applies to the element itself and to everything below it. An inner declaration shadows an outer
one, an unprefixed element name takes whatever the default namespace is in scope, and an unprefixed
*attribute* never does.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/namespaces.rs
:language: rust
:start-after: ANCHOR: resolve
:end-before: ANCHOR_END: resolve
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/namespaces.py
:language: python
:start-after: ANCHOR: resolve
:end-before: ANCHOR_END: resolve
:dedent:
```
:::
::::

## Attributes and the `xml` prefix

Attributes are expanded names too, with one twist: an unprefixed attribute is in *no* namespace,
even when a default namespace is in scope. The `xml` prefix, on the other hand, is always bound
to `http://www.w3.org/XML/1998/namespace` without a declaration, so `xml:lang`, `xml:space` and
`xml:id` always resolve.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/namespaces.rs
:language: rust
:start-after: ANCHOR: attributes
:end-before: ANCHOR_END: attributes
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/namespaces.py
:language: python
:start-after: ANCHOR: attributes
:end-before: ANCHOR_END: attributes
:dedent:
```
:::
::::

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/namespaces.rs
:language: rust
:start-after: ANCHOR: xml_prefix
:end-before: ANCHOR_END: xml_prefix
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/namespaces.py
:language: python
:start-after: ANCHOR: xml_prefix
:end-before: ANCHOR_END: xml_prefix
:dedent:
```
:::
::::

## `xmlns=""`

An empty default declaration removes the default namespace from the element it is declared on. The
tree records the declaration explicitly, so it survives a round trip:

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/namespaces.rs
:language: rust
:start-after: ANCHOR: undeclare
:end-before: ANCHOR_END: undeclare
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/namespaces.py
:language: python
:start-after: ANCHOR: undeclare
:end-before: ANCHOR_END: undeclare
:dedent:
```
:::
::::

## No magic

The editing API never touches declarations. Removing a declaration that a subtree relies on
succeeds, moving an element into a scope where its prefix means something else succeeds, and the
serializer writes exactly the declarations that are in the tree — it never invents one to "fix" the
output. The contract is: **edits are silent, `validate` reports**.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/namespaces.rs
:language: rust
:start-after: ANCHOR: silent
:end-before: ANCHOR_END: silent
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/namespaces.py
:language: python
:start-after: ANCHOR: silent
:end-before: ANCHOR_END: silent
:dedent:
```
:::
::::

Next: [Parsing and serializing](parsing-and-serializing.md) for reading and writing documents, and
[Validating a document](validation.md) for what is reported.

