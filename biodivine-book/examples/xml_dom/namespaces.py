"""Book chapter "Namespaces" — the Python half."""

import biodivine.xml_dom as xml

# ANCHOR: parse
document = xml.Document.parse(
    '<root xmlns:ex="http://example.com" xmlns="http://default">'
    '<child ex:attr="v"/></root>'
)
root = document.root
child = root.child_elements()[0]

assert str(root.qualified_name) == "root"
assert child.namespace.uri == "http://default"
# ANCHOR_END: parse

# ANCHOR: resolve
# Resolution helpers work in the scope of any node.
assert child.resolve_element_name("item").namespace.uri == "http://default"
assert root.resolve_element_name("ex:item").namespace.uri == "http://example.com"
# ANCHOR_END: resolve

# ANCHOR: attributes
# An unprefixed *attribute* never takes the default namespace, even when one
# is in scope.
assert child.attribute(("attr", xml.Namespace("http://example.com", "ex"))) == "v"
assert child.resolve_attribute_name("item").namespace is None
# ANCHOR_END: attributes

# ANCHOR: xml_prefix
# The `xml` prefix is bound to its reserved URI without any declaration.
assert (
    child.resolve_attribute_name("xml:lang").namespace.uri
    == "http://www.w3.org/XML/1998/namespace"
)
# ANCHOR_END: xml_prefix

# ANCHOR: undeclare
# `xmlns=""` removes the default namespace from the element it is declared on.
document = xml.Document.parse(
    '<root xmlns="http://d"><inner xmlns=""><leaf/></inner></root>'
)
inner = document.root.child_elements()[0]
assert inner.namespace is None
assert inner.child_elements()[0].namespace is None
assert inner.namespace_declarations == {None: None}
# ANCHOR_END: undeclare

# ANCHOR: silent
# Editing never synchronises declarations: removing one is silent, and
# `validate` reports.
document = xml.Document.parse(
    '<ex:root xmlns:ex="http://example.com"><ex:child/></ex:root>'
)
root = document.root
root.remove_namespace_declaration("ex")
assert len(document.validation_errors()) == 2
assert [problem.kind for problem in document.validation_errors()] == [
    "undeclared_prefix",
    "undeclared_prefix",
]
assert document.write() == "<ex:root><ex:child/></ex:root>"
print(document.write())
# ANCHOR_END: silent
