# Building documents

This chapter is about the tree itself: what a document owns, what a handle is, how a node is
attached to (or detached from) its parent, and what the different kinds of "copy" mean. It assumes
you have seen [Getting started](getting-started.md); the editing operations it mentions are covered
in detail in [Traversing and editing](traversing-and-editing.md).

## Documents, nodes and handles

A document owns all of its nodes in a single arena and protects them with a single reader-writer
lock. What you hold in your hand is a **handle**: a document reference plus an index into that
arena.

<!-- diagram: model.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="720" height="300" viewBox="0 0 720 300" role="img" aria-label="A document handle owns a reference to the shared document state; node and element handles are a document handle plus a counted reference to one arena slot.">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#4b5563"/>
    </marker>
  </defs>
  <style>
    .box { fill: #f8fafc; stroke: #475569; stroke-width: 1.2; }
    .inner { fill: #eef2f7; stroke: #94a3b8; stroke-width: 1; }
    .label { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 13px; fill: #0f172a; }
    .small { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 11px; fill: #475569; }
    .title { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 14px; font-weight: 600; fill: #0f172a; }
    .edge { stroke: #4b5563; stroke-width: 1.4; fill: none; marker-end: url(#arrow); }
  </style>
  <text class="title" x="24" y="26">Your program</text>
  <rect class="box" x="24" y="40" width="196" height="88" rx="8"/>
  <text class="label" x="40" y="66">Document</text>
  <text class="small" x="40" y="86">a cheap, shareable handle</text>
  <line x1="40" y1="96" x2="204" y2="96" stroke="#cbd5e1"/>
  <text class="label" x="40" y="116">Node, Element</text>
  <rect class="box" x="24" y="150" width="196" height="60" rx="8"/>
  <text class="label" x="40" y="174">one node reference</text>
  <text class="small" x="40" y="194">counted; dropped when unused</text>
  <rect class="box" x="300" y="40" width="396" height="170" rx="8"/>
  <text class="title" x="320" y="66">Document state</text>
  <text class="small" x="320" y="86">one reader-writer lock per document</text>
  <rect class="inner" x="320" y="98" width="356" height="94" rx="6"/>
  <text class="label" x="336" y="122">arena: one slot per node</text>
  <text class="small" x="336" y="142">payload, parent index, external count</text>
  <text class="small" x="336" y="160">free slots are reused after a collection</text>
  <text class="small" x="336" y="180">the root slot is kept alive by the document</text>
  <path class="edge" d="M 220 84 C 260 84, 262 84, 298 84"/>
  <text class="small" x="228" y="76">owns a reference</text>
  <path class="edge" d="M 220 180 C 260 180, 262 140, 298 130"/>
  <text class="small" x="228" y="200">keeps its slot alive</text>
  <text class="small" x="24" y="248">Internal links between nodes are slot indices: they cost nothing and cannot form a cycle.</text>
  <text class="small" x="24" y="268">Reachable nodes are those reachable from the document root or from a node reference.</text>
  <text class="small" x="24" y="288">Everything else is reclaimed by the collector, and its slot is handed out again.</text>
</svg>
<!-- /diagram -->

* copying a handle is cheap and refers to the *same* node;
* a handle stays valid even if the node is detached;
* handles with the same identity compare equal and can be used as dictionary keys;
* handles can be sent to other threads.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/editing.rs
:language: rust
:start-after: ANCHOR: handles
:end-before: ANCHOR_END: handles
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/editing.py
:language: python
:start-after: ANCHOR: handles
:end-before: ANCHOR_END: handles
:dedent:
```
:::
::::

## Attached and detached

A freshly created node is **detached**: it belongs to a document, but it has no parent yet. You can
edit it, clone it, validate it, and attach it later. Attaching a node that is already attached
*moves* it, and the two things that are never allowed are cycles and cross-document attachments:

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/editing.rs
:language: rust
:start-after: ANCHOR: detached
:end-before: ANCHOR_END: detached
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/editing.py
:language: python
:start-after: ANCHOR: detached
:end-before: ANCHOR_END: detached
:dedent:
```
:::
::::

The fallible operations come in two flavours: `append_child` panics with a clear message, and
`append_child_checked` returns an error you can handle. In Python only the checked behaviour exists,
as an exception — Python has no panics.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/editing.rs
:language: rust
:start-after: ANCHOR: errors
:end-before: ANCHOR_END: errors
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/editing.py
:language: python
:start-after: ANCHOR: errors
:end-before: ANCHOR_END: errors
:dedent:
```
:::
::::

## Copying

There are four different kinds of "copy", and they are spelled differently on purpose:

| what you want | Rust | Python |
| --- | --- | --- |
| another handle to the same node | `clone()` | the object itself / `copy.copy` |
| a detached copy of one node | `shallow_clone()` | `shallow_clone()` |
| a detached copy of a subtree | `deep_clone()` | `deep_clone()` |
| a copy of a subtree in *another* document | `deep_clone_into(&target)` | `deep_clone_into(target)` |

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/editing.rs
:language: rust
:start-after: ANCHOR: clones
:end-before: ANCHOR_END: clones
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/editing.py
:language: python
:start-after: ANCHOR: clones
:end-before: ANCHOR_END: clones
:dedent:
```
:::
::::

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/editing.rs
:language: rust
:start-after: ANCHOR: import
:end-before: ANCHOR_END: import
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/editing.py
:language: python
:start-after: ANCHOR: import
:end-before: ANCHOR_END: import
:dedent:
```
:::
::::

The cross-document copy is the sanctioned way to move a tree between documents: attaching a handle
to a parent in another document is an error, while copying works and rebuilds the subtree with the
target document's own names. It takes a point-in-time snapshot of the source, so a concurrent edit
in the source cannot produce a half-copied tree.

Next: [Traversing and editing](traversing-and-editing.md) shows how to walk and change a tree, and
[Namespaces](namespaces.md) explains what an edit can leave inconsistent.
