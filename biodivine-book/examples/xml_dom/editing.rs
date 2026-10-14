//! Book chapter "Traversing and editing": handles, structural edits, clones, cross-document copies.
//!
//! Run with `cargo run --example xml_dom_editing`.

use biodivine_lib_xml_dom::{Document, QualifiedName};

fn main() {
    let document = Document::parse_string("<root><a/><b/><c/></root>").unwrap();
    let root = document.root().unwrap();

    // ANCHOR: handles
    // Handles are cheap: cloning one copies the *handle*, not the node.
    let a = root.child_elements()[0].clone();
    let a_again = a.clone();
    assert!(a.ptr_eq(&a_again));
    // ANCHOR_END: handles

    // ANCHOR: traversal
    // Traversal.
    assert_eq!(root.children().len(), 3);
    assert_eq!(
        a.next_sibling().unwrap().as_element().unwrap().local_name(),
        "b"
    );
    assert_eq!(
        root.last_child()
            .unwrap()
            .as_element()
            .unwrap()
            .local_name(),
        "c"
    );
    assert_eq!(a.index_in_parent(), Some(0));
    // ANCHOR_END: traversal

    // ANCHOR: editing
    // Structural editing is atomic and cycle-safe.
    let x = document.create_element(QualifiedName::without_namespace("x").unwrap());
    root.insert_child(1, x.clone());
    assert_eq!(
        root.child_elements()
            .iter()
            .map(|e| e.local_name().to_string())
            .collect::<Vec<_>>(),
        ["a", "x", "b", "c"]
    );
    x.detach();
    root.insert_after(a.clone(), x.clone());
    assert_eq!(root.children().len(), 4);
    // ANCHOR_END: editing

    // ANCHOR: replace
    // Replacing leaves the old node detached but alive.
    let replacement =
        document.create_element(QualifiedName::without_namespace("y").unwrap());
    let old = x.replace_with(replacement);
    assert!(!old.is_attached());
    assert_eq!(old.as_element().unwrap().local_name(), "x");
    // ANCHOR_END: replace

    // ANCHOR: errors
    // Cycles and foreign documents are errors, not silent corruption.
    assert!(root.append_child_checked(root.clone()).is_err());
    let other = Document::new();
    let foreign = other.create_element(QualifiedName::without_namespace("f").unwrap());
    assert!(root.append_child_checked(foreign).is_err());
    // ANCHOR_END: errors

    // ANCHOR: detached
    // A fresh node is detached (but already belongs to a document) until it is
    // attached.
    let detached =
        document.create_element(QualifiedName::without_namespace("d").unwrap());
    assert!(!detached.is_attached());
    root.append_child(detached.clone());
    assert!(detached.is_attached());
    // ANCHOR_END: detached

    // ANCHOR: clones
    // Clones: `deep_clone` copies the subtree, `shallow_clone` only the node.
    let deep = root.deep_clone().unwrap();
    assert_eq!(deep.children().len(), root.children().len());
    assert!(!deep.is_attached());
    let shallow = root.shallow_clone();
    assert!(shallow.children().is_empty());
    // ANCHOR_END: clones

    // ANCHOR: import
    // Copying into another document is the sanctioned way to move a tree between
    // documents.
    let target = Document::new();
    let imported = root.deep_clone_into(&target).unwrap();
    assert!(imported.belongs_to(&target));
    let new_root =
        target.create_element(QualifiedName::without_namespace("wrapper").unwrap());
    target.set_root(new_root.clone());
    new_root.append_child(imported);
    assert!(target.is_valid().unwrap());

    println!("{}", document.write_string().unwrap());
    // ANCHOR_END: import
}
