from statistics import median, mean
from math import ceil, floor


def load_input(file_name):
    locations = []
    with open(file_name, "r") as input_file:
        for line in input_file:
            locations.extend([int(l) for l in line.strip().split(",")])
    return locations


def part_1(locations):
    # median gives us the exact minimum when fuel usage is linear
    return sum(map(lambda x: abs(x - round(median(locations))), locations))


def part_2(locations):
    center_position = median(locations)
    average_position = mean(locations)
    # rounding of the mean should be toward the majority of the positions provided
    # it's possible this solution is missing a potential value if the mean is
    # really close to a whole number
    # proofs from r/adventofcode back up mean as being +-0.5 from the solution
    round_func = ceil if average_position < center_position else floor
    center = round_func(average_position)
    return sum(map(lambda x: sum(range(abs(x - center) + 1)), locations))


if __name__ == "__main__":
    location_inputs = load_input("input.txt")
    print(part_1(location_inputs))
    print(part_2(location_inputs))
