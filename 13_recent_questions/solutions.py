"""
=============================================================================
RECENTLY LEAKED AMAZON QUESTIONS — SOLUTIONS (Jan–Mar 2026)
=============================================================================
"""

from collections import defaultdict, deque
from itertools import combinations
import bisect


# ---------------------------------------------------------------------------
# Problem 1: Analyzing One-Time Visitors
# ---------------------------------------------------------------------------
# APPROACH: Count visits per user with a dict, filter for count == 1.
#
# TIME: O(n)   SPACE: O(n)
#
# TRICK TO REMEMBER: "Frequency count, then filter."
# Classic hash map frequency problem — straightforward.
# ---------------------------------------------------------------------------
def one_time_visitors(logs: list[list[str]]) -> list[str]:
    visit_count = {}
    for user_id, page in logs:
        visit_count[user_id] = visit_count.get(user_id, 0) + 1
    return sorted(uid for uid, count in visit_count.items() if count == 1)


# Follow-up: also return the page they visited
def one_time_visitors_with_pages(logs: list[list[str]]) -> list[tuple[str, str]]:
    visit_count = {}
    first_page = {}
    for user_id, page in logs:
        visit_count[user_id] = visit_count.get(user_id, 0) + 1
        if user_id not in first_page:
            first_page[user_id] = page
    return sorted(
        (uid, first_page[uid]) for uid, count in visit_count.items() if count == 1
    )


# ---------------------------------------------------------------------------
# Problem 2: Word Break II (LC 140)
# ---------------------------------------------------------------------------
# APPROACH: Backtracking with memoization.
#   - Try every word in dict as a prefix of s
#   - If it matches, recursively solve for the remainder
#   - Memoize results for each starting index
#
# TIME: O(n * 2^n) worst case   SPACE: O(n * 2^n) for all sentences
#
# TRICK TO REMEMBER: "Try each word as prefix, recurse on suffix."
# Use a set for O(1) word lookup. Memo maps index -> list of sentences.
# ---------------------------------------------------------------------------
def word_break_ii(s: str, wordDict: list[str]) -> list[str]:
    word_set = set(wordDict)
    memo = {}

    def backtrack(start):
        if start in memo:
            return memo[start]
        if start == len(s):
            return [""]

        sentences = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                rest = backtrack(end)
                for sentence in rest:
                    if sentence:
                        sentences.append(word + " " + sentence)
                    else:
                        sentences.append(word)
        memo[start] = sentences
        return sentences

    return backtrack(0)


# ---------------------------------------------------------------------------
# Problem 3: Unique Morse Code Words (LC 804)
# ---------------------------------------------------------------------------
# APPROACH: Map each word to its Morse code, use a set for uniqueness.
#
# TIME: O(n * k) where k = avg word length   SPACE: O(n)
#
# TRICK TO REMEMBER: "Map + set = unique transformations."
# ---------------------------------------------------------------------------
def unique_morse_representations(words: list[str]) -> int:
    morse = [".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..",
             ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.",
             "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."]
    seen = set()
    for word in words:
        code = "".join(morse[ord(c) - ord('a')] for c in word)
        seen.add(code)
    return len(seen)


# ---------------------------------------------------------------------------
# Problem 4: Copy List with Random Pointer (LC 138)
# ---------------------------------------------------------------------------
# APPROACH: Hash map — old node -> new node.
#   - First pass: create all new nodes, store mapping
#   - Second pass: wire up next and random pointers using the map
#
# TIME: O(n)   SPACE: O(n)
#
# TRICK TO REMEMBER: "Two passes: create nodes, then wire pointers."
# The map lets you find the copy of any original node in O(1).
#
# ALTERNATIVE: O(1) space interleaving approach — insert copies between
# originals, set random pointers, then separate the lists.
# ---------------------------------------------------------------------------
class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list(head: 'Node') -> 'Node':
    if not head:
        return None

    # First pass: create copies
    old_to_new = {}
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next

    # Second pass: wire pointers
    curr = head
    while curr:
        old_to_new[curr].next = old_to_new.get(curr.next)
        old_to_new[curr].random = old_to_new.get(curr.random)
        curr = curr.next

    return old_to_new[head]


