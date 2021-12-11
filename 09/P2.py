from dataclasses import dataclass, field
from typing import List, Set, Tuple
from os import linesep
from sortedcontainers import SortedList, sortedlist


@dataclass
class HeatMap:
    locations: List[List[int]] = field(default_factory=list)

    def __repr__(self) -> str:
        r = []
        for row in self.locations:
            r.append("".join([str(n) for n in row]))
        return linesep.join(r)

    def is_low_point(self, row_index: int, column_index: int) -> bool:
        n = self.locations[row_index][column_index]
        if row_index > 0 and self.locations[row_index - 1][column_index] <= n:  # up
            return False
        if (
            row_index < len(self.locations) - 1
            and self.locations[row_index + 1][column_index] <= n
        ):  # down
            return False
        if (
            column_index > 0 and self.locations[row_index][column_index - 1] <= n
        ):  # left
            return False
        if (
            column_index < len(self.locations[row_index]) - 1
            and self.locations[row_index][column_index + 1] <= n
        ):  # down
            return False
        return True

    def calculate_basin(
        self, row_index: int, column_index: int, visited: Set[Tuple[int, int]]
    ) -> int:
        if (row_index, column_index) in visited:
            return 0
        if row_index < 0 or row_index >= len(self.locations):
            return 0
        if column_index < 0 or column_index >= len(self.locations[row_index]):
            return 0
        if self.locations[row_index][column_index] == 9:
            return 0
        visited.add((row_index, column_index))
        return (
            1
            + self.calculate_basin(row_index - 1, column_index, visited)
            + self.calculate_basin(row_index + 1, column_index, visited)
            + self.calculate_basin(row_index, column_index - 1, visited)
            + self.calculate_basin(row_index, column_index + 1, visited)
        )


def solve() -> int:
    heatMap = HeatMap()

    input = open("input.txt", "r")
    for line in input.readlines():
        heatMap.locations.append([int(c) for c in line.strip()])

    low_points: Set[Tuple[int, int]] = set()
    for row_index, row in enumerate(heatMap.locations):
        for column_index, _ in enumerate(row):
            if heatMap.is_low_point(row_index, column_index):
                low_points.add((row_index, column_index))

    basins: SortedList[int] = SortedList()
    for (row_index, column_index) in low_points:
        basins.add(heatMap.calculate_basin(row_index, column_index, set()))

    return basins[-1] * basins[-2] * basins[-3]


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
