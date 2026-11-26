"""Tests of validate_graph (Celestin) on small hand-made graphs, one per property.
They do not depend on read_tasks/build_graph.   Run:  python -m tests.test_validation"""
from scheduling.graph import Graph
from scheduling.validation import validate_graph, eliminate_entry_points

X = None


def g(matrix):
    return Graph(n=len(matrix) - 2, tasks={}, matrix=matrix)


# Subject example (0 -> 1, 2 ... -> 6): valid
VALID = g([[X, 0, 0, X, X, X, X],
           [X, X, X, 1, 1, X, X],
           [X, X, X, X, 2, 2, X],
           [X, X, X, X, X, X, 3],
           [X, X, X, X, X, 4, X],
           [X, X, X, X, X, X, 5],
           [X, X, X, X, X, X, X]])

TWO_ENTRIES = g([[X, 0, X, X],      # 2 has no predecessor
                 [X, X, X, 1],
                 [X, X, X, 2],
                 [X, X, X, X]])

TWO_EXITS = g([[X, 0, 0, X],        # 2 has no successor
               [X, X, X, 1],
               [X, X, X, X],
               [X, X, X, X]])

CYCLE = g([[X, 0, X, X, X],         # 1 -> 2 -> 3 -> 1
           [X, X, 1, X, X],
           [X, X, X, 2, X],
           [X, 3, X, X, 3],
           [X, X, X, X, X]])

DIFFERENT_WEIGHTS = g([[X, 0, 0, X, X],
                       [X, X, X, 1, 2],   # 1 -> 3 = 1 but 1 -> 4 = 2
                       [X, X, X, 2, X],
                       [X, X, X, X, 3],
                       [X, X, X, X, X]])

ENTRY_NOT_ZERO = g([[X, 5, X],     # 0 -> 1 = 5
                    [X, X, 1],
                    [X, X, X]])

NEGATIVE = g([[X, 0, X, X],
              [X, X, -2, X],
              [X, X, X, 1],
              [X, X, X, X]])


def check(graph, expected_ok, expected_word=None):
    ok, reasons = validate_graph(graph, trace=False)
    assert ok == expected_ok, reasons
    if expected_word:
        assert any(expected_word in r for r in reasons), reasons


def test_all():
    check(VALID, True)
    check(TWO_ENTRIES, False, "entry points")
    check(TWO_EXITS, False, "exit points")
    check(CYCLE, False, "cycle")
    check(DIFFERENT_WEIGHTS, False, "different weights")
    check(ENTRY_NOT_ZERO, False, "non-zero")
    check(NEGATIVE, False, "negative")
    waves, remaining = eliminate_entry_points(VALID, trace=False)
    assert waves == [[0], [1, 2], [3, 4], [5], [6]] and remaining == []   # waves = ranks
    assert eliminate_entry_points(CYCLE, trace=False)[1] == [1, 2, 3, 4]


if __name__ == "__main__":
    test_all()
    print("All validation tests passed.")
