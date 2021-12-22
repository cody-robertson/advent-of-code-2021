import numpy as np

OVERLAP_THRESHOLD = 12

rotation_matrices = [
    # https://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
    # normal
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    # normal 90 around y
    [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
    # normal 180 around y
    [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
    # normal 270 around y
    [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
    # attitude 90
    [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
    [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
    [[0, 1, 0], [1, 0, 0], [0, 0, -1]],
    [[0, 0, -1], [1, 0, 0], [0, -1, 0]],
    # attitude -90
    [[0, 1, 0], [-1, 0, 0], [0, 0, 1]],
    [[0, 0, 1], [-1, 0, 0], [0, -1, 0]],
    [[0, -1, 0], [-1, 0, 0], [0, 0, -1]],
    [[0, 0, -1], [-1, 0, 0], [0, 1, 0]],
    # bank 90
    [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
    [[0, 1, 0], [0, 0, -1], [-1, 0, 0]],
    [[-1, 0, 0], [0, 0, -1], [0, -1, 0]],
    [[0, -1, 0], [0, 0, -1], [1, 0, 0]],
    # bank 180
    [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
    [[0, 0, -1], [0, -1, 0], [-1, 0, 0]],
    [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
    [[0, 0, 1], [0, -1, 0], [1, 0, 0]],
    # bank -90
    [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
    [[0, -1, 0], [0, 0, 1], [-1, 0, 0]],
    [[-1, 0, 0], [0, 0, 1], [0, 1, 0]],
    [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
]


def load_input(file_name: str):
    scanners = []
    scanner = []
    with open(file_name, "r") as input_file:
        for line in input_file:
            if line.strip() == "" or line.startswith("---"):
                if len(scanner) > 0:
                    scanners.append(scanner)
                    scanner = []
            else:
                scanner.append([int(item) for item in line.strip().split(",")])
    if len(scanner) > 0:
        scanners.append(scanner)
    return scanners


def manhattan(point_1, point_2):
    return (
        abs(point_1[0] - point_2[0])
        + abs(point_1[1] - point_2[1])
        + abs(point_1[2] - point_2[2])
    )


def distance_between_points(point_1, point_2):
    x_1, y_1, z_1 = point_1
    x_2, y_2, z_2 = point_2
    return x_2 - x_1, y_2 - y_1, z_2 - z_1


def distances_within_scanner(points_set):
    all_distances = set()
    for i, point_1 in enumerate(points_set):
        for point_2 in points_set[i + 1 :]:
            all_distances.add(manhattan(point_1, point_2))
    return all_distances


def distance_from_all_points(points_set_1, points_set_2):
    all_distances = []
    for point_1 in points_set_1:
        for point_2 in points_set_2:
            all_distances.append(distance_between_points(point_1, point_2))
    return all_distances


def generate_scanner_rotations(beacons):
    for rotation_matrix in rotation_matrices:
        dot_product = [np.dot(beacon, rotation_matrix) for beacon in beacons]
        yield [[round(v) for v in items] for items in dot_product], rotation_matrix


def get_rotation_and_translation_between_scanners(scanner_1, scanner_2):
    for scanner_2_rotated, rotation_matrix in generate_scanner_rotations(scanner_2):
        distances = distance_from_all_points(scanner_1, scanner_2_rotated)
        possible_translations = set(distances)
        scanner_1_set = set([tuple(beacon) for beacon in scanner_1])
        for translation in possible_translations:
            scanner_2_translated = {
                tuple(
                    [value - distance for value, distance in zip(values, translation)]
                )
                for values in scanner_2_rotated
            }
            overlapping = scanner_1_set.intersection(scanner_2_translated)
            if len(overlapping) >= OVERLAP_THRESHOLD:
                return True, scanner_2_translated, rotation_matrix, translation
    # failed to find overlap
    return False, scanner_2, None, None


def orient_scanners(scanners):
    rotated_indices = {0}
    translations = [(0, 0, 0) for _ in range(len(scanners))]
    scanner_distances = [distances_within_scanner(scanner) for scanner in scanners]
    while len(rotated_indices) < len(scanners):
        for i in range(len(scanners)):
            for j in range(len(scanners)):
                if i != j and i in rotated_indices and j not in rotated_indices:
                    overlap_distances = len(
                        scanner_distances[i].intersection(scanner_distances[j])
                    )
                    if overlap_distances > OVERLAP_THRESHOLD - 1:
                        (
                            has_rotated,
                            scanners[j],
                            rotation_matrix,
                            translation_vector,
                        ) = get_rotation_and_translation_between_scanners(
                            scanners[i], scanners[j]
                        )
                        if has_rotated:
                            x, y, z = translation_vector
                            # negate the values to be relative to the first scanner
                            translations[j] = (-x, -y, -z)
                            print(f"rotated {j} to match {i}!")
                            rotated_indices.add(j)
        print(f"loop {len(rotated_indices)} / {len(scanners)}")
    return scanners, translations


def count_beacons(scanners):
    oriented_scanners, translations = orient_scanners(scanners)
    beacons = set()
    for scanner in oriented_scanners:
        for beacon in scanner:
            beacons.add(tuple(beacon))
    max_manhattan = 0
    # manhattan distance needs to be calculated both directions?
    for first in translations:
        for second in translations:
            max_manhattan = max(max_manhattan, manhattan(first, second))
    return len(beacons), max_manhattan


if __name__ == "__main__":
    input_scanners = load_input("input.txt")
    print(count_beacons(input_scanners))
