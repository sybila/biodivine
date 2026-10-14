//! Book chapter "The Python layer": what the two APIs look like side by side.
//!
//! This is the Rust half of a chapter that also shows the Python layer, so it demonstrates the Rust
//! API that the Pythonic conveniences map onto: iterating children, reading attributes by local
//! name, and validating.
//!
//! Run with `cargo run --example xml_dom_pythonic`.
use biodivine_lib_xml_dom::Document;

fn main() {
    let document =
        Document::parse_string(r#"<root><child class="a"/><child class="b"/></root>"#)
            .unwrap();
    let root = document.root().unwrap();

    // ANCHOR: mapping
    // The Python layer offers `for child in node` and `child.get("class")`; the Rust
    // API spells the same operations as an explicit child list and an attribute
    // lookup by local name.
    let children = root.child_elements();
    assert_eq!(children.len(), 2);
    let classes: Vec<String> = children
        .iter()
        .map(|child| {
            child
                .attribute_without_namespace(&biodivine_lib_xml_dom::xml_spec::nc_name(
                    "class",
                ))
                .unwrap()
                .to_string()
        })
        .collect();
    assert_eq!(classes, ["a", "b"]);
    // ANCHOR_END: mapping

    // ANCHOR: indexing
    // Indexing by position is `children.get(i)`.
    assert_eq!(children.get(1).unwrap().local_name(), "child");
    // ANCHOR_END: indexing

    // ANCHOR: handles
    // A handle refers to one node: it can be compared, used as a map key, and asked
    // for its document.
    let child = root.child_elements()[0].clone();
    assert!(child.ptr_eq(&root.child_elements()[0]));
    assert!(child.belongs_to(&document));
    assert_eq!(child.parent().unwrap().id(), root.id());
    assert_eq!(child.id(), u32::from(child.id()).into());
    // ANCHOR_END: handles

    // ANCHOR: validation
    // Validation is a whole-document call in both languages.
    assert!(document.is_valid().unwrap());
    println!("{} children", children.len());
    // ANCHOR_END: validation
}
