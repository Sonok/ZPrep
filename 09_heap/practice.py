"""
=============================================================================
PATTERN 9: HEAP / PRIORITY QUEUE
=============================================================================

HOW TO RECOGNIZE:
- "Find the Kth largest/smallest"
- "Merge K sorted lists/arrays"
- "Continuously find min/max" from a stream
- "Median from data stream"
- Scheduling problems, "next event"

KEY IDEA:
  A heap gives O(log n) insert and O(1) access to min (or max).

  Python's heapq is a MIN-HEAP. For max-heap, negate the values.

  Common patterns:
  - Top K: use a min-heap of size k → top gives kth largest
  - Merge K: use a min-heap to always process the smallest element
  - Two heaps: max-heap for lower half + min-heap for upper half → median

AMAZON FAVORITES:
  - Kth Largest Element
  - Merge K Sorted Lists
  - Find Median from Data Stream
  - Task Scheduler
=============================================================================
"""

import heapq
from collections import Counter


# ---------------------------------------------------------------------------
# Problem 1: Kth Largest Element in an Array (LC 215)
# ---------------------------------------------------------------------------
# Given an integer array nums and integer k, return the kth largest element.
# Not the kth distinct element.
#
# Example:
#   Input:  nums = [3,2,1,5,6,4], k = 2
#   Output: 5
# ---------------------------------------------------------------------------
def find_kth_largest(nums: list[int], k: int) -> int:
    heap = []
    for num in nums:
        heapq.heappush(heap, -num)
    for _ in range(k-1):
        heapq.heappop(heap)
    return -heap[0]


# ---------------------------------------------------------------------------
# Problem 2: Merge K Sorted Lists (LC 23)
# ---------------------------------------------------------------------------
# Given an array of k sorted linked lists, merge them into one sorted list.
#
# Use the ListNode class below.
# ---------------------------------------------------------------------------
class ListNode: # very important to remever __init__ contains self 
# all attribtuoes go with self.
    def __init__(self, val=0,next=None):
        self.val = val
        self.next = next


def merge_k_lists(lists: list[ListNode]) -> ListNode:
    # we should first make an auxillary nodes
    n = ListNode() # default is val = 0 and next is none 
    head = n # place holder

    heap = []
    for i, ll in enumerate(lists):
        if ll: # make sure non empty linked list 
            heapq.heappush(heap, (ll.val, i))
    
    while heap:
        value, i = heapq.heappop(heap) # pair 
        n.next = ListNode(value) # we need to make a copy
        lists[i] = lists[i].next # we process the element 
        if lists[i]:
            heapq.heappush(heap, (lists[i].val, i)) # push it back into the comparison
        n = n.next
    return head.next


# ---------------------------------------------------------------------------
# Problem 3: Find Median from Data Stream (LC 295)
# ---------------------------------------------------------------------------
# Design a data structure that supports:
#   - addNum(num): add an integer from the data stream
#   - findMedian(): return the median of all elements so far
#
# Example:
#   mf = MedianFinder()
#   mf.addNum(1)
#   mf.addNum(2)
#   mf.findMedian() → 1.5
#   mf.addNum(3)
#   mf.findMedian() → 2.0
# ---------------------------------------------------------------------------
class MedianFinder:
    def __init__(self):
        pass  # YOUR CODE HERE

    def addNum(self, num: int) -> None:
        pass  # YOUR CODE HERE

    def findMedian(self) -> float:
        pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: Task Scheduler (LC 621)
# ---------------------------------------------------------------------------
# Given a list of tasks (chars) and a cooldown n, find the minimum number
# of intervals (time units) needed to finish all tasks. Same tasks must be
# separated by at least n intervals. Idle slots can be inserted.
#
# Example:
#   Input:  tasks = ["A","A","A","B","B","B"], n = 2
#   Output: 8  (A B idle A B idle A B)
# ---------------------------------------------------------------------------
def least_interval(tasks: list[str], n: int) -> int:
    pass  # YOUR CODE HERE


# ========================== TEST YOUR SOLUTIONS ==========================
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING HEAP / PRIORITY QUEUE")
    print("=" * 60)

    # Test Problem 1
    print("\n--- Kth Largest Element ---")
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5, "Test 1 failed"
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4, "Test 2 failed"
    print("All tests passed!")

    # Test Problem 2
    print("\n--- Merge K Sorted Lists ---")
    # Helper to create and verify linked lists
    def to_list(node):
        result = []
        while node:
            result.append(node.val)
            node = node.next
        return result

    def from_list(arr):
        dummy = ListNode(0)
        curr = dummy
        for val in arr:
            curr.next = ListNode(val)
            curr = curr.next
        return dummy.next

    lists = [from_list([1, 4, 5]), from_list([1, 3, 4]), from_list([2, 6])]
    assert to_list(merge_k_lists(lists)) == [1, 1, 2, 3, 4, 4, 5, 6], "Test 1 failed"
    assert merge_k_lists([]) is None, "Test 2 failed"
    print("All tests passed!")

    # Test Problem 3
    print("\n--- Find Median from Data Stream ---")
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    assert abs(mf.findMedian() - 1.5) < 1e-5, "Test 1 failed"
    mf.addNum(3)
    assert abs(mf.findMedian() - 2.0) < 1e-5, "Test 2 failed"
    print("All tests passed!")

    # Test Problem 4
    print("\n--- Task Scheduler ---")
    assert least_interval(["A", "A", "A", "B", "B", "B"], 2) == 8, "Test 1 failed"
    assert least_interval(["A", "A", "A", "B", "B", "B"], 0) == 6, "Test 2 failed"
    assert least_interval(["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2) == 16, "Test 3 failed"
    print("All tests passed!")

    print("\n" + "=" * 60)
    print("ALL HEAP PROBLEMS SOLVED!")
    print("=" * 60)
