//  Book chapter "Getting started": read a model, look at it, change it, write it
// back.
//!
//  Run with `cargo run --example sbml_getting_started`. The assertions are what makes
// this file a
//  test as well as an example: the book includes this file verbatim, so a chapter
// cannot show code
//! that no longer works.

use biodivine_lib_sbml::Sbml;
use biodivine_lib_sbml::core::{SBase, SId, Species};
use biodivine_lib_sbml::xml::{
    OptionalXmlChild, OptionalXmlProperty, RequiredXmlProperty, XmlChildDefault,
    XmlWrapper,
};

/// A tiny model, so that the example does not depend on a file on disk.
// ANCHOR: model
const MODEL: &str = r#"
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
"#;
// ANCHOR_END: model

fn main() {
    // ANCHOR: read
    // Reading parses the XML and checks that it is a document this library
    // understands: the
    // container element, its level and version, and the well-formedness of the whole
    // tree. A
    // document of a level/version the library does not model is an error (see the
    // chapter on
    // levels and packages).
    let document = Sbml::read_str(MODEL).expect("the document is valid XML and SBML");

    // The container reports what it declares.
    // A *required* attribute reads as its value (`get` would panic on a document that
    // violates the
    // specification; `get_checked` reports the problem instead).
    assert_eq!(document.level().get(), 3);
    assert_eq!(document.version().get(), 2);
    // ANCHOR_END: read

    // ANCHOR: inspect
    // The `model` child is optional (the specification allows a document without a
    // model), so the
    // accessor returns an `Option`-like view.
    let model = document.model().get().expect("the document has a model");

    // A list of children is an `XmlList`: it has a length, indexing and iteration.
    // Note that the
    // list itself is optional too, so it is created on demand.
    let species = model.species().get_or_create();
    assert_eq!(species.len(), 1);

    // The typed accessors read a value with the rules of the specification: an
    // identifier, a
    // number, a boolean or an enumerated value. `get()` returns `None` when the
    // attribute is
    // missing or does not convert.
    let glucose = species.get(0);
    assert_eq!(glucose.id().get(), SId::try_from("glucose").unwrap());
    assert_eq!(glucose.compartment().get(), SId::try_from("cell").unwrap());
    assert_eq!(glucose.initial_concentration().get(), Some(5.0));
    // ANCHOR_END: inspect

    // ANCHOR: edit
    // An accessor is a *view*: it borrows the element and writes through it, so an
    // edit is a
    // mutation of the document in place. `set_some` writes a value, `set_none`
    // removes it.
    glucose.name().set_some(&"D-glucose".to_string());
    glucose.initial_concentration().set_some(&4.5);
    assert_eq!(glucose.name().get(), Some("D-glucose".to_string()));

    // A new object is built from the document, then added to a list.
    let id = SId::try_from("atp").unwrap();
    let compartment = SId::try_from("cell").unwrap();
    let atp = Species::new(model.xml_element().document(), &id, &compartment);
    atp.name().set_some(&"ATP".to_string());
    species.push(atp);
    assert_eq!(species.len(), 2);
    // ANCHOR_END: edit

    // ANCHOR: validate
    // Validation walks the document and reports every finding. It can be cancelled
    // (see the
    // chapter on validation), so it returns a `Result`; nothing is registered here.
    let issues = document
        .validate()
        .expect("no cancellation trigger is registered");
    for issue in &issues {
        println!("{}: {}", issue.rule(), issue.message());
    }
    assert!(issues.is_empty(), "the model above is a valid document");
    // ANCHOR_END: validate

    // ANCHOR: write
    // Writing serializes the document that is in memory. The text of a `notes`, an
    // `annotation` or
    // a formula is kept verbatim; only what the specification *interprets* as a value
    // is read with
    // its whitespace rules.
    let xml = document
        .to_xml_string()
        .expect("the document can be serialized");
    // The new species was written into the list, next to the one that was already
    // there.
    assert!(xml.contains(r#"id="glucose""#), "{xml}");
    assert!(xml.contains(r#"id="atp""#), "{xml}");
    // ANCHOR_END: write

    println!("{} species, {xml:.0}", species.len());
}
