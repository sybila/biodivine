# How the packages fit together

This chapter describes how the Biodivine libraries are packaged for Rust and Python. You do not need
it to use a library; it is for readers who want to know what is installed, why there is a package
called `biodivine-sys`, or how to write bindings for a new library.

## The four layers

Every library reaches Python through four layers. For the XML DOM library:

| layer | name | published as | what it contains |
| --- | --- | --- | --- |
| Rust library | `biodivine-lib-xml-dom` | a crate on crates.io | the implementation and its Rust API; no Python code |
| `_sys` crate | `biodivine-lib-xml-dom-py-sys` | not published | one thin PyO3 wrapper per public Rust item, with no behaviour of its own |
| native extension | `biodivine-sys` (imported as `biodivine_sys`) | a Python package on PyPI | the `_sys` crates of *all* libraries, linked into one module with a submodule per library (`biodivine_sys.xml_dom`) |
| Python package | `biodivine` | a Python package on PyPI | one idiomatic submodule per library (`biodivine.xml_dom`, `biodivine.sbml`), wrapping the native submodule |

The first two layers live in the library's repository and change together: the `_sys` crate mirrors
the Rust API item by item, so a change to the API and its wrapper is one change. The last two live
in the `biodivine-py` repository, which depends on each `_sys` crate through git, pinned to a commit
or a release tag of the library.

Rust users only ever see the first layer. Python users only ever see the last one: its classes
accept Python values in convenient forms, follow Python protocols, and never return an object of the
native extension.

## Why one native extension

A Rust type wrapped by PyO3 becomes a Python class when the extension module that contains it is
loaded. If every library shipped its own extension, a type used by two libraries would become two
unrelated Python classes. Consider a library for a model format that is stored as XML: its bindings
would want to accept and return XML documents, but a `Document` created by the XML extension would
not be an instance of the `Document` class known to the model extension, and passing one to the
other would fail.

Linking every `_sys` crate into one extension avoids this: each Rust type has exactly one Python
class, so the bindings of one library can use the types of another directly, and Python code can
pass objects between libraries freely.

The trade-off is that the native extension is released as one unit. A change to the bindings of
any library means a new release of `biodivine-sys`, and the `biodivine` package pins the exact
version of `biodivine-sys` it was written against, so the two are always released together.

## Names

The name of a library's Python submodule is the crate name without the `biodivine-lib-` prefix, in
`snake_case`: `biodivine-lib-xml-dom` is `biodivine.xml_dom` (and `biodivine_sys.xml_dom` in the
native extension). The same name is used for the library's directory of examples in this book.

## Versions

Each crate has its own version. `biodivine` and `biodivine-sys` share a version of their own, which
is independent of the crates they contain; the version of the crate behind a submodule is available
as that submodule's `__version__`:

```python
import biodivine
import biodivine.xml_dom

print(biodivine.__version__)           # the version of the Python packages
print(biodivine.xml_dom.__version__)   # the version of biodivine-lib-xml-dom
```

Next: the libraries themselves, starting with [XML DOM](xml-dom/index.md).
