"""Book chapter "Traversing and editing" — the Python half."""

import biodivine.xml_dom as xml

document = xml.Document.parse("<root><a/><b/><c/></root>")
root = document.root

# ANCHOR: handles
# Handles compare by node, not by Python object identity.
a = root.child_elements()[0]
assert a == root.child_elements()[0]
assert a is not root.child_elements()[0]
assert a.ptr_eq(root.child_elements()[0])
# ANCHOR_END: handles

# ANCHOR: traversal
# Traversal, with the Pythonic protocols.
assert len(root) == 3
assert [child.local_name for child in root] == ["a", "b", "c"]
assert root[0].local_name == "a"
assert root[-1].local_name == "c"
assert a.next_sibling.local_name == "b"
assert root.last_child.local_name == "c"
assert a.index_in_parent == 0
# ANCHOR_END: traversal

# ANCHOR: editing
# Structural editing is atomic and cycle-safe.
x = document.create_element("x")
root.insert_child(1, x)
assert [child.local_name for child in root] == ["a", "x", "b", "c"]
x.detach()
root.insert_after(a, x)
assert len(root) == 4
# ANCHOR_END: editing

# ANCHOR: replace
# Replacing leaves the old node detached but alive.
replacement = document.create_element("y")
old = x.replace_with(replacement)
assert not old.is_attached
assert old.local_name == "x"
# ANCHOR_END: replace

# ANCHOR: errors
# Cycles and foreign documents raise instead of corrupting anything.
try:
    root.append_child(root)
except xml.XmlDocumentError:
    pass
else:  # pragma: no cover - only if the error handling regressed
    raise AssertionError("attaching an ancestor must fail")
other = xml.Document()
try:
    root.append_child(other.create_element("f"))
except xml.XmlDocumentError:
    pass
else:  # pragma: no cover
    raise AssertionError("attaching a foreign node must fail")
# ANCHOR_END: errors

# ANCHOR: detached
# A fresh node is detached (but already belongs to a document) until it is attached.
detached = document.create_element("d")
assert not detached.is_attached
root.append_child(detached)
assert detached.is_attached
# ANCHOR_END: detached

# ANCHOR: clones
# Clones: `deep_clone` copies the subtree, `shallow_clone` only the node.
deep = root.deep_clone()
assert len(deep) == len(root)
assert not deep.is_attached
assert len(root.shallow_clone()) == 0
# ANCHOR_END: clones

# ANCHOR: import
# Copying into another document is the sanctioned way to move a tree between documents.
target = xml.Document()
wrapper = target.create_element("wrapper")
target.set_root(wrapper)
wrapper.append_child(root.deep_clone_into(target))
assert target.is_valid()
print(document.write())
# ANCHOR_END: import
