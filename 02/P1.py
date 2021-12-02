def solve() -> int:
    input = open("input.txt", "r")
    horizontal_position = 0
    depth = 0
    for line in input.readlines():
        splitted = line.strip().split(" ")
        command = splitted[0]
        value = int(splitted[1])
        if command == "forward":
            horizontal_position += value
        elif command == "down":
            depth += value
        else:
            depth -= value
    return horizontal_position * depth


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
