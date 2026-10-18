//! Book chapter "Validation": the report of a validation pass, its severities, and
//! the guard that
//! says part of a document was not walked.
//!
//! Run with `cargo run --example sbml_validation`.

use biodivine_lib_sbml::core::SId;
use biodivine_lib_sbml::xml::{OptionalXmlChild, RequiredXmlProperty, XmlChildDefault};
use biodivine_lib_sbml::{RuleKind, Sbml, SbmlIssueSeverity};

// ANCHOR: broken
/// Two species with the same identifier: a violation of rule 10301.
const BROKEN: &str = r#"
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
"#;

// ANCHOR_END: broken

fn main() {
    let document = Sbml::read_str(BROKEN).expect("the document is well-formed XML");

    // ANCHOR: report
    // Validation returns the *issues* it found; it does not fail. Every issue names
    // the rule that
    // produced it (a specification rule number, or a name of the library's own
    // diagnostics), the
    // severity of that rule and a message.
    let issues = document
        .validate()
        .expect("no cancellation trigger is registered");
    assert_eq!(issues.len(), 1);

    let issue = issues.first().expect("the report has one issue");
    assert_eq!(issue.rule(), "10301");
    assert_eq!(issue.severity(), SbmlIssueSeverity::Error);
    // A *library lint* is a diagnostic of this library rather than a rule of the
    // specification.
    assert_eq!(issue.kind(), RuleKind::SpecRule);
    println!("{}", issue.message());
    // ANCHOR_END: report

    // ANCHOR: severities
    // A document can have warnings and notes and still be fine: only an `Error` means
    // the document
    // violates the specification.
    let errors = issues
        .iter()
        .filter(|it| it.severity() == SbmlIssueSeverity::Error);
    assert_eq!(errors.count(), 1);
    // ANCHOR_END: severities

    // ANCHOR: not-validated
    // The walk skips a subtree whose *type check* failed, because the typed accessors
    // of that
    // subtree would be unsafe; it reports one issue for the subtree instead. A report
    // without such
    // an issue means that every object of the document was walked, which is what a
    // test wants to
    // know before it trusts the rest of the report.
    let not_validated = issues.iter().filter(|it| it.is_not_validated()).count();
    assert_eq!(not_validated, 0);
    // ANCHOR_END: not-validated

    // ANCHOR: fix
    // Fixing the violation makes the report empty: the second species gets an
    // identifier of its
    // own. (`id` is a *required* attribute, so its view takes the value directly.)
    let model = document.model().get().expect("the document has a model");
    let species = model.species().get_or_create();
    let second = species.get(1);
    second.id().set(&SId::try_from("t").unwrap());
    let issues = document
        .validate()
        .expect("no cancellation trigger is registered");
    assert!(issues.is_empty(), "{issues:?}");
    // ANCHOR_END: fix
}
