import math


def load_input(file_name: str):
    enhancement, image = "", dict()
    with open(file_name, "r") as input_file:
        for i, line in enumerate(input_file):
            if i == 0:
                enhancement = [0 if char == "." else 1 for char in line.strip()]
            elif i >= 2:
                for j, char in enumerate(line.strip()):
                    image[(i - 2, j)] = 0 if char == "." else 1
    return enhancement, image


def enhancement_at_key(enhancement, image, key, step):
    border = 0 if enhancement[0] == 0 or step % 2 == 0 else 1
    x, y = key
    index = ""
    for x_add in (-1, 0, 1):
        for y_add in (-1, 0, 1):
            neighbor_key = (x + x_add, y + y_add)
            if neighbor_key in image:
                index += str(image[neighbor_key])
            else:
                index += str(border)
    return enhancement[int(index, 2)]


def enhance(enhancement: list[int], image: dict[tuple[int, int], int], step: int):
    new_image = image.copy()
    for key, value in image.items():
        x, y = key
        for x_add in (-1, 0, 1):
            for y_add in (-1, 0, 1):
                neighbor_key = (x + x_add, y + y_add)
                new_image[neighbor_key] = enhancement_at_key(
                    enhancement, image, neighbor_key, step
                )
    return new_image


def enhance_n_times(enhancement, image, n_times: int):
    new_image = image
    for i in range(n_times):
        print(i)
        new_image = enhance(enhancement, new_image, i)
    return new_image


def number_on_after_n_times(enhancement, image, n_times: int):
    enhanced = enhance_n_times(enhancement, image, n_times)
    if enhancement[0] == 1 and n_times % 2 == 1:
        return math.inf
    return len([v for v in enhanced.values() if v == 1])


if __name__ == "__main__":
    input_enhancement, input_image = load_input("input.txt")
    print(number_on_after_n_times(input_enhancement, input_image, 50))
