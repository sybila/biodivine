//! Book chapter "Namespaces": declarations, scope, and the implicit `xml` prefix.
//!
//! Run with `cargo run --example xml_dom_namespaces`.

use biodivine_lib_xml_dom::{Document, Namespace, QualifiedName};

fn main() {
    // ANCHOR: parse
    // Parsing assigns every name its expanded form, resolving prefixes against the
    // declarations that are in scope.
    let document = Document::parse_string(concat!(
        r#"<root xmlns:ex="http://example.com" xmlns="http://default">"#,
        r#"<child ex:attr="v"/></root>"#
    ))
    .unwrap();
    let root = document.root().unwrap();
    let child = root.child_elements()[0].clone();

    assert_eq!(root.qualified_name().to_string(), "root");
    assert_eq!(child.namespace().unwrap().uri(), "http://default");
    assert_eq!(
        child
            .attribute(
                &QualifiedName::with_namespace(
                    "attr",
                    &Namespace::prefixed("http://example.com", "ex").unwrap()
                )
                .unwrap()
            )
            .unwrap()
            .as_ref(),
        "v"
    );
    // ANCHOR_END: parse

    // ANCHOR: resolve
    // Resolution helpers work in the scope of any node.
    assert_eq!(
        child
            .resolve_element_name("item")
            .unwrap()
            .namespace()
            .unwrap()
            .uri(),
        "http://default"
    );
    // ANCHOR_END: resolve

    // ANCHOR: attributes
    // ... and an unprefixed *attribute* never takes the default namespace.
    assert!(
        child
            .resolve_attribute_name("item")
            .unwrap()
            .namespace()
            .is_none()
    );
    // ANCHOR_END: attributes

    // ANCHOR: xml_prefix
    // The `xml` prefix needs no declaration.
    assert_eq!(
        child
            .resolve_attribute_name("xml:lang")
            .unwrap()
            .namespace()
            .unwrap()
            .uri(),
        "http://www.w3.org/XML/1998/namespace"
    );
    // ANCHOR_END: xml_prefix

    // ANCHOR: undeclare
    // `xmlns=""` removes the default namespace from the element it is declared on.
    let document = Document::parse_string(
        r#"<root xmlns="http://d"><inner xmlns=""><leaf/></inner></root>"#,
    )
    .unwrap();
    let inner = document.root().unwrap().child_elements()[0].clone();
    assert!(inner.namespace().is_none());
    assert!(inner.child_elements()[0].namespace().is_none());
    assert_eq!(inner.namespace_declarations().get(&None), Some(&None));
    // ANCHOR_END: undeclare

    // ANCHOR: silent
    // Editing never synchronises declarations for you: removing one that a subtree
    // relies on succeeds silently, and `validate` reports the inconsistency.
    let document = Document::parse_string(
        r#"<ex:root xmlns:ex="http://example.com"><ex:child/></ex:root>"#,
    )
    .unwrap();
    let root = document.root().unwrap();
    root.remove_namespace_declaration(Some(&biodivine_lib_xml_dom::xml_spec::nc_name(
        "ex",
    )));
    assert_eq!(document.validation_errors().unwrap().len(), 2);
    assert_eq!(
        document.write_string().unwrap(),
        "<ex:root><ex:child/></ex:root>"
    );
    println!("{}", document.write_string().unwrap());
    // ANCHOR_END: silent
}
