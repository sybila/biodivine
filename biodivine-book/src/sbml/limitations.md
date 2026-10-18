# Known limitations

This chapter states what the library does *not* do, in one place, so that you do not have to
discover it from an exception. Everything here is a decision rather than an accident, and most of
them come from the specification itself.

## Which documents resolve a model

The exact contract, repeated here because it is the thing a newcomer needs first:

| level | versions | a model resolves? |
| --- | --- | --- |
| Level 3 | 1, 2 | **yes** |
| Level 2 | 1, 2, 3, 4, 5 | **yes** |
| Level 1 | any | **no** - readable, but the model is not modelled |
| anything else | any | no |

Level 2 Version 1 is worth one sentence of its own, because it is the version a reader is most
likely to get wrong by hand: its namespace is `http://www.sbml.org/sbml/level2`, with *no* version
in it (the versioned namespace starts at Level 2 Version 2), and its objects are named rather than
identified - a compartment of that version has a `name`, and reading its `id` finds nothing.

A document of a level the library does not model is *readable*: the XML tree is there, the container
reports its level and version, its MathML is typed, and it can be edited and written back. What is
missing is the model: `document.model` is `None`, and validation says so with the `unmodelled-level`
lint, which is a `LibraryLint` of severity `INFO` - a diagnostic of this library rather than a rule
of the specification, and not an error, because a document this library cannot model is not a
*broken* document. A program that needs a model must therefore check for one:

```python
document = sbml.reads(source)
if document.model is None:
    raise ValueError(f"not modelled: {document.level}.{document.version}")
```

The lint is the signal, and `document.validate()` reports it with the reason. Level 1 in particular
is a different language rather than an older spelling of this one: its compartments have names
instead of identifiers and volumes instead of sizes, and its reactions are numbered rather than
named. Reading such a document into the Level 3 object model would produce a model that *looks*
right and is not, which is why the library declines instead.

## The subset of MathML

SBML permits a subset of MathML, and the library models that subset (see
[MathML formulas](mathml.md)). A formula element outside the subset is not lost - it stays in the
document, and it is reachable through the XML element of the node it belongs to - but it has no
typed node, and the validation layer reports it.

## Validation is a walk, not a proof

The validator implements the rules of the specification that the library implements, and it says
which ones it checked: the report names the rule of every finding, and a rule that never fires
leaves no trace. A document that validates is a document for which the implemented rules found
nothing, which is not the same as a document that is correct - see the crate's `VALIDATION.md` for
the list, and the `unmodelled-level` lint above for the case where a whole model was skipped.

## A rule set cannot be implemented in Python

The rule machinery is public in Rust and reachable from Python as *data* (`RuleSet`,
`RuleDescriptor`, `RuleKind`, the severities), but a rule set implemented in Python cannot be
injected into a validation pass: a rule set is a slice of Rust objects, and calling back into Python
in the middle of the walk would put the interpreter inside the document lock. Writing a package is
a Rust exercise (see [Writing an SBML extension](extensions.md)).

## Notes, annotations and foreign content are opaque

`notes` is XHTML and `annotation` is arbitrary XML, and the library keeps both as XML: it does not
interpret them, does not validate them beyond what the specification says about their presence, and
does not rewrite them. The same is true of the content of a package the library does not know: it is
reachable through the dynamic accessors and the XML layer, and it survives a read/edit/write cycle.

## Thread safety

A document is a handle to a shared tree, and the tree is thread-safe: two threads can read the same
document at once, and an edit is a mutation of the tree that other threads see. The typed accessors
are cheap handles, so a value read on one thread stays valid on another. Interrupting a long
operation (a parse, a validation, a serialization) is what the `cancel-this` crate is for, and the
Python bindings do it for you: a `KeyboardInterrupt` during a long call stops the work and raises.
