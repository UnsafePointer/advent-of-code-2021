from typing import Dict


def solve() -> int:
    input = open("input.txt", "r")
    count: Dict[int, int] = {}
    n = 0
    for line in input.readlines():
        n += 1
        for index, char in enumerate(reversed(line.strip())):
            if char == "1":
                if index in count:
                    count[index] += 1
                else:
                    count[index] = 1
            elif char == "0":
                if index not in count:
                    count[index] = 0
    gamma_rate = 0
    epsilon_rate = 0
    for index in range(len(count)):
        if count[index] > n / 2:
            bit_mask = 1 << index
            gamma_rate |= bit_mask
        else:
            bit_mask = 1 << index
            epsilon_rate |= bit_mask
    return gamma_rate * epsilon_rate


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
