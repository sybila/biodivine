# Validating a document

Whole-document validation: what is checked, why editing stays silent about it, and how to act on
the problems it reports. The namespace rules it checks are explained in [Namespaces](namespaces.md),
and what is deliberately *not* checked is in [Known limitations and gotchas](limitations.md).

## Two kinds of integrity

**Local** properties are enforced by the types and checked while you construct: a name that is not a
valid `NCName`, text containing a control character, a comment containing `--`, an attribute value
that is not legal XML — none of them can enter a document. Nothing to remember, nothing to validate.

**Whole-document** properties need a view of the tree, so they are collected by one call that
reports *every* problem it can find, with the node it belongs to and the rule it comes from. That
way a whole class of issues can be fixed in one sweep instead of one failed operation at a time.

## What is checked

| group | examples |
| --- | --- |
| namespace scope | a prefix that is not declared where it is used; a prefix bound to a different URI; an element name in a default namespace that is not declared; an unprefixed element name inside a default-namespace scope (writing it out would move it); an attribute carrying a namespace without a prefix |
| structure | a missing root; and the tree invariants (parent links agreeing, no cycles) as defensive self-checks |
| values | `xml:id` values must be valid names and unique; `xml:lang` must be a language tag or empty; `xml:space` must be `default` or `preserve` |

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/validation.rs
:language: rust
:start-after: ANCHOR: problems
:end-before: ANCHOR_END: problems
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/validation.py
:language: python
:start-after: ANCHOR: problems
:end-before: ANCHOR_END: problems
:dedent:
```
:::
::::

Each issue also knows which rule file in `specification/rules/` it enforces, so the message points
at the part of the XML specification it comes from.

## Fixing what validation reports

Validation is a report, not a repair: the editing API is what changes a document, and it stays
silent while you do it.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/validation.rs
:language: rust
:start-after: ANCHOR: fix
:end-before: ANCHOR_END: fix
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/validation.py
:language: python
:start-after: ANCHOR: fix
:end-before: ANCHOR_END: fix
:dedent:
```
:::
::::

## Why `validate` and not the edits

Making every edit check namespace integrity would mean a whole-document scan per operation, and it
would still not help: moving an element into a strange scope is only a *problem* if the surrounding
document is genuinely inconsistent, which is a property of the whole tree. So the division is
deliberate — see [Namespaces](namespaces.md#no-magic):

* edits never check namespace or structural integrity, so they are fast and predictable;
* `validate` is where you ask, and it tells you everything at once.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/xml_dom/validation.rs
:language: rust
:start-after: ANCHOR: silent
:end-before: ANCHOR_END: silent
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/xml_dom/validation.py
:language: python
:start-after: ANCHOR: silent
:end-before: ANCHOR_END: silent
:dedent:
```
:::
::::

A document that came from `parse` is well-formed and its names resolve, but parsing does not run the
whole-document checks: duplicate `xml:id` values or a malformed `xml:lang` parse fine and are
reported only by validation.

Next: [Thread safety](thread-safety.md) for sharing a document between threads.
