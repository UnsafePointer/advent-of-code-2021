from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, Dict, List, Set
from sys import maxsize
from collections import defaultdict


@dataclass
class Node:
    identifier: Tuple[int, int]
    distance: int
    adjacent_nodes: List[Node] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.identifier)

    def __repr__(self) -> str:
        return str(self.identifier)


def solve() -> int:
    input = open("input.txt", "r")
    data: List[List[int]] = []
    for line in input.readlines():
        data.append([int(c) for c in line.strip()])

    nodes: Dict[Tuple[int, int], Node] = {}
    for row_index, row in enumerate(data):
        for column_index, n in enumerate(row):
            current_node: Node
            if (row_index, column_index) not in nodes:
                current_node = Node((row_index, column_index), n)
                nodes[(row_index, column_index)] = current_node
            else:
                current_node = nodes[(row_index, column_index)]

            adjacent_node: Node

            if column_index > 0:  # left
                identifier = (row_index, column_index - 1)
                if identifier not in nodes:
                    adjacent_node = Node(identifier, data[row_index][column_index - 1])
                    nodes[identifier] = adjacent_node
                else:
                    adjacent_node = nodes[identifier]
                current_node.adjacent_nodes.append(adjacent_node)

            if column_index < len(data[row_index]) - 1:  # right
                identifier = (row_index, column_index + 1)
                if identifier not in nodes:
                    adjacent_node = Node(identifier, data[row_index][column_index + 1])
                    nodes[identifier] = adjacent_node
                else:
                    adjacent_node = nodes[identifier]
                current_node.adjacent_nodes.append(adjacent_node)

            if row_index > 0:  # up
                identifier = (row_index - 1, column_index)
                if identifier not in nodes:
                    adjacent_node = Node(identifier, data[row_index - 1][column_index])
                    nodes[identifier] = adjacent_node
                else:
                    adjacent_node = nodes[identifier]
                current_node.adjacent_nodes.append(adjacent_node)

            if row_index < len(data) - 1:  # down
                identifier = (row_index + 1, column_index)
                if identifier not in nodes:
                    adjacent_node = Node(identifier, data[row_index + 1][column_index])
                    nodes[identifier] = adjacent_node
                else:
                    adjacent_node = nodes[identifier]
                current_node.adjacent_nodes.append(adjacent_node)

    visited: Set[Node] = set()
    distances: Dict[Node, int] = defaultdict(lambda: maxsize)
    distances[nodes[(0, 0)]] = 0
    current_node = nodes[(0, 0)]
    while len(visited) < len(nodes):
        for node in current_node.adjacent_nodes:
            distances[node] = min(
                distances[node], distances[current_node] + node.distance
            )
        min_distance = maxsize
        min_distance_node: Node
        visited.add(current_node)
        for node, distance in distances.items():
            if distance < min_distance and node not in visited:
                min_distance_node = node
                min_distance = distance
        current_node = min_distance_node

    return distances[nodes[(len(data) - 1, len(data) - 1)]]


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
