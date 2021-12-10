from typing import Dict, DefaultDict
from collections import defaultdict
from functools import reduce


def solve(days: int) -> int:
    count: DefaultDict[int, int] = defaultdict(lambda: 0)

    input = open("input.txt", "r")
    for n in [int(n) for n in input.readline().strip().split(",")]:
        count[n] += 1

    for _ in range(days):
        new_count: DefaultDict[int, int] = defaultdict(lambda: 0)
        for fish, total in count.items():
            if fish == 0 and total > 0:
                new_count[6] += total
                new_count[8] += total
            else:
                new_count[fish - 1] += total
        count = new_count

    return reduce(lambda prev, curr: prev + curr, count.values())


def main() -> None:
    print(solve(256))


if __name__ == "__main__":
    main()
