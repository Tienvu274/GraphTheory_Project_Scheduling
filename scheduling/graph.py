"""Shared data structures. Everybody imports from here; do not change without telling the team."""
from dataclasses import dataclass


@dataclass
class Task:
    id: int                  # 1..N
    duration: int
    predecessors: list[int]  # as read in the .txt file


@dataclass
class Graph:
    n: int                          # number of real tasks -> vertices are 0..n+1 (0 = alpha, n+1 = omega)
    tasks: dict[int, Task]          # tasks read from the file (1..N)
    matrix: list[list[int | None]]  # (n+2) x (n+2): matrix[i][j] = weight of i -> j, None if no edge

    @property
    def size(self) -> int:
        return self.n + 2

    @property
    def entry(self) -> int:
        return 0

    @property
    def exit(self) -> int:
        return self.n + 1

    def vertices(self) -> range:
        return range(self.size)

    def successors(self, v: int) -> list[int]:
        return [j for j, w in enumerate(self.matrix[v]) if w is not None]

    def predecessors(self, v: int) -> list[int]:
        return [i for i in self.vertices() if self.matrix[i][v] is not None]

    def edges(self) -> list[tuple[int, int, int]]:
        return [(i, j, w) for i in self.vertices()
                for j, w in enumerate(self.matrix[i]) if w is not None]
