import operator
from functools import reduce


def load_input(file_name):
    height_map: list[list[int]] = []
    with open(file_name, "r") as input_file:
        for line in input_file:
            height_map.append([int(v) for v in line.strip()])
    return height_map


def is_location_lowest(height_map, i, j):
    location_value = height_map[i][j]
    for i_add, j_add in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if 0 <= i + i_add < len(height_map) and 0 <= j + j_add < len(
            height_map[i + i_add]
        ):
            if location_value >= height_map[i + i_add][j + j_add]:
                return False
    return True


def part_1(height_map: list[list[int]]):
    risk_level = 0
    for i, row in enumerate(height_map):
        for j, location in enumerate(row):
            if is_location_lowest(height_map, i, j):
                risk_level += location + 1
    return risk_level


def basin_flood_fill(height_map, i, j, traversed: set[tuple[int, int]]):
    invalid_index = i < 0 or i >= len(height_map) or j < 0 or j >= len(height_map[i])
    if invalid_index or (i, j) in traversed or height_map[i][j] == 9:
        return traversed

    traversed.add((i, j))
    traversed = basin_flood_fill(height_map, i + 1, j, traversed)
    traversed = basin_flood_fill(height_map, i - 1, j, traversed)
    traversed = basin_flood_fill(height_map, i, j + 1, traversed)
    traversed = basin_flood_fill(height_map, i, j - 1, traversed)
    return traversed


def part_2(height_map: list[list[int]]):
    basins = []
    total_traversed = set()
    for i, row in enumerate(height_map):
        for j, location in enumerate(height_map[i]):
            if (i, j) not in total_traversed:
                found = basin_flood_fill(height_map, i, j, set())
                if len(found) > 0:
                    basins.append(found)
                    total_traversed = total_traversed.union(found)
    basins.sort(key=len, reverse=True)
    max_lengths = [len(basin) for basin in basins[:3]]
    return reduce(operator.mul, max_lengths, 1)


if __name__ == "__main__":
    input_map = load_input("input.txt")
    for input_map_line in input_map:
        print(input_map_line)
    print(part_1(input_map))
    print(part_2(input_map))
