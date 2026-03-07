"""
=============================================================================
PATTERN 3: HASH MAP / SET
=============================================================================

HOW TO RECOGNIZE:
- "Find if something exists" → set
- "Count occurrences" → Counter / dict
- "Find pairs/groups with property X" → hash map for O(1) lookup
- "Group items by some key" → defaultdict(list)
- Anagram, frequency, or duplicate problems

KEY IDEA:
  Trade space for time. Store seen values for O(1) lookup instead of
  scanning the array again (turning O(n^2) into O(n)).

AMAZON FAVORITES:
  - Two Sum
  - Group Anagrams
  - Top K Frequent Elements
  - Subarray Sum Equals K
=============================================================================
"""

from collections import Counter, defaultdict
import heapq

# ---------------------------------------------------------------------------
# Problem 1: Two Sum (LC 1) — THE classic Amazon question
# ---------------------------------------------------------------------------
# Given an array nums and a target, return indices of the two numbers
# that add up to target. Exactly one solution exists. Can't use same
# element twice.
#
# Example:
#   Input:  nums = [2,7,11,15], target = 9
#   Output: [0, 1]
# ---------------------------------------------------------------------------
def two_sum(nums: list[int], target: int) -> list[int]:
    s = {}
    for index, x in enumerate(nums):
        if target - x in s: # we found the compliment
            return [index, s[target - x]]
        s[x] = index
    return [-1, -1]


# ---------------------------------------------------------------------------
# Problem 2: Group Anagrams (LC 49)
# ---------------------------------------------------------------------------
# Given an array of strings, group the anagrams together.
#
# Example:
#   Input:  strs = ["eat","tea","tan","ate","nat","bat"]
#   Output: [["eat","tea","ate"], ["tan","nat"], ["bat"]]
#   (order doesn't matter)
# ---------------------------------------------------------------------------
def group_anagrams(strs: list[str]) -> list[list[str]]:
    dic = defaultdict(list)
    for string in strs:
        s = str(sorted(string))
        dic[s].append(string)
    
    return list(dic.values())



# ---------------------------------------------------------------------------
# Problem 3: Top K Frequent Elements (LC 347)
# ---------------------------------------------------------------------------
# Given an integer array nums and an integer k, return the k most
# frequent elements. Answer is guaranteed unique.
#
# Example:
#   Input:  nums = [1,1,1,2,2,3], k = 2
#   Output: [1, 2]
# ---------------------------------------------------------------------------
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    c = Counter(nums)
    heap = []
    out = []
    for val, count in c.items():
        heapq.heappush(heap, (-count, val)) # this makes a max heap
    while(k and heap): # making sure there are k unique elements 
        out.append(heapq.heappop(heap)[1]) # we append the value
        k -= 1
    return out


    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: Subarray Sum Equals K (LC 560)
# ---------------------------------------------------------------------------
# Given an integer array nums and an integer k, return the total number
# of subarrays whose sum equals k.
#
# Example:
#   Input:  nums = [1,1,1], k = 2
#   Output: 2
#
# Example:
#   Input:  nums = [1,2,3], k = 3
#   Output: 2  (subarrays [1,2] and [3])
# ---------------------------------------------------------------------------
def subarray_sum(nums: list[int], k: int) -> int:
    pass  # YOUR CODE HERE


# ========================== TEST YOUR SOLUTIONS ==========================
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING HASH MAP")
    print("=" * 60)

    # Test Problem 1
    print("\n--- Two Sum ---")
    assert sorted(two_sum([2, 7, 11, 15], 9)) == [0, 1], "Test 1 failed"
    assert sorted(two_sum([3, 2, 4], 6)) == [1, 2], "Test 2 failed"
    assert sorted(two_sum([3, 3], 6)) == [0, 1], "Test 3 failed"
    print("All tests passed!")

    # Test Problem 2
    print("\n--- Group Anagrams ---")
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    result_sorted = sorted([sorted(g) for g in result])
    expected = sorted([sorted(g) for g in [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]])
    assert result_sorted == expected, "Test 1 failed"
    print("All tests passed!")

    # Test Problem 3
    print("\n--- Top K Frequent Elements ---")
    assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2], "Test 1 failed"
    assert top_k_frequent([1], 1) == [1], "Test 2 failed"
    print("All tests passed!")

    # Test Problem 4
    print("\n--- Subarray Sum Equals K ---")
    assert subarray_sum([1, 1, 1], 2) == 2, "Test 1 failed"
    assert subarray_sum([1, 2, 3], 3) == 2, "Test 2 failed"
    assert subarray_sum([1], 0) == 0, "Test 3 failed"
    print("All tests passed!")

    print("\n" + "=" * 60)
    print("ALL HASH MAP PROBLEMS SOLVED!")
    print("=" * 60)
