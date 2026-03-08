"""
=============================================================================
RECENTLY LEAKED AMAZON QUESTIONS (Jan–Mar 2026)
=============================================================================

SOURCE: 1point3acres, Glassdoor, programhelp — verified timestamps.

These are REAL questions reported in the last ~3 weeks from Amazon SDE
intern phone screens, OAs, and video interviews.

NOTE: Amazon's OA now includes an AI assistant you can use during the
assessment. They evaluate HOW you use it, not just if you can code.

PROBLEMS COVERED:
  1. Analyzing One-Time Visitors (HashMap)         — Phone Screen, ~5 days ago
  2. Word Break II (LC 140, DP/Backtracking)       — VO, ~10 days ago
  3. Unique Morse Code Words (LC 804, String)       — VO, ~10 days ago
  4. Deep Copy Linked List w/ Random Pointer (138)  — Interview, ~19 days ago
  5. Next Greater Element / Monotonic Stack          — Interview, ~19 days ago
  6. EC2 Instance Allocation Cost (Greedy)           — OA, ~12 days ago
  7. Frequent Item Pair (HashMap)                    — OA, ~12 days ago
  8. Refactoring Modules / Min Days Scheduling       — OA, ~12 days ago
  9. Merge Sorted Arrays (Two Pointer)               — VO, ~10 days ago
=============================================================================
"""

from collections import defaultdict


# ---------------------------------------------------------------------------
# Problem 1: Analyzing One-Time Visitors (~5 days ago, Phone Screen)
# ---------------------------------------------------------------------------
# Given a list of user visit logs where each entry is [user_id, page],
# find all users who visited only once (one-time visitors).
# Return the list of user IDs sorted in ascending order.
#
# Follow-up: For each one-time visitor, also return which page they visited
# so we can target them with promotional offers for that page.
#
# Example:
#   Input:  logs = [["u1","home"],["u2","home"],["u1","about"],
#                   ["u3","home"],["u2","product"],["u4","home"]]
#   Output: ["u3", "u4"]
#   (u3 and u4 each visited only once; u1 visited twice, u2 visited twice)
#
# Follow-up output: [("u3","home"), ("u4","home")]
# ---------------------------------------------------------------------------
def one_time_visitors(logs: list[list[str]]) -> list[str]:
    pass  # YOUR CODE HERE


def one_time_visitors_with_pages(logs: list[list[str]]) -> list[tuple[str, str]]:
    pass  # YOUR CODE HERE (follow-up)


