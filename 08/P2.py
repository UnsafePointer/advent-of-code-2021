from typing import Dict, List, DefaultDict
from collections import defaultdict


def solve() -> int:
    fixed_segments: Dict[int, str] = {}
    fixed_segments[0] = "abcefg"
    fixed_segments[1] = "cf"
    fixed_segments[2] = "acdeg"
    fixed_segments[3] = "acdfg"
    fixed_segments[4] = "bcdf"
    fixed_segments[5] = "abdfg"
    fixed_segments[6] = "abdefg"
    fixed_segments[7] = "acf"
    fixed_segments[8] = "abcdefg"
    fixed_segments[9] = "abcdfg"

    input = open("input.txt", "r")
    total = 0
    for line in [line.strip() for line in input.readlines()]:
        pattern_segments_by_size: DefaultDict[int, List[str]] = defaultdict(lambda: [])
        patterns = line.split(" | ")[0]
        for pattern in patterns.split():
            pattern_segments_by_size[len(pattern)].append(pattern)

        mapping: Dict[str, str] = {}

        if (
            pattern_segments_by_size[2][0][1] in pattern_segments_by_size[6][0]
            and pattern_segments_by_size[2][0][1] in pattern_segments_by_size[6][1]
            and pattern_segments_by_size[2][0][1] in pattern_segments_by_size[6][2]
        ):
            mapping["f"] = pattern_segments_by_size[2][0][1]
            mapping["c"] = pattern_segments_by_size[2][0][0]
        else:
            mapping["c"] = pattern_segments_by_size[2][0][1]
            mapping["f"] = pattern_segments_by_size[2][0][0]

        mapping_for_a = set(pattern_segments_by_size[3][0]).difference(
            pattern_segments_by_size[2][0]
        )
        mapping["a"] = mapping_for_a.pop()

        options_for_b = list(
            set(pattern_segments_by_size[4][0]).difference(
                pattern_segments_by_size[2][0]
            )
        )
        if (
            options_for_b[0] in pattern_segments_by_size[6][0]
            and options_for_b[0] in pattern_segments_by_size[6][1]
            and options_for_b[0] in pattern_segments_by_size[6][2]
        ):
            mapping["b"] = options_for_b[0]
            mapping["d"] = options_for_b[1]
        else:
            mapping["d"] = options_for_b[0]
            mapping["b"] = options_for_b[1]

        options_for_g = list(
            set(pattern_segments_by_size[7][0]).difference(mapping.values())
        )
        if (
            options_for_g[0] in pattern_segments_by_size[6][0]
            and options_for_g[0] in pattern_segments_by_size[6][1]
            and options_for_g[0] in pattern_segments_by_size[6][2]
        ):
            mapping["g"] = options_for_g[0]
            mapping["e"] = options_for_g[1]
        else:
            mapping["e"] = options_for_g[0]
            mapping["g"] = options_for_g[1]

        lookup: Dict[str, int] = {
            "".join(sorted([mapping[c] for c in v])): k
            for k, v in fixed_segments.items()
        }

        values = line.split(" | ")[1]
        number = 0
        for index, value in enumerate(reversed(values.split())):
            number += lookup["".join(sorted(value))] * pow(10, index)
        total += number

    return total


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
