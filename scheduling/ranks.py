"""Trung - ranks, topological order, earliest dates."""
from .graph import Graph


def compute_ranks(graph: Graph, trace: bool = True) -> tuple[dict[int, int], list[int]]:
    """Return (rank of each vertex, vertices sorted by increasing rank). Call only if there is no cycle."""
    raise NotImplementedError


def compute_earliest(graph: Graph, order: list[int], trace: bool = True) -> dict[int, int]:
    """Earliest date of each vertex: E(0) = 0, E(j) = max over predecessors i of E(i) + w(i, j)."""
    raise NotImplementedError
