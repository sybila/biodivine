# Known limitations and gotchas

Everything here is a deliberate decision that is documented somewhere in the library's
repository; this chapter collects them so the book does not over-promise. Nothing on this page is a
bug report — each entry says where the reasoning lives.

## The data model

**One root element, nothing else at the top level.** A comment or processing instruction outside the
root element is *discarded* when parsing (there is nowhere in the model to keep it), whitespace
outside the root is ignored, non-whitespace text outside the root is an error, and a second root
element is an error. If you need to preserve a leading comment, keep it inside the root.

**Empty text nodes have no representation.** `create_text("")` is accepted, but XML cannot express
an empty text node, so it is omitted when writing and does not come back when parsing. Empty
comments (`<!---->`) and empty CDATA sections (`<![CDATA[]]>`) *can* be expressed and are preserved.

**Comments, CDATA and processing-instruction content are line-end normalised at construction.**
Their content cannot contain an escape sequence, so a literal carriage return there could not
survive a round trip; it is stored as a line feed instead, exactly as a parser would read it. Text
nodes and attribute values are *not* normalised — their bytes are preserved and escaped on output.

**Attribute order is not preserved.** Attributes are stored in a map keyed by expanded name, so they
are written in a deterministic but not necessarily input order. XML attaches no meaning to attribute
order, so this does not change the document's meaning, but the bytes differ.

**No output formatting.** Text is written verbatim, so the serializer never re-indents or wraps a
document, and there is no pretty-printer. Mixed content is therefore never disturbed.

## Standards coverage

**No DTD processing.** `DOCTYPE` declarations are read and ignored: no entities defined by a DTD, no
attribute types, no content models, no validity checking. Consequences worth knowing:

* only the five predefined entities and character references are expanded; any other entity
  reference is a typed error, because it can never be declared;
* `xml:id` is the only attribute whose type this library can know, so "unique IDs" is checked for
  `xml:id` only;
* the two `xml:lang`/`xml:space` "must be declared" rules are validity constraints and are not
  checked — their *value* shapes are (see the `documentation::rule_coverage` page).

**UTF-8 only.** Other encodings are rejected with a typed error rather than silently mis-decoded.
The `documentation::rule_coverage` page lists every rule file and gives the verdict for each rule in
the parser, validation and serializer layers — 54 enforced, 6 partial (the DTD half), 4 deferred
(UTF-16, DTD validity) and 2 not applicable.

## Intended behaviours that surprise people

**Editing does not check namespaces.** Removing a declaration that a subtree relies on succeeds,
moving an element into a scope where its prefix means something else succeeds, and the serializer
never adds a declaration to make the output valid. `validate()` reports all of it; that is the
contract, and the reason edits stay fast and predictable.

**`Document::validate` is the only reporter.** A parsed document is well-formed by construction, but
a document assembled through the API can be inconsistent, and until you validate it nothing will tell
you: the document stays as it is and validation reports it.

**Cancellation is cooperative and only where it pays off.** The document-wide operations (parsing,
serializing, validating, deep copies, and the explicit `collect_garbage`) periodically consult the
`cancel_this` triggers of the current thread, so a long one can be stopped; per-node edits,
shallow copies and `Display` never are. A cancelled operation reports `XmlError::Cancelled` and
leaves the document unchanged: a cancelled copy builds nothing and a cancelled collection reclaims
nothing. The one visible effect is output: a cancelled `write_file` or `write_to` has already
written part of the document. The collector that the allocator triggers on its own is deliberately
*not* cancellable, because an allocation has to either succeed or fail, not stop half-way.

**Arena slots are reused after collection.** A `NodeId` stays valid only while the node it was
created for is alive: the collector reclaims unreachable nodes and hands their slots out again, so
an id held across a collection can resolve to a different node, or to nothing at all. Keep a handle
(`Node`/`Element`) whenever a node has to stay put. The arena itself never shrinks or compacts, and
the name interner only ever grows, so a document that repeatedly builds and discards huge subtrees
should be recycled as a whole.

**Deep nesting is safe but not free.** Parsing, serialization, `Display` and the clone operations are
all iterative, so no depth can crash the process; a very deep document still costs memory
proportional to its depth.

## Python-specific

**The native module is not the documented surface.** `biodivine_sys.xml_dom` is importable, but
the supported API is `biodivine.xml_dom`; a test enumerates exactly what is exported from it.

**`NodeContent` is not mirrored.** Rust's content enum has no Python counterpart: `node.kind` plus the
typed accessors (`text()`, `comment()`, …) carry the same information without a discriminator dance.

**Interrupting only works through signals, on the main thread.** Ctrl+C (or any signal handler that
raises) interrupts a long operation started on the main thread, and the handler's exception is
raised unchanged. There is no cancellation token or `timeout=` argument yet, and an operation
started on another thread runs to completion.

**No `abi3` wheels yet.** The extension is built for the interpreter maturin finds, so a wheel is
specific to one CPython version (see the `documentation::bindings` page).

**Compound edits are not transactional.** Each operation is atomic, but a sequence of them is not;
see [Thread safety](thread-safety.md#what-thread-safe-does-not-mean).

Next: [Design notes](design-notes.md) points to the reasoning behind these decisions.
