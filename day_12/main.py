from collections import defaultdict
from typing import Optional


def load_input(file_name: str):
    graph = defaultdict(set)
    with open(file_name) as input_file:
        for line in input_file:
            first, second = line.strip().split("-")
            graph[first].add(second)
            graph[second].add(first)
    return graph


def dfs_all_paths(
    graph: dict[str, set[str]],
    current: str = "start",
    path: Optional[set[str]] = None,
    has_visited_twice=False,
):
    if path is None:
        path = {current}

    if current == "end":
        return [path]

    paths = []
    children = graph[current]
    for child in children:
        if child != "start" and (
            child not in path or child.isupper() or not has_visited_twice
        ):
            has_visited_child_twice = has_visited_twice or (
                child in path and not child.isupper()
            )
            paths.extend(
                dfs_all_paths(
                    graph, child, path.union({child}), has_visited_child_twice
                )
            )
    return paths


if __name__ == "__main__":
    file_input = load_input("input.txt")
    print("part 1:", len(dfs_all_paths(file_input, has_visited_twice=True)))
    print("part 2:", len(dfs_all_paths(file_input)))
