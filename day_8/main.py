def load_input(file_name) -> list[tuple]:
    patterns_and_outputs = []
    with open(file_name, "r") as input_file:
        for line in input_file:
            patterns, outputs = list(
                map(
                    lambda x: [set(letters) for letters in x.split(" ")],
                    line.strip().split(" | "),
                )
            )
            patterns_and_outputs.append((patterns, outputs))
    return patterns_and_outputs


def part_1(patterns_and_outputs: list[tuple]) -> int:
    return sum(
        len(items)
        for items in [
            [item for item in y if len(item) in (2, 3, 4, 7)]
            for _, y in patterns_and_outputs
        ]
    )


def get_number_patterns(patterns_for_output: list[set]) -> list[set]:
    number_patterns = [set() for _ in range(10)]
    # get easily found patterns first
    for pattern in patterns_for_output:
        if len(pattern) == 7:
            number_patterns[8] = pattern
        elif len(pattern) == 4:
            number_patterns[4] = pattern
        elif len(pattern) == 3:
            number_patterns[7] = pattern
        elif len(pattern) == 2:
            number_patterns[1] = pattern
    # at this point, we know 1, 4, 7, and 8
    # we still need 0, 2, 3, 5, 6, and 9
    for pattern in patterns_for_output:
        if len(pattern) == 6:
            # 0, 6, or 9
            if number_patterns[4].issubset(pattern):
                number_patterns[9] = pattern
            elif number_patterns[1].issubset(pattern):
                number_patterns[0] = pattern
            else:
                number_patterns[6] = pattern
    # at this point, we know 0, 1, 4, 6, 7, 8, and 9
    # we still need 2, 3, and 5
    for pattern in patterns_for_output:
        if len(pattern) == 5:
            # 2, 3, or 5
            if number_patterns[1].issubset(pattern):
                number_patterns[3] = pattern
            elif pattern.issubset(number_patterns[9]):
                number_patterns[5] = pattern
            else:
                number_patterns[2] = pattern
    # we have them all, return
    return number_patterns


def translate_message(patterns, output):
    key = get_number_patterns(patterns)
    return list(map(lambda o: key.index(set(o)), output))


if __name__ == "__main__":
    input_data = load_input("input.txt")
    print(part_1(input_data))
    sum_value = 0
    for patterns_list, output_list in input_data:
        sum_value += int(
            "".join(
                map(lambda x: str(x), translate_message(patterns_list, output_list))
            )
        )
    print(sum_value)
