# Validating a document

Validation is *explicit* in this library. Every check the library performs is one function with a
rule id (the number of the rule in the specification, or a name of the library's own for a
diagnostic that no rule covers), a severity, and a message that says what is wrong and where. A
validation pass returns all of it as a report; it does not throw the first problem away.

## The report

The document the examples validate is the same model twice:

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/validation.rs
:language: rust
:start-after: ANCHOR: broken
:end-before: ANCHOR_END: broken
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/validation.py
:language: python
:start-after: ANCHOR: broken
:end-before: ANCHOR_END: broken
:dedent:
```
:::
::::

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/validation.rs
:language: rust
:start-after: ANCHOR: report
:end-before: ANCHOR_END: report
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/validation.py
:language: python
:start-after: ANCHOR: report
:end-before: ANCHOR_END: report
:dedent:
```
:::
::::

The document in the example is the same model twice: two species that share an identifier, which
rule 10301 forbids. The message names the object and the model it belongs to, because a report that
says *what* is wrong without saying *where* is not much use on a document with a thousand species.

## Severities

A finding is an `Error`, a `Warning` or a `Note` - which the API calls `INFO` and the Rust API calls
`SbmlIssueSeverity::Info`. Only an `Error` means the document violates the specification; the other
two are things a reader should know about, and a document with them is still a valid document. The *kind* of a rule is a separate axis: a `SpecRule` is a rule of the
specification, and a `LibraryLint` is a diagnostic this library adds (an unused namespace
declaration, a model that was not modelled).

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/validation.rs
:language: rust
:start-after: ANCHOR: severities
:end-before: ANCHOR_END: severities
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/validation.py
:language: python
:start-after: ANCHOR: severities
:end-before: ANCHOR_END: severities
:dedent:
```
:::
::::

## What was *not* checked

The walk is a *typed* walk: it visits the objects of the document as the objects they claim to be.
When the type check of a subtree fails - an element that claims to be a `species` but is missing the
attributes that make one, for instance - the walk skips that subtree, because the typed accessors
inside it would read attributes that may not be there. It reports one issue for the subtree instead.

That is why every report is worth reading to the end: a report *without* such an issue is the
stronger statement, because it means every object of the document was actually walked.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/validation.rs
:language: rust
:start-after: ANCHOR: not-validated
:end-before: ANCHOR_END: not-validated
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/validation.py
:language: python
:start-after: ANCHOR: not-validated
:end-before: ANCHOR_END: not-validated
:dedent:
```
:::
::::

## Fixing what it reports

Validation reads the document as it is, so fixing a violation is an edit like any other, and the
next pass sees the fix.

::::{tab-set}
:::{tab-item} Rust
:sync: rust
```{literalinclude} ../../examples/sbml/validation.rs
:language: rust
:start-after: ANCHOR: fix
:end-before: ANCHOR_END: fix
:dedent:
```
:::
:::{tab-item} Python
:sync: python
```{literalinclude} ../../examples/sbml/validation.py
:language: python
:start-after: ANCHOR: fix
:end-before: ANCHOR_END: fix
:dedent:
```
:::
::::

## Strict validation

A program that cannot do anything useful with a broken document usually wants an exception rather
than a report. In Python that is one call: `document.validate_strict()` raises `SbmlValidationError`
when the report contains an error, and the exception carries the issues (`error.issues`) so the
report is not lost. In Rust the report is the only form, and the caller decides:

```rust
let issues = document.validate()?;
if !issues.is_valid() {
    return Err(issues);
}
```

## The rules themselves

The set of rules the library implements is public data: a rule set holds one descriptor per rule,
with the id, the kind, the severity and a one-line summary, and it can be looked up by id. In Python
that is `sbml.RuleSet.CORE`, which is useful for two things: reporting *which* rules a run checked,
and building a rule set of your own when you write a package (see
[Writing an SBML extension](extensions.md)).
