"""
=============================================================================
PATTERN 1: TWO POINTERS — SOLUTIONS
=============================================================================
"""


# ---------------------------------------------------------------------------
# Problem 1: Two Sum II - Input Array Is Sorted
# ---------------------------------------------------------------------------
# APPROACH: Left + Right pointers moving inward.
#   - If sum < target: move left pointer right (need bigger number)
#   - If sum > target: move right pointer left (need smaller number)
#
# TIME: O(n)   SPACE: O(1)
#
# WHY IT WORKS: The array is sorted, so moving left increases the sum and
# moving right decreases it. We never skip a valid pair.
# ---------------------------------------------------------------------------
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]  # 1-indexed
        elif total < target:
            left += 1
        else:
            right -= 1
    return []


# ---------------------------------------------------------------------------
# Problem 2: 3Sum
# ---------------------------------------------------------------------------
# APPROACH: Sort + fix one number + two-pointer on remainder.
#   1. Sort the array
#   2. For each nums[i], find two_sum_sorted in nums[i+1:]
#      with target = -nums[i]
#   3. Skip duplicates at every level
#
# TIME: O(n^2)   SPACE: O(1) extra (ignoring output)
#
# TRICK TO REMEMBER: "Fix one, two-pointer the rest."
# Skip duplicates by checking nums[i] == nums[i-1].
# ---------------------------------------------------------------------------
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        # Skip duplicate for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicates for second and third elements
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result


# ---------------------------------------------------------------------------
# Problem 3: Container With Most Water
# ---------------------------------------------------------------------------
# APPROACH: Left + Right pointers moving inward.
#   - Area = min(height[l], height[r]) * (r - l)
#   - Move the pointer with the SHORTER height (only way to potentially
#     find a bigger area)
#
# TIME: O(n)   SPACE: O(1)
#
# WHY MOVE THE SHORTER SIDE? Moving the taller side can only decrease or
# maintain the area (the min stays the same but width shrinks).
# ---------------------------------------------------------------------------
def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        area = min(height[left], height[right]) * (right - left)
        best = max(best, area)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best


# ---------------------------------------------------------------------------
# Problem 4: Trapping Rain Water
# ---------------------------------------------------------------------------
# APPROACH: Two pointers with running max from each side.
#   - Track left_max and right_max
#   - Water at position i = min(left_max, right_max) - height[i]
#   - Process the side with the smaller max (it's the bottleneck)
#
# TIME: O(n)   SPACE: O(1)
#
# TRICK TO REMEMBER: "The shorter side determines the water level."
# If left_max < right_max, we KNOW water at left is bounded by left_max
# regardless of what's on the right.
# ---------------------------------------------------------------------------
def trap(height: list[int]) -> int:
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
    return water
