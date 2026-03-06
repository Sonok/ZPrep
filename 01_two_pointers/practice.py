"""
=============================================================================
PATTERN 1: TWO POINTERS
=============================================================================

HOW TO RECOGNIZE:
- Array/string problems asking for pairs, triplets, or subarrays
- "Find two elements that..." or "Remove duplicates"
- Sorted array + searching for a combination
- Comparing elements from both ends or moving inward
- Partitioning an array in-place

KEY IDEA:
  Use two indices that move toward each other (or in the same direction)
  to reduce a brute-force O(n^2) down to O(n).

AMAZON FAVORITES:
  - Two Sum II (sorted array)
  - 3Sum
  - Container With Most Water
  - Trapping Rain Water
=============================================================================
"""


# ---------------------------------------------------------------------------
# Problem 1: Two Sum II - Input Array Is Sorted (LC 167)
# ---------------------------------------------------------------------------
# Given a 1-indexed sorted array and a target, return the indices of the
# two numbers that add up to target. Exactly one solution exists.
#
# Example:
#   Input:  numbers = [2,7,11,15], target = 9
#   Output: [1, 2]
#
# Constraints: O(1) extra space
# ---------------------------------------------------------------------------
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    # since it's already sorted we have a lhs pointer and a rhs pointer
    # rhs > lhs and that list[rhs] > list[lhs]

    # we move the rhs downward as much as possible. If there's a match - great!
    # otherwise the lhs index isn't the correct one. So we should increment the lhs pointer
    # we move the rhs down until it succeeds or we realize the new lhs isn't it so on so forth
    n = len(numbers)
    l = 0

    for r in range(n-1, -1, -1): # decreasing python loop from n-1 to -1
        if numbers[l] + numbers[r] == target:
            return [l + 1, r + 1]
        if numbers[l] + numbers[r] < target:
            l += 1
    
    return [-1, -1] # clearly can't happen


# ---------------------------------------------------------------------------
# Problem 2: 3Sum (LC 15)
# ---------------------------------------------------------------------------
# Given an array nums, return all unique triplets [a, b, c] such that
# a + b + c = 0. No duplicate triplets.
#
# Example:
#   Input:  nums = [-1, 0, 1, 2, -1, -4]
#   Output: [[-1, -1, 2], [-1, 0, 1]]
# ---------------------------------------------------------------------------
def three_sum(nums: list[int]) -> list[list[int]]:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 3: Container With Most Water (LC 11)
# ---------------------------------------------------------------------------
# Given n non-negative integers representing heights of vertical lines,
# find two lines that together with the x-axis form a container that
# holds the most water.
#
# Example:
#   Input:  height = [1,8,6,2,5,4,8,3,7]
#   Output: 49
# ---------------------------------------------------------------------------
def max_area(height: list[int]) -> int:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: Trapping Rain Water (LC 42)
# ---------------------------------------------------------------------------
# Given n non-negative integers representing an elevation map where the
# width of each bar is 1, compute how much water it can trap after rain.
#
# Example:
#   Input:  height = [0,1,0,2,1,0,1,3,2,1,2,1]
#   Output: 6
# ---------------------------------------------------------------------------
def trap(height: list[int]) -> int:
    pass  # YOUR CODE HERE


# ========================== TEST YOUR SOLUTIONS ==========================
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING TWO POINTERS")
    print("=" * 60)

    # Test Problem 1
    print("\n--- Two Sum Sorted ---")
    assert two_sum_sorted([2, 7, 11, 15], 9) == [1, 2], "Test 1 failed"
    assert two_sum_sorted([2, 3, 4], 6) == [1, 3], "Test 2 failed"
    assert two_sum_sorted([-1, 0], -1) == [1, 2], "Test 3 failed"
    print("All tests passed!")

    # Test Problem 2
    print("\n--- 3Sum ---")
    result = three_sum([-1, 0, 1, 2, -1, -4])
    assert sorted([sorted(t) for t in result]) == [[-1, -1, 2], [-1, 0, 1]], "Test 1 failed"
    assert three_sum([0, 1, 1]) == [], "Test 2 failed"
    assert three_sum([0, 0, 0]) == [[0, 0, 0]], "Test 3 failed"
    print("All tests passed!")

    # Test Problem 3
    print("\n--- Container With Most Water ---")
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49, "Test 1 failed"
    assert max_area([1, 1]) == 1, "Test 2 failed"
    assert max_area([4, 3, 2, 1, 4]) == 16, "Test 3 failed"
    print("All tests passed!")

    # Test Problem 4
    print("\n--- Trapping Rain Water ---")
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6, "Test 1 failed"
    assert trap([4, 2, 0, 3, 2, 5]) == 9, "Test 2 failed"
    assert trap([1, 0, 1]) == 1, "Test 3 failed"
    print("All tests passed!")

    print("\n" + "=" * 60)
    print("ALL TWO POINTER PROBLEMS SOLVED!")
    print("=" * 60)
