def solve() -> int:
    input = open("input.txt", "r")
    horizontal_position = 0
    aim = 0
    depth = 0
    for line in input.readlines():
        splitted = line.strip().split(" ")
        command = splitted[0]
        value = int(splitted[1])
        if command == "forward":
            horizontal_position += value
            depth += aim * value
        elif command == "down":
            aim += value
        else:
            aim -= value
    return horizontal_position * depth


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
