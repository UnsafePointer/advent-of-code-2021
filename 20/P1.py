from typing import List, Dict, Tuple
from collections import defaultdict
from sys import maxsize
from functools import reduce


def output_pixel_for_location(
    x: int, y: int, image: Dict[Tuple[int, int], int], algorithm: List[int]
) -> int:
    number: List[str] = []
    for x_iterator in range(x - 1, x + 2):
        for y_iterator in range(y - 1, y + 2):
            number.append(str(image[(x_iterator, y_iterator)]))
    index = int("".join(number), 2)
    return algorithm[index]


def enhance_image(
    image: Dict[Tuple[int, int], int], algorithm: List[int], default: int
) -> Dict[Tuple[int, int], int]:
    max_x = -maxsize
    min_x = maxsize
    max_y = -maxsize
    min_y = maxsize
    for (x, y) in image.keys():
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y

    new_image: Dict[Tuple[int, int], int] = defaultdict(lambda: default)
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            new_image[(x, y)] = output_pixel_for_location(x, y, image, algorithm)

    return new_image


def print_image(image: Dict[Tuple[int, int], int]) -> None:
    max_x = -maxsize
    min_x = maxsize
    max_y = -maxsize
    min_y = maxsize
    for (x, y) in image.keys():
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y

    for x in range(min_x, max_x + 1):
        row = []
        for y in range(min_y, max_y + 1):
            row.append("#" if image[(x, y)] else ".")
        print("".join(row))


def solve() -> int:
    input = open("input.txt", "r")

    algorithm: List[int] = []
    reading_image = False
    row = 0
    image: Dict[Tuple[int, int], int]
    for line in input.readlines():
        if line.strip() == "":
            reading_image = True
            image = defaultdict(lambda: 0)
            continue
        if reading_image:
            for column, value in enumerate(line.strip()):
                key = (row, column)
                image[key] = 1 if value == "#" else 0
            row += 1
        else:
            algorithm += [1 if c == "#" else 0 for c in list(line.strip())]

    image = enhance_image(image, algorithm, algorithm[0])
    image = enhance_image(image, algorithm, algorithm[8])

    return reduce(lambda x, y: x + y, image.values())


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
