"""Book chapter "Getting started" — the Python half of the garbage-collection section."""

import biodivine.xml_dom as xml

document = xml.Document()
root = document.create_element("root")
document.set_root(root)
scratch = document.create_element("scratch")

# ANCHOR: collected
# A handle keeps its node alive; the document root keeps the tree it points at.
assert document.collect_garbage().collected == 0
assert document.node_count == 2

# Dropping the last handle of a detached node makes it collectable, and the
# slot is reused.
id = scratch.id
del scratch
assert document.collect_garbage().collected == 1
assert document.node_count == 1

# An id is a slot number, not a reference: it stops resolving once the slot
# has been reclaimed.
assert document.node(id) is None
# ANCHOR_END: collected

assert document.root is not None
assert document.is_valid()
