## Context

- The book documents every Biodivine library, in Rust and Python. `README.md` describes the layout and the conventions a
  chapter follows; read it before editing.
- The examples run against the checked-out submodules (`../biodivine-lib-*` for Rust, `../biodivine-py` for Python).
  `make python-env` patches the git dependencies of `biodivine-py` onto the library submodules (`SYS_PATCHES` in the
  `Makefile`, explained in `README.md`); a new library needs an entry there.
  When a library's API changes, update its examples and chapters here in the same piece of work.

## Instructions

- `make verify` runs every check (it needs `make python-env` first, and again after a library or its bindings
  changed). Run it after every change to a chapter or an example.
- Never show code in a chapter that is not included from an example file, except for short illustrative fragments.
