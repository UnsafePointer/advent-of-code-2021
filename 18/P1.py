from modname.node import node_from_data, add_nodes, magnitude
from functools import reduce


def solve() -> int:
    numbers = [node_from_data(eval(s)) for s in open("input.txt", "r").readlines()]
    result = reduce(lambda left, right: add_nodes(left, right), numbers)
    return magnitude(result)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
