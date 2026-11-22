"""Vuong - latest dates and floats."""
from .graph import Graph


def compute_latest(graph: Graph, order: list[int], earliest: dict[int, int],
                   trace: bool = True) -> dict[int, int]:
    """Latest date of each vertex: L(N+1) = E(N+1), L(i) = min over successors j of L(j) - w(i, j)."""
    raise NotImplementedError


def compute_floats(earliest: dict[int, int], latest: dict[int, int],
                   trace: bool = True) -> dict[int, int]:
    """Total float of each vertex: L(i) - E(i)."""
    raise NotImplementedError
