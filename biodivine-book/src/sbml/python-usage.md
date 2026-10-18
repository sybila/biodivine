# Using the Python package

This chapter is the Python entry point: what to install, what the module looks like, and where the
Python API differs from the Rust one on purpose. The other chapters show the two side by side.

## Install

```sh
pip install biodivine
```

The package ships the compiled extension, so nothing else is needed. To build it from source, see
[Installation](../installation.md); the module is the `sbml` part of the `biodivine` package, and
the native extension it sits on is `biodivine_sys.sbml` (you never need to import the latter).

## The shape of the module

```python
import biodivine.sbml as sbml

document = sbml.read("model.sbml")     # or sbml.reads(text)
model = document.model
for species in model.species:
    print(species.id, species.compartment)
issues = document.validate()
if not issues.is_valid:
    raise ValueError(issues.errors)
document.write("fixed.sbml")
```

The names are the names of the specification: `Model`, `Species`, `Compartment`, `Reaction`,
`KineticLaw`, `FunctionDefinition`, `InitialAssignment`, `Rule` (and its three kinds), `Event`,
`Parameter`, `UnitDefinition`, and so on. Every type of the object model has a class here, so
`isinstance(species, sbml.Species)` is true for a species of any level the library models.

## What is Pythonic on purpose

The Rust API is a mirror of the specification, and the Python API is a mirror of *Python*: the
differences are deliberate, and they are the reason the two layers are separate.

| Rust | Python | why |
| --- | --- | --- |
| `species.id().set_some(&x)` | `species.id = x` | a property, not a setter method |
| `species.id().get()` | `species.id` | a value or `None` |
| `model.species().get_or_create()` | `model.create_species()` | a name that says it writes |
| `XmlList<Species>` | a sequence of `Species` | `len`, indexing, iteration, `append`, `pop` |
| `document.validate()?` returning issues | `document.validate()` returning a report | iteration and `len`; `validate_strict()` raises |
| `SbmlError::Xml(..)` | `SbmlXmlError` | an exception that can be caught |
| `species.id` (an `SId`) | `species.id` (a `str`) | the type is a Rust safety net, not a Python one |
| `MathNodeKind::Operator(MathOperator::Times)` | `sbml.MathOperator.TIMES` | a closed set, named |
| `document.to_xml_string()` | `document.to_string()` | the usual spelling |

The validation report is worth one more sentence: it is iterable, it has a length, it groups its
findings (`errors`, `warnings`) and it says whether the document is valid (`is_valid`). `bool()`
follows the container convention: a report is true when it is *not empty*.

## Errors

Every failure is an exception that derives from `SbmlError`: `SbmlXmlError` (not well-formed XML),
`SbmlDocumentError` (no root element), `SbmlUnsupportedLevelError` (a level the library cannot
read), `SbmlCancelledError` (the operation was interrupted), `SbmlIoError` (the file could not be
read or written), and `SbmlValidationError` (a strict validation that found an error, carrying the
`issues`).

## Interruption

A long operation (parsing a large document, validating it, serializing it) can be interrupted with
`Ctrl-C`: the bindings release the interpreter lock while the Rust code runs, and a signal stops the
work and raises. That is what the `cancel-this` crate does for the Rust side, and the Python
bindings wire it up for you.
