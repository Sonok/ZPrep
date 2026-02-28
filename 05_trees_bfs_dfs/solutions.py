"""
=============================================================================
PATTERN 5: TREES — BFS & DFS — SOLUTIONS
=============================================================================
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------------------
# Problem 1: Binary Tree Level Order Traversal
# ---------------------------------------------------------------------------
# APPROACH: BFS with a queue.
#   - Use deque, process one level at a time
#   - Key trick: len(queue) at the start of each iteration = level size
#
# TIME: O(n)   SPACE: O(n)
#
# BFS TEMPLATE:
#   queue = deque([root])
#   while queue:
#       for _ in range(len(queue)):  ← THIS processes one level
#           node = queue.popleft()
#           ... process node ...
#           if node.left: queue.append(node.left)
#           if node.right: queue.append(node.right)
# ---------------------------------------------------------------------------
def level_order(root: TreeNode) -> list[list[int]]:
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result


# ---------------------------------------------------------------------------
# Problem 2: Validate Binary Search Tree
# ---------------------------------------------------------------------------
# APPROACH: DFS with bounds (low, high).
#   - Each node must be within (low, high) exclusive
#   - Go left: update high to node.val
#   - Go right: update low to node.val
#
# TIME: O(n)   SPACE: O(h) where h = height
#
# COMMON MISTAKE: Only checking node.left.val < node.val < node.right.val
# is NOT enough. Must check ALL ancestors' constraints.
#
# TRICK TO REMEMBER: "Pass bounds down the tree."
# ---------------------------------------------------------------------------
def is_valid_bst(root: TreeNode) -> bool:
    def validate(node, low=float("-inf"), high=float("inf")):
        if not node:
            return True
        if node.val <= low or node.val >= high:
            return False
        return validate(node.left, low, node.val) and validate(
            node.right, node.val, high
        )

    return validate(root)


# ---------------------------------------------------------------------------
# Problem 3: Lowest Common Ancestor of a Binary Tree
# ---------------------------------------------------------------------------
# APPROACH: Recursive DFS.
#   - If root is None or root is p or q → return root
#   - Recurse left and right
#   - If both return non-None → root is the LCA (split point)
#   - Otherwise return whichever side is non-None
#
# TIME: O(n)   SPACE: O(h)
#
# WHY IT WORKS: We're searching for p and q. The first node where the
# search results from left and right are both non-None is where the
# paths to p and q diverge — that's the LCA.
#
# TRICK TO REMEMBER: "Post-order: ask children, then decide at parent."
# ---------------------------------------------------------------------------
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root  # split point = LCA
    return left if left else right


# ---------------------------------------------------------------------------
# Problem 4: Diameter of Binary Tree
# ---------------------------------------------------------------------------
# APPROACH: DFS computing height, tracking max diameter as side effect.
#   - Diameter through a node = left_height + right_height
#   - Height of a node = 1 + max(left_height, right_height)
#   - Use a nonlocal variable to track the global max diameter
#
# TIME: O(n)   SPACE: O(h)
#
# TRICK TO REMEMBER: "Compute height, but track diameter as a side effect."
# The diameter at any node = left_height + right_height.
# ---------------------------------------------------------------------------
def diameter_of_binary_tree(root: TreeNode) -> int:
    diameter = 0

    def height(node):
        nonlocal diameter
        if not node:
            return 0
        left_h = height(node.left)
        right_h = height(node.right)
        diameter = max(diameter, left_h + right_h)
        return 1 + max(left_h, right_h)

    height(root)
    return diameter
