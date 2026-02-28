"""
=============================================================================
PATTERN 6: GRAPHS — BFS & DFS — SOLUTIONS
=============================================================================
"""

from collections import deque, defaultdict


# ---------------------------------------------------------------------------
# Problem 1: Number of Islands
# ---------------------------------------------------------------------------
# APPROACH: DFS/BFS flood fill.
#   - Scan grid for '1'. When found, increment count and flood fill
#     (mark all connected '1's as '0' or visited).
#
# TIME: O(m * n)   SPACE: O(m * n) worst case for DFS stack
#
# GRID BFS/DFS TEMPLATE:
#   directions = [(0,1),(0,-1),(1,0),(-1,0)]
#   for dr, dc in directions:
#       nr, nc = r + dr, c + dc
#       if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
#           ...
# ---------------------------------------------------------------------------
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"  # mark visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)
    return count


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


# ---------------------------------------------------------------------------
# Problem 2: Rotting Oranges
# ---------------------------------------------------------------------------
# APPROACH: Multi-source BFS.
#   - Start BFS from ALL rotten oranges simultaneously (add all to queue)
#   - Each BFS level = 1 minute
#   - After BFS, if any fresh oranges remain → return -1
#
# TIME: O(m * n)   SPACE: O(m * n)
#
# TRICK TO REMEMBER: "Multi-source BFS = add all sources to queue at start."
# This gives shortest distance from ANY source, not just one.
# ---------------------------------------------------------------------------
def oranges_rotting(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    # Find all rotten oranges and count fresh ones
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0

    minutes = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while queue:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))

    return minutes - 1 if fresh == 0 else -1


# ---------------------------------------------------------------------------
# Problem 3: Clone Graph
# ---------------------------------------------------------------------------
# APPROACH: DFS/BFS with a hash map {old_node: cloned_node}.
#   - If node already cloned (in map), return the clone
#   - Otherwise create clone, add to map, recurse on neighbors
#
# TIME: O(V + E)   SPACE: O(V)
#
# TRICK TO REMEMBER: "Hash map from old → new prevents infinite loops
# and handles the 'visited' logic simultaneously."
# ---------------------------------------------------------------------------
def clone_graph(node: "Node") -> "Node":
    if not node:
        return None

    cloned = {}

    def dfs(n):
        if n in cloned:
            return cloned[n]
        copy = Node(n.val)
        cloned[n] = copy
        for neighbor in n.neighbors:
            copy.neighbors.append(dfs(neighbor))
        return copy

    return dfs(node)


# ---------------------------------------------------------------------------
# Problem 4: Course Schedule (Topological Sort)
# ---------------------------------------------------------------------------
# APPROACH: Kahn's algorithm (BFS-based topological sort).
#   1. Build adjacency list and in-degree count
#   2. Start with all nodes having in-degree 0 (no prerequisites)
#   3. BFS: process node, decrement in-degree of neighbors
#   4. If a neighbor reaches in-degree 0, add to queue
#   5. If we process all nodes → no cycle → True
#
# TIME: O(V + E)   SPACE: O(V + E)
#
# ALTERNATIVE: DFS with 3-color marking (white/gray/black) for cycle
# detection. Kahn's is more intuitive for interviews.
#
# TRICK TO REMEMBER: "Kahn's = BFS starting from nodes with no dependencies."
# ---------------------------------------------------------------------------
def can_finish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    graph = defaultdict(list)
    in_degree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # Start with courses that have no prerequisites
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    completed = 0

    while queue:
        course = queue.popleft()
        completed += 1
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)

    return completed == numCourses
