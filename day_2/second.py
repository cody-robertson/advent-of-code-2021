from day_2.first import parse_instructions_from_input, Submarine, Direction


class SubmarineWithAim(Submarine):
    def __init__(self, horizontal: int = 0, depth: int = 0, aim: int = 0):
        self.horizontal = horizontal
        self.depth = depth
        self.aim = aim

    def follow_instruction(self, direction: Direction, value: int):
        if direction == Direction.Forward:
            self.horizontal += value
            self.depth += self.aim * value
        elif direction == Direction.Down:
            self.aim += value
        elif direction == Direction.Up:
            self.aim -= value
        else:
            return ValueError("Direction not supported")


if __name__ == "__main__":
    instructions = parse_instructions_from_input("input.txt")
    sub = SubmarineWithAim()
    sub.follow_instructions(instructions)
    print(sub.horizontal, sub.depth)
    print(sub.get_product())
