"""
=============================================================================
PATTERN 9: HEAP / PRIORITY QUEUE — SOLUTIONS
=============================================================================
"""

import heapq
from collections import Counter


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ---------------------------------------------------------------------------
# Problem 1: Kth Largest Element in an Array
# ---------------------------------------------------------------------------
# APPROACH: Min-heap of size k.
#   - Push elements into heap
#   - If heap size > k, pop the smallest
#   - After processing all elements, heap[0] is the kth largest
#
# TIME: O(n log k)   SPACE: O(k)
#
# ALTERNATIVE: quickselect for O(n) average, but heap is simpler to code.
#
# TRICK TO REMEMBER: "Kth largest → min-heap of size k."
# The heap holds the k largest elements, and the smallest of those (top)
# is exactly the kth largest.
# ---------------------------------------------------------------------------
def find_kth_largest(nums: list[int], k: int) -> int:
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


# ---------------------------------------------------------------------------
# Problem 2: Merge K Sorted Lists
# ---------------------------------------------------------------------------
# APPROACH: Min-heap of (value, index, node).
#   - Push the head of each list into heap
#   - Pop smallest, add to result, push its next node
#   - index is needed for tie-breaking (ListNode isn't comparable)
#
# TIME: O(N log k) where N = total nodes   SPACE: O(k)
#
# TRICK TO REMEMBER: "Heap always has k elements (one from each list).
# Pop min, advance that list, repeat."
# ---------------------------------------------------------------------------
def merge_k_lists(lists: list[ListNode]) -> ListNode:
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    curr = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next


# ---------------------------------------------------------------------------
# Problem 3: Find Median from Data Stream
# ---------------------------------------------------------------------------
# APPROACH: Two heaps — max-heap (lower half) + min-heap (upper half).
#   - max_heap stores the smaller half (negate for max-heap in Python)
#   - min_heap stores the larger half
#   - Keep balanced: len(max_heap) == len(min_heap) or len(max_heap) == len(min_heap) + 1
#   - Median = max_heap[0] (odd) or average of both tops (even)
#
# TIME: O(log n) per add, O(1) for median   SPACE: O(n)
#
# TRICK TO REMEMBER: "Two heaps split the data in half.
# max-heap top = largest of lower half, min-heap top = smallest of upper half.
# Median is at the boundary."
# ---------------------------------------------------------------------------
class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (negated) — lower half
        self.hi = []  # min-heap — upper half

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        # Balance: largest of lo must <= smallest of hi
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # Keep lo same size or 1 bigger
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2


# ---------------------------------------------------------------------------
# Problem 4: Task Scheduler
# ---------------------------------------------------------------------------
# APPROACH: Math / greedy.
#   - The most frequent task determines the structure
#   - max_freq = max frequency of any task
#   - max_count = how many tasks have this max frequency
#   - Formula: (max_freq - 1) * (n + 1) + max_count
#   - Answer = max(formula, len(tasks)) — never less than total tasks
#
# TIME: O(n)   SPACE: O(1) (26 chars max)
#
# VISUALIZATION for tasks=[A,A,A,B,B,B], n=2:
#   A B _ | A B _ | A B    ← (3-1) * (2+1) + 2 = 8
#   ^frames^         ^tail^
#
# TRICK TO REMEMBER: "Build a grid: (max_freq - 1) rows of width (n+1),
# plus a partial last row of width max_count."
# ---------------------------------------------------------------------------
def least_interval(tasks: list[str], n: int) -> int:
    freq = Counter(tasks)
    max_freq = max(freq.values())
    max_count = sum(1 for f in freq.values() if f == max_freq)
    return max((max_freq - 1) * (n + 1) + max_count, len(tasks))
