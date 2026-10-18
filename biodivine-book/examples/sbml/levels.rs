//! Book chapter "Levels, packages and versions": which documents this library
//! resolves a model for, and what it reports when it cannot.
//!
//! Run with `cargo run --example sbml_levels`.

use biodivine_lib_sbml::core::SBase;
use biodivine_lib_sbml::xml::{
    OptionalXmlChild, OptionalXmlProperty, RequiredXmlProperty, XmlProperty,
};
use biodivine_lib_sbml::{RuleKind, Sbml, SbmlIssueSeverity};

// ANCHOR: documents
/// A Level 3 Version 1 document: the previous revision of the same level.
const L3V1: &str = r#"
<sbml xmlns="http://www.sbml.org/sbml/level3/version1/core" level="3" version="1">
  <model>
    <listOfCompartments>
      <compartment id="cell" constant="true" size="1"/>
    </listOfCompartments>
  </model>
</sbml>
"#;

/// A Level 2 Version 4 document: an older *level*.
const L2V4: &str = r#"
<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2" version="4">
  <model>
    <listOfCompartments>
      <compartment id="cell" size="1"/>
    </listOfCompartments>
  </model>
</sbml>
"#;

//  A Level 2 Version 1 document: the first version of Level 2, whose namespace has no
// version in
/// it (`.../level2`), which is the one thing that makes this pair special.
const L2V1: &str = r#"
<sbml xmlns="http://www.sbml.org/sbml/level2" level="2" version="1">
  <model>
    <listOfCompartments>
      <compartment name="cell" size="1"/>
    </listOfCompartments>
  </model>
</sbml>
"#;

/// A Level 3 Version 2 document: the version the base tables are written for.
const L3V2: &str = r#"
<sbml xmlns="http://www.sbml.org/sbml/level3/version2/core" level="3" version="2">
  <model>
    <listOfCompartments>
      <compartment id="cell" constant="true" size="1"/>
    </listOfCompartments>
  </model>
</sbml>
"#;

/// A Level 1 document: a level this library does not model.
const L1V2: &str = r#"
<sbml xmlns="http://www.sbml.org/sbml/level1" level="1" version="2">
  <model>
    <listOfCompartments>
      <compartment name="cell" volume="1"/>
    </listOfCompartments>
  </model>
</sbml>
"#;

// ANCHOR_END: documents

fn main() {
    // ANCHOR: resolve
    // The library models Level 3 (every version) and Level 2 (every version,
    // including the first one): reading such a document gives a model, and the
    // accessors behave as they do for Level 3 Version 2.
    for (name, source) in [
        ("l3v1", L3V1),
        ("l3v2", L3V2),
        ("l2v1", L2V1),
        ("l2v4", L2V4),
    ] {
        let document = Sbml::read_str(source).expect("the document is well-formed XML");
        let model = document.model().get();
        assert!(model.is_some(), "{name} resolves a model");
        let model = model.unwrap();
        let compartments = model.compartments().get().expect("the list is there");
        assert_eq!(compartments.len(), 1);
        // Level 2 Version 1 has no identifiers: its compartments have *names*. The
        // two accessors
        // say which one this document uses, and `get_checked` is the read that
        // reports instead of
        // panicking when the attribute is not there.
        let compartment = compartments.get(0);
        let label = compartment
            .id()
            .get_checked()
            .expect("an identifier converts when it is there")
            .map(|id| id.as_str().to_string())
            .or_else(|| compartment.name().get())
            .expect("a compartment has an identifier or a name");
        assert_eq!(label, "cell");
    }
    // ANCHOR_END: resolve

    // ANCHOR: unmodelled
    // A document of a level/version this library does not model is still *readable*:
    // the XML tree
    // is there, the container reports what it declares, and validation says that the
    // model was not
    // modelled. Reading it as a model is what an older-level document is *for*, so
    // the library
    // reports the situation as a lint rather than failing the read.
    let document = Sbml::read_str(L1V2).expect("the document is well-formed XML");
    assert_eq!(document.level().get(), 1);
    let issues = document
        .validate()
        .expect("no cancellation trigger is registered");
    let unmodelled: Vec<&biodivine_lib_sbml::SbmlIssue> = issues
        .iter()
        .filter(|it| it.rule() == "unmodelled-level")
        .collect();
    assert_eq!(unmodelled.len(), 1);
    // The lint is a diagnostic of this library rather than a rule of the
    // specification, and it is
    // an `Info`: the document is not wrong, it is just not a document this library
    // models.
    assert_eq!(unmodelled[0].kind(), RuleKind::LibraryLint);
    assert_eq!(unmodelled[0].severity(), SbmlIssueSeverity::Info);
    // ANCHOR_END: unmodelled

    println!("{} issues on the Level 1 document", issues.len());
}
