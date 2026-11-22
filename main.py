"""Main loop - follows the pseudo-code of the subject."""
import os

from scheduling.reader import read_tasks, build_graph, format_matrix
from scheduling.validation import validate_graph
from scheduling.ranks import compute_ranks, compute_earliest
from scheduling.calendars import compute_latest, compute_floats
from scheduling.critical import find_critical_paths

TABLES_DIR = os.path.join(os.path.dirname(__file__), "tables")


def choose_table() -> str | None:
    files = sorted(f for f in os.listdir(TABLES_DIR) if f.endswith(".txt"))
    print("\nAvailable constraint tables:")
    for k, name in enumerate(files, 1):
        print(f"  {k:2d}. {name}")
    choice = input("Table number (or a file path, empty = quit): ").strip()
    if not choice:
        return None
    if choice.isdigit() and 1 <= int(choice) <= len(files):
        return os.path.join(TABLES_DIR, files[int(choice) - 1])
    return choice


def run(path: str) -> None:
    tasks = read_tasks(path)                    # 1. read and store in memory
    graph = build_graph(tasks, trace=True)      # 2. build the graph
    print(format_matrix(graph))                 #    display the value matrix from memory
    ok, reasons = validate_graph(graph, trace=True)   # 3. check the 6 properties
    if not ok:
        print("-> This is not a scheduling graph:", "; ".join(reasons))
        return
    ranks, order = compute_ranks(graph, trace=True)               # 4. ranks
    earliest = compute_earliest(graph, order, trace=True)         # 5. calendars and floats
    latest = compute_latest(graph, order, earliest, trace=True)
    compute_floats(earliest, latest, trace=True)
    find_critical_paths(graph, earliest, latest, trace=True)      # 6. critical path(s)


def main() -> None:
    while True:
        path = choose_table()
        if path is None:
            break
        try:
            run(path)
        except FileNotFoundError:
            print("File not found:", path)
        except NotImplementedError as e:
            print("Module not written yet:", e)
    print("Bye.")


if __name__ == "__main__":
    main()
