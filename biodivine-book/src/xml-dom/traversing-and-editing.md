# Traversing and editing

Walking a tree and changing it: parents, children, siblings and descendants; inserting, moving,
replacing and removing nodes; and the non-element node kinds. This is the chapter to read after
[Building documents](building-documents.md); [Namespaces](namespaces.md) explains why moving a node
can leave a document inconsistent, and [Validating a document](validation.md) is how you find out.

## Walking the tree

Parents, children, siblings and descendants are all available; the descendants traversal is
iterative, so a deeply nested document cannot overflow the stack. Python additionally offers
`len(node)`, `node[i]` and `for child in node`.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/editing.rs
:language: rust
:start-after: ANCHOR: traversal
:end-before: ANCHOR_END: traversal
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/editing.py
:language: python
:start-after: ANCHOR: traversal
:end-before: ANCHOR_END: traversal
:dedent:
```
:::
::::

## Changing the tree

Inserting, moving, replacing and removing are all one critical section on the document lock, which
is what makes them atomic: another thread can never observe a half-finished edit, and the
cycle check cannot be raced against.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/editing.rs
:language: rust
:start-after: ANCHOR: editing
:end-before: ANCHOR_END: editing
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/editing.py
:language: python
:start-after: ANCHOR: editing
:end-before: ANCHOR_END: editing
:dedent:
```
:::
::::

| operation | Rust | Python |
| --- | --- | --- |
| append | `append_child` / `append_child_checked` | `append_child` (raises) |
| insert at a position | `insert_child` / `insert_child_checked` | `insert_child` |
| insert next to a sibling | `insert_before`, `insert_after` | same |
| remove from the parent | `detach` (returns the old parent) | `detach` |
| remove and keep the node | `remove` | `remove` |
| swap a node out | `replace_with` | `replace_with` |

Replacing a node leaves the old one in the document, detached but fully usable — which is how
you undo a replacement or move the old node somewhere else.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/editing.rs
:language: rust
:start-after: ANCHOR: replace
:end-before: ANCHOR_END: replace
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/editing.py
:language: python
:start-after: ANCHOR: replace
:end-before: ANCHOR_END: replace
:dedent:
```
:::
::::

## Text, comments, CDATA and processing instructions

Non-element nodes are children like any other; they are created by the document and appended. Their
content is validated on creation, and their kind is discoverable from a handle:

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/parsing.rs
:language: rust
:start-after: ANCHOR: other_nodes
:end-before: ANCHOR_END: other_nodes
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/parsing.py
:language: python
:start-after: ANCHOR: other_nodes
:end-before: ANCHOR_END: other_nodes
:dedent:
```
:::
::::

An element's children keep their order, and mixed content (text, elements, comments, CDATA and
processing instructions interleaved) round-trips exactly. The serialized output is escaped so that
a literal carriage return and a `]]>` in text, and whitespace inside attribute values, survive a
re-parse.

Next: [Namespaces](namespaces.md) explains how names carry their namespace, and what editing does
(and does not do) to the declarations.
