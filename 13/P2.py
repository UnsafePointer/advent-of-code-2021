from os import linesep
from sys import maxsize
from typing import Set, Tuple, List


def solve() -> str:
    dots: Set[Tuple[int, int]] = set()
    folds: List[Tuple[str, int]] = []

    input = open("input.txt", "r")
    for line in input.readlines():
        if line.startswith("fold along "):
            (axis, value) = tuple(line.strip()[len("fold along ") :].split("="))
            folds.append((axis, int(value)))
        elif line == linesep:
            continue
        else:
            (x, y) = [int(c) for c in line.strip().split(",")]
            dots.add((x, y))

    for (fold_axis, fold_value) in folds:
        input_dots = dots.copy()
        dots.clear()
        for (x, y) in input_dots:
            if fold_axis == "y" and y > fold_value:
                y = fold_value - (y - fold_value)
            if fold_axis == "x" and x > fold_value:
                x = fold_value - (x - fold_value)
            dots.add((x, y))

    max_x = -maxsize
    max_y = -maxsize
    for (x, y) in dots:
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    code = ""
    for y in range(max_y + 1):
        row = ""
        for x in range(max_x + 1):
            row += "#" if (x, y) in dots else "."
        code += row
        code += linesep

    return code[:-1]


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
