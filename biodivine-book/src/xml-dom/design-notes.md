# Design notes

This chapter is a pointer rather than a tutorial: the design decisions, the alternatives that were
rejected and the reasoning live in the crate documentation, in the `documentation` module, next to
the API it describes:

| page | what is in it |
| --- | --- |
| `documentation::architecture` | the model and its trade-offs, the concurrency and cancellation arguments, the error model, the namespace contract, module layout and the testing strategy |
| `documentation::bindings` | the item-by-item mapping of the Python bindings: what is mirrored, what is deliberately not and why, the error mapping, the GIL policy and how signals interrupt long operations |
| `documentation::rule_coverage` | every XML rule, the layer that acts on it, and what is deliberately out of scope |
| `xml_spec::rule_set` | one module per XML rule, documented with the rule summary itself |

Run `cargo doc --open` in the `biodivine-lib-xml-dom` repository and follow those links; the same
pages are the design documents in its `docs/design/` directory, next to `build.md`, which explains
how to set the project up and run the checks.

Two decisions are worth summarising here because they shape everything a user sees:

**One lock per document, and an arena of nodes.** Nodes live in a vector and refer to each other by
index; a handle is a document reference, an index and a counted reference that keeps the node alive.
That makes an edit a single critical section (so a cycle cannot be raced into existence), removes
reference cycles from the design entirely, and makes reads cheap. The cost is that a node's slot is
held until a collection reclaims it — a documented trade-off, not an oversight.

**"Parse, don't validate" at the boundaries, one validation pass for the whole document.** Names,
text and namespace URIs cannot be constructed invalid, so the type system carries the local
guarantees; the whole-document properties (namespace scope, unique ids, the value shapes of
`xml:lang` and `xml:space`) are collected by `validate` in one pass, reporting every problem at once. Edits stay silent so they stay
fast and predictable.

The XML-specification logic itself lives in the `xml_spec` module, one function per rule, annotated
with the rule it implements: the annotation names the rule summary, the documentation links it, and
the tests assert the summary exists.
