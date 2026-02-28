"""
=============================================================================
PATTERN 3: HASH MAP / SET — SOLUTIONS
=============================================================================
"""

from collections import Counter, defaultdict


# ---------------------------------------------------------------------------
# Problem 1: Two Sum
# ---------------------------------------------------------------------------
# APPROACH: One-pass hash map.
#   - For each num, check if (target - num) is already in the map
#   - If yes, return both indices
#   - If no, store {num: index}
#
# TIME: O(n)   SPACE: O(n)
#
# TRICK TO REMEMBER: "Store the complement."
# For every num you see, ask: "Have I seen someone who completes me?"
# ---------------------------------------------------------------------------
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


# ---------------------------------------------------------------------------
# Problem 2: Group Anagrams
# ---------------------------------------------------------------------------
# APPROACH: Use sorted string as key.
#   - Two strings are anagrams iff they have the same sorted characters
#   - Group by sorted(word) as the dict key
#
# TIME: O(n * k log k) where k = max word length   SPACE: O(n * k)
#
# ALTERNATIVE: Use a tuple of character counts as the key:
#   key = tuple(Counter(word).items())  — but sorting is simpler to code.
# ---------------------------------------------------------------------------
def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for word in strs:
        key = tuple(sorted(word))
        groups[key].append(word)
    return list(groups.values())


# ---------------------------------------------------------------------------
# Problem 3: Top K Frequent Elements
# ---------------------------------------------------------------------------
# APPROACH: Bucket sort (optimal for this problem).
#   - Count frequencies with Counter
#   - Create buckets where index = frequency, value = list of nums
#   - Walk buckets from high to low, collect k elements
#
# TIME: O(n)   SPACE: O(n)
#
# ALTERNATIVE: Use a heap → O(n log k). But bucket sort is O(n) and
# very clean for this problem.
# ---------------------------------------------------------------------------
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    # Buckets: index = frequency, value = list of numbers with that frequency
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result
    return result


# ---------------------------------------------------------------------------
# Problem 4: Subarray Sum Equals K
# ---------------------------------------------------------------------------
# APPROACH: Prefix sum + hash map.
#   - prefix_sum[i] = nums[0] + ... + nums[i-1]
#   - Subarray sum from i to j = prefix_sum[j+1] - prefix_sum[i]
#   - We need prefix_sum[j+1] - prefix_sum[i] == k
#   - So for each j, we need prefix_sum[i] == prefix_sum[j+1] - k
#   - Use a hash map to count how many prefix sums we've seen
#
# TIME: O(n)   SPACE: O(n)
#
# TRICK TO REMEMBER: "Prefix sum + hash map = subarray sum problems."
# This same pattern works for many subarray-sum variants.
# Initialize the map with {0: 1} because an empty prefix has sum 0.
# ---------------------------------------------------------------------------
def subarray_sum(nums: list[int], k: int) -> int:
    prefix_count = {0: 1}  # sum -> number of times we've seen this sum
    current_sum = 0
    count = 0
    for num in nums:
        current_sum += num
        # How many previous prefix sums equal (current_sum - k)?
        count += prefix_count.get(current_sum - k, 0)
        prefix_count[current_sum] = prefix_count.get(current_sum, 0) + 1
    return count
