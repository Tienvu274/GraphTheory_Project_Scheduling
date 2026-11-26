"""Jiake - critical path(s)."""
from __future__ import annotations
from .graph import Graph


def find_critical_paths(graph: Graph, earliest: dict[int, int], latest: dict[int, int],
                        trace: bool = True) -> list[list[int]]:
    """All paths from 0 to N+1 made of zero-float vertices where E(i) + w(i, j) = E(j) for each edge."""
    start, end = graph.entry, graph.exit
    critical = {v for v in graph.vertices() if v in earliest and v in latest and earliest[v] == latest[v]}
    if trace:
        print(f"Critical tasks (float = 0): {sorted(critical)}")

    if start not in critical or end not in critical:
        if trace:
            print("No critical path found.")
        return []

    paths: list[list[int]] = []

    def dfs(u: int, path: list[int]) -> None:
        if u == end:
            paths.append(path[:])
            return
        for v in graph.successors(u):
            w = graph.matrix[u][v]
            if v in critical and w is not None and earliest[u] + w == earliest[v]:
                path.append(v)
                dfs(v, path)
                path.pop()

    dfs(start, [start])
    if trace:
        if paths:
            for p in paths:
                print("Critical path:", " -> ".join(map(str, p)))
        else:
            print("No critical path found.")
    return paths
