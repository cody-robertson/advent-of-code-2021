from collections import defaultdict
from typing import Optional


def load_input(file_name: str):
    graph = defaultdict(list)
    with open(file_name) as input_file:
        for line in input_file:
            first, second = line.strip().split("-")
            graph[first].append(second)
            graph[second].append(first)
    return graph


def dfs_all_paths(graph: dict[str, list[str]], path: Optional[list[str]] = None):
    if path is None:
        path = ["start"]
    previous = path[-1]

    if previous == "end":
        return [path]

    paths = []
    children = graph[previous]
    for child in children:
        if child != "start" and child not in path or child.isupper():
            paths.extend(dfs_all_paths(graph, path + [child]))
    return paths


def dfs_all_paths_additional_trip(
    graph: dict[str, list[str]],
    path: Optional[list[str]] = None,
    has_visited_twice=False,
):
    if path is None:
        path = ["start"]
    previous = path[-1]

    if previous == "end":
        return [path]

    paths = []
    children = graph[previous]
    for child in children:
        child_occurrences = len([item for item in path if item == child])
        if child != "start" and (child_occurrences < 1 or child.isupper()):
            paths.extend(
                dfs_all_paths_additional_trip(graph, path + [child], has_visited_twice)
            )
        elif child != "start" and child_occurrences == 1 and not has_visited_twice:
            paths.extend(dfs_all_paths_additional_trip(graph, path + [child], True))
    return paths


if __name__ == "__main__":
    file_input = load_input("input.txt")
    print(file_input)
    print(len(dfs_all_paths(file_input)))
    print(len(dfs_all_paths_additional_trip(file_input)))
