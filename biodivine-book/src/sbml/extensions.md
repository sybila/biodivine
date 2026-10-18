# Writing an SBML extension

A package is an extension of the core language: it adds elements and attributes of its own, it may
add rules, and it has its own specification and namespace. This chapter shows how to implement one
with this library, using the worked example that ships with the crate:
`biodivine-lib-sbml/examples/extension-example.rs`. The regions below are that file verbatim, and
`cargo test` runs the whole of it - so a package written this way is checked, not just described.

## The namespace comes first

A package's namespace is its identity: the prefix it writes its names with and the URL that
identifies it. The URL has the shape of a standard package's namespace
(`.../level3/version2/<package>/version1`), and that is not cosmetic: the core type check reports
the content of a namespace that is neither one of the standard nor a foreign one, so a package that
adds content to a document has to declare a namespace of this shape.

```{literalinclude} ../../../biodivine-lib-sbml/examples/extension-example.rs
:language: rust
:start-after: /// to an SBML document has to declare a namespace of this shape.
:end-before: // ---------------------------------------------------------------------------------------------
:dedent:
```

## The elements of the package

A package's element is a wrapper exactly like a wrapper of the core: `#[derive(XmlWrapper)]` with an
`#[sbml_object(..)]` attribute that names the element and the namespace. The derive writes the
identity (the element name, the namespace, the `xsi:type` of a discriminated type) and the
`new_empty(document)` constructor, so the element a value is built from and the element the type
recognizes are the same by construction.

```{literalinclude} ../../../biodivine-lib-sbml/examples/extension-example.rs
:language: rust
:start-after: /// package too, for a package element), which is what tells the accessor that the attribute may
:end-before: pub fn value(&self) -> OptionalSbmlProperty<'_
:dedent:
```

An accessor is one line, because the namespace of the package is the namespace the attribute lives
in: the four arguments of the accessor say where the attribute lives and in which namespace the
element it is read from lives, so an accessor of a package element is one call.

## The view of a core object

A package usually *adds* something to an object of the core: an attribute of `<model>`, a child
list, a flag on a reaction. That is a *view*: a thin wrapper that holds the core object and reaches
the package's data through the XML layer. `ExtensionOf` names the package and converts in both
directions, and the cast of `ExtensionCast` is what a caller uses to get a view *checked* - a view
cannot be read out of a document that does not declare the package.

```{literalinclude} ../../../biodivine-lib-sbml/examples/extension-example.rs
:language: rust
:start-after: /// view *checked*: a view cannot be read out of a document that does not declare the package.
:end-before: The `myext:strictness` attribute the package adds to
:dedent:
```

The view's own accessors are then one line each, because the helper of `ExtensionOf` fills the
package's namespace in:

```{literalinclude} ../../../biodivine-lib-sbml/examples/extension-example.rs
:language: rust
:start-after: /// The helper of [`ExtensionOf`] fills the package namespace in, so the accessor is one line.
:end-before: // ---------------------------------------------------------------------------------------------
:dedent:
```

## The rules of the package

A package that adds constraints to a document adds *rules*, and the library's rule machinery is
public for exactly this reason: a rule is a descriptor (an id, a kind, a severity and a summary) and
a check. A specification rule's id is its number in the package's specification; a diagnostic the
package invents for itself is a `LibraryLint` with a name of its own.

Two things about the rules are worth pointing out, because they are the parts a package gets wrong:

* **A rule must be cancellable.** Validation is interruptible (see the
  [Design notes](design-notes.md)), so a check that walks a list ticks the cancellation check between
  steps. That is what the `check` argument of the check function is for.
* **A rule reports *where*.** An issue carries the element it was found on, so a report can be
  navigated back into the document.

## Using the package

A package's data is reached by a *cast* from the core object, which is what makes the two halves of
the design meet: the core library does not know the package, and the package does not own the
document. The cast checks that the document declares the package (and that the element is what it
claims to be) and reports why not otherwise - `ExtensionError::NotDeclared`, or a mismatch of the
element type.

The full example also shows the other direction: a package that adds content to a document it is
asked to edit has to *activate* itself, which is what `document.activate_package(prefix, url)` does.
That call declares the package's namespace and records the package as required, which is what makes
the document valid *after* the edit.

## What a package cannot do from Python

The Python package exposes the *data* of the rule machinery (`RuleSet`, `RuleDescriptor`, `RuleKind`
and the severities) but not the injection of a rule set implemented in Python: a rule set is a slice
of Rust objects, and building one from Python callbacks would put Python code in the middle of the
validation walk. Writing a package is therefore a Rust exercise, and the extension chapter of the
book is the one chapter without a Python half. A document that *uses* such a package is of course
readable, editable and validatable from Python like any other.
