//! Book chapter "MathML": build a formula, attach it to a model, and read it back.
//!
//! Run with `cargo run --example sbml_mathml`.

use biodivine_lib_sbml::Sbml;
use biodivine_lib_sbml::core::{SId, Species};
use biodivine_lib_sbml::math::{MathNode, MathNodeKind, MathOperator};
use biodivine_lib_sbml::xml::{
    OptionalXmlChild, RequiredXmlProperty, XmlChildDefault, XmlWrapper,
};

const MODEL: &str = r#"
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
"#;

fn main() {
    let document = Sbml::read_str(MODEL).expect("the document is valid SBML");
    let model = document.model().get().expect("the document has a model");
    let document_element = model.xml_element().document();

    // ANCHOR: build
    // A formula is a tree of `MathNode`s. The leaves are built from the document they
    // will belong
    // to, and the operators are a closed set: `MathOperator` names every operator the
    // subset
    // contains, and each one knows its element name and its arity.
    let x = MathNode::ci(document_element.clone(), "x");
    let k = MathNode::ci(document_element.clone(), "k");
    let product = MathNode::apply(
        document_element.clone(),
        MathOperator::Times,
        vec![x.clone(), k.clone()],
    );

    // A node knows what it is and which children it has.
    // An `apply` node holds the operator first and then its arguments, so a formula
    // is navigated by
    // kind: the root is the application, and the operator is the kind of its first
    // child.
    assert_eq!(product.kind(), MathNodeKind::Apply);
    assert_eq!(product.children().len(), 3);
    let operator = product.children()[0].kind();
    assert_eq!(operator, MathNodeKind::Operator(MathOperator::Times));
    // The kind of an operator node carries the operator itself, and an operator is
    // not one of the
    // *declared* element kinds: it is one of the closed set of operators.
    assert!(!operator.is_declared_element());
    assert_eq!(operator.element_name(), "times");
    assert_eq!(MathOperator::Times.name(), "times");
    assert_eq!(x.kind(), MathNodeKind::Ci);
    assert_eq!(x.children().len(), 0);
    // ANCHOR_END: build

    // ANCHOR: attach
    // The `<math>` element is the child that holds a formula: `KineticLaw` has one,
    // and so do a
    // rule and an event's delay. Attaching a tree serializes it into that element.
    let parameters = model.parameters().get_or_create();
    assert_eq!(parameters.len(), 1);
    let reaction =
        biodivine_lib_sbml::core::Reaction::new_empty(document_element.clone());
    reaction.id().set(&SId::try_from("r").unwrap());
    reaction.reversible().set(&false);
    model.reactions().get_or_create().push(reaction.clone());
    let law = reaction.kinetic_law().get_or_create();
    let math = law.math().get_or_create();
    math.set_expression(product.clone());
    assert_eq!(
        math.expression().map(|it| it.kind()),
        Some(MathNodeKind::Apply)
    );
    // ANCHOR_END: attach

    // ANCHOR: read
    // Reading a formula back walks the same tree: the kinds come from the element
    // names, and the
    // text of a `ci` is the symbol it refers to. `to_xml_string` is where the tree
    // becomes text.
    let written = document
        .to_xml_string()
        .expect("the document can be serialized");
    assert!(written.contains("<apply>"), "{written}");
    assert!(written.contains("<times/>"), "{written}");
    assert!(written.contains("<ci>x</ci>"), "{written}");

    // A `cn` node holds a number, and `MathNode::real`/`integer` build one.
    let two = MathNode::integer(document_element.clone(), 2);
    assert_eq!(two.kind(), MathNodeKind::Cn);
    // A `cn` node's payload is the number it holds, as the document spells it.
    let number = biodivine_lib_sbml::math::Cn::from(two.into_element());
    assert_eq!(number.payload(), "2");
    // ANCHOR_END: read

    // The model still validates: the formula above is inside the subset SBML permits.
    let issues = document
        .validate()
        .expect("no cancellation trigger is registered");
    let errors = issues
        .iter()
        .filter(|it| it.severity() == biodivine_lib_sbml::SbmlIssueSeverity::Error)
        .count();
    assert_eq!(errors, 0, "{issues:?}");
    let _ = Species::new_empty(document_element);
}
