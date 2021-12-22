from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from bisect import bisect_left


@dataclass
class Step:
    x_start: int
    x_end: int
    y_start: int
    y_end: int
    z_start: int
    z_end: int
    on: bool


def solve() -> int:
    input = open("input.txt", "r")

    steps: List[Step] = []
    x_count: Set[int] = set()
    y_count: Set[int] = set()
    z_count: Set[int] = set()
    for (action, cuboid) in [s.strip().split(" ") for s in input.readlines()]:
        ranges: Dict[str, Tuple[int, int]] = {}
        for (dimension, range_spec) in [s.split("=") for s in cuboid.split(",")]:
            (range_start, range_end) = [int(s) for s in range_spec.split("..")]
            ranges[dimension] = (range_start, range_end)
        step = Step(
            ranges["x"][0],
            ranges["x"][1] + 1,
            ranges["y"][0],
            ranges["y"][1] + 1,
            ranges["z"][0],
            ranges["z"][1] + 1,
            True if action == "on" else False,
        )
        x_count.add(ranges["x"][0])
        x_count.add(ranges["x"][1] + 1)
        y_count.add(ranges["y"][0])
        y_count.add(ranges["y"][1] + 1)
        z_count.add(ranges["z"][0])
        z_count.add(ranges["z"][1] + 1)
        steps.append(step)

    x: List[int] = sorted(list(x_count))
    y: List[int] = sorted(list(y_count))
    z: List[int] = sorted(list(z_count))

    grid = []
    for _ in range(0, len(x)):
        u = []
        for _ in range(0, len(y)):
            v = [False] * len(z)
            u.append(v)
        grid.append(u)

    for step in steps:
        x_start = bisect_left(x, step.x_start)
        x_end = bisect_left(x, step.x_end)
        y_start = bisect_left(y, step.y_start)
        y_end = bisect_left(y, step.y_end)
        z_start = bisect_left(z, step.z_start)
        z_end = bisect_left(z, step.z_end)
        for x_idx in range(x_start, x_end):
            for y_idx in range(y_start, y_end):
                for z_idx in range(z_start, z_end):
                    grid[x_idx][y_idx][z_idx] = step.on

    total = 0
    for x_idx in range(0, len(x) - 1):
        for y_idx in range(0, len(y) - 1):
            for z_idx in range(0, len(z) - 1):
                if grid[x_idx][y_idx][z_idx]:
                    total += (
                        (x[x_idx + 1] - x[x_idx])
                        * (y[y_idx + 1] - y[y_idx])
                        * (z[z_idx + 1] - z[z_idx])
                    )

    return total


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
