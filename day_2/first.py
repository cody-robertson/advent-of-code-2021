from enum import Enum
from typing import NamedTuple


class Direction(Enum):
    Forward = "forward"
    Down = "down"
    Up = "up"


class Instruction(NamedTuple):
    direction: Direction
    value: int


def parse_instructions_from_input(file_name: str) -> list[Instruction]:
    instructions = []
    with open(file_name, "r") as input_file:
        for line in input_file:
            direction, value = line.lower().strip().split(" ")
            instructions.append(
                Instruction(direction=Direction(direction), value=int(value))
            )
    return instructions


class Submarine:
    def __init__(self, horizontal: int = 0, depth: int = 0):
        self.horizontal = horizontal
        self.depth = depth

    def follow_instructions(self, instructions: list[Instruction]):
        for instruction in instructions:
            self.follow_instruction(instruction.direction, instruction.value)

    def follow_instruction(self, direction: Direction, value: int):
        if direction == Direction.Forward:
            self.horizontal += value
        elif direction == Direction.Down:
            self.depth += value
        elif direction == Direction.Up:
            self.depth -= value
        else:
            return ValueError("Direction not supported")

    def get_product(self):
        return self.horizontal * self.depth


if __name__ == "__main__":
    instructions = parse_instructions_from_input("input.txt")
    sub = Submarine()
    sub.follow_instructions(instructions)
    print(sub.horizontal, sub.depth)
    print(sub.get_product())
