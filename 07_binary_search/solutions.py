"""
=============================================================================
PATTERN 7: BINARY SEARCH — SOLUTIONS
=============================================================================
"""

import math


# ---------------------------------------------------------------------------
# Problem 1: Search in Rotated Sorted Array
# ---------------------------------------------------------------------------
# APPROACH: Modified binary search.
#   - At least one half [lo..mid] or [mid..hi] is always sorted
#   - Determine which half is sorted
#   - Check if target falls within that sorted half
#   - If yes, search there; if no, search the other half
#
# TIME: O(log n)   SPACE: O(1)
#
# TRICK TO REMEMBER: "One half is always sorted. Check if target is in
# the sorted half. If not, go to the other half."
# ---------------------------------------------------------------------------
def search_rotated(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        # Left half is sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


# ---------------------------------------------------------------------------
# Problem 2: Find First and Last Position of Element
# ---------------------------------------------------------------------------
# APPROACH: Two binary searches — one for leftmost, one for rightmost.
#
# Find leftmost:  when nums[mid] >= target → hi = mid  (go left)
# Find rightmost: when nums[mid] <= target → lo = mid  (go right)
#
# TIME: O(log n)   SPACE: O(1)
#
# TRICK TO REMEMBER: "Two binary searches: one biased left, one biased right."
# ---------------------------------------------------------------------------
def search_range(nums: list[int], target: int) -> list[int]:
    if not nums:
        return [-1, -1]

    # Find leftmost target
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    if nums[lo] != target:
        return [-1, -1]
    left = lo

    # Find rightmost target
    hi = len(nums) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2  # ceil to avoid infinite loop
        if nums[mid] > target:
            hi = mid - 1
        else:
            lo = mid
    return [left, lo]


# ---------------------------------------------------------------------------
# Problem 3: Search a 2D Matrix
# ---------------------------------------------------------------------------
# APPROACH: Treat the 2D matrix as a flat sorted array.
#   - Total elements = rows * cols
#   - Index i in flat array → matrix[i // cols][i % cols]
#   - Standard binary search on this virtual array
#
# TIME: O(log(m * n))   SPACE: O(1)
#
# TRICK TO REMEMBER: "Flatten with divmod: row = i // cols, col = i % cols"
# ---------------------------------------------------------------------------
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    if not matrix:
        return False
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // cols][mid % cols]
        if val == target:
            return True
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


# ---------------------------------------------------------------------------
# Problem 4: Koko Eating Bananas
# ---------------------------------------------------------------------------
# APPROACH: Binary search on the answer (speed k).
#   - Search space: k in [1, max(piles)]
#   - For a given k, compute hours needed: sum(ceil(p / k) for p in piles)
#   - If hours <= h: k might work, try smaller → hi = mid
#   - If hours > h: k too slow → lo = mid + 1
#
# TIME: O(n * log(max(piles)))   SPACE: O(1)
#
# TRICK TO REMEMBER: "Binary search on the answer" — when the problem asks
# for "minimum X such that condition is satisfied" and X is monotonic.
# Always think: "Can I binary search on the answer?"
# ---------------------------------------------------------------------------
def min_eating_speed(piles: list[int], h: int) -> int:
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        hours = sum(math.ceil(p / mid) for p in piles)
        if hours <= h:
            hi = mid  # mid could be the answer, try smaller
        else:
            lo = mid + 1  # too slow
    return lo
