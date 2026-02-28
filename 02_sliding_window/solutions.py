"""
=============================================================================
PATTERN 2: SLIDING WINDOW — SOLUTIONS
=============================================================================
"""

from collections import Counter, defaultdict


# ---------------------------------------------------------------------------
# Problem 1: Longest Substring Without Repeating Characters
# ---------------------------------------------------------------------------
# APPROACH: Variable-size window with a set tracking chars in window.
#   - Expand right: add char
#   - If duplicate: shrink from left until no duplicate
#   - Track max window size
#
# TIME: O(n)   SPACE: O(min(n, 26))
#
# TEMPLATE (variable window, maximize):
#   while right < n:
#       add nums[right] to window
#       while window is invalid:
#           remove nums[left], left += 1
#       ans = max(ans, right - left + 1)
#       right += 1
# ---------------------------------------------------------------------------
def length_of_longest_substring(s: str) -> int:
    char_set = set()
    left = 0
    max_len = 0
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len


# ---------------------------------------------------------------------------
# Problem 2: Minimum Window Substring
# ---------------------------------------------------------------------------
# APPROACH: Variable-size window with frequency counts.
#   - need = Counter(t): what we still need
#   - missing = len(t): how many chars still missing
#   - Expand right: if adding char satisfies a need, decrement missing
#   - When missing == 0: shrink from left to minimize, track best
#
# TIME: O(n + m)   SPACE: O(m) where m = len(t)
#
# TRICK TO REMEMBER: "Expand to satisfy, shrink to minimize."
# The 'missing' counter avoids re-checking the entire need dict each time.
# ---------------------------------------------------------------------------
def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need = Counter(t)
    missing = len(t)
    left = 0
    best_start, best_len = 0, float("inf")

    for right, char in enumerate(s):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1

        while missing == 0:  # window contains all of t
            # Update best
            if right - left + 1 < best_len:
                best_start = left
                best_len = right - left + 1
            # Shrink from left
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1

    return "" if best_len == float("inf") else s[best_start : best_start + best_len]


# ---------------------------------------------------------------------------
# Problem 3: Maximum Average Subarray I
# ---------------------------------------------------------------------------
# APPROACH: Fixed-size sliding window.
#   - Compute sum of first k elements
#   - Slide: add nums[right], subtract nums[right - k]
#   - Track max sum, divide by k at the end
#
# TIME: O(n)   SPACE: O(1)
# ---------------------------------------------------------------------------
def find_max_average(nums: list[int], k: int) -> float:
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for right in range(k, len(nums)):
        window_sum += nums[right] - nums[right - k]
        max_sum = max(max_sum, window_sum)
    return max_sum / k


# ---------------------------------------------------------------------------
# Problem 4: Fruit Into Baskets
# ---------------------------------------------------------------------------
# APPROACH: Variable-size window, at most 2 distinct values.
#   - Use a dict to count fruit types in window
#   - When dict has > 2 keys: shrink from left
#   - Track max window size
#
# TIME: O(n)   SPACE: O(1) — at most 3 keys in dict
#
# GENERALIZATION: "Longest subarray with at most K distinct" — same pattern
# with k instead of 2.
# ---------------------------------------------------------------------------
def total_fruit(fruits: list[int]) -> int:
    basket = defaultdict(int)
    left = 0
    max_fruits = 0
    for right in range(len(fruits)):
        basket[fruits[right]] += 1
        while len(basket) > 2:
            basket[fruits[left]] -= 1
            if basket[fruits[left]] == 0:
                del basket[fruits[left]]
            left += 1
        max_fruits = max(max_fruits, right - left + 1)
    return max_fruits
