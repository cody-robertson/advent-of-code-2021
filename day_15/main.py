from queue import PriorityQueue
from typing import NamedTuple
from collections import defaultdict
from math import inf


class Point(NamedTuple):
    x: int
    y: int


def load_weights(file_name: str) -> list[list[int]]:
    weights = []
    with open(file_name, "r") as input_file:
        for line in input_file:
            weights.append(list(map(int, line.strip())))
    return weights


def expand_weights(weights):
    expanded_weights = []
    for i in range(len(weights) * 5):
        row = []
        for j in range(len(weights[0]) * 5):
            weight = (
                weights[i % len(weights)][j % len(weights)]
                + (i // len(weights))
                + (j // len(weights[0]))
            )
            divisible = weight // 10
            row.append(weight % 10 + divisible)
        expanded_weights.append(row)
    return expanded_weights


def dijkstra(weights):
    distances: dict[Point, float] = defaultdict(lambda: inf)
    queue = PriorityQueue()
    start = Point(0, 0)
    queue.put((0, start))
    distances[start] = 0

    while not queue.empty():
        distance, point = queue.get()
        if distance > distances[point]:
            continue
        adjacent_points = [
            Point(point.x + x_add, point.y + y_add)
            for x_add, y_add in ((1, 0), (-1, 0), (0, 1), (0, -1))
        ]
        for adjacent in adjacent_points:
            if 0 <= adjacent.y < len(weights) and 0 <= adjacent.x < len(
                weights[adjacent.y]
            ):
                if (
                    distances[point] + weights[adjacent.y][adjacent.x]
                    < distances[adjacent]
                ):
                    distances[adjacent] = (
                        distances[point] + weights[adjacent.y][adjacent.x]
                    )
                    queue.put((distances[adjacent], adjacent))
    destination = Point(len(weights[-1]) - 1, len(weights) - 1)
    return distances[destination]


if __name__ == "__main__":
    input_weights = load_weights("input.txt")
    print(dijkstra(input_weights))
    expanded = expand_weights(input_weights)
    print(dijkstra(expanded))