# ---------------------------------------------------------------------------
# Problem 5: Next Greater Element II (Monotonic Stack)
# ---------------------------------------------------------------------------
# APPROACH: Monotonic decreasing stack + circular traversal (2 passes).
#   - Traverse the array twice (simulating circular)
#   - Stack stores indices of elements waiting for a greater element
#   - When we find a greater element, pop and record it
#
# TIME: O(n)   SPACE: O(n)
#
# TRICK TO REMEMBER: "Circular = traverse 2x. Stack holds indices waiting
# for their next greater. Pop when you find something bigger."
# ---------------------------------------------------------------------------
def next_greater_elements(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices

    for i in range(2 * n):
        while stack and nums[stack[-1]] < nums[i % n]:
            result[stack.pop()] = nums[i % n]
        if i < n:
            stack.append(i)

    return result


# ---------------------------------------------------------------------------
# Problem 6: EC2 Instance Allocation Cost
# ---------------------------------------------------------------------------
# APPROACH: Greedy — sort tasks, for each task find smallest fitting instance.
#   - Sort tasks ascending
#   - For each task, binary search for the smallest instance >= task size
#   - Remove that instance (each can only be used once)
#   - If no instance fits, return -1 (impossible)
#
# TIME: O(t log t + t log i) where t = tasks, i = instances
# SPACE: O(i)
#
# TRICK TO REMEMBER: "Sort tasks, greedily assign smallest fitting instance."
# ---------------------------------------------------------------------------
def min_allocation_cost(instances: list[int], tasks: list[int]) -> int:
    available = sorted(instances)
    tasks_sorted = sorted(tasks)
    total_cost = 0

    for task in tasks_sorted:
        idx = bisect.bisect_left(available, task)
        if idx == len(available):
            return -1  # no instance big enough
        total_cost += available[idx]
        available.pop(idx)

    return total_cost


# ---------------------------------------------------------------------------
# Problem 7: Frequent Item Pair
# ---------------------------------------------------------------------------
# APPROACH: For each transaction, generate all pairs. Count pair frequency.
#   - Sort items in each transaction to get canonical pair ordering
#   - Use combinations(sorted_transaction, 2) for all pairs
#   - Track counts in a dict, return max (ties broken lexicographically)
#
# TIME: O(T * k^2) where T = transactions, k = items per transaction
# SPACE: O(P) where P = unique pairs
#
# TRICK TO REMEMBER: "Generate sorted pairs, count with dict, return max."
# ---------------------------------------------------------------------------
def most_frequent_pair(transactions: list[list[int]]) -> list[int]:
    pair_count = defaultdict(int)
    for transaction in transactions:
        for pair in combinations(sorted(transaction), 2):
            pair_count[pair] += 1

    # Find max frequency, then lexicographically smallest pair with that freq
    max_freq = max(pair_count.values())
    best = min(pair for pair, count in pair_count.items() if count == max_freq)
    return list(best)


# ---------------------------------------------------------------------------
# Problem 8: Min Days to Complete Releases (Topological Sort / BFS)
# ---------------------------------------------------------------------------
# APPROACH: BFS topological sort, counting levels.
#   - Build adjacency list and in-degree array
#   - Start BFS with all nodes that have in-degree 0 (no dependencies)
#   - Each BFS level = one day
#   - Number of levels = minimum days
#
# TIME: O(n + e)   SPACE: O(n + e)
#
# TRICK TO REMEMBER: "Topological BFS levels = minimum parallel rounds."
# This is Kahn's algorithm with level counting.
# ---------------------------------------------------------------------------
def min_days_to_release(n: int, dependencies: list[list[int]]) -> int:
    adj = defaultdict(list)
    in_degree = [0] * n
    for module, dep in dependencies:
        adj[dep].append(module)
        in_degree[module] += 1

    # Start with all modules that have no dependencies
    queue = deque(i for i in range(n) if in_degree[i] == 0)
    days = 0

    while queue:
        days += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    return days


# ---------------------------------------------------------------------------
# Problem 9: Merge Sorted Arrays (LC 88)
# ---------------------------------------------------------------------------
# APPROACH: Three pointers, merge from the back.
#   - Start from the end of both arrays
#   - Place the larger element at the end of nums1
#   - This avoids shifting elements forward
#
# TIME: O(m + n)   SPACE: O(1)
#
# TRICK TO REMEMBER: "Merge from the back. The empty slots are at the end
# of nums1, so fill them right-to-left with the largest remaining element."
# ---------------------------------------------------------------------------
def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    p1 = m - 1
    p2 = n - 1
    p = m + n - 1

    while p2 >= 0:
        if p1 >= 0 and nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
