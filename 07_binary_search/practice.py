"""
=============================================================================
PATTERN 7: BINARY SEARCH
=============================================================================

HOW TO RECOGNIZE:
- Sorted array + searching for something
- "Find minimum/maximum that satisfies condition"
- "Search in rotated sorted array"
- Monotonic function: if f(x) is True, then f(x+1) is True
- O(log n) required

KEY IDEA:
  Repeatedly halve the search space. Two main templates:
  1. Classic: find exact target
  2. Boundary: find first/last position satisfying a condition

  TEMPLATE (find leftmost True):
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if condition(mid):
            hi = mid        # mid could be the answer
        else:
            lo = mid + 1    # mid is definitely not
    return lo

AMAZON FAVORITES:
  - Search in Rotated Sorted Array
  - Find First and Last Position
  - Search a 2D Matrix
  - Koko Eating Bananas (binary search on answer)
=============================================================================
"""

import math


# ---------------------------------------------------------------------------
# Problem 1: Search in Rotated Sorted Array (LC 33)
# ---------------------------------------------------------------------------
# A sorted array was rotated at some pivot. Given target, return its index
# or -1 if not found. All values are unique. Must be O(log n).
#
# Example:
#   Input:  nums = [4,5,6,7,0,1,2], target = 0
#   Output: 4
# ---------------------------------------------------------------------------
def search_rotated(nums: list[int], target: int) -> int:
    n = len(nums)
    lo, hi = 0, n-1

    while(lo <= hi): # tbd if it's lo < hi or this is correct
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid

        if nums[lo] < nums[mid]: # lhs is sorted
            if nums[mid] > target >= nums[lo]:
                hi = mid - 1 #check the interval for lo to mid 
            else:
                lo = mid + 1 # the target is in the lhs sorted part
         
        else: # rhs is sorted so nums[mid] < nums[hi]
            if (nums[hi] >= target > nums[mid]):
               lo = mid + 1
            else:
                hi = mid - 1
    return -1 
        
            

        
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 2: Find First and Last Position of Element (LC 34)
# ---------------------------------------------------------------------------
# Given a sorted array of integers and a target, find the starting and
# ending position. Return [-1, -1] if not found. Must be O(log n).
#
# Example:
#   Input:  nums = [5,7,7,8,8,10], target = 8
#   Output: [3, 4]
# ---------------------------------------------------------------------------
def search_range(nums: list[int], target: int) -> list[int]:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 3: Search a 2D Matrix (LC 74)
# ---------------------------------------------------------------------------
# Each row is sorted left to right. The first integer of each row is
# greater than the last integer of the previous row. Given a target,
# return True if it exists in the matrix.
#
# Example:
#   matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
#   target = 3 → True
# ---------------------------------------------------------------------------
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: Koko Eating Bananas (LC 875)
# ---------------------------------------------------------------------------
# Koko has piles of bananas. Guards return in h hours. Each hour she eats
# at speed k (bananas/hour) from ONE pile (ceil if pile < k). Find minimum
# k so she finishes all piles in h hours.
#
# Example:
#   Input:  piles = [3,6,7,11], h = 8
#   Output: 4
# ---------------------------------------------------------------------------
def min_eating_speed(piles: list[int], h: int) -> int:
    pass  # YOUR CODE HERE


# ========================== TEST YOUR SOLUTIONS ==========================
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING BINARY SEARCH")
    print("=" * 60)

    # Test Problem 1
    print("\n--- Search in Rotated Sorted Array ---")
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4, "Test 1 failed"
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1, "Test 2 failed"
    assert search_rotated([1], 0) == -1, "Test 3 failed"
    assert search_rotated([1], 1) == 0, "Test 4 failed"
    print("All tests passed!")

    # Test Problem 2
    print("\n--- Find First and Last Position ---")
    assert search_range([5, 7, 7, 8, 8, 10], 8) == [3, 4], "Test 1 failed"
    assert search_range([5, 7, 7, 8, 8, 10], 6) == [-1, -1], "Test 2 failed"
    assert search_range([], 0) == [-1, -1], "Test 3 failed"
    print("All tests passed!")

    # Test Problem 3
    print("\n--- Search a 2D Matrix ---")
    mat = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    assert search_matrix(mat, 3) == True, "Test 1 failed"
    assert search_matrix(mat, 13) == False, "Test 2 failed"
    print("All tests passed!")

    # Test Problem 4
    print("\n--- Koko Eating Bananas ---")
    assert min_eating_speed([3, 6, 7, 11], 8) == 4, "Test 1 failed"
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30, "Test 2 failed"
    assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23, "Test 3 failed"
    print("All tests passed!")

    print("\n" + "=" * 60)
    print("ALL BINARY SEARCH PROBLEMS SOLVED!")
    print("=" * 60)
