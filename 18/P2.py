from modname.node import node_from_data, add_nodes, magnitude
import itertools
from sys import maxsize


def solve() -> int:
    numbers = [eval(s) for s in open("input.txt", "r").readlines()]
    combinations = list(itertools.combinations(numbers, 2))
    max_magnitude = -maxsize
    for (left, right) in combinations:
        result = add_nodes(node_from_data(left), node_from_data(right))
        max_magnitude = max(max_magnitude, magnitude(result))
        result = add_nodes(node_from_data(right), node_from_data(left))
        max_magnitude = max(max_magnitude, magnitude(result))
    return max_magnitude


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
