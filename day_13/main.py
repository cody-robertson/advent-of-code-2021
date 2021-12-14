from enum import Enum
from typing import NamedTuple, Iterable


class Axis(Enum):
    X = "x"
    Y = "y"


class Fold(NamedTuple):
    axis: Axis
    location: int


class Point(NamedTuple):
    x: int
    y: int


def load_input(file_name: str):
    with open(file_name, "r") as input_file:
        lines = list(map(lambda x: x.strip(), input_file.readlines()))
    divider = lines.index("")
    points = [
        Point(int(x), int(y)) for x, y in [line.split(",") for line in lines[:divider]]
    ]
    folds = [
        Fold(Axis(axis), int(location))
        for axis, location in [
            line.split(" ")[-1].split("=") for line in lines[divider + 1 :]
        ]
    ]
    return points, folds


def print_points(points: Iterable[Point]):
    max_x = max([point.x for point in points])
    max_y = max([point.y for point in points])
    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for point in points:
        grid[point.y][point.x] = "#"
    for row in grid:
        print(" ".join(row))


def fold_points(points: Iterable[Point], folds: Iterable[Fold]) -> list[Point]:
    points_set = set(points)
    for fold in folds:
        next_points_set = set()
        for point in points_set:
            new_x, new_y = point.x, point.y
            if fold.axis == Axis.X and point.x > fold.location:
                new_x = fold.location - abs(point.x - fold.location)
            elif fold.axis == Axis.Y and point.y > fold.location:
                new_y = fold.location - abs(point.y - fold.location)
            next_points_set.add(Point(new_x, new_y))
        points_set = next_points_set
    return list(points_set)


if __name__ == "__main__":
    input_points, input_folds = load_input("input.txt")
    print("part 1: ", len(fold_points(input_points, input_folds[:1])))
    print("part 2:")
    print_points(fold_points(input_points, input_folds))
