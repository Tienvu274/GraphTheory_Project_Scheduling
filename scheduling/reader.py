"""Mathurin - input, graph construction, value matrix display."""
from .graph import Graph, Task


def read_tasks(path: str) -> dict[int, Task]:
    """Read a constraint table: each line = id duration [predecessors...]."""
    raise NotImplementedError


def build_graph(tasks: dict[int, Task], trace: bool = True) -> Graph:
    """Build the value matrix with the fictitious tasks 0 and N+1.
    Rules: p -> t weight duration(p) for each predecessor p of t;
           0 -> t weight 0 if t has no predecessor;
           t -> N+1 weight duration(t) if t is nobody's predecessor.
    Trace: number of vertices, number of edges, then 'i -> j = w' edge by edge."""
    raise NotImplementedError


def format_matrix(graph: Graph) -> str:
    """Return the value matrix as an aligned string ('*' = no edge), built from memory."""
    raise NotImplementedError
