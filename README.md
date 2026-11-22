# Graph Theory project - Scheduling (Team: Trung, Celestin, Jiake, Vuong, Mathurin)

Design agreement (point 4). Python 3.10+, no external library.

## Run
    python main.py                 # loop on the tables of tables/
    python -m tests.test_example   # shared tests (must pass before each push)

## Structure
    main.py                  main loop (pseudo-code of the subject)
    scheduling/graph.py      shared data structures Task and Graph  -> everybody
    scheduling/reader.py     read_tasks, build_graph, format_matrix -> Mathurin
    scheduling/validation.py validate_graph (6 properties, cycles)  -> Celestin
    scheduling/ranks.py      compute_ranks, compute_earliest        -> Trung
    scheduling/calendars.py  compute_latest, compute_floats         -> Vuong
    scheduling/critical.py   find_critical_paths                    -> Jiake
    tables/                  table01..table14 (teacher), example.txt (subject), invalid_negative.txt
    tests/test_example.py    expected results of the subject example, solved by hand

## Data structure
- `Task(id, duration, predecessors)`
- `Graph(n, tasks, matrix)`: vertices 0..n+1 (0 = alpha, n+1 = omega);
  `matrix[i][j]` = weight of i -> j, `None` if no edge. The matrix is the single source of truth
  (the subject requires displaying it from memory).
- Helpers: `vertices()`, `successors(v)`, `predecessors(v)`, `edges()`, `entry`, `exit`, `size`.

## Construction rules
- p -> t with weight duration(p) for each predecessor p of t
- 0 -> t with weight 0 if t has no predecessor
- t -> N+1 with weight duration(t) if t is nobody's predecessor

## Conventions
- Every function has a `trace: bool` parameter: True = print the execution trace, False = silent (tests).
- Dates, ranks and floats are `dict[int, int]` indexed by vertex.
- Each member works in their own file; `graph.py` and `main.py` are changed only after telling the team.
- One branch per member (`feature/<name>`), pull request to `main`, shared tests must pass.

## Expected results on the subject example
| Vertex   | 0 | 1 | 2 | 3 | 4 | 5 | 6  |
|----------|---|---|---|---|---|---|----|
| Rank     | 0 | 1 | 1 | 2 | 2 | 3 | 4  |
| Earliest | 0 | 0 | 0 | 1 | 2 | 6 | 11 |
| Latest   | 0 | 1 | 0 | 8 | 2 | 6 | 11 |
| Float    | 0 | 1 | 0 | 7 | 0 | 0 | 0  |

Critical path: 0 -> 2 -> 4 -> 5 -> 6 (length 11). Tables 01 and 12 contain a cycle.
