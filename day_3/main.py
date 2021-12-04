from typing import NamedTuple, Optional


class MetricStrings(NamedTuple):
    oxygen: str
    co2: str


def load_input(file_name: str) -> list[str]:
    binary_numbers = []
    with open(file_name, 'r') as input_file:
        for line in input_file:
            binary_numbers.append(line.strip())
    return binary_numbers


def average_bits(binary_numbers: list[str]):
    number_count = len(binary_numbers)
    bit_sums = [0 for _ in binary_numbers[0]]
    for binary in binary_numbers:
        for i, bit in enumerate(binary):
            bit_sums[i] += int(bit)
    return [sum / number_count for sum in bit_sums]


def average_bit_column(binary_numbers: list[str], column_index: int):
    return sum([int(binary[column_index]) for binary in binary_numbers]) / len(binary_numbers)


def recursive_minmax(binary_numbers: list[str], column_index: int = 0, use_max: bool = True) -> str:
    if len(binary_numbers) == 0 or column_index >= len(binary_numbers[0]):
        return ""
    elif len(binary_numbers) == 1:
        return binary_numbers[0][column_index:]

    if average_bit_column(binary_numbers, column_index) >= 0.5:
        value = "1" if use_max else "0"
        return value + recursive_minmax([n for n in binary_numbers if n[column_index] == value], column_index + 1, use_max)
    else:
        value = "0" if use_max else "1"
        return value + recursive_minmax([n for n in binary_numbers if n[column_index] == value], column_index + 1, use_max)


def calculate_oxygen_and_c02(binary_numbers: list[str]):
    oxygen = recursive_minmax(binary_numbers, use_max=True)
    co2 = recursive_minmax(binary_numbers, use_max=False)
    return int(oxygen, 2), int(co2, 2)


def calculate_gamma_and_epsilon(binary_numbers: list[str]):
    bit_averages = average_bits(binary_numbers)
    mask = int("".join(["1" for _ in bit_averages]), 2)
    gamma = int("".join(map(lambda x: str(round(x)), bit_averages)), 2)
    return gamma, gamma ^ mask


def calculate_power(binary_numbers):
    gamma, epsilon = calculate_gamma_and_epsilon(binary_numbers)
    return gamma * epsilon


def calculate_life_support(binary_numbers):
    oxygen, co2 = calculate_oxygen_and_c02(binary_numbers)
    return oxygen * co2


if __name__ == "__main__":
    input_data = load_input("input.txt")
    print(calculate_power(input_data))
    print(calculate_life_support(input_data))
