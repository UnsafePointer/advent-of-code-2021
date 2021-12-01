from collections import deque
from typing import Deque


def solve() -> int:
    file = open("input.txt", "r")

    depths: Deque[int] = deque()
    for line in file:
        depths.append(int(line))

    sliding_window: Deque[int] = deque()
    current_window = 0
    for _ in range(3):
        depth = depths.popleft()
        current_window += depth
        sliding_window.append(depth)

    n_increases = 0
    while depths:
        previous_window = current_window
        depth = depths.popleft()
        sliding_window.append(depth)
        current_window -= sliding_window.popleft()
        current_window += depth
        if previous_window < current_window:
            n_increases += 1

    return n_increases


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
