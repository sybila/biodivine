//! Book chapter "Validation": whole-document checks, all problems at once.
//!
//! Run with `cargo run --example xml_dom_validation`.

use biodivine_lib_xml_dom::{Document, Namespace, QualifiedName};

fn main() {
    // ANCHOR: silent
    // A document assembled through the API is not validated as you edit: edits are
    // silent, and `validate` is where you ask.
    let document = Document::new();
    let missing = Namespace::prefixed("http://example.com", "ex").unwrap();
    let root = document
        .create_element(QualifiedName::with_namespace("root", &missing).unwrap());
    document.set_root(root.clone());
    let xml =
        Namespace::prefixed("http://www.w3.org/XML/1998/namespace", "xml").unwrap();
    root.set_attribute(
        QualifiedName::with_namespace("space", &xml).unwrap(),
        "preserve-everything",
    );
    root.set_attribute(
        QualifiedName::with_namespace("id", &xml).unwrap(),
        "not a name",
    );
    // ANCHOR_END: silent

    // ANCHOR: problems
    // Every problem is reported in one call, with the node it belongs to and the
    // rule it comes from, so a whole class of issues can be fixed in one sweep.
    let errors = document.validation_errors().unwrap();
    assert_eq!(errors.len(), 3);
    for error in &errors {
        println!(
            "{}: {} [{}]",
            error.node().unwrap(),
            error.message(),
            error.kind().rule()
        );
    }
    assert!(!document.is_valid().unwrap());
    // ANCHOR_END: problems

    // ANCHOR: fix
    // Fixing the three problems makes the document valid.
    root.set_qualified_name(QualifiedName::with_namespace("root", &missing).unwrap());
    root.declare_namespace(missing);
    root.set_attribute(
        QualifiedName::with_namespace("space", &xml).unwrap(),
        "preserve",
    );
    root.remove_attribute(&QualifiedName::with_namespace("id", &xml).unwrap());
    assert!(document.is_valid().unwrap());
    // ANCHOR_END: fix

    // A parsed document that satisfies the specification is valid too.
    assert!(
        Document::parse_string(r#"<a xmlns:ex="http://e"><ex:b/></a>"#)
            .unwrap()
            .is_valid()
            .unwrap()
    );
    println!("ok");
}
