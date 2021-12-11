from collections import deque
from typing import Dict, Deque, Set


def solve() -> int:
    pairs: Dict[str, str] = {")": "(", "]": "[", "}": "{", ">": "<"}
    scoring: Dict[str, int] = {")": 3, "]": 57, "}": 1197, ">": 25137}
    closing: Set[str] = set(pairs.keys())
    queue: Deque[str] = deque()

    score = 0
    input = open("input.txt", "r")
    for line in input.readlines():
        for c in line.strip():
            if c in closing:
                if pairs[c] != queue.pop():
                    score += scoring[c]
                    break
            else:
                queue.append(c)

    return score


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
