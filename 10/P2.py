from collections import deque
from typing import Dict, Deque, Set, List


def solve() -> int:
    pairs: Dict[str, str] = {")": "(", "]": "[", "}": "{", ">": "<"}
    inverse_pairs = {v: k for k, v in pairs.items()}
    scoring: Dict[str, int] = {")": 1, "]": 2, "}": 3, ">": 4}
    closing: Set[str] = set(pairs.keys())
    queue: Deque[str] = deque()
    scores: List[int] = []

    input = open("input.txt", "r")
    for line in input.readlines():
        queue.clear()
        corrupted = False
        for c in line.strip():
            if c in closing:
                if pairs[c] != queue.pop():
                    corrupted = True
                    break
            else:
                queue.append(c)

        if corrupted:
            continue

        score = 0
        for c in reversed(queue):
            score *= 5
            score += scoring[inverse_pairs[c]]
        scores.append(score)

    return sorted(scores)[int(len(scores) / 2)]


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
