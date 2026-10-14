# Entry points for building and checking the book. Python targets use the virtual environment in
# `.venv`, whose `biodivine` package is built from the `biodivine-py` checkout next to the book.
.PHONY: help python-env test test-rust test-python check book verify

VENV ?= $(CURDIR)/.venv
PYTHON := $(VENV)/bin/python
BIODIVINE_PY := $(CURDIR)/../biodivine-py

# `biodivine-py` depends on the `_sys` crate of every library through git, pinned to a release tag,
# but the book documents the libraries as they are checked out in this workspace. `python-env`
# therefore builds the extension with one Cargo `[patch]` per library, given on the command line,
# which replaces that git dependency with the library's submodule next to the book. A new library
# needs a line here; `python-env` fails if a git dependency on a Biodivine repository is left
# unpatched. See "Python examples and the checked-out libraries" in README.md.
WORKSPACE := $(abspath $(CURDIR)/..)
SYS_PATCHES := \
	--config 'patch."https://github.com/sybila/biodivine-lib-xml-dom".biodivine-lib-xml-dom-py-sys.path="$(WORKSPACE)/biodivine-lib-xml-dom/biodivine-lib-xml-dom-py-sys"'
# Cargo records patched sources in the lock file of `biodivine-py`. The build runs between a backup
# and a restore of that file, so that the `biodivine-py` checkout is left unchanged.
LOCK_BACKUP := $(VENV)/biodivine-py.Cargo.lock

# macOS 27's loader rejects extension modules processed by the system `strip`, which the release
# profile runs by default, so the locally built extension is not stripped.
DEVELOP_ENV := CARGO_PROFILE_RELEASE_STRIP=none VIRTUAL_ENV=$(VENV)

help:
	@echo "make python-env  create .venv with the book toolchain and biodivine built from ../biodivine-py"
	@echo "make test        run every example: Rust (cargo test) and Python (pytest)"
	@echo "make check       check the book sources: structure, anchors, diagrams, formatting"
	@echo "make book        build the book into _build and check the result"
	@echo "make verify      all of the above"

python-env:
	test -x $(PYTHON) || python3 -m venv $(VENV)
	$(PYTHON) -m pip install maturin -r requirements.txt
	cd $(BIODIVINE_PY)/biodivine-py-sys || exit 1; \
	cp ../Cargo.lock $(LOCK_BACKUP); \
	cargo metadata --format-version 1 $(SYS_PATCHES) > /dev/null || exit 1; \
	if grep 'source = "git+https://github.com/sybila/' ../Cargo.lock; then \
		echo "The git dependencies above are not patched; add them to SYS_PATCHES."; status=1; \
	else \
		$(DEVELOP_ENV) $(VENV)/bin/maturin develop --release $(SYS_PATCHES); status=$$?; \
	fi; \
	cp $(LOCK_BACKUP) ../Cargo.lock; rm $(LOCK_BACKUP); exit $$status
	$(PYTHON) -m pip install --no-deps -e $(BIODIVINE_PY)/biodivine

test: test-rust test-python

test-rust:
	cargo test

test-python:
	$(PYTHON) -m pytest tests

check:
	$(PYTHON) scripts/check_book.py
	$(PYTHON) scripts/sync_diagrams.py --check
	cargo fmt --check
	cargo clippy --all-targets -- -D warnings

book:
	rm -rf _build
	$(PYTHON) -m sphinx -W -b html src _build
	$(PYTHON) scripts/check_book.py --built

verify: check test book
