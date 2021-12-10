from typing import List, Set
from sys import maxsize


def calculate_fuel(fixed_position: int, lowest_fuel: int, positions: List[int]) -> int:
    total_fuel = 0
    for position in positions:
        total_fuel += abs(fixed_position - position)
        if total_fuel > lowest_fuel:
            return lowest_fuel
    return total_fuel


def solve() -> int:
    input = open("input.txt", "r")
    positions: List[int] = [int(n) for n in input.readline().strip().split(",")]
    lowest_fuel = maxsize
    calculated: Set[int] = set()
    for position in positions:
        if position in calculated:
            continue
        lowest_fuel = calculate_fuel(position, lowest_fuel, positions)
        calculated.add(position)
    return lowest_fuel


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
