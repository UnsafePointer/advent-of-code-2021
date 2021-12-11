from dataclasses import dataclass, field
from typing import List
from os import linesep


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


def solve() -> int:
    heatMap = HeatMap()

    input = open("input.txt", "r")
    for line in input.readlines():
        heatMap.locations.append([int(c) for c in line.strip()])

    risk_level = 0
    for row_index, row in enumerate(heatMap.locations):
        for column_index, n in enumerate(row):
            if heatMap.is_low_point(row_index, column_index):
                risk_level += 1 + n

    return risk_level


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
