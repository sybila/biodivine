//! Book chapter "Parsing and serializing": round trips, options, and what parsing rejects.
//!
//! Run with `cargo run --example xml_dom_parsing`.

use biodivine_lib_xml_dom::{
    DeclarationStyle, Document, EmptyElementStyle, NodeKind, WriteOptions,
};

fn main() {
    // ANCHOR: roundtrip
    // A round trip is faithful: prefixes, declarations, escaping and the XML
    // declaration survive.
    let source = concat!(
        r#"<?xml version="1.0" encoding="UTF-8"?>"#,
        r#"<ex:a xmlns:ex="http://e"><ex:b x="1 &amp; 2">t</ex:b>"#,
        r#"<!--c--><![CDATA[<raw>]]><?pi data?></ex:a>"#
    );
    let document = Document::parse_string(source).unwrap();
    assert_eq!(document.write_string().unwrap(), source);
    assert!(document.xml_declaration().is_some());
    // ANCHOR_END: roundtrip

    // ANCHOR: options
    // Output options.
    let options = WriteOptions::default()
        .with_declaration(DeclarationStyle::Never)
        .with_empty_elements(EmptyElementStyle::ExplicitEndTag);
    assert_eq!(
        Document::parse_string("<a><b/></a>")
            .unwrap()
            .write_string_with(&options)
            .unwrap(),
        "<a><b></b></a>"
    );
    // ANCHOR_END: options

    // ANCHOR: errors
    // The parser rejects malformed input with a typed error instead of panicking.
    for bad in [
        "<a>",                   // unclosed element
        "<a/><b/>",              // more than one root
        "text<a/>",              // content outside the root
        r#"<a b="x<y"/>"#,       // `<` in an attribute value
        r#"<a xmlns:p=""/>"#,    // an empty prefix declaration
        "<p:a/>",                // an undeclared prefix
        r#"<a a="1" a="2"/>"#,   // duplicate attribute
        r#"<a>&undefined;</a>"#, // an entity this library cannot resolve
    ] {
        let error = Document::parse_string(bad).unwrap_err();
        println!("{bad:28} -> {error}");
    }
    // ANCHOR_END: errors

    // ANCHOR: other_nodes
    // Text, comments, CDATA sections and processing instructions are separate node
    // kinds, each with a constructor that validates its content.
    let mixed =
        Document::parse_string("<a>b<!--c--><![CDATA[<raw>]]><?pi data?></a>").unwrap();
    let kinds: Vec<NodeKind> = mixed
        .root()
        .unwrap()
        .children()
        .iter()
        .map(|node| node.kind())
        .collect();
    assert_eq!(
        kinds,
        [
            NodeKind::Text,
            NodeKind::Comment,
            NodeKind::CData,
            NodeKind::ProcessingInstruction
        ]
    );
    // ANCHOR_END: other_nodes

    // ANCHOR: entities
    // Predefined entities and character references are expanded.
    let text = Document::parse_string("<a>AT&amp;T &#65;</a>").unwrap();
    assert_eq!(
        text.root().unwrap().children()[0].text().unwrap().as_str(),
        "AT&T A"
    );
    println!("{}", text.write_string().unwrap());
    // ANCHOR_END: entities
}
