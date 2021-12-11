from typing import Set, Tuple


def solve() -> int:
    segments: Set[int] = set([2, 3, 4, 7])
    digit_times = 0

    input = open("input.txt", "r")
    for output_values in [line.strip().split(" | ")[1] for line in input.readlines()]:
        for output_value in output_values.split(" "):
            if len(output_value) in segments:
                digit_times += 1

    return digit_times


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
