def load_input(file_name: str):
    with open(file_name, "r") as input_file:
        line = input_file.readline().strip().lstrip("target area: ")
    x_range, y_range = line.split(", ")
    x_range, y_range = list(map(int, x_range.lstrip("x=").split(".."))), list(
        map(int, y_range.lstrip("y=").split(".."))
    )
    x_range, y_range = range(x_range[0], x_range[1] + 1), range(
        y_range[0], y_range[1] + 1
    )
    return x_range, y_range


def trick_shot(x_range: range, y_range: range):
    max_y = y_range.start
    for t in range(x_range.stop + 100):
        for x_start in range(1, x_range.stop + 1):
            max_x = sum(range(x_start + 1))
            if sum(range(t)) > max_x:
                x = max_x
            else:
                x = x_start * t - sum(range(t))
            if x in x_range:
                for y_start in range(y_range.start, x_range.stop + 1 + 100):
                    y = y_start * t - sum(range(t))
                    if y in y_range:
                        highest_y = y_start if y_start < 0 else sum(range(y_start + 1))
                        max_y = max(max_y, highest_y)
                        print(max_y, x_start, y_start)
    return max_y


def solutions_count(x_range: range, y_range: range):
    solutions = set()
    for t in range(x_range.stop + 100):
        for x_start in range(1, x_range.stop + 1):
            max_x = sum(range(x_start + 1))
            if sum(range(t)) > max_x:
                x = max_x
            else:
                x = x_start * t - sum(range(t))
            if x in x_range:
                for y_start in range(y_range.start, x_range.stop + 1 + 100):
                    y = y_start * t - sum(range(t))
                    if y in y_range:
                        solutions.add((x_start, y_start))
    return len(solutions)


if __name__ == "__main__":
    input_target = load_input("input.txt")
    print(trick_shot(input_target[0], input_target[1]))
    print(solutions_count(input_target[0], input_target[1]))
