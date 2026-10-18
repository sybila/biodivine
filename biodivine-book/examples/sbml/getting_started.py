"""Book chapter "Getting started" - the Python half.

The chapter includes this file verbatim, and `tests/test_examples.py` runs it, so the
book cannot show code that no longer works.
"""

import biodivine.sbml as sbml

# ANCHOR: model
MODEL = """
<sbml xmlns="http://www.sbml.org/sbml/level3/version2/core" level="3" version="2">
  <model>
    <listOfCompartments>
      <compartment id="cell" constant="true" size="1"/>
    </listOfCompartments>
    <listOfSpecies>
      <species id="glucose" compartment="cell" initialConcentration="5"
               hasOnlySubstanceUnits="false" boundaryCondition="false"
               constant="false"/>

    </listOfSpecies>
  </model>
</sbml>
"""
# ANCHOR_END: model

# ANCHOR: read
# Reading parses the XML and checks that it is a document this library understands:
# the container
# element, its level and version, and the well-formedness of the whole tree. A
# document of a
# level/version the library does not model raises an error (see the chapter on levels
# and packages).
document = sbml.reads(MODEL)

# The container reports what it declares.
assert document.level == 3
assert document.version == 2
# ANCHOR_END: read

# ANCHOR: inspect
# The `model` child is optional (the specification allows a document without a model),
# so the
# accessor returns `None` when the document has none.
model = document.model

# A list of children is a sequence: it has a length, indexing and iteration. Note that
# the list
# itself is optional too, so it is created on demand.
species = model.create_species()
assert len(species) == 1

# The accessors read a value with the rules of the specification: an identifier, a
# number, a boolean
# or an enumerated value. A value that is missing or does not convert reads as `None`.
glucose = species[0]
assert glucose.id == "glucose"
assert glucose.compartment == "cell"
assert glucose.initial_concentration == 5.0
# ANCHOR_END: inspect

# ANCHOR: edit
# An accessor is a *property*: assigning to it writes through to the document.
# Assigning `None`
# removes the attribute.
glucose.name = "D-glucose"
glucose.initial_concentration = 4.5
assert glucose.name == "D-glucose"

# A new object is built from the document, then added to a list.
atp = sbml.Species.new_empty(document)
atp.id = "atp"
atp.compartment = "cell"
atp.initial_concentration = 1.0
atp.has_only_substance_units = False
atp.boundary_condition = False
atp.constant = False
atp.name = "ATP"
species.append(atp)
assert len(species) == 2
# ANCHOR_END: edit

# ANCHOR: validate
# Validation walks the document and reports every finding. The result is iterable, has
# a length and
# says whether the document is valid (see the chapter on validation).
issues = document.validate()
for issue in issues:
    print(issue.rule, issue.severity, issue.message)
assert issues.is_valid, issues
# ANCHOR_END: validate

# ANCHOR: write
# Writing serializes the document that is in memory. The text of a `notes`, an
# `annotation` or a
# formula is kept verbatim; only what the specification *interprets* as a value is
# read with its
# whitespace rules.
xml = document.to_string()
assert 'id="glucose"' in xml
assert 'id="atp"' in xml
# ANCHOR_END: write

print(f"{len(species)} species")
