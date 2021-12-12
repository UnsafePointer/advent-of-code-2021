from __future__ import annotations
from typing import Dict, Set
from dataclasses import dataclass, field


@dataclass
class Node:
    name: str
    neighbors: Set[Node] = field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.name)


def count_paths(to_visit: Node, visited: Set[Node]) -> int:
    if to_visit in visited and to_visit.name.islower():
        return 0
    if to_visit.name == "end":
        return 1
    visited.add(to_visit)
    paths = 0
    for neighbor in to_visit.neighbors:
        paths += count_paths(neighbor, visited.copy())
    return paths


def solve() -> int:
    nodes: Dict[str, Node] = {}

    input = open("input.txt", "r")
    for (origin, destination) in [
        tuple(line.strip().split("-")) for line in input.readlines()
    ]:
        origin_node: Node
        destination_node: Node
        if origin not in nodes:
            origin_node = Node(origin)
            nodes[origin] = origin_node
        else:
            origin_node = nodes[origin]
        if destination not in nodes:
            destination_node = Node(destination)
            nodes[destination] = destination_node
        else:
            destination_node = nodes[destination]
        origin_node.neighbors.add(destination_node)
        destination_node.neighbors.add(origin_node)

    visited: Set[Node] = set()

    return count_paths(nodes["start"], visited)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
