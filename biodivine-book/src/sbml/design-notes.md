# Design notes

This chapter is for a reader who wants to know *why* the library is shaped the way it is. It is not
needed to use it.

## Two layers, one object model

The Python package is a thin layer over the Rust library, and the layer in between is mechanical: the
`_sys` crate mirrors the Rust API one item at a time (one Python class per Rust type, one accessor
per accessor, the same arguments and the same result), and the pure-Python layer adds what Python
expects - properties, sequences, exceptions, docstrings. The mechanical layer exists so that the
Python API cannot drift from the Rust one: it is *generated*, and a gate fails when it is out of
date, and another gate fails when the native module exposes something the Python layer does not
wrap.

## Why the accessors are views

The alternative - returning copies - would make an edit a rebuild of the document, and would lose
the parts of a document the library does not understand. A view reads and writes through the element
it came from, so a `notes` blob, an unknown package's content and a formula all survive a
read/edit/write cycle.

## Why validation returns a report

A validator that stops at the first problem is easy to write and useless on a real document. The
walk therefore collects everything it finds, and it reports what it *could not* check: a subtree
whose type check failed is skipped (its typed accessors would read attributes that may not be
there), and one issue stands for that subtree. A report without such an issue is the stronger
statement.

## Why a rule is a function with a name

Every rule is one function, one id (the number of the specification, or a name of the library's own
for a diagnostic no rule covers), one severity and one message. That is what makes the rule set
*data*: it can be listed, looked up, and published - and a package can add to it (see
[Writing an SBML extension](extensions.md)).

## Why the level matters

Level 2 and Level 3 differ in ways that are small locally and large globally (units, reactions,
events), and Level 1 is a different language. The library therefore *reads* every level it knows
into the same object model, and refuses to model one it does not: a model that looks right and is
not is worse than no model at all. See [Known limitations](limitations.md) for the exact contract.
