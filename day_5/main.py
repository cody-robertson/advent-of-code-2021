from typing import NamedTuple
from math import gcd
from collections import defaultdict


class Point(NamedTuple):
    x: int
    y: int


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    @property
    def slope(self):
        numerator = self.end.y - self.start.y
        denominator = self.end.x - self.start.x
        common = gcd(numerator, denominator)
        return numerator // common, denominator // common

    def get_points(self):
        points = {self.start, self.end}
        delta_y, delta_x = self.slope
        current_x, current_y = self.start.x + delta_x, self.start.y + delta_y
        while (
            (current_x < self.end.x or delta_x <= 0)
            and (current_x > self.end.x or delta_x >= 0)
            and (current_y < self.end.y or delta_y <= 0)
            and (current_y > self.end.y or delta_y >= 0)
        ):
            points.add(Point(current_x, current_y))
            current_x += delta_x
            current_y += delta_y
        return points

    def __str__(self):
        return f"start: {self.start}, end: {self.end}"

    def __repr__(self):
        return f"start: {self.start}, end: {self.end}"


def load_input(file_name):
    lines = []
    with open(file_name, "r") as input_file:
        for line in input_file:
            start, end = line.strip().split(" -> ")
            start, end = list(map(int, start.split(","))), list(
                map(int, end.split(","))
            )
            lines.append(Line(Point(start[0], start[1]), Point(end[0], end[1])))
    return lines


def count_intersections(lines: list[Line]):
    points = defaultdict(lambda: 0)
    for line in lines:
        for point in line.get_points():
            points[point] += 1
    return len([point for point in points.values() if point > 1])


if __name__ == "__main__":
    input_lines = load_input("input.txt")
    only_horizontal_or_vertical = [line for line in input_lines if 0 in line.slope]
    print(count_intersections(only_horizontal_or_vertical))
    print(count_intersections(input_lines))
