"""
=============================================================================
PATTERN 6: GRAPHS — BFS & DFS
=============================================================================

HOW TO RECOGNIZE:
- Grid problems ("island", "maze", "shortest path in grid")
- "Connected components", "cycle detection"
- Adjacency list / matrix given
- "Can you reach from A to B?"
- Topological ordering ("course schedule", "build order")

KEY IDEA:
  BFS: Shortest path in unweighted graph. Use queue + visited set.
  DFS: Explore all paths, connected components, cycle detection.
  Topological Sort: Order tasks with dependencies (DAG).

  For grids: each cell is a node, 4-directional neighbors are edges.

AMAZON FAVORITES:
  - Number of Islands
  - Rotting Oranges (BFS on grid)
  - Clone Graph
  - Course Schedule (topological sort)
=============================================================================
"""

from collections import deque, defaultdict


# ---------------------------------------------------------------------------
# Problem 1: Number of Islands (LC 200)
# ---------------------------------------------------------------------------
# Given an m x n grid of '1's (land) and '0's (water), count the number
# of islands. An island is surrounded by water and is formed by connecting
# adjacent land cells horizontally or vertically.
#
# Example:
#   grid = [
#     ["1","1","0","0","0"],
#     ["1","1","0","0","0"],
#     ["0","0","1","0","0"],
#     ["0","0","0","1","1"]
#   ]
#   Output: 3
# ---------------------------------------------------------------------------
def num_islands(grid: list[list[str]]) -> int:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 2: Rotting Oranges (LC 994)
# ---------------------------------------------------------------------------
# In a grid, 0 = empty, 1 = fresh orange, 2 = rotten orange.
# Every minute, fresh oranges adjacent (4-dir) to rotten ones become rotten.
# Return the minimum minutes until no fresh orange remains, or -1.
#
# Example:
#   grid = [[2,1,1],[1,1,0],[0,1,1]]
#   Output: 4
# ---------------------------------------------------------------------------
def oranges_rotting(grid: list[list[int]]) -> int:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 3: Clone Graph (LC 133)
# ---------------------------------------------------------------------------
# Given a reference to a node in a connected undirected graph, return a
# deep copy. Each node has val (int) and neighbors (list[Node]).
#
# Use the Node class below.
# ---------------------------------------------------------------------------
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node: "Node") -> "Node":
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: Course Schedule (LC 207) — Topological Sort
# ---------------------------------------------------------------------------
# There are numCourses courses (0 to n-1). prerequisites[i] = [a, b]
# means you must take b before a. Return True if you can finish all courses.
#
# (This is: "Does the directed graph have a cycle?")
#
# Example:
#   numCourses = 2, prerequisites = [[1,0]]  → True
#   numCourses = 2, prerequisites = [[1,0],[0,1]]  → False (cycle)
# ---------------------------------------------------------------------------
def can_finish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    pass  # YOUR CODE HERE


# ========================== TEST YOUR SOLUTIONS ==========================
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING GRAPHS")
    print("=" * 60)

    # Test Problem 1
    print("\n--- Number of Islands ---")
    grid1 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert num_islands(grid1) == 3, "Test 1 failed"
    grid2 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert num_islands(grid2) == 1, "Test 2 failed"
    print("All tests passed!")

    # Test Problem 2
    print("\n--- Rotting Oranges ---")
    assert oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4, "Test 1 failed"
    assert oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1, "Test 2 failed"
    assert oranges_rotting([[0, 2]]) == 0, "Test 3 failed"
    print("All tests passed!")

    # Test Problem 3
    print("\n--- Clone Graph ---")
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n1.neighbors = [n2, n3]
    n2.neighbors = [n1, n3]
    n3.neighbors = [n1, n2]
    cloned = clone_graph(n1)
    assert cloned is not n1, "Should be a new node"
    assert cloned.val == 1, "Test 1 failed"
    assert len(cloned.neighbors) == 2, "Test 2 failed"
    assert cloned.neighbors[0] is not n2, "Neighbors should be cloned"
    print("All tests passed!")

    # Test Problem 4
    print("\n--- Course Schedule ---")
    assert can_finish(2, [[1, 0]]) == True, "Test 1 failed"
    assert can_finish(2, [[1, 0], [0, 1]]) == False, "Test 2 failed"
    assert can_finish(4, [[1, 0], [2, 1], [3, 2]]) == True, "Test 3 failed"
    print("All tests passed!")

    print("\n" + "=" * 60)
    print("ALL GRAPH PROBLEMS SOLVED!")
    print("=" * 60)
