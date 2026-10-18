"""Book chapter "Validation" - the Python half.

The chapter includes this file verbatim, and `tests/test_examples.py` runs it.
"""

import biodivine.sbml as sbml

# ANCHOR: broken
# Two species with the same identifier: a violation of rule 10301.
BROKEN = """
<sbml xmlns="http://www.sbml.org/sbml/level3/version2/core" level="3" version="2">
  <model>
    <listOfCompartments>
      <compartment id="cell" constant="true" size="1"/>
    </listOfCompartments>
    <listOfSpecies>
      <species id="s" compartment="cell" initialConcentration="1"
               hasOnlySubstanceUnits="false" boundaryCondition="false"
               constant="false"/>
      <species id="s" compartment="cell" initialConcentration="2"
               hasOnlySubstanceUnits="false" boundaryCondition="false"
               constant="false"/>
    </listOfSpecies>
  </model>
</sbml>
"""
# ANCHOR_END: broken

document = sbml.reads(BROKEN)

# ANCHOR: report
# Validation returns the *issues* it found; it does not fail. Every issue names the
# rule that
# produced it (a specification rule number, or a name of the library's own
# diagnostics), the
# severity of that rule and a message.
issues = document.validate()
assert len(issues) == 1

issue = issues[0]
assert issue.rule == "10301"
assert issue.severity is sbml.Severity.ERROR
# A *library lint* is a diagnostic of this library rather than a rule of the
# specification.
assert issue.kind is sbml.RuleKind.SPEC_RULE
print(issue.message)
# ANCHOR_END: report

# ANCHOR: severities
# A document can have warnings and notes and still be fine: only an `ERROR` means the
# document
# violates the specification.
assert not issues.is_valid
assert len(issues.errors) == 1
assert len(issues.warnings) == 0
# ANCHOR_END: severities

# ANCHOR: not-validated
# The walk skips a subtree whose *type check* failed, because the typed accessors of
# that subtree
# would be unsafe; it reports one issue for the subtree instead. A report without such
# an issue
# means that every object of the document was walked, which is what a test wants to
# know before it
# trusts the rest of the report.
not_validated = [issue for issue in issues if issue.is_not_validated]
assert not_validated == []
# ANCHOR_END: not-validated

# ANCHOR: fix
# Fixing the violation makes the report empty.
model = document.model
species = model.species
species[1].id = "t"
issues = document.validate()
assert issues.is_valid, issues
# ANCHOR_END: fix
