"""Celestin - the 6 properties of a scheduling graph + cycle detection."""
from .graph import Graph


def validate_graph(graph: Graph, trace: bool = True) -> tuple[bool, list[str]]:
    """Check: single entry, single exit, no cycle (elimination of entry points),
    same weight on all outgoing edges of a vertex, zero weight on the entry's outgoing edges,
    no negative edge. Returns (is_scheduling_graph, list of reasons when it is not)."""
    raise NotImplementedError