# ---------------------------------------------------------------------------
# Problem 2: Word Break II (LC 140) (~10 days ago, VO) — HARD
# ---------------------------------------------------------------------------
# Given a string s and a dictionary of strings wordDict, add spaces in s
# to construct a sentence where each word is a valid dictionary word.
# Return all such possible sentences in any order.
#
# Example:
#   Input:  s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
#   Output: ["cats and dog", "cat sand dog"]
#
# Example:
#   Input:  s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]
#   Output: ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]
# ---------------------------------------------------------------------------
def word_break_ii(s: str, wordDict: list[str]) -> list[str]:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 3: Unique Morse Code Words (LC 804) (~10 days ago, VO)
# ---------------------------------------------------------------------------
# Each letter maps to a Morse code representation. Given a list of words,
# return the number of different transformations among all words.
#
# Morse codes: [".-","-...","-.-.","-..",".","..-.","--.","....","..",
#               ".---","-.-",".-..","--","-.","---",".--.","--.-",".-.",
#               "...","-","..-","...-",".--","-..-","-.--","--.."]
#
# Example:
#   Input:  words = ["gin","zen","gig","msg"]
#   Output: 2
#   Explanation: "gin" -> "--...-."
#                "zen" -> "--...-."
#                "gig" -> "--...--."
#                "msg" -> "--...--."
#   There are 2 unique transformations.
# ---------------------------------------------------------------------------
def unique_morse_representations(words: list[str]) -> int:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: Copy List with Random Pointer (LC 138) (~19 days ago)
# ---------------------------------------------------------------------------
# A linked list where each node has a next pointer AND a random pointer
# that can point to any node in the list or null. Construct a deep copy.
#
# Example:
#   Input:  head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
#   (each pair is [val, random_index])
#   Output: Deep copy of the same structure
#
# NOTE: Using Node class below for this problem.
# ---------------------------------------------------------------------------
class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list(head: 'Node') -> 'Node':
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 5: Next Greater Element II (Monotonic Stack) (~19 days ago)
# ---------------------------------------------------------------------------
# Given a circular integer array nums, return the next greater number for
# every element. The next greater number of x is the first greater number
# traversing circularly. If it doesn't exist, output -1.
#
# Example:
#   Input:  nums = [1, 2, 1]
#   Output: [2, -1, 2]
#
# Example:
#   Input:  nums = [1, 2, 3, 4, 3]
#   Output: [2, 3, 4, -1, 4]
# ---------------------------------------------------------------------------
def next_greater_elements(nums: list[int]) -> list[int]:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 6: EC2 Instance Allocation Cost (~12 days ago, OA)
# ---------------------------------------------------------------------------
# You have n tasks, each requiring a certain amount of compute. You can
# allocate EC2 instances of various sizes. Given a sorted list of available
# instance capacities and a list of task requirements, find the minimum
# total cost to allocate instances such that every task is covered.
# Each instance can only serve one task, and you must pick the smallest
# instance that fits each task. Cost = sum of chosen instance capacities.
#
# Example:
#   Input:  instances = [1, 2, 4, 8, 16], tasks = [2, 5, 1]
#   Output: 11
#   Explanation: task 2 -> instance 2, task 5 -> instance 8, task 1 -> instance 1
#                cost = 2 + 8 + 1 = 11
#
# Example:
#   Input:  instances = [1, 2, 4, 8], tasks = [3, 3]
#   Output: 8
#   Explanation: task 3 -> instance 4, task 3 -> instance 4 — but only one 4!
#                task 3 -> instance 4, task 3 -> instance 8 => cost = 12
#   (Each instance can only be used once)
# ---------------------------------------------------------------------------
def min_allocation_cost(instances: list[int], tasks: list[int]) -> int:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 7: Frequent Item Pair (~12 days ago, OA)
# ---------------------------------------------------------------------------
# Given a list of transactions where each transaction is a list of item IDs,
# find the pair of items that appears together most frequently across all
# transactions. Return the pair sorted in ascending order. If there's a tie,
# return the lexicographically smallest pair.
#
# Example:
#   Input:  transactions = [[1,2,3], [1,2,4], [1,2,5], [3,4,5]]
#   Output: [1, 2]
#   Explanation: (1,2) appears in 3 transactions — the most frequent pair.
#
# Example:
#   Input:  transactions = [[1,2], [2,3], [1,3]]
#   Output: [1, 2]
#   Explanation: All pairs appear once — return lexicographically smallest.
# ---------------------------------------------------------------------------
def most_frequent_pair(transactions: list[list[int]]) -> list[int]:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 8: Refactoring Modules / Min Days to Complete Releases (~12 days ago, OA)
# ---------------------------------------------------------------------------
# You have n modules to release. Some modules depend on others (given as
# a list of [module, dependency] pairs). On each day, you can release all
# modules whose dependencies have already been released. Find the minimum
# number of days to release all modules.
#
# This is essentially: find the longest path in a DAG (topological sort
# with level tracking).
#
# Example:
#   Input:  n = 5, dependencies = [[1,0],[2,0],[3,1],[3,2],[4,3]]
#   Output: 4
#   Explanation: Day 1: release 0
#                Day 2: release 1, 2
#                Day 3: release 3
#                Day 4: release 4
#
# Example:
#   Input:  n = 3, dependencies = [[1,0],[2,1]]
#   Output: 3
#   Explanation: Day 1: 0, Day 2: 1, Day 3: 2 (linear chain)
# ---------------------------------------------------------------------------
def min_days_to_release(n: int, dependencies: list[list[int]]) -> int:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 9: Merge Sorted Arrays (Two Pointer) (~10 days ago, VO)
# ---------------------------------------------------------------------------
# Given two sorted arrays nums1 (size m+n with trailing zeros) and nums2
# (size n), merge nums2 into nums1 in-place in sorted order.
# This is LC 88. Merge from the back to avoid shifting.
#
# Example:
#   Input:  nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
#   Output: [1,2,2,3,5,6]  (nums1 modified in-place)
#
# Example:
#   Input:  nums1 = [1], m = 1, nums2 = [], n = 0
#   Output: [1]
# ---------------------------------------------------------------------------
def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    pass  # YOUR CODE HERE (modify nums1 in-place)


