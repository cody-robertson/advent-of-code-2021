matching_symbols = {"(": ")", "[": "]", "{": "}", "<": ">"}


def load_input(file_name: str) -> list[str]:
    input_lines = []
    with open(file_name, "r") as input_file:
        for line in input_file:
            input_lines.append(line.strip())
    return input_lines


def get_expected_for_symbol(symbol: chr) -> chr:
    return matching_symbols[symbol]


def categorize_line(line: str):
    stack = []
    missing = []
    for symbol in line:
        if symbol in matching_symbols:
            stack.append(symbol)
        elif len(stack) == 0:
            raise Exception("stack is empty!")
        else:
            expected = get_expected_for_symbol(stack.pop())
            if expected != symbol:
                return "corrupted", symbol
    if len(stack) == 0 and len(missing) == 0:
        return "complete", None
    else:
        return "incomplete", list(reversed(missing + stack))


def categorize_lines(lines: list[str]):
    return [(line, *categorize_line(line)) for line in lines]


def part_1(lines: list[str]) -> int:
    point_values = {")": 3, "]": 57, "}": 1197, ">": 25137}
    categorized = [
        point_values[symbol]
        for _, category, symbol in categorize_lines(lines)
        if category == "corrupted"
    ]
    return sum(categorized)


def calculate_points_for_missing(missing: list[chr]) -> int:
    point_values = {"(": 1, "[": 2, "{": 3, "<": 4}
    points = 0
    for symbol in missing:
        points *= 5
        points += point_values[symbol]
    return points


def part_2(lines: list[str]) -> int:
    incomplete = [
        missing
        for _, category, missing in categorize_lines(lines)
        if category == "incomplete"
    ]
    incomplete_scores = sorted(
        [calculate_points_for_missing(missing) for missing in incomplete]
    )
    center_index = round(len(incomplete) / 2)
    return incomplete_scores[center_index]


if __name__ == "__main__":
    input_values = load_input("input.txt")
    print(part_1(input_values))
    print(part_2(input_values))
