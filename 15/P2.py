from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, Dict, List, Set
from sys import maxsize
from collections import defaultdict
from heapq import heappush, heappop


@dataclass
class Node:
    identifier: Tuple[int, int]
    distance: int
    adjacent_nodes: List[Node] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.identifier)

    def __repr__(self) -> str:
        return str(self.identifier)

    def __lt__(self, other: Node) -> bool:
        return self.identifier < other.identifier


def solve() -> int:
    input = open("input.txt", "r")
    data: List[List[int]] = []
    for line in input.readlines():
        data.append([int(c) for c in line.strip()])

    initial_len = len(data)
    for row_index in range(len(data)):
        data[row_index] += [-1] * 4 * initial_len

    for _ in range(len(data), len(data) * 5):
        new_row = [-1] * 5 * initial_len
        data.append(new_row)

    for row_index in range(len(data)):
        for column_index in range(len(data)):
            page_0_value = data[row_index % initial_len][column_index % initial_len]
            tile_x = int(column_index / initial_len)
            tile_y = int(row_index / initial_len)
            new_value = int((page_0_value + 1 * (tile_x + tile_y)))
            if new_value > 9:
                new_value -= 9
            data[row_index][column_index] = new_value

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

    priority_queue: List[Tuple[int, Node]] = []
    heappush(priority_queue, (0, nodes[(0, 0)]))
    while priority_queue:
        while True:
            (_, current_node) = heappop(priority_queue)
            if current_node not in visited:
                break

        for node in current_node.adjacent_nodes:
            adjacent_node_distance = distances[current_node] + node.distance
            if adjacent_node_distance < distances[node]:
                distances[node] = adjacent_node_distance
                heappush(priority_queue, (adjacent_node_distance, node))
        visited.add(current_node)

    return distances[nodes[(len(data) - 1, len(data) - 1)]]


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
