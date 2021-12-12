from dataclasses import dataclass, field
from typing import List, Tuple, Set, DefaultDict
from os import linesep


@dataclass
class Cavern:
    octopi: List[List[int]] = field(default_factory=list)

    def __repr__(self) -> str:
        r = ""
        for row in self.octopi:
            r += "".join([str(i) if i != 0 else "\033[1m0\033[0m" for i in row])
            r += linesep
        return r

    def check_octopi(
        self, row_index: int, column_index: int, flashed: Set[Tuple[int, int]]
    ) -> bool:
        if (row_index, column_index) in flashed:
            return False
        if self.octopi[row_index][column_index] == 9:
            self.octopi[row_index][column_index] = 0
            return True
        else:
            self.octopi[row_index][column_index] += 1
            return False

    def process_flashes(
        self, flashes: List[Tuple[int, int]], flashed: Set[Tuple[int, int]]
    ) -> None:
        new_flashes: List[Tuple[int, int]] = []
        for (row_index, column_index) in flashes:
            available_directions: DefaultDict[str, bool] = DefaultDict(lambda: False)
            if row_index > 0:
                available_directions["up"] = True
            if row_index < len(self.octopi) - 1:
                available_directions["down"] = True
            if column_index > 0:
                available_directions["left"] = True
            if column_index < len(self.octopi[row_index]) - 1:
                available_directions["right"] = True

            if available_directions["up"]:
                if self.check_octopi(row_index - 1, column_index, flashed):
                    new_flashes.append((row_index - 1, column_index))
                    flashed.add((row_index - 1, column_index))
            if available_directions["down"]:
                if self.check_octopi(row_index + 1, column_index, flashed):
                    new_flashes.append((row_index + 1, column_index))
                    flashed.add((row_index + 1, column_index))
            if available_directions["left"]:
                if self.check_octopi(row_index, column_index - 1, flashed):
                    new_flashes.append((row_index, column_index - 1))
                    flashed.add((row_index, column_index - 1))
            if available_directions["right"]:
                if self.check_octopi(row_index, column_index + 1, flashed):
                    new_flashes.append((row_index, column_index + 1))
                    flashed.add((row_index, column_index + 1))

            if available_directions["up"] and available_directions["left"]:
                if self.check_octopi(row_index - 1, column_index - 1, flashed):
                    new_flashes.append((row_index - 1, column_index - 1))
                    flashed.add((row_index - 1, column_index - 1))
            if available_directions["up"] and available_directions["right"]:
                if self.check_octopi(row_index - 1, column_index + 1, flashed):
                    new_flashes.append((row_index - 1, column_index + 1))
                    flashed.add((row_index - 1, column_index + 1))
            if available_directions["down"] and available_directions["left"]:
                if self.check_octopi(row_index + 1, column_index - 1, flashed):
                    new_flashes.append((row_index + 1, column_index - 1))
                    flashed.add((row_index + 1, column_index - 1))
            if available_directions["down"] and available_directions["right"]:
                if self.check_octopi(row_index + 1, column_index + 1, flashed):
                    new_flashes.append((row_index + 1, column_index + 1))
                    flashed.add((row_index + 1, column_index + 1))

        for flash in new_flashes:
            flashed.add(flash)

        if new_flashes:
            self.process_flashes(new_flashes, flashed)

        return

    def increase_energy_level(self) -> int:
        flashes: List[Tuple[int, int]] = []
        flashed: Set[Tuple[int, int]] = set()

        for row_index, row in enumerate(self.octopi):
            for column_index, _ in enumerate(row):
                if self.check_octopi(row_index, column_index, flashed):
                    flashes.append((row_index, column_index))

        for flash in flashes:
            flashed.add(flash)

        self.process_flashes(flashes, flashed)

        return len(flashed)


def solve() -> int:
    cavern = Cavern()

    input = open("input.txt", "r")
    for line in input.readlines():
        cavern.octopi.append([int(c) for c in line.strip()])

    total_flashes = 0
    for _ in range(100):
        total_flashes += cavern.increase_energy_level()

    return total_flashes


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
