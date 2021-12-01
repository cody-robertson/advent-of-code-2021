def load_input(file_name: str) -> list[int]:
    depths = []
    with open(file_name, 'r') as input_file:
        for line in input_file:
            depths.append(int(line.strip()))
    return depths


def calculate_differences(items: list[int]) -> list[int]:
    result = []
    for i in range(len(items)-1):
        result.append(items[i+1] - items[i])
    return result


def increase_count(items: list[int]) -> int:
    differences = calculate_differences(items)
    return len([num for num in differences if num > 0])


if __name__ == "__main__":
    params = load_input("part_1_input_2.txt")
    print(increase_count(params))
