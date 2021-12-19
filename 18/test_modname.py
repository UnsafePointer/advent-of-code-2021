from modname import __version__
from modname.node import (
    node_from_data,
    add_nodes,
    depth_from_node,
    split,
    explode,
    get_first_regular_node_to_left,
    get_first_regular_node_to_right,
    same_nodes,
    magnitude,
    Node,
)
from typing import List, Optional, Tuple
from functools import reduce


def test_node_from_data() -> None:
    data = [[[[1, 3], [5, 3]], [[1, 3], [8, 7]]], [[[4, 9], [6, 9]], [[8, 2], [7, 3]]]]
    node = node_from_data(data)
    assert node != None


def test_compare_nodes() -> None:
    node = node_from_data([[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]])
    assert same_nodes(node.left.left.right, node.right.left.left) == False
    assert same_nodes(node.left.left.right, node.left.left.right) == True


def test_depth_from_node() -> None:
    test_cases: List[Tuple[Node, int]] = [
        (node_from_data([1, 2]), 0),
        (node_from_data([[1, 2], 3]), 1),
        (node_from_data([[1, 9], [8, 5]]), 1),
        (node_from_data([[[[[9, 8], 1], 2], 3], 4]), 4),
    ]
    for (node, depth) in test_cases:
        assert depth_from_node(node) == depth


def test_split() -> None:
    test_cases: List[Tuple[Node, bool, Node]] = [
        (node_from_data([10, 1]), True, node_from_data([[5, 5], 1])),
        (node_from_data([11, 1]), True, node_from_data([[5, 6], 1])),
        (node_from_data([12, 1]), True, node_from_data([[6, 6], 1])),
    ]
    for (node_before_split, splitted, node_after_split) in test_cases:
        result = split(node_before_split)
        assert result == splitted
        assert node_before_split == node_after_split


def test_get_first_regular_node_to_left() -> None:
    node: Node = node_from_data([[[[[9, 8], 1], 2], 3], 4])
    test_cases: List[Tuple[Node, Node, Optional[Node]]] = [
        (
            node,
            node.left.left.left.left,
            None,
        ),
        (
            node,
            node.right,
            node.left.right,
        ),
        (
            node,
            node.left.right,
            node.left.left.right,
        ),
    ]
    for (root, node, left_node) in test_cases:
        result = get_first_regular_node_to_left(root, node)
        assert result == left_node


def test_get_first_regular_node_to_right() -> None:
    node: Node = node_from_data([[[[[9, 8], 1], 2], 3], 4])
    test_cases: List[Tuple[Node, Node, Optional[Node]]] = [
        (
            node,
            node.left.left.left.left,
            node.left.left.left.right,
        ),
        (
            node,
            node.right,
            None,
        ),
        (
            node,
            node.left.left,
            node.left.right,
        ),
    ]
    for (root, node, right_node) in test_cases:
        assert get_first_regular_node_to_right(root, node) == right_node


def test_explode() -> None:
    test_cases: List[Tuple[Node, bool, Node]] = [
        (
            node_from_data([[[[[9, 8], 1], 2], 3], 4]),
            True,
            node_from_data([[[[0, 9], 2], 3], 4]),
        ),
        (
            node_from_data([7, [6, [5, [4, [3, 2]]]]]),
            True,
            node_from_data([7, [6, [5, [7, 0]]]]),
        ),
        (
            node_from_data([[6, [5, [4, [3, 2]]]], 1]),
            True,
            node_from_data([[6, [5, [7, 0]]], 3]),
        ),
        (
            node_from_data([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]),
            True,
            node_from_data([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]),
        ),
        (
            node_from_data([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]),
            True,
            node_from_data([[3, [2, [8, 0]]], [9, [5, [7, 0]]]]),
        ),
        (
            node_from_data(
                [
                    [[[4, 0], [0, 4]], [[0, [[6, 6], 6]], [9, 5]]],
                    [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
                ]
            ),
            True,
            node_from_data(
                [
                    [[[4, 0], [0, 4]], [[6, [0, 12]], [9, 5]]],
                    [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
                ]
            ),
        ),
    ]
    for (node_before_explode, exploded, node_after_explode) in test_cases:
        result = explode(node_before_explode)
        assert result == exploded
        assert node_before_explode == node_after_explode


def test_reduce_nodes() -> None:
    test_cases: List[Tuple[List[Node], Node]] = [
        (
            [
                node_from_data([1, 2]),
                node_from_data([[3, 4], 5]),
            ],
            node_from_data([[1, 2], [[3, 4], 5]]),
        ),
        (
            [
                node_from_data([[[[4, 3], 4], 4], [7, [[8, 4], 9]]]),
                node_from_data([1, 1]),
            ],
            node_from_data([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]),
        ),
        (
            [
                node_from_data([1, 1]),
                node_from_data([2, 2]),
                node_from_data([3, 3]),
                node_from_data([4, 4]),
            ],
            node_from_data([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]),
        ),
        (
            [
                node_from_data([1, 1]),
                node_from_data([2, 2]),
                node_from_data([3, 3]),
                node_from_data([4, 4]),
                node_from_data([5, 5]),
            ],
            node_from_data([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]),
        ),
        (
            [
                node_from_data([1, 1]),
                node_from_data([2, 2]),
                node_from_data([3, 3]),
                node_from_data([4, 4]),
                node_from_data([5, 5]),
                node_from_data([6, 6]),
            ],
            node_from_data([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]),
        ),
        (
            [
                node_from_data([[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]]),
                node_from_data([7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]),
                node_from_data([[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]]),
                node_from_data(
                    [[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]]
                ),
                node_from_data([7, [5, [[3, 8], [1, 4]]]]),
                node_from_data([[2, [2, 2]], [8, [8, 1]]]),
                node_from_data([2, 9]),
                node_from_data([1, [[[9, 3], 9], [[9, 0], [0, 7]]]]),
                node_from_data([[[5, [7, 4]], 7], 1]),
                node_from_data([[[[4, 2], 2], 6], [8, 7]]),
            ],
            node_from_data(
                [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
            ),
        ),
    ]
    for (nodes, expected_result) in test_cases:
        result = reduce(lambda left, right: add_nodes(left, right), nodes)
        assert result == expected_result


def test_magnitude() -> None:
    test_cases: List[Tuple[Node, int]] = [
        (node_from_data([1, 9]), 21),
        (node_from_data([[9, 1], [1, 9]]), 129),
        (node_from_data([[1, 2], [[3, 4], 5]]), 143),
        (node_from_data([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]), 1384),
        (node_from_data([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]), 445),
        (node_from_data([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]), 791),
        (node_from_data([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]), 1137),
        (
            node_from_data(
                [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
            ),
            3488,
        ),
    ]
    for (node, result) in test_cases:
        assert magnitude(node) == result