# ========================== TEST YOUR SOLUTIONS ==========================
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING RECENTLY LEAKED AMAZON QUESTIONS")
    print("=" * 60)

    # Test Problem 1: One-Time Visitors
    print("\n--- One-Time Visitors ---")
    logs = [["u1", "home"], ["u2", "home"], ["u1", "about"],
            ["u3", "home"], ["u2", "product"], ["u4", "home"]]
    assert sorted(one_time_visitors(logs)) == ["u3", "u4"], "Test 1 failed"
    assert one_time_visitors([["u1", "a"]]) == ["u1"], "Test 2 failed"
    assert one_time_visitors([["u1", "a"], ["u1", "b"]]) == [], "Test 3 failed"
    print("All tests passed!")

    print("\n--- One-Time Visitors with Pages (Follow-up) ---")
    result = sorted(one_time_visitors_with_pages(logs))
    assert result == [("u3", "home"), ("u4", "home")], "Test 1 failed"
    print("All tests passed!")

    # Test Problem 2: Word Break II
    print("\n--- Word Break II ---")
    result = sorted(word_break_ii("catsanddog", ["cat", "cats", "and", "sand", "dog"]))
    assert result == sorted(["cats and dog", "cat sand dog"]), "Test 1 failed"
    result = sorted(word_break_ii("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]))
    assert result == sorted(["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]), "Test 2 failed"
    assert word_break_ii("catsandog", ["cats", "dog", "sand", "and", "cat"]) == [], "Test 3 failed"
    print("All tests passed!")

    # Test Problem 3: Unique Morse Code Words
    print("\n--- Unique Morse Code Words ---")
    assert unique_morse_representations(["gin", "zen", "gig", "msg"]) == 2, "Test 1 failed"
    assert unique_morse_representations(["a"]) == 1, "Test 2 failed"
    print("All tests passed!")

    # Test Problem 4: Copy List with Random Pointer
    print("\n--- Copy List with Random Pointer ---")
    # Build: 7 -> 13 -> 11 -> 10 -> 1
    n1 = Node(7)
    n2 = Node(13)
    n3 = Node(11)
    n4 = Node(10)
    n5 = Node(1)
    n1.next, n2.next, n3.next, n4.next = n2, n3, n4, n5
    n1.random = None
    n2.random = n1
    n3.random = n5
    n4.random = n3
    n5.random = n1
    copied = copy_random_list(n1)
    # Verify deep copy
    assert copied is not n1, "Must be a deep copy, not same reference"
    assert copied.val == 7, "Test val failed"
    assert copied.next.val == 13, "Test next val failed"
    assert copied.next.random.val == 7, "Test random pointer failed"
    assert copied.next.random is not n1, "Random must point to copied node, not original"
    assert copied.next.next.random.val == 1, "Test random pointer 2 failed"
    print("All tests passed!")

    # Test Problem 5: Next Greater Element (Circular)
    print("\n--- Next Greater Element II (Monotonic Stack) ---")
    assert next_greater_elements([1, 2, 1]) == [2, -1, 2], "Test 1 failed"
    assert next_greater_elements([1, 2, 3, 4, 3]) == [2, 3, 4, -1, 4], "Test 2 failed"
    assert next_greater_elements([5, 4, 3, 2, 1]) == [-1, 5, 5, 5, 5], "Test 3 failed"
    print("All tests passed!")

    # Test Problem 6: EC2 Instance Allocation Cost
    print("\n--- EC2 Instance Allocation Cost ---")
    assert min_allocation_cost([1, 2, 4, 8, 16], [2, 5, 1]) == 11, "Test 1 failed"
    assert min_allocation_cost([1, 2, 4, 8], [3, 3]) == 12, "Test 2 failed"
    assert min_allocation_cost([2, 4, 8], [1, 1, 1]) == 14, "Test 3 failed"
    print("All tests passed!")

    # Test Problem 7: Frequent Item Pair
    print("\n--- Frequent Item Pair ---")
    assert most_frequent_pair([[1, 2, 3], [1, 2, 4], [1, 2, 5], [3, 4, 5]]) == [1, 2], "Test 1 failed"
    assert most_frequent_pair([[1, 2], [2, 3], [1, 3]]) == [1, 2], "Test 2 failed"
    assert most_frequent_pair([[5, 10], [5, 10], [1, 2]]) == [5, 10], "Test 3 failed"
    print("All tests passed!")

    # Test Problem 8: Min Days to Release
    print("\n--- Min Days to Complete Releases ---")
    assert min_days_to_release(5, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3]]) == 4, "Test 1 failed"
    assert min_days_to_release(3, [[1, 0], [2, 1]]) == 3, "Test 2 failed"
    assert min_days_to_release(3, []) == 1, "Test 3 failed (no deps = all release day 1)"
    print("All tests passed!")

    # Test Problem 9: Merge Sorted Arrays
    print("\n--- Merge Sorted Arrays ---")
    nums1 = [1, 2, 3, 0, 0, 0]
    merge(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6], "Test 1 failed"
    nums1 = [1]
    merge(nums1, 1, [], 0)
    assert nums1 == [1], "Test 2 failed"
    nums1 = [0]
    merge(nums1, 0, [1], 1)
    assert nums1 == [1], "Test 3 failed"
    print("All tests passed!")

    print("\n" + "=" * 60)
    print("ALL RECENTLY LEAKED QUESTIONS SOLVED!")
    print("=" * 60)
