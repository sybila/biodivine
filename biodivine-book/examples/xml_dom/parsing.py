"""Book chapter "Parsing and serializing" — the Python half."""

import biodivine.xml_dom as xml

# ANCHOR: roundtrip
# A round trip is faithful: prefixes, declarations, escaping and the
# declaration survive.
source = (
    '<?xml version="1.0" encoding="UTF-8"?><ex:a xmlns:ex="http://e">'
    '<ex:b x="1 &amp; 2">t</ex:b><!--c--><![CDATA[<raw>]]><?pi data?></ex:a>'
)
document = xml.Document.parse(source)
assert document.write() == source
assert document.xml_declaration is not None
# ANCHOR_END: roundtrip

# ANCHOR: options
# Output options.
options = xml.WriteOptions(
    declaration=xml.DeclarationStyle.NEVER,
    empty_elements=xml.EmptyElementStyle.EXPLICIT_END_TAG,
)
assert xml.Document.parse("<a><b/></a>").write(options) == "<a><b></b></a>"
# ANCHOR_END: options

# ANCHOR: errors
# Malformed input raises a typed error instead of panicking.
for bad in [
    "<a>",                      # unclosed element
    "<a/><b/>",                 # more than one root
    "text<a/>",                 # content outside the root
    '<a b="x<y"/>',             # `<` in an attribute value
    '<a xmlns:p=""/>',          # an empty prefix declaration
    "<p:a/>",                   # an undeclared prefix
    '<a a="1" a="2"/>',         # duplicate attribute
    "<a>&undefined;</a>",       # an entity this library cannot resolve
]:
    try:
        xml.Document.parse(bad)
    except xml.XmlSyntaxError as error:
        print(f"{bad:26} -> {error}")
    except xml.XmlNamespaceError as error:
        print(f"{bad:26} -> {error}")
# ANCHOR_END: errors

# ANCHOR: other_nodes
# Text, comments, CDATA sections and processing instructions are separate node kinds.
mixed = xml.Document.parse("<a>b<!--c--><![CDATA[<raw>]]><?pi data?></a>")
assert [child.kind for child in mixed.root] == [
    xml.NodeKind.TEXT,
    xml.NodeKind.COMMENT,
    xml.NodeKind.CDATA,
    xml.NodeKind.PROCESSING_INSTRUCTION,
]
# ANCHOR_END: other_nodes

# ANCHOR: entities
# Predefined entities and character references are expanded.
text = xml.Document.parse("<a>AT&amp;T &#65;</a>")
assert text.root[0].text() == "AT&T A"
print(text.write())
# ANCHOR_END: entities
