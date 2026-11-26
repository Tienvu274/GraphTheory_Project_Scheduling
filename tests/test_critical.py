"""Unit & edge-case tests for scheduling.critical.find_critical_paths.
Run from the project folder:  python3 -m tests.test_critical
"""
from __future__ import annotations
import io
from contextlib import redirect_stdout

from scheduling.graph import Graph, Task
from scheduling.critical import find_critical_paths


def _make_graph(durations: dict[int, int], edges: list[tuple[int, int, int]]) -> Graph:
    n = len(durations)
    size = n + 2
    matrix: list[list[int | None]] = [[None] * size for _ in range(size)]
    preds: dict[int, list[int]] = {t: [] for t in durations}
    for u, v, w in edges:
        matrix[u][v] = w
        if u != 0 and v != n + 1:
            preds[v].append(u)
    tasks = {t: Task(id=t, duration=d, predecessors=preds[t]) for t, d in durations.items()}
    return Graph(n=n, tasks=tasks, matrix=matrix)


def test_subject_example() -> None:
    """Subject example (tables/example.txt) using hand-computed earliest & latest."""
    durations = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
    edges = [
        (0, 1, 0), (0, 2, 0),
        (1, 3, 1), (1, 4, 1),
        (2, 4, 2), (2, 5, 2),
        (3, 6, 3),
        (4, 5, 4),
        (5, 6, 5),
    ]
    g = _make_graph(durations, edges)
    earliest = {0: 0, 1: 0, 2: 0, 3: 1, 4: 2, 5: 6, 6: 11}
    latest = {0: 0, 1: 1, 2: 0, 3: 8, 4: 2, 5: 6, 6: 11}
    assert find_critical_paths(g, earliest, latest, trace=False) == [[0, 2, 4, 5, 6]]


def test_single_critical_path() -> None:
    """Edge case 1: single critical path among two branches of different lengths."""
    # 0 -> 1(5) -> 3(2) -> 4 (total 7) vs 0 -> 2(3) -> 3(2) -> 4 (total 5)
    g = _make_graph(
        {1: 5, 2: 3, 3: 2},
        [(0, 1, 0), (0, 2, 0), (1, 3, 5), (2, 3, 3), (3, 4, 2)],
    )
    earliest = {0: 0, 1: 0, 2: 0, 3: 5, 4: 7}
    latest = {0: 0, 1: 0, 2: 2, 3: 5, 4: 7}
    assert find_critical_paths(g, earliest, latest, trace=False) == [[0, 1, 3, 4]]


def test_multiple_critical_paths() -> None:
    """Edge case 2: two branches of equal longest length -> both paths returned."""
    # 0 -> 1(4) -> 3(2) -> 4 (total 6) and 0 -> 2(4) -> 3(2) -> 4 (total 6)
    g = _make_graph(
        {1: 4, 2: 4, 3: 2},
        [(0, 1, 0), (0, 2, 0), (1, 3, 4), (2, 3, 4), (3, 4, 2)],
    )
    earliest = {0: 0, 1: 0, 2: 0, 3: 4, 4: 6}
    latest = {0: 0, 1: 0, 2: 0, 3: 4, 4: 6}
    assert find_critical_paths(g, earliest, latest, trace=False) == [
        [0, 1, 3, 4],
        [0, 2, 3, 4],
    ]


def test_all_tasks_critical() -> None:
    """Edge case 3: linear chain 0 -> 1 -> 2 -> 3 -> 4 where every task is critical."""
    g = _make_graph(
        {1: 2, 2: 4, 3: 3},
        [(0, 1, 0), (1, 2, 2), (2, 3, 4), (3, 4, 3)],
    )
    earliest = {0: 0, 1: 0, 2: 2, 3: 6, 4: 9}
    latest = {0: 0, 1: 0, 2: 2, 3: 6, 4: 9}
    assert find_critical_paths(g, earliest, latest, trace=False) == [[0, 1, 2, 3, 4]]


def test_single_task() -> None:
    """Edge case 4: single real task 0 -> 1 -> 2."""
    g = _make_graph({1: 5}, [(0, 1, 0), (1, 2, 5)])
    earliest = {0: 0, 1: 0, 2: 5}
    latest = {0: 0, 1: 0, 2: 5}
    assert find_critical_paths(g, earliest, latest, trace=False) == [[0, 1, 2]]


def test_non_tight_edge_between_critical_tasks() -> None:
    """Edge case 5: 1 and 2 are both critical (float=0), but edge 1->2 is NOT tight."""
    # 1(2), 3(6), 2(3): edges 0->1(0), 1->3(2), 1->2(2), 3->2(6), 2->4(3)
    # E = {0:0, 1:0, 3:2, 2:8, 4:11}, L = {0:0, 1:0, 3:2, 2:8, 4:11}
    # Edge 1->2 has E(1) + 2 = 2 != 8 = E(2), so [0, 1, 2, 4] must NOT be returned.
    g = _make_graph(
        {1: 2, 2: 3, 3: 6},
        [(0, 1, 0), (1, 2, 2), (1, 3, 2), (3, 2, 6), (2, 4, 3)],
    )
    earliest = {0: 0, 1: 0, 2: 8, 3: 2, 4: 11}
    latest = {0: 0, 1: 0, 2: 8, 3: 2, 4: 11}
    assert find_critical_paths(g, earliest, latest, trace=False) == [[0, 1, 3, 2, 4]]


def test_trace_flag() -> None:
    """trace=True prints output; trace=False is silent."""
    g = _make_graph({1: 5}, [(0, 1, 0), (1, 2, 5)])
    earliest = {0: 0, 1: 0, 2: 5}
    latest = {0: 0, 1: 0, 2: 5}

    buf_silent = io.StringIO()
    with redirect_stdout(buf_silent):
        find_critical_paths(g, earliest, latest, trace=False)
    assert buf_silent.getvalue() == ""

    buf_trace = io.StringIO()
    with redirect_stdout(buf_trace):
        find_critical_paths(g, earliest, latest, trace=True)
    out = buf_trace.getvalue()
    assert "Critical tasks (float = 0): [0, 1, 2]" in out
    assert "Critical path: 0 -> 1 -> 2" in out


if __name__ == "__main__":
    test_subject_example()
    test_single_critical_path()
    test_multiple_critical_paths()
    test_all_tasks_critical()
    test_single_task()
    test_non_tight_edge_between_critical_tasks()
    test_trace_flag()
    print("All critical path tests passed.")
