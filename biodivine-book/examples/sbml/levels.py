"""Book chapter "Levels, packages and versions" - the Python half.

The chapter includes this file verbatim, and `tests/test_examples.py` runs it.
"""

import biodivine.sbml as sbml

# ANCHOR: documents
# A Level 3 Version 1 document: the previous revision of the same level.
L3V1 = """
<sbml xmlns="http://www.sbml.org/sbml/level3/version1/core" level="3" version="1">
  <model>
    <listOfCompartments>
      <compartment id="cell" constant="true" size="1"/>
    </listOfCompartments>
  </model>
</sbml>
"""

# A Level 2 Version 4 document: an older *level*.
L2V4 = """
<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2" version="4">
  <model>
    <listOfCompartments>
      <compartment id="cell" size="1"/>
    </listOfCompartments>
  </model>
</sbml>
"""

# A Level 2 Version 1 document: the first version of Level 2, whose namespace has no
# version in it (`.../level2`), which is the one thing that makes this pair special.
L2V1 = """
<sbml xmlns="http://www.sbml.org/sbml/level2" level="2" version="1">
  <model>
    <listOfCompartments>
      <compartment name="cell" size="1"/>
    </listOfCompartments>
  </model>
</sbml>
"""

# A Level 3 Version 2 document: the version the base tables are written for.
L3V2 = """
<sbml xmlns="http://www.sbml.org/sbml/level3/version2/core" level="3" version="2">
  <model>
    <listOfCompartments>
      <compartment id="cell" constant="true" size="1"/>
    </listOfCompartments>
  </model>
</sbml>
"""

# A Level 1 document: a level this library does not model.
L1V2 = """
<sbml xmlns="http://www.sbml.org/sbml/level1" level="1" version="2">
  <model>
    <listOfCompartments>
      <compartment name="cell" volume="1"/>
    </listOfCompartments>
  </model>
</sbml>
"""
# ANCHOR_END: documents

# ANCHOR: resolve
# The library models Level 3 (every version) and Level 2 (every version, including the
# first one): reading such a document gives a model, and the accessors behave as they do
# for Level 3 Version 2.
for name, source in [
    ("l3v1", L3V1),
    ("l3v2", L3V2),
    ("l2v1", L2V1),
    ("l2v4", L2V4),
]:
    document = sbml.reads(source)
    model = document.model
    assert model is not None, f"{name} resolves a model"
    compartments = model.compartments
    assert len(compartments) == 1
    # Level 2 Version 1 has no identifiers: its compartments have *names*, so the
    # label of a
    # compartment is whichever of the two the document uses.
    compartment = compartments[0]
    assert (compartment.id or compartment.name) == "cell"
# ANCHOR_END: resolve

# ANCHOR: unmodelled
# A document of a level/version this library does not model is still *readable*: the
# XML tree is
# there, the container reports what it declares, and validation says that the model
# was not
# modelled. Reading it as a model is what an older-level document is *for*, so the
# library reports
# the situation as a lint rather than failing the read.
document = sbml.reads(L1V2)
assert document.level == 1
issues = document.validate()
unmodelled = [issue for issue in issues if issue.rule == "unmodelled-level"]
assert len(unmodelled) == 1
# The lint is a diagnostic of this library rather than a rule of the specification,
# and it
# is an `INFO`: the document is not wrong, it is just not a document this library
# models.
assert unmodelled[0].kind is sbml.RuleKind.LIBRARY_LINT
assert unmodelled[0].severity is sbml.Severity.INFO
# ANCHOR_END: unmodelled

print(f"{len(issues)} issues on the Level 1 document")
