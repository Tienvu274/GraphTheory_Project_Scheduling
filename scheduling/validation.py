"""Celestin - the 6 properties of a scheduling graph + cycle detection.

A graph can be used for scheduling only if:
  1. it has a single entry point (vertex without predecessor),
  2. it has a single exit point (vertex without successor),
  3. it has no cycle,
  4. all the outgoing edges of a vertex have the same weight,
  5. the outgoing edges of the entry point have a weight of 0,
  6. it has no negative edge.
"""
from .graph import Graph


def _fmt(vertices) -> str:
    """'1 2 3' for a list of vertices, 'None' for an empty list."""
    return " ".join(str(v) for v in vertices) if vertices else "None"


def entry_points(graph: Graph, among=None) -> list[int]:
    """Vertices without predecessor (inside `among`, the whole graph by default)."""
    among = set(graph.vertices()) if among is None else set(among)
    return sorted(v for v in among
                  if not any(p in among for p in graph.predecessors(v)))


def exit_points(graph: Graph) -> list[int]:
    """Vertices without successor."""
    return [v for v in graph.vertices() if not graph.successors(v)]


def eliminate_entry_points(graph: Graph, trace: bool = True) -> tuple[list[list[int]], list[int]]:
    """Cycle detection by the method of eliminating entry points (course method).

    At each step, the entry points of the remaining graph are removed.
    Returns (waves, remaining):
      - waves[k] = vertices removed at step k (= vertices of rank k when there is no cycle),
      - remaining = vertices that could never be removed: empty <=> no cycle.
    """
    remaining = list(graph.vertices())
    waves: list[list[int]] = []
    if trace:
        print("* Detecting a cycle")
        print("* Method of eliminating entry points")
    while remaining:
        entries = entry_points(graph, remaining)
        if trace:
            print(f"Entry points: {_fmt(entries)}")
        if not entries:          # every remaining vertex has a predecessor: there is a cycle
            break
        waves.append(entries)
        remaining = [v for v in remaining if v not in entries]
        if trace:
            print("Eliminating entry points")
            print(f"Remaining vertices: {_fmt(remaining)}")
    return waves, remaining


def validate_graph(graph: Graph, trace: bool = True) -> tuple[bool, list[str]]:
    """Check the 6 properties of a scheduling graph.

    Returns (is_scheduling_graph, reasons) where `reasons` lists every property
    that is not satisfied (empty list when the graph is valid).
    """
    reasons: list[str] = []

    def say(text: str) -> None:
        if trace:
            print(text)

    if trace:
        print("\n* Checking the properties of a scheduling graph")

    # 1. Single entry point
    entries = entry_points(graph)
    if len(entries) == 1:
        say(f"There is one entry point, {entries[0]}")
    else:
        reasons.append(f"{len(entries)} entry points ({_fmt(entries)}) instead of one")
        say(f"There are {len(entries)} entry points: {_fmt(entries)}")

    # 2. Single exit point
    exits = exit_points(graph)
    if len(exits) == 1:
        say(f"There is one exit point, {exits[0]}")
    else:
        reasons.append(f"{len(exits)} exit points ({_fmt(exits)}) instead of one")
        say(f"There are {len(exits)} exit points: {_fmt(exits)}")

    # 3. No cycle
    _, remaining = eliminate_entry_points(graph, trace)
    if remaining:
        reasons.append(f"there is a cycle (vertices that cannot be eliminated: {_fmt(remaining)})")
        say(f"-> There is a cycle: vertices {_fmt(remaining)} cannot be eliminated "
            "(the cycle and the vertices that depend on it)")
    else:
        say("-> There is no cycle")

    # 4. Same weight for all the outgoing edges of each vertex
    different = []
    for v in graph.vertices():
        weights = {graph.matrix[v][s] for s in graph.successors(v)}
        if len(weights) > 1:
            different.append(v)
            say(f"The outgoing edges of vertex {v} have different weights: "
                f"{', '.join(f'{v}->{s} = {graph.matrix[v][s]}' for s in graph.successors(v))}")
    if different:
        reasons.append(f"outgoing edges with different weights for vertex(es) {_fmt(different)}")
    else:
        say("The values of outgoing edges for each vertex are the same")

    # 5. Outgoing edges of the entry point have a weight of 0
    not_zero = [(e, s, graph.matrix[e][s]) for e in entries
                for s in graph.successors(e) if graph.matrix[e][s] != 0]
    if not_zero:
        reasons.append("outgoing edges of the entry point with a non-zero weight: "
                       + ", ".join(f"{e}->{s} = {w}" for e, s, w in not_zero))
        for e, s, w in not_zero:
            say(f"The edge {e}->{s} has a weight {w} (should be 0)")
    elif entries:
        out = [f"{e}->{s}" for e in entries for s in graph.successors(e)]
        say(f"The edges {' and '.join(out) if len(out) <= 2 else ', '.join(out)} have a weight 0")

    # 6. No negative edge
    negative = [(i, j, w) for i, j, w in graph.edges() if w < 0]
    if negative:
        reasons.append("negative edges: " + ", ".join(f"{i}->{j} = {w}" for i, j, w in negative))
        for i, j, w in negative:
            say(f"The edge {i}->{j} has a negative weight {w}")
    else:
        say("There are no negative-weight edges")

    ok = not reasons
    say("-> This is a scheduling graph" if ok else "-> This is NOT a scheduling graph")
    return ok, reasons
