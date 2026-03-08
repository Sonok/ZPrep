"""
=============================================================================
PATTERN 8: DYNAMIC PROGRAMMING
=============================================================================

HOW TO RECOGNIZE:
- "Count the number of ways"
- "What is the minimum/maximum cost/profit/path?"
- "Can you reach...?" / "Is it possible...?"
- Optimal substructure: solution built from solutions to subproblems
- Overlapping subproblems: same subproblems solved multiple times
- Choices at each step (take or skip, left or right, etc.)

KEY IDEA:
  1. Define state: what information do I need to solve a subproblem?
  2. Define recurrence: how does dp[i] relate to smaller subproblems?
  3. Define base case: what's the simplest subproblem?
  4. Define order: compute dp bottom-up (or use memoized top-down)

  COMMON DP TYPES:
  - 1D: dp[i] = answer for first i elements (climbing stairs, house robber)
  - 2D: dp[i][j] = answer for subproblem (i, j) (LCS, knapsack, grid paths)
  - String DP: dp[i][j] on two strings
  - Decision DP: dp[i] = max(take, skip)

AMAZON FAVORITES:
  - Climbing Stairs
  - Coin Change
  - Longest Common Subsequence
  - Word Break
=============================================================================
"""
from functools import cache

# ---------------------------------------------------------------------------
# Problem 1: Climbing Stairs (LC 70)
# ---------------------------------------------------------------------------
# You are climbing a staircase with n steps. Each time you can climb
# 1 or 2 steps. How many distinct ways can you reach the top?
#
# Example:
#   Input:  n = 3
#   Output: 3  (1+1+1, 1+2, 2+1)
# ---------------------------------------------------------------------------
def climb_stairs(n: int) -> int:
    # this is given by states
    # where state[n] = state[n-1] + state[n-2]
    # we want to know what state[n] is 
    # so state[1] = 1 state[2] = 2
    if (n == 1 or n == 2):
        return n

    states = [0] * (n+1)
    states[1], states[2] = 1, 2

    for i in range(3, n+1):
        states[i] = states[i-1] + states[i-2]

    return states[-1]


# ---------------------------------------------------------------------------
# Problem 2: Coin Change (LC 322)
# ---------------------------------------------------------------------------
# Given coin denominations and a target amount, return the fewest number
# of coins needed. Return -1 if not possible.
#
# Example:
#   Input:  coins = [1,5,11], amount = 15
#   Output: 3  (5+5+5)
# ---------------------------------------------------------------------------
def coin_change(coins: list[int], amount: int) -> int:
    states = [float('inf')] * (amount + 1)
    states[0] = 0

    for i in range(0, amount + 1):
        if states[i] != float('inf'): # means that possible to get to that dollar amount
            for coin in coins:
                if i + coin <= amount: # see if in range
                    states[i + coin] = min(states[i] + 1, states[i + coin]) 
                    # checking if there's alr a better consturction 
    if states[-1] == float('inf'):
         return -1
    return states[-1]


# ---------------------------------------------------------------------------
# Problem 3: Longest Common Subsequence (LC 1143)
# ---------------------------------------------------------------------------
# Given two strings text1 and text2, return the length of their longest
# common subsequence. A subsequence can skip characters but keeps order.
#
# Example:
#   Input:  text1 = "abcde", text2 = "ace"
#   Output: 3  ("ace")
# ---------------------------------------------------------------------------
def longest_common_subsequence(text1: str, text2: str) -> int:

    @cache
    def dp(i, j):
        if (i < 0 or j < 0) : # no way to have a common substring
            return 0
        if (text1[i] == text2[j]):
            return 1 + dp(i-1, j-1)
        
        return max(dp(i-1, j), dp(i, j-1))

    n, m = len(text1), len(text2) 
    return dp(n-1, m-1)


# ---------------------------------------------------------------------------
# Problem 4: Word Break (LC 139)
# ---------------------------------------------------------------------------
# Given a string s and a dictionary wordDict, return True if s can be
# segmented into a space-separated sequence of dictionary words.
#
# Example:
#   Input:  s = "leetcode", wordDict = ["leet", "code"]
#   Output: True
#
#   Input:  s = "applepenapple", wordDict = ["apple", "pen"]
#   Output: True
# ---------------------------------------------------------------------------
def word_break(s: str, wordDict: list[str]) -> bool:
    pass  # YOUR CODE HERE


# ========================== TEST YOUR SOLUTIONS ==========================
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING DYNAMIC PROGRAMMING")
    print("=" * 60)

    # Test Problem 1
    print("\n--- Climbing Stairs ---")
    assert climb_stairs(2) == 2, "Test 1 failed"
    assert climb_stairs(3) == 3, "Test 2 failed"
    assert climb_stairs(5) == 8, "Test 3 failed"
    print("All tests passed!")

    # Test Problem 2
    print("\n--- Coin Change ---")
    assert coin_change([1, 5, 11], 15) == 3, "Test 1 failed"
    assert coin_change([2], 3) == -1, "Test 2 failed"
    assert coin_change([1], 0) == 0, "Test 3 failed"
    assert coin_change([1, 2, 5], 11) == 3, "Test 4 failed"
    print("All tests passed!")

    # Test Problem 3
    print("\n--- Longest Common Subsequence ---")
    assert longest_common_subsequence("abcde", "ace") == 3, "Test 1 failed"
    assert longest_common_subsequence("abc", "abc") == 3, "Test 2 failed"
    assert longest_common_subsequence("abc", "def") == 0, "Test 3 failed"
    print("All tests passed!")

    # Test Problem 4
    print("\n--- Word Break ---")
    assert word_break("leetcode", ["leet", "code"]) == True, "Test 1 failed"
    assert word_break("applepenapple", ["apple", "pen"]) == True, "Test 2 failed"
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False, "Test 3 failed"
    print("All tests passed!")

    print("\n" + "=" * 60)
    print("ALL DP PROBLEMS SOLVED!")
    print("=" * 60)
