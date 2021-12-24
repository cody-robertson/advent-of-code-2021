from collections import defaultdict
from enum import Enum
from typing import NamedTuple, Iterable
import matplotlib.pyplot as plt


class Command(Enum):
    OFF = "off"
    ON = "on"


class Instruction(NamedTuple):
    command: Command
    x_range: range
    y_range: range
    z_range: range


def load_input(file_name: str):
    instructions = []
    with open(file_name, "r") as input_file:
        for line in input_file:
            line = line.strip().split(" ")
            command = Command(line[0])
            ranges = line[1].split(",")
            x_range = list(map(int, ranges[0].lstrip("x=").split("..")))
            x_range = range(x_range[0], x_range[1] + 1)
            y_range = list(map(int, ranges[1].lstrip("y=").split("..")))
            y_range = range(y_range[0], y_range[1] + 1)
            z_range = list(map(int, ranges[2].lstrip("z=").split("..")))
            z_range = range(z_range[0], z_range[1] + 1)
            instructions.append(Instruction(command, x_range, y_range, z_range))
    return instructions


def cuboids_naive(instructions: list[Instruction]):
    cuboids = set()
    for instruction in instructions:
        if instruction.x_range.start < -50 or instruction.x_range.stop > 51:
            continue
        for x in instruction.x_range:
            for y in instruction.y_range:
                for z in instruction.z_range:
                    if instruction.command == Command.ON:
                        cuboids.add((x, y, z))
                    else:
                        cuboids.discard((x, y, z))
    return len(cuboids)


def volume(cube: tuple[range, range, range]):
    return max(
        (cube[0].stop - cube[0].start)
        * (cube[1].stop - cube[1].start)
        * (cube[2].stop - cube[2].start),
        0,
    )


def get_intersection(
    cube_1: tuple[range, range, range], cube_2: tuple[range, range, range]
) -> tuple[bool, tuple[range, range, range]]:
    overlaps = [range(0), range(0), range(0)]
    overlaps[0] = range(
        max(cube_1[0].start, cube_2[0].start), min(cube_1[0].stop, cube_2[0].stop)
    )
    overlaps[1] = range(
        max(cube_1[1].start, cube_2[1].start), min(cube_1[1].stop, cube_2[1].stop)
    )
    overlaps[2] = range(
        max(cube_1[2].start, cube_2[2].start), min(cube_1[2].stop, cube_2[2].stop)
    )
    if (
        (overlaps[0].stop - overlaps[0].start) <= 0
        or (overlaps[1].stop - overlaps[1].start) <= 0
        or (overlaps[2].stop - overlaps[2].start) <= 0
    ):
        return False, (overlaps[0], overlaps[1], overlaps[2])
    return True, (overlaps[0], overlaps[1], overlaps[2])


def cuboids_volume_tracking(instructions: list[Instruction]):
    cuboids: dict[tuple[range, range, range], int] = defaultdict(lambda: 0)
    for instruction in instructions:
        # if instruction.x_range.start >= -50 and instruction.x_range.stop < 51:
        next_cuboids = cuboids.copy()
        instruction_cuboid = (
            instruction.x_range,
            instruction.y_range,
            instruction.z_range,
        )
        for cuboid, cuboid_value in cuboids.items():
            has_intersection, intersection = get_intersection(
                cuboid, instruction_cuboid
            )
            if has_intersection:
                next_cuboids[intersection] -= cuboid_value
        if instruction.command == Command.ON:
            next_cuboids[instruction_cuboid] += 1
        cuboids = next_cuboids.copy()
        for cuboid, cuboid_value in cuboids.items():
            if cuboid_value == 0 or volume(cuboid) == 0:
                del next_cuboids[cuboid]
        cuboids = next_cuboids
    total = 0
    for cuboid, cuboid_value in cuboids.items():
        total += volume(cuboid) * cuboid_value
    return total


if __name__ == "__main__":
    input_instructions = load_input("input.txt")
    print(cuboids_naive(input_instructions))
    print(cuboids_volume_tracking(input_instructions))
