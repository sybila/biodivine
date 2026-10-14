# Installation

Each Biodivine library is a separate Rust crate, so a Rust project adds exactly the libraries it
uses. In Python, all libraries are submodules of one package, `biodivine`.

## Rust

Add the crate of the library you need, for example the XML DOM:

```sh
cargo add biodivine-lib-xml-dom
```

The crates have no Python code in them and no dependency on a Python interpreter.

## Python

```sh
pip install biodivine
```

This also installs `biodivine-sys`, the native extension that contains the Rust code of every
library. The libraries are then importable as submodules:

```python
import biodivine.xml_dom as xml

document = xml.Document.parse("<root/>")
```

### Building from source

The Python packages are built from the [`biodivine-py`](https://github.com/sybila/biodivine-py)
repository, which needs a Rust toolchain and a Python development environment:

```sh
make venv       # .venv with maturin, pytest and the documentation tools
make develop    # build biodivine-sys, install biodivine (editable)
```

## Running the examples of this book

The book's own repository contains every example as a file under `examples/<library>/`: a Rust
program and a Python script of the same name. From the book's directory:

```sh
cargo run --example xml_dom_getting_started            # one Rust example
cargo test                                             # every Rust example
make python-env                                        # .venv with biodivine
.venv/bin/python examples/xml_dom/getting_started.py   # one Python example
make test                                              # every example
```

`make python-env` builds the Python packages from the `biodivine-py` checkout next to the book, so
the examples run against the same source as the Rust ones.

Next: [How the packages fit together](packages.md).
