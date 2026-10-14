//! Book chapter "Thread safety": one document, many threads.
//!
//! Run with `cargo run --example xml_dom_threads`.

use biodivine_lib_xml_dom::{Document, QualifiedName, XmlError, cancel_this};

fn main() {
    let document = Document::new();
    let root =
        document.create_element(QualifiedName::without_namespace("root").unwrap());
    document.set_root(root.clone());

    // ANCHOR: threads
    // Handles are `Send + Sync`: pass the document, or a node, to another thread.
    let workers: Vec<_> = (0..4)
        .map(|index| {
            let document = document.clone();
            let root = root.clone();
            std::thread::spawn(move || {
                for item in 0..25 {
                    let node = document.create_element(
                        QualifiedName::without_namespace(format!("item{index}_{item}"))
                            .unwrap(),
                    );
                    node.append_child(document.create_text("payload").unwrap());
                    root.append_child(node);
                }
            })
        })
        .collect();
    for worker in workers {
        worker.join().unwrap();
    }
    // ANCHOR_END: threads

    // ANCHOR: readers
    // Readers can run concurrently with each other; a read never sees a
    // half-finished edit, because every operation is one critical section on the
    // document's single lock.
    let readers: Vec<_> = (0..4)
        .map(|_| {
            let document = document.clone();
            std::thread::spawn(move || {
                let mut total = 0usize;
                for _ in 0..50 {
                    total += document.root().unwrap().children().len();
                    let _ = document.write_string().unwrap();
                }
                total
            })
        })
        .collect();
    for reader in readers {
        assert!(reader.join().unwrap() > 0);
    }
    // ANCHOR_END: readers

    // ANCHOR: cancel
    // A long operation consults the cancellation triggers registered on its thread.
    // Here the trigger has already fired, so validation stops right away.
    let trigger = cancel_this::CancelAtomic::new();
    trigger.cancel();
    let result = cancel_this::on_atomic(trigger, || document.validate());
    assert!(matches!(result, Err(XmlError::Cancelled(_))));

    // `on_timeout` is the usual way to bound how long an operation may take.
    let result = cancel_this::on_timeout(std::time::Duration::from_secs(60), || {
        document.write_string()
    });
    assert!(result.is_ok());
    // ANCHOR_END: cancel

    assert_eq!(root.children().len(), 4 * 25);
    assert!(document.is_valid().unwrap());
    println!("{} children, document valid", root.children().len());
}
