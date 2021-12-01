from typing import List, Optional


def solve() -> int:
    file = open("input.txt", "r")

    depths: List[int] = []
    for line in file:
        depths.append(int(line))

    last_measurement: Optional[int] = None
    n_increases = 0
    for depth in depths:
        if last_measurement and last_measurement < depth:
            n_increases += 1
        last_measurement = depth

    return n_increases


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
