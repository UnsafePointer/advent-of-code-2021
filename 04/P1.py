from collections import deque
from typing import List, Deque, Tuple
from dataclasses import dataclass, field


@dataclass
class Board:
    rows: List[List[Tuple[int, bool]]] = field(default_factory=list)

    def find_completed_column_decresing(
        self, row_index: int, fixed_column_index: int
    ) -> bool:
        if row_index < 0:
            return True
        (_, found) = self.rows[row_index][fixed_column_index]
        if not found:
            return False
        return self.find_completed_column_decresing(row_index - 1, fixed_column_index)

    def find_completed_column_increasing(
        self, row_index: int, fixed_column_index: int
    ) -> bool:
        if row_index >= len(self.rows[0]):
            return True
        (_, found) = self.rows[row_index][fixed_column_index]
        if not found:
            return False
        return self.find_completed_column_increasing(row_index + 1, fixed_column_index)

    def find_completed_column(self, row_index: int, column_index: int) -> bool:
        return self.find_completed_column_decresing(
            row_index, column_index
        ) and self.find_completed_column_increasing(row_index, column_index)

    def find_completed_row_decreasing(
        self, fixed_row_index: int, column_index: int
    ) -> bool:
        if column_index < 0:
            return True
        (_, found) = self.rows[fixed_row_index][column_index]
        if not found:
            return False
        return self.find_completed_row_decreasing(fixed_row_index, column_index - 1)

    def find_completed_row_increasing(
        self, fixed_row_index: int, column_index: int
    ) -> bool:
        if column_index >= len(self.rows):
            return True
        (_, found) = self.rows[fixed_row_index][column_index]
        if not found:
            return False
        return self.find_completed_row_increasing(fixed_row_index, column_index + 1)

    def find_completed_row(self, row_index: int, column_index: int) -> bool:
        return self.find_completed_row_decreasing(
            row_index, column_index
        ) and self.find_completed_row_increasing(row_index, column_index)

    def find_completed(self, row_index: int, column_index: int) -> bool:
        return self.find_completed_row(
            row_index, column_index
        ) or self.find_completed_column(row_index, column_index)

    def mark(self, draw: int) -> bool:
        for row_index, row in enumerate(self.rows):
            for column_index, (number, _) in enumerate(row):
                if number == draw:
                    self.rows[row_index][column_index] = (number, True)
                    return self.find_completed(row_index, column_index)
        return False

    def calculate_score(self, draw: int) -> int:
        total_unmarked_numbers = 0
        for row in self.rows:
            for (number, found) in row:
                if not found:
                    total_unmarked_numbers += number
        return total_unmarked_numbers * draw


def solve() -> int:
    input = open("input.txt", "r")
    draws: Deque[int] = deque([int(n) for n in input.readline().strip().split(",")])

    boards: List[Board] = []
    current_board = -1
    for line in input.readlines():
        if len(line.strip()) == 0:
            boards.append(Board())
            current_board += 1
        else:
            row: List[Tuple[int, bool]] = [
                (int(n), False) for n in line.strip().split()
            ]
            boards[current_board].rows.append(row)

    while draws:
        draw = draws.popleft()
        for board in boards:
            if board.mark(draw):
                return board.calculate_score(draw)

    return 0


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
