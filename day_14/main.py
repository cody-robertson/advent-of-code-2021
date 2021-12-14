from collections import defaultdict
from copy import deepcopy
from math import inf


def load_input(file_name: str):
    with open(file_name, "r") as input_file:
        input_lines = list(map(lambda x: x.strip(), input_file.readlines()))
    initial_state = defaultdict(lambda: 0)
    for i, char in enumerate(input_lines[0]):
        if i + 1 < len(input_lines[0]):
            initial_state[input_lines[0][i] + input_lines[0][i + 1]] += 1
    recipes = {
        key: value for key, value in map(lambda x: x.split(" -> "), input_lines[2:])
    }
    return initial_state, recipes


def process_recipes(state: dict[str, int], recipes: dict[str, chr]):
    next_state = deepcopy(state)
    for pair in state:
        if pair in recipes:
            center = recipes[pair]
            left_pair, right_pair = pair[0] + center, center + pair[1]
            count = state[pair]

            next_state[pair] -= count
            next_state[left_pair] += count
            next_state[right_pair] += count
    return next_state


def most_and_least(state: dict[str, int], recipes: dict[str, chr], iterations: int):
    for i in range(iterations):
        state = process_recipes(state, recipes)
    letters = {key[0] for key in state}.union({key[1] for key in state})
    most = -inf
    least = inf
    for letter in letters:
        single = sum(
            [
                value
                for key, value in state.items()
                if letter in key and not key == letter + letter
            ]
        )
        double = sum([value for key, value in state.items() if key == letter + letter])
        # this gives us a count +- 1 from the solution due to rounding
        count = round(single / 2) + double

        most = max(most, count)
        least = min(least, count)
    return most - least


def part_1(state, recipes):
    state_copy = deepcopy(state)
    return most_and_least(state_copy, recipes, 10)


def part_2(state, recipes):
    state_copy = deepcopy(state)
    return most_and_least(state_copy, recipes, 40)


if __name__ == "__main__":
    input_state, input_recipes = load_input("sample.txt")
    print("part 1: ", part_1(input_state, input_recipes))
    print("part 2: ", part_2(input_state, input_recipes))
