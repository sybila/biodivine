# Parsing and serializing

The two ends of the life of a document: how much a round trip preserves, what the serializer's
options change, and what the parser rejects. If you are building a document instead of reading one,
start with [Building documents](building-documents.md); the rules the library deliberately does not
check are listed in [Known limitations and gotchas](limitations.md).

## A faithful round trip

`parse` and `write` are inverses for anything the data model can represent: prefixes, namespace
declarations, the order of children, escaping and the XML declaration all survive. Output is not
reformatted — text is preserved verbatim, so mixed content is never disturbed.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/parsing.rs
:language: rust
:start-after: ANCHOR: roundtrip
:end-before: ANCHOR_END: roundtrip
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/parsing.py
:language: python
:start-after: ANCHOR: roundtrip
:end-before: ANCHOR_END: roundtrip
:dedent:
```
:::
::::

## Output options

`WriteOptions` chooses whether the `<?xml …?>` declaration is written (`Never`, `IfPresent` — the
default — or `Always`) and whether an element without children is written as `<a/>` or `<a></a>`.
The defaults reproduce the input of a parsed document as closely as the model allows.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/parsing.rs
:language: rust
:start-after: ANCHOR: options
:end-before: ANCHOR_END: options
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/parsing.py
:language: python
:start-after: ANCHOR: options
:end-before: ANCHOR_END: options
:dedent:
```
:::
::::

## What parsing rejects

Everything that is decidable while looking at one element is enforced *while parsing*, with a typed
error rather than a panic — including input that makes many parsers unhappy:

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/parsing.rs
:language: rust
:start-after: ANCHOR: errors
:end-before: ANCHOR_END: errors
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/parsing.py
:language: python
:start-after: ANCHOR: errors
:end-before: ANCHOR_END: errors
:dedent:
```
:::
::::

Note what is *not* an error: a comment or a processing instruction outside the root element is
accepted and discarded (the model has one root and nothing else at the top level). Everything else
above is rejected; the whole-document properties that the parser does not check, such as unique
`xml:id` values, are what [validation](validation.md) is for.

## Entities

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/parsing.rs
:language: rust
:start-after: ANCHOR: entities
:end-before: ANCHOR_END: entities
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/parsing.py
:language: python
:start-after: ANCHOR: entities
:end-before: ANCHOR_END: entities
:dedent:
```
:::
::::

`DOCTYPE` is read and ignored: this library does not process DTDs. The five predefined entities
(`&amp;`, `&lt;`, `&gt;`, `&apos;`, `&quot;`) and character references (`&#65;`, `&#x41;`) are
expanded; any other entity reference is an error, because without a DTD it can never be declared.

Next: [Validating a document](validation.md) for the checks that need the whole tree, and
[Known limitations and gotchas](limitations.md) for what is out of scope.
