from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Any, List
from math import floor, ceil
import uuid


@dataclass
class Node:
    value: Optional[int]
    id: uuid.UUID
    parent: Optional[Node] = None
    left: Optional[Node] = None
    right: Optional[Node] = None

    def is_end_node(self) -> bool:
        left = self.left != None and self.left.value != None
        right = self.right != None and self.right.value != None
        return left and right

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return compare_nodes(self, __o)
        if __o == None:
            return False
        else:
            raise RuntimeError(
                f"Unsupported comparison with instance of class: {__o.__class__.__name__}"
            )

    def __repr__(self) -> str:
        return stringify(self)


def visit_leaves(node: Node) -> None:
    if node.right != None:
        visit_leaves(node.right)
    if node.value != None:
        print(node.value, end=" ")
    if node.left != None:
        visit_leaves(node.left)


def stringify(node: Node) -> str:
    if node.value != None:
        return str(node.value)
    return "[" + stringify(node.left) + ", " + stringify(node.right) + "]"


def compare_nodes(node_a: Node, node_b: Node) -> bool:
    if node_a.value == None and node_b.value == None:
        return compare_nodes(node_a.left, node_b.left) and compare_nodes(
            node_a.right, node_b.right
        )
    elif (node_a.value == None and node_b.value != None) or (
        node_a.value != None and node_b.value == None
    ):
        return False
    else:
        return node_a.value == node_b.value


def get_children(node: Node, children: List[Node]) -> None:
    if node == None:
        return
    children.append(node)
    get_children(node.left, children)
    get_children(node.right, children)
    return


def same_nodes(node_a: Node, node_b: Node) -> bool:
    return node_a.id == node_b.id


def node_from_data(data: Any, parent: Optional[Node] = None) -> Node:
    if isinstance(data, int):
        return Node(value=data, parent=parent, id=uuid.uuid4())
    elif isinstance(data, List):
        node = Node(value=None, parent=parent, id=uuid.uuid4())
        node.left = node_from_data(data[0], node)
        node.right = node_from_data(data[-1], node)
        return node
    else:
        raise RuntimeError(f"Unsupported data class: {data.__class__.__name__}")


def add_nodes(left: Node, right: Node) -> Node:
    result = Node(value=None, left=left, right=right, id=uuid.uuid4())
    return reduce_nodes(result)


def depth_from_node_recursive(node: Node) -> int:
    if node.value != None:
        return 0
    else:
        return 1 + max(
            depth_from_node_recursive(node.left), depth_from_node_recursive(node.right)
        )


def depth_from_node(node: Node) -> int:
    return depth_from_node_recursive(node) - 1


def get_first_regular_node_to_left_with_pre_order_traversal(
    current_node: Optional[Node],
    node_to_find: Optional[Node],
    visited_leaves: List[Node],
) -> None:
    if current_node == None:
        return None
    if same_nodes(current_node, node_to_find):
        if visited_leaves:
            return visited_leaves.pop()
        else:
            return None
    if current_node.value != None:
        visited_leaves.append(current_node)
    result = get_first_regular_node_to_left_with_pre_order_traversal(
        current_node.left, node_to_find, visited_leaves
    )
    if result:
        return result
    else:
        return get_first_regular_node_to_left_with_pre_order_traversal(
            current_node.right, node_to_find, visited_leaves
        )


def get_first_regular_node_to_left(root: Node, node: Node) -> Optional[None]:
    return get_first_regular_node_to_left_with_pre_order_traversal(root, node, [])


def get_first_regular_node_to_right_with_post_order_traversal(
    current_node: Optional[Node],
    node_to_find: Optional[Node],
    visited_leaves: List[Node],
) -> None:
    if current_node == None:
        return None
    if same_nodes(current_node, node_to_find):
        if visited_leaves:
            return visited_leaves.pop()
        else:
            return None
    if current_node.value != None:
        visited_leaves.append(current_node)
    result = get_first_regular_node_to_right_with_post_order_traversal(
        current_node.right, node_to_find, visited_leaves
    )
    if result:
        return result
    else:
        return get_first_regular_node_to_right_with_post_order_traversal(
            current_node.left, node_to_find, visited_leaves
        )


def get_first_regular_node_to_right(root: Node, node: Node) -> Optional[None]:
    return get_first_regular_node_to_right_with_post_order_traversal(root, node, [])


def explode_deepest_left(root: Node, node: Node, depth: int) -> bool:
    if node == None:
        return False
    if not node.is_end_node():
        if explode_deepest_left(root, node.left, depth + 1):
            return True
        else:
            return explode_deepest_left(root, node.right, depth + 1)
    if depth < 4:
        return False

    node_to_left = get_first_regular_node_to_left(root, node)
    if node_to_left != None:
        node_to_left.value += node.left.value
    node_to_right = get_first_regular_node_to_right(root, node)
    if node_to_right != None:
        node_to_right.value += node.right.value
    node.left = None
    node.right = None
    node.value = 0
    return True


def explode(node: Node) -> bool:
    if depth_from_node(node) < 4:
        return False

    return explode_deepest_left(node, node, 0)


def split(node: Node) -> bool:
    if node.value != None:
        if node.value >= 10:
            node.left = Node(value=floor(node.value / 2), parent=node, id=uuid.uuid4())
            node.right = Node(value=ceil(node.value / 2), parent=node, id=uuid.uuid4())
            node.value = None
            return True
        else:
            return False
    if split(node.left):
        return True
    if split(node.right):
        return True
    return False


def reduce_nodes(node: Node) -> Node:
    if explode(node):
        return reduce_nodes(node)
    if split(node):
        return reduce_nodes(node)
    return node


def magnitude(node: Node) -> int:
    if node.is_end_node():
        return node.left.value * 3 + node.right.value * 2
    elif node.value != None:
        return node.value
    else:
        return 3 * magnitude(node.left) + 2 * magnitude(node.right)
