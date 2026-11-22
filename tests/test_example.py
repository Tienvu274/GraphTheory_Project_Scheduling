"""Shared test: the example of the subject (tables/example.txt), solved by hand.
Run from the project folder:  python -m tests.test_example"""
import os
from scheduling.reader import read_tasks, build_graph
from scheduling.validation import validate_graph
from scheduling.ranks import compute_ranks, compute_earliest
from scheduling.calendars import compute_latest, compute_floats
from scheduling.critical import find_critical_paths

HERE = os.path.dirname(__file__)
TABLES = os.path.join(HERE, "..", "tables")

EXPECTED_EDGES = {(0, 1, 0), (0, 2, 0), (1, 3, 1), (1, 4, 1), (2, 4, 2),
                  (2, 5, 2), (3, 6, 3), (4, 5, 4), (5, 6, 5)}          # 7 vertices, 9 edges (subject)
EXPECTED_RANKS = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4}
EXPECTED_EARLIEST = {0: 0, 1: 0, 2: 0, 3: 1, 4: 2, 5: 6, 6: 11}
EXPECTED_LATEST = {0: 0, 1: 1, 2: 0, 3: 8, 4: 2, 5: 6, 6: 11}
EXPECTED_FLOATS = {0: 0, 1: 1, 2: 0, 3: 7, 4: 0, 5: 0, 6: 0}
EXPECTED_CRITICAL = [[0, 2, 4, 5, 6]]


def test_example():
    g = build_graph(read_tasks(os.path.join(TABLES, "example.txt")), trace=False)
    assert set(g.edges()) == EXPECTED_EDGES
    ok, reasons = validate_graph(g, trace=False)
    assert ok, reasons
    ranks, order = compute_ranks(g, trace=False)
    assert ranks == EXPECTED_RANKS
    e = compute_earliest(g, order, trace=False)
    assert e == EXPECTED_EARLIEST
    l = compute_latest(g, order, e, trace=False)
    assert l == EXPECTED_LATEST
    assert compute_floats(e, l, trace=False) == EXPECTED_FLOATS
    assert find_critical_paths(g, e, l, trace=False) == EXPECTED_CRITICAL


def test_invalid():
    for name in ("table01.txt", "table12.txt", "invalid_negative.txt"):   # 2 cycles, 1 negative duration
        g = build_graph(read_tasks(os.path.join(TABLES, name)), trace=False)
        ok, reasons = validate_graph(g, trace=False)
        assert not ok and reasons, name


if __name__ == "__main__":
    test_example()
    test_invalid()
    print("All shared tests passed.")
