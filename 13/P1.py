from os import linesep
from typing import Set, Tuple, List


def solve() -> int:
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

    input_dots = dots.copy()
    dots.clear()
    (fold_axis, fold_value) = folds[0]
    for (x, y) in input_dots:
        if fold_axis == "y" and y > fold_value:
            y = fold_value - (y - fold_value)
        if fold_axis == "x" and x > fold_value:
            x = fold_value - (x - fold_value)
        dots.add((x, y))

    return len(dots)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
