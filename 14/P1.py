from typing import Dict, DefaultDict


def solve() -> int:
    input = open("input.txt", "r")
    template = input.readline().strip()
    character_count: DefaultDict[str, int] = DefaultDict(lambda: 0)
    for c in template:
        character_count[c] += 1

    input.readline()

    rules: Dict[str, str] = {}
    for (pair, insert) in [tuple(r.strip().split(" -> ")) for r in input.readlines()]:
        rules[pair] = insert

    for _ in range(10):
        new_template = template
        n_inserted = 0
        for rear_index in range(1, len(template)):
            pair = template[rear_index - 1 : rear_index + 1]
            if pair in rules:
                new_template = (
                    new_template[: (rear_index + n_inserted)]
                    + rules[pair]
                    + new_template[rear_index + n_inserted :]
                )
                n_inserted += 1
                character_count[rules[pair]] += 1
        template = new_template

    values = sorted([v for _, v in character_count.items()])
    return values[-1] - values[0]


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
