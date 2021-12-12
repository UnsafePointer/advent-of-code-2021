from __future__ import annotations
from typing import DefaultDict, Dict, Set
from dataclasses import dataclass, field


@dataclass
class Node:
    name: str
    neighbors: Set[Node] = field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.name)


def count_paths(
    to_visit: Node,
    visited: Set[Node],
    visited_times: Dict[Node, int],
    already_visited_twice: bool,
) -> int:
    if to_visit in visited and to_visit.name.islower() and already_visited_twice:
        return 0
    if to_visit.name == "end":
        return 1
    if to_visit.name == "start" and to_visit in visited:
        return 0
    visited.add(to_visit)
    if to_visit.name.islower():
        visited_times[to_visit] += 1
        if visited_times[to_visit] >= 2:
            already_visited_twice = True
    paths = 0
    for neighbor in to_visit.neighbors:
        paths += count_paths(
            neighbor, visited.copy(), visited_times.copy(), already_visited_twice
        )
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
    visited_times: DefaultDict[Node, int] = DefaultDict(lambda: 0)

    return count_paths(nodes["start"], visited, visited_times, False)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
