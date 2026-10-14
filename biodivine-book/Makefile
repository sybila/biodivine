# Entry points for building and checking the book. Python targets use the virtual environment in
# `.venv`, whose `biodivine` package is built from the `biodivine-py` checkout next to the book.
.PHONY: help python-env test test-rust test-python check book verify

VENV ?= $(CURDIR)/.venv
PYTHON := $(VENV)/bin/python
BIODIVINE_PY := $(CURDIR)/../biodivine-py

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
	cd $(BIODIVINE_PY)/biodivine-py-sys && $(DEVELOP_ENV) $(VENV)/bin/maturin develop --release
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
