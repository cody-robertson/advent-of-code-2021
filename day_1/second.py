from day_1.first import load_input


def calculate_sliding_difference(items: list[int]) -> list[int]:
    results = []
    for i in range(3, len(items)):
        prev = sum(items[i-3:i])
        curr = sum(items[i-2:i+1])
        results.append(curr - prev)
    return results


def increase_count(items: list[int]) -> int:
    differences = calculate_sliding_difference(items)
    return len([value for value in differences if value > 0])


if __name__ == "__main__":
    values = load_input("input.txt")
    print(increase_count(values))
