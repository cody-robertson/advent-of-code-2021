from collections import Counter


def load_input(file_name: str):
    with open(file_name, "r") as input_file:
        input_lines = list(map(lambda x: x.strip(), input_file.readlines()))
    initial_state = list(input_lines[0])
    recipes = {
        key: value for key, value in map(lambda x: x.split(" -> "), input_lines[2:])
    }
    return initial_state, recipes


def process_recipes(state: list[chr], recipes: dict[str, chr]):
    i = 0
    while i < len(state) - 1:
        pair = state[i] + state[i + 1]
        if pair in recipes:
            state.insert(i + 1, recipes[pair])
            i += 1
        i += 1
    return state


def most_and_least(state, recipes, iterations: int):
    for i in range(iterations):
        state = process_recipes(state, recipes)
    counter = Counter(state)
    common = counter.most_common()
    most = common[0][1]
    least = common[-1][1]
    return most - least


def part_1(state, recipes):
    return most_and_least(state, recipes, 10)


def part_2(state, recipes):
    return most_and_least(state, recipes, 40)


if __name__ == "__main__":
    input_state, input_recipes = load_input("sample.txt")
    print(part_1(input_state, input_recipes))
    print(part_2(input_state, input_recipes))
