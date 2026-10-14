"""Book chapter "Thread safety" — the Python half.

The point of this file is that it terminates: one document, several threads writing and reading,
and no deadlock - because a document owns exactly one lock, no operation holds two, and the long
operations release the GIL.
"""

import concurrent.futures
import signal

import biodivine.xml_dom as xml

# ANCHOR: threads
document = xml.Document()
root = document.create_element("root")
document.set_root(root)


def writer(index: int) -> None:
    for item in range(25):
        node = document.create_element(f"item{index}_{item}")
        node.append_child(document.create_text("payload"))
        root.append_child(node)


def reader() -> int:
    total = 0
    for _ in range(50):
        total += len(root)
        document.write()
    return total


# ANCHOR_END: threads
# ANCHOR: readers
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    writers = [pool.submit(writer, index) for index in range(4)]
    readers = [pool.submit(reader) for _ in range(4)]
    for future in writers:
        future.result(timeout=30)
    assert all(future.result(timeout=30) > 0 for future in readers)

assert len(root) == 4 * 25
assert document.is_valid()
print(f"{len(root)} children, document valid")
# ANCHOR_END: readers

# ANCHOR: cancel
# Ctrl+C interrupts a long operation started on the main thread, and so does any
# other signal handler that raises. Here a timer does it (Unix only).
class TimedOut(Exception):
    pass


def on_timer(signum, frame):
    raise TimedOut()


large = xml.Document.parse("<root>" + "<item/>" * 200_000 + "</root>")
if hasattr(signal, "setitimer"):
    previous = signal.signal(signal.SIGALRM, on_timer)
    signal.setitimer(signal.ITIMER_REAL, 0.01)
    try:
        while True:
            large.validate()
    except TimedOut:
        print("validation interrupted")
    finally:
        signal.signal(signal.SIGALRM, previous)
# ANCHOR_END: cancel
