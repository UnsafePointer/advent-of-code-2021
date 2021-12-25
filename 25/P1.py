from typing import Set, Tuple
from sys import maxsize


def print_sea(
    max_row: int,
    max_column: int,
    moving_right: Set[Tuple[int, int]],
    moving_down: Set[Tuple[int, int]],
) -> None:
    for row in range(max_row + 1):
        r = []
        for column in range(max_column + 1):
            if (row, column) in moving_right:
                r.append(">")
            elif (row, column) in moving_down:
                r.append("v")
            else:
                r.append(".")
        print("".join(r))


def solve() -> int:
    input = open("input.txt", "r")
    moving_right: Set[Tuple[int, int]] = set()
    moving_down: Set[Tuple[int, int]] = set()
    max_row = -maxsize
    max_column = -maxsize
    for row, line in enumerate([s.strip() for s in input.readlines()]):
        for column, c in enumerate(list(line)):
            if c == "v":
                moving_down.add((row, column))
            elif c == ">":
                moving_right.add((row, column))
            max_column = max(max_column, column)
        max_row = max(max_row, row)

    times = 0
    while True:
        times += 1
        moves = 0

        sea = moving_right | moving_down
        new_moving_right = moving_right.copy()
        for (row, column) in moving_right:
            new_column = column + 1
            if new_column > max_column:
                new_column = 0
            if (row, new_column) not in sea:
                new_moving_right.remove((row, column))
                new_moving_right.add((row, new_column))
                moves += 1
        moving_right = new_moving_right

        sea = moving_right | moving_down
        new_moving_down = moving_down.copy()
        for (row, column) in moving_down:
            new_row = row + 1
            if new_row > max_row:
                new_row = 0
            if (new_row, column) not in sea:
                new_moving_down.remove((row, column))
                new_moving_down.add((new_row, column))
                moves += 1
        moving_down = new_moving_down

        if moves == 0:
            break

    return times


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
