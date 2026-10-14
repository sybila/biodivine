//! Small program showing the collector: a handle keeps a node alive, and an id does not.
//!
//! The book includes the anchored region below; run it with `cargo run --example xml_dom_gc`.

use biodivine_lib_xml_dom::{Document, QualifiedName};

fn main() {
    let document = Document::new();
    let root =
        document.create_element(QualifiedName::without_namespace("root").unwrap());
    document.set_root(root.clone());
    let scratch =
        document.create_element(QualifiedName::without_namespace("scratch").unwrap());

    // ANCHOR: collected
    // A handle keeps its node alive; the document root keeps the tree it points at.
    assert_eq!(document.collect_garbage().unwrap().collected, 0);
    assert_eq!(document.node_count(), 2);

    // Dropping the last handle of a detached node makes it collectable, and the
    // slot is reused.
    let id = scratch.id();
    drop(scratch);
    let stats = document.collect_garbage().unwrap();
    assert_eq!(stats.collected, 1);
    assert_eq!(document.node_count(), 1);

    // An id is a slot number, not a reference: it stops resolving once the slot
    // has been reclaimed.
    assert!(document.node(id).is_none());
    // ANCHOR_END: collected

    // The root is still there, with its subtree, and the document is still valid.
    assert!(document.root().is_some());
    assert!(document.is_valid().unwrap());
}
