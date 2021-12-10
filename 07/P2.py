from typing import List, Set
from sys import maxsize


def calculate_fuel(fixed_position: int, lowest_fuel: int, positions: List[int]) -> int:
    total_fuel = 0
    for position in positions:
        for f in range(1, abs(fixed_position - position) + 1):
            total_fuel += f
            if total_fuel > lowest_fuel:
                return lowest_fuel
    return total_fuel


def solve() -> int:
    input = open("input.txt", "r")
    positions: List[int] = [int(n) for n in input.readline().strip().split(",")]
    lowest_fuel = maxsize
    calculated: Set[int] = set()
    for position in range(0, max(positions) + 1):
        if position in calculated:
            continue
        lowest_fuel = calculate_fuel(position, lowest_fuel, positions)
        calculated.add(position)
    return lowest_fuel


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
