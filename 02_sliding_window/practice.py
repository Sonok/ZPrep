"""
=============================================================================
PATTERN 2: SLIDING WINDOW
=============================================================================

HOW TO RECOGNIZE:
- "Find the longest/shortest subarray/substring with property X"
- Contiguous sequence of elements
- "At most K distinct...", "minimum window containing..."
- Problems about subarrays or substrings with a constraint

KEY IDEA:
  Maintain a window [left, right] that expands right and shrinks from left.
  Two flavors:
    - Fixed-size window:  right - left + 1 == k always
    - Variable-size window: expand right, shrink left when constraint breaks

AMAZON FAVORITES:
  - Longest Substring Without Repeating Characters
  - Minimum Window Substring
  - Maximum Average Subarray
  - Fruit Into Baskets (at most 2 distinct)
=============================================================================
"""

from collections import Counter, defaultdict


# ---------------------------------------------------------------------------
# Problem 1: Longest Substring Without Repeating Characters (LC 3)
# ---------------------------------------------------------------------------
# Given a string s, find the length of the longest substring without
# repeating characters.
#
# Example:
#   Input:  s = "abcabcbb"
#   Output: 3  (the answer is "abc")
# ---------------------------------------------------------------------------
def length_of_longest_substring(s: str) -> int:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 2: Minimum Window Substring (LC 76)
# ---------------------------------------------------------------------------
# Given strings s and t, return the minimum window substring of s that
# contains all characters of t (including duplicates). Return "" if none.
#
# Example:
#   Input:  s = "ADOBECODEBANC", t = "ABC"
#   Output: "BANC"
# ---------------------------------------------------------------------------
def min_window(s: str, t: str) -> str:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 3: Maximum Average Subarray I (LC 643)
# ---------------------------------------------------------------------------
# Given an integer array nums and an integer k, find a contiguous subarray
# of length k that has the maximum average value. Return the max average.
#
# Example:
#   Input:  nums = [1,12,-5,-6,50,3], k = 4
#   Output: 12.75  (subarray [12,-5,-6,50])
# ---------------------------------------------------------------------------
def find_max_average(nums: list[int], k: int) -> float:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: Fruit Into Baskets (LC 904)
# ---------------------------------------------------------------------------
# You have a row of trees (array). Each tree[i] is a type of fruit.
# You have 2 baskets, each basket can hold ONE type of fruit (unlimited qty).
# Starting from any tree, pick every tree going right. Stop when you'd need
# a 3rd basket. Return the maximum number of fruits you can collect.
#
# (In other words: longest subarray with at most 2 distinct values)
#
# Example:
#   Input:  fruits = [1,2,3,2,2]
#   Output: 4  (subarray [2,3,2,2] — wait, that's wrong, it's [3,2,2] = 3?)
#   Actually: Input: [1,2,1], Output: 3
#             Input: [0,1,2,2], Output: 3
#             Input: [1,2,3,2,2], Output: 4  -> [2,3,2,2]
# ---------------------------------------------------------------------------
def total_fruit(fruits: list[int]) -> int:
    pass  # YOUR CODE HERE


# ========================== TEST YOUR SOLUTIONS ==========================
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING SLIDING WINDOW")
    print("=" * 60)

    # Test Problem 1
    print("\n--- Longest Substring Without Repeating Characters ---")
    assert length_of_longest_substring("abcabcbb") == 3, "Test 1 failed"
    assert length_of_longest_substring("bbbbb") == 1, "Test 2 failed"
    assert length_of_longest_substring("pwwkew") == 3, "Test 3 failed"
    assert length_of_longest_substring("") == 0, "Test 4 failed"
    print("All tests passed!")

    # Test Problem 2
    print("\n--- Minimum Window Substring ---")
    assert min_window("ADOBECODEBANC", "ABC") == "BANC", "Test 1 failed"
    assert min_window("a", "a") == "a", "Test 2 failed"
    assert min_window("a", "aa") == "", "Test 3 failed"
    print("All tests passed!")

    # Test Problem 3
    print("\n--- Maximum Average Subarray ---")
    assert abs(find_max_average([1, 12, -5, -6, 50, 3], 4) - 12.75) < 1e-5, "Test 1 failed"
    assert abs(find_max_average([5], 1) - 5.0) < 1e-5, "Test 2 failed"
    print("All tests passed!")

    # Test Problem 4
    print("\n--- Fruit Into Baskets ---")
    assert total_fruit([1, 2, 1]) == 3, "Test 1 failed"
    assert total_fruit([0, 1, 2, 2]) == 3, "Test 2 failed"
    assert total_fruit([1, 2, 3, 2, 2]) == 4, "Test 3 failed"
    print("All tests passed!")

    print("\n" + "=" * 60)
    print("ALL SLIDING WINDOW PROBLEMS SOLVED!")
    print("=" * 60)
