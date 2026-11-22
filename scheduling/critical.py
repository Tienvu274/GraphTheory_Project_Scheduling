"""Jiake - critical path(s)."""
from .graph import Graph


def find_critical_paths(graph: Graph, earliest: dict[int, int], latest: dict[int, int],
                        trace: bool = True) -> list[list[int]]:
    """All paths from 0 to N+1 made of zero-float vertices where E(i) + w(i, j) = E(j) for each edge."""
    raise NotImplementedError
