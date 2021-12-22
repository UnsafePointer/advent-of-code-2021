from typing import Set, Tuple, Dict, List


def solve() -> int:
    input = open("input.txt", "r")

    space: Set[Tuple[int, int, int]] = set()
    line = 0
    for (action, cuboid) in [s.strip().split(" ") for s in input.readlines()]:
        print(line)
        ranges: Dict[str, List[int]] = {}
        for (dimension, range_spec) in [s.split("=") for s in cuboid.split(",")]:
            (range_start, range_end) = [int(s) for s in range_spec.split("..")]
            if range_start < -50:
                range_start = -50
            if range_end > 50:
                range_end = 50
            ranges[dimension] = list(range(range_start, range_end + 1))
        if action == "on":
            for x in ranges["x"]:
                for y in ranges["y"]:
                    for z in ranges["z"]:
                        space.add((x, y, z))
        else:
            for x in ranges["x"]:
                for y in ranges["y"]:
                    for z in ranges["z"]:
                        if (x, y, z) in space:
                            space.remove((x, y, z))
        line += 1

    return len(space)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
