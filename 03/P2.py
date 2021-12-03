from typing import List
from sys import maxsize


def solve() -> int:
    input = open("input.txt", "r")
    input_values: List[str] = []
    for line in input.readlines():
        input_values.append(line.strip())
    index = 0
    lists: List[List[str]] = [[], []]
    oxigen_generator_rating = -maxsize
    values = input_values.copy()
    while True:
        for number in values:
            if number[index] == "0":
                lists[0].append(number)
            else:
                lists[1].append(number)
        if len(lists[0]) == len(lists[1]):
            if len(lists[0]) == 1:
                oxigen_generator_rating = int(lists[1][0], 2)
                break
            else:
                values = lists[1].copy()
        else:
            values = (
                lists[0].copy() if len(lists[0]) > len(lists[1]) else lists[1].copy()
            )
        lists[0].clear()
        lists[1].clear()
        index += 1

    index = 0
    lists = [[], []]
    co2_scrubber_rating = -maxsize
    values = input_values.copy()
    while True:
        for number in values:
            if number[index] == "0":
                lists[0].append(number)
            else:
                lists[1].append(number)
        if len(lists[0]) == len(lists[1]):
            if len(lists[0]) == 1:
                co2_scrubber_rating = int(lists[0][0], 2)
                break
            else:
                values = lists[0].copy()
        else:
            values = (
                lists[0].copy() if len(lists[0]) < len(lists[1]) else lists[1].copy()
            )
        lists[0].clear()
        lists[1].clear()
        index += 1

    return oxigen_generator_rating * co2_scrubber_rating


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
