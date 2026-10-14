"""Book chapter "Getting started" — the Python half.

The chapter includes this file verbatim, and `tests/test_examples.py` runs it, so the
book cannot show code that no longer works.
"""

import biodivine.xml_dom as xml

# ANCHOR: document
document = xml.Document()
assert document.root is None

ex = xml.Namespace("http://example.com", "ex")
root = document.create_element(("root", ex))
root.declare_namespace(ex)
document.set_root(root)

child = document.create_element(("child", ex))
child.set_attribute("id", "first")
child.append_child(document.create_text("Hello, World!"))
root.append_child(child)
# ANCHOR_END: document

# ANCHOR: serialize
assert document.write() == (
    '<ex:root xmlns:ex="http://example.com">'
    '<ex:child id="first">Hello, World!</ex:child></ex:root>'
)
assert document.is_valid()
# ANCHOR_END: serialize

# ANCHOR: names
# Names are *expanded* names: the prefix belongs to the namespace, not to the
# local name.
child = root.child_elements()[0]
assert child.local_name == "child"
assert child.namespace.uri == "http://example.com"
assert child.qualified_name == xml.QualifiedName("child", ex)
print(document.write())
# ANCHOR_END: names
