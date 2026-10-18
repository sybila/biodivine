//  Book chapter "Levels, packages and versions": which documents this library
// resolves a model
//! for, and what it reports when it cannot.
//!
//! Run with `cargo run --example sbml_levels`.

use biodivine_lib_sbml::Sbml;
use biodivine_lib_sbml::xml::{OptionalXmlChild, RequiredXmlProperty};

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
    // The library models Level 3 (every version) and Level 2 (from Version 2 on):
    // reading such a
    // document gives a model, and the accessors behave as they do for Level 3 Version
    // 2.
    for (name, source) in [("l3v1", L3V1), ("l2v4", L2V4)] {
        let document = Sbml::read_str(source).expect("the document is well-formed XML");
        let model = document.model().get();
        assert!(model.is_some(), "{name} resolves a model");
        let model = model.unwrap();
        let compartments = model.compartments().get().expect("the list is there");
        assert_eq!(compartments.len(), 1);
        assert_eq!(compartments.get(0).id().get().as_str(), "cell");
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
    let unmodelled = issues
        .iter()
        .filter(|it| it.rule() == "unmodelled-level")
        .count();
    assert_eq!(unmodelled, 1);
    assert!(!issues.is_empty());
    // ANCHOR_END: unmodelled

    println!("{} issues on the Level 1 document", issues.len());
}
