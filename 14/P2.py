from typing import Dict
from collections import defaultdict


def solve() -> int:
    input = open("input.txt", "r")
    template = input.readline().strip()
    character_count: Dict[str, int] = defaultdict(lambda: 0)
    for c in template:
        character_count[c] += 1

    input.readline()

    rules: Dict[str, str] = {}
    for (pair, insert) in [tuple(r.strip().split(" -> ")) for r in input.readlines()]:
        rules[pair] = insert

    pairs: Dict[str, int] = defaultdict(lambda: 0)
    for rear_index in range(1, len(template)):
        pair = template[rear_index - 1 : rear_index + 1]
        pairs[pair] += 1

    for _ in range(40):
        for pair, count in pairs.copy().items():
            if pair in rules and count > 0:
                pairs[pair[0] + rules[pair]] += count
                pairs[rules[pair] + pair[1]] += count
                pairs[pair] -= count

                character_count[rules[pair]] += count

    values = sorted([v for _, v in character_count.items()])
    return values[-1] - values[0]


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
