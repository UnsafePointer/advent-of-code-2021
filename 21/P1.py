from typing import List


current = 0


def roll() -> int:
    global current
    current += 1
    if current > 100:
        current = 1
    return current


def solve() -> int:
    input = open("input.txt", "r")
    players: List[int] = [
        int(input.readline().strip().split()[4]) - 1,
        int(input.readline().strip().split()[4]) - 1,
    ]
    scores = [0, 0]
    times = 0

    while True:
        players[times % 2] = (players[times % 2] + sum([roll(), roll(), roll()])) % 10
        scores[times % 2] += players[times % 2] + 1
        if scores[times % 2] >= 1000:
            break
        times += 1
    return scores[times % 2 + 1] * (times + 1) * 3


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
