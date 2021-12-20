import json
from typing import Union
from math import floor, ceil
from copy import deepcopy


def load_input(file_name: str):
    lines = []
    with open(file_name, "r") as input_file:
        for line in input_file:
            lines.append(json.loads(line))
    return lines


def add_left(item: Union[list, int], value: int):
    if value is None:
        return True, item
    if isinstance(item, int):
        return True, item + value
    added, new_value = add_left(item[1], value)
    if added:
        item[1] = new_value
        return True, item
    added, new_value = add_left(item[0], value)
    if added:
        item[0] = new_value
        return True, item
    return False, item


def add_right(item: Union[list, int], value: int):
    if value is None:
        return True, item
    if isinstance(item, int):
        return True, item + value
    added, new_value = add_right(item[0], value)
    if added:
        item[0] = new_value
        return True, item
    added, new_value = add_right(item[1], value)
    if added:
        item[1] = new_value
        return True, item
    return False, item


def explode(item: Union[list, int], depth: int = 0):
    simplified = False
    additions = None
    if isinstance(item, list):
        if not simplified and depth > 4:
            simplified = True
            additions = (item[0], item[1])
            item = 0
            # print("exploded", additions)
        if not simplified:
            for i, value in enumerate(item):
                simplified, new_value, additions = explode(value, depth + 1)
                item[i] = new_value
                if additions is not None:
                    if i == 0:
                        added, new_value = add_right(item[1], additions[1])
                        item[1] = new_value
                        if added:
                            additions = (additions[0], None)
                    elif i == 1:
                        added, new_value = add_left(item[0], additions[0])
                        item[0] = new_value
                        if added:
                            additions = (None, additions[1])
                if not simplified and depth == 4:
                    simplified = True
                    additions = (item[0], item[1])
                    item = 0
                    # print("exploded", additions)
                if simplified:
                    break
    return simplified, item, additions


def split(item: Union[list, int], depth: int = 0):
    simplified = False
    additions = None
    if isinstance(item, list):
        for i, value in enumerate(item):
            simplified, new_value, additions = split(value, depth + 1)
            item[i] = new_value
            if simplified:
                break
    elif isinstance(item, int):
        if item >= 10:
            simplified = True
            item = [floor(item / 2), ceil(item / 2)]
            # print("split", item)
    return simplified, item, additions


def simplify(item: list):
    simplified, result, additions = explode(item)
    if simplified:
        return simplified, result, additions
    return split(item)


def add_snailnumbers(first, second):
    result = [first] + [second]
    # print(result)
    simplified = True
    while simplified:
        simplified, result, additions = simplify(result)
        # print(additions)
        # print(result)
    return result


def calculate_magnitude(value: Union[list, int]) -> int:
    if isinstance(value, int):
        return value
    return 3 * calculate_magnitude(value[0]) + 2 * calculate_magnitude(value[1])


def part_1(numbers: list):
    current = numbers[0]
    for number in numbers[1:]:
        print(f"{current} + {number}")
        current = add_snailnumbers(current, number)
        print(f"= {current}")
    return calculate_magnitude(current)


def part_2(numbers: list):
    max_magnitude = -1
    for i, first in enumerate(deepcopy(numbers)):
        for j, second in enumerate(deepcopy(numbers)):
            if i != j:
                result = add_snailnumbers(deepcopy(first), deepcopy(second))
                magnitude = calculate_magnitude(result)
                max_magnitude = max(magnitude, max_magnitude)
    return max_magnitude


if __name__ == "__main__":
    input_numbers = load_input("input.txt")
    print(part_1(deepcopy(input_numbers)))
    print(part_2(deepcopy(input_numbers)))
