"""Book chapter "The Python layer" — what is Pythonic rather than mirrored."""

import biodivine.xml_dom as xml

# ANCHOR: mapping
# Iterating children and reading an attribute by local name are the Pythonic
# spellings of the Rust `child_elements()` and `attribute_without_namespace()`.
document = xml.Document.parse('<root><child class="a"/><child class="b"/></root>')
root = document.root
assert [child.local_name for child in root] == ["child", "child"]
assert root[0].get("class") == "a"
# ANCHOR_END: mapping

# ANCHOR: indexing
# Indexing by position and `len` are the Pythonic spellings of `children.get(i)`.
assert root[1].local_name == "child"
assert len(root) == 2
# ANCHOR_END: indexing

# ANCHOR: handles
# A handle refers to one node: it can be used as a dictionary key, and
# `document`/`id`/`parent` are properties.
child = root[0]
index = {root: "root", child: "child"}
assert index[document.root] == "root"
assert child.parent == root
assert child.document == document
assert isinstance(child.id, xml.NodeId)
# ANCHOR_END: handles

# ANCHOR: validation
# Validation is a whole-document call in both languages.
assert document.is_valid()
print(f"{len(root)} children")
# ANCHOR_END: validation
