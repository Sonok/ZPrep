"""
=============================================================================
PATTERN 5: TREES — BFS & DFS
=============================================================================

HOW TO RECOGNIZE:
- Given a TreeNode / binary tree
- "Level order" → BFS
- "Path sum", "depth", "validate BST" → DFS (recursive)
- "Serialize/deserialize" → BFS or DFS
- "Lowest common ancestor" → DFS

KEY IDEA:
  DFS: Go deep first. Use recursion (or explicit stack).
    - Preorder:  root → left → right  (process root first)
    - Inorder:   left → root → right  (gives sorted order for BST)
    - Postorder: left → right → root  (process children before root)

  BFS: Go level by level. Use a queue.
    - Process all nodes at depth d before depth d+1

AMAZON FAVORITES:
  - Binary Tree Level Order Traversal
  - Validate Binary Search Tree
  - Lowest Common Ancestor
  - Maximum Depth / Diameter of Binary Tree
=============================================================================
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------------------
# Problem 1: Binary Tree Level Order Traversal (LC 102)
# ---------------------------------------------------------------------------
# Given the root of a binary tree, return the level order traversal
# as a list of lists (each inner list = one level).
#
# Example:
#       3
#      / \
#     9  20
#        / \
#       15  7
#   Output: [[3], [9, 20], [15, 7]]
# ---------------------------------------------------------------------------
def level_order(root: TreeNode) -> list[list[int]]:
    q = deque()
    if not root:
      return []

    out = []
    q.append(root)
    while(q):
      count = len(q)
      lst = []
      for i in range(count):
        node =  q.popleft()
        lst.append(node.val)
        if node.left:
          q.append(node.left)
        if node.right:
          q.append(node.right)
      out.append(lst)
    return out


# ---------------------------------------------------------------------------
# Problem 2: Validate Binary Search Tree (LC 98)
# ---------------------------------------------------------------------------
# Given the root of a binary tree, determine if it is a valid BST.
# A valid BST: left subtree values < node < right subtree values (strictly).
#
# Example:
#       2
#      / \
#     1   3    → True
#
#       5
#      / \
#     1   4
#        / \
#       3   6  → False (3 < 5 but is in right subtree)
# ---------------------------------------------------------------------------
def is_valid_bst(root: TreeNode) -> bool:
    # we can run a inorder traversal. We see if that is in order then it's correct
    def inorder(node):
      if not node:
        return []
      return inorder(node.left) + [node] + inorder(node.right)
    
    lstInorder = inorder(root)
    for i in range(len(lstInorder) - 1):
      if lstInorder[i].val >= lstInorder[i+1].val:
        return False
    return True


# ---------------------------------------------------------------------------
# Problem 3: Lowest Common Ancestor of a Binary Tree (LC 236)
# ---------------------------------------------------------------------------
# Given root and two nodes p, q, find their lowest common ancestor.
# LCA = deepest node that has both p and q as descendants (a node can
# be a descendant of itself).
#
# Example:
#         3
#        / \
#       5   1
#      / \ / \
#     6  2 0  8
#       / \
#      7   4
#   p=5, q=1 → LCA = 3
#   p=5, q=4 → LCA = 5
# ---------------------------------------------------------------------------
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: Diameter of Binary Tree (LC 543)
# ---------------------------------------------------------------------------
# The diameter is the length of the longest path between any two nodes
# (measured in number of EDGES). The path may or may not pass through root.
#
# Example:
#       1
#      / \
#     2   3
#    / \
#   4   5
#   Output: 3  (path: 4 → 2 → 1 → 3, or 5 → 2 → 1 → 3)
# ---------------------------------------------------------------------------
def diameter_of_binary_tree(root: TreeNode) -> int:
    pass  # YOUR CODE HERE


# ========================== TEST YOUR SOLUTIONS ==========================
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING TREES — BFS & DFS")
    print("=" * 60)

    # Test Problem 1: Level Order
    print("\n--- Level Order Traversal ---")
    tree1 = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert level_order(tree1) == [[3], [9, 20], [15, 7]], "Test 1 failed"
    assert level_order(None) == [], "Test 2 failed"
    assert level_order(TreeNode(1)) == [[1]], "Test 3 failed"
    print("All tests passed!")

    # Test Problem 2: Validate BST
    print("\n--- Validate BST ---")
    bst_valid = TreeNode(2, TreeNode(1), TreeNode(3))
    assert is_valid_bst(bst_valid) == True, "Test 1 failed"
    bst_invalid = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
    assert is_valid_bst(bst_invalid) == False, "Test 2 failed"
    print("All tests passed!")

    # Test Problem 3: LCA
    print("\n--- Lowest Common Ancestor ---")
    #         3
    #        / \
    #       5   1
    #      / \
    #     6   2
    n6 = TreeNode(6)
    n2 = TreeNode(2)
    n5 = TreeNode(5, n6, n2)
    n1 = TreeNode(1)
    n3 = TreeNode(3, n5, n1)
    assert lowest_common_ancestor(n3, n5, n1) == n3, "Test 1 failed"
    assert lowest_common_ancestor(n3, n5, n2) == n5, "Test 2 failed"
    print("All tests passed!")

    # Test Problem 4: Diameter
    print("\n--- Diameter of Binary Tree ---")
    dtree = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    assert diameter_of_binary_tree(dtree) == 3, "Test 1 failed"
    assert diameter_of_binary_tree(TreeNode(1, TreeNode(2))) == 1, "Test 2 failed"
    print("All tests passed!")

    print("\n" + "=" * 60)
    print("ALL TREE PROBLEMS SOLVED!")
    print("=" * 60)
