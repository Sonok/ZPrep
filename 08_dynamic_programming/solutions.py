"""
=============================================================================
PATTERN 8: DYNAMIC PROGRAMMING — SOLUTIONS
=============================================================================
"""


# ---------------------------------------------------------------------------
# Problem 1: Climbing Stairs
# ---------------------------------------------------------------------------
# RECURRENCE: dp[i] = dp[i-1] + dp[i-2]
#   - To reach step i, you came from step i-1 (1 step) or i-2 (2 steps)
#   - This is literally the Fibonacci sequence!
#
# BASE CASE: dp[1] = 1, dp[2] = 2
# TIME: O(n)   SPACE: O(1) with two variables
#
# TRICK TO REMEMBER: "Climbing stairs = Fibonacci."
# ---------------------------------------------------------------------------
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1


# ---------------------------------------------------------------------------
# Problem 2: Coin Change
# ---------------------------------------------------------------------------
# STATE: dp[amount] = fewest coins to make this amount
# RECURRENCE: dp[a] = min(dp[a - coin] + 1) for each coin
# BASE CASE: dp[0] = 0
#
# TIME: O(amount * len(coins))   SPACE: O(amount)
#
# TRICK TO REMEMBER: "For each amount, try each coin and take the best."
# Initialize dp with infinity (impossible) and dp[0] = 0.
# ---------------------------------------------------------------------------
def coin_change(coins: list[int], amount: int) -> int:
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1


# ---------------------------------------------------------------------------
# Problem 3: Longest Common Subsequence
# ---------------------------------------------------------------------------
# STATE: dp[i][j] = LCS of text1[:i] and text2[:j]
# RECURRENCE:
#   If text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
#   Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
# BASE CASE: dp[0][j] = dp[i][0] = 0 (empty string has LCS 0)
#
# TIME: O(m * n)   SPACE: O(m * n), can optimize to O(min(m, n))
#
# TRICK TO REMEMBER:
#   "Match → diagonal + 1. Mismatch → max(skip from either string)."
# ---------------------------------------------------------------------------
def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


# ---------------------------------------------------------------------------
# Problem 4: Word Break
# ---------------------------------------------------------------------------
# STATE: dp[i] = True if s[:i] can be segmented into dictionary words
# RECURRENCE: dp[i] = any(dp[j] and s[j:i] in wordSet) for 0 <= j < i
# BASE CASE: dp[0] = True (empty string)
#
# TIME: O(n^2 * k) where k = avg word length for substring comparison
# SPACE: O(n)
#
# OPTIMIZATION: Use a set for O(1) word lookup.
# Only check j values where i - j <= max_word_length.
#
# TRICK TO REMEMBER: "dp[i] = can I split s[:i]? Try every split point j."
# ---------------------------------------------------------------------------
def word_break(s: str, wordDict: list[str]) -> bool:
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True  # empty string
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]
