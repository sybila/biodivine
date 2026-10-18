"""Book chapter "MathML" - the Python half.

The chapter includes this file verbatim, and `tests/test_examples.py` runs it.
"""

import biodivine.sbml as sbml

MODEL = """
<sbml xmlns="http://www.sbml.org/sbml/level3/version2/core" level="3" version="2">
  <model>
    <listOfCompartments>
      <compartment id="cell" constant="true" size="1"/>
    </listOfCompartments>
    <listOfSpecies>
      <species id="x" compartment="cell" initialConcentration="1"
               hasOnlySubstanceUnits="false" boundaryCondition="false"
               constant="false"/>

    </listOfSpecies>
    <listOfParameters>
      <parameter id="k" constant="true" value="2"/>
    </listOfParameters>
  </model>
</sbml>
"""

document = sbml.reads(MODEL)
model = document.model

# ANCHOR: build
# A formula is a tree of `MathNode`s. The leaves are built from the document they will
# belong to,
# and the operators are a closed set: `MathOperator` names every operator the subset
# contains, and
# each one knows its element name.
x = sbml.MathNode.ci(document, "x")
k = sbml.MathNode.ci(document, "k")
product = sbml.MathNode.apply(document, sbml.MathOperator.TIMES, [x, k])

# An `apply` node holds the operator first and then its arguments, so a formula is
# navigated by
# kind: the root is the application, and the operator is the kind of its first child.
assert product.kind == sbml.MathNodeKind.APPLY
assert len(product.children) == 3
operator = product.children[0].kind
assert operator.element_name == "times"
assert x.kind == sbml.MathNodeKind.CI
assert x.children == []
assert sbml.MathOperator.TIMES.name == "times"
# ANCHOR_END: build

# ANCHOR: attach
# The `<math>` element is the child that holds a formula: a kinetic law has one, and
# so do a rule
# and an event's delay. Attaching a tree serializes it into that element.
reaction = sbml.Reaction.new_empty(document)
reaction.id = "r"
reaction.reversible = False
model.create_reactions().append(reaction)
law = reaction.create_kinetic_law()
math = law.create_math()
math.set_expression(product)
assert math.expression.kind == sbml.MathNodeKind.APPLY
# ANCHOR_END: attach

# ANCHOR: read
# Reading a formula back walks the same tree: the kinds come from the element names,
# and the text of
# a `ci` is the symbol it refers to. `to_string` is where the tree becomes text.
written = document.to_string()
assert "<apply>" in written, written
assert "<times/>" in written, written
assert "<ci>x</ci>" in written, written

# A `cn` node holds a number, and `MathNode.integer`/`real` build one. The typed
# class of the element is one cast away, which is how a caller reads the payload.
two = sbml.MathNode.integer(document, 2)
assert two.kind == sbml.MathNodeKind.CN
assert sbml.Cn.try_from_element(two.element).payload == "2"
# ANCHOR_END: read

# The model still validates: the formula above is inside the subset SBML permits.
issues = document.validate()
assert issues.errors == [], issues
