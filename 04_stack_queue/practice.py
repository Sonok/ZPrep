"""
=============================================================================
PATTERN 4: STACK & QUEUE
=============================================================================

HOW TO RECOGNIZE:
- "Next greater/smaller element" → monotonic stack
- "Valid parentheses/brackets" → stack
- Matching or nesting problems → stack
- "Sliding window maximum" → monotonic deque
- "Design" problems (LRU Cache, Min Stack)

KEY IDEA:
  Stack: LIFO — great for matching (parentheses), backtracking, and
         maintaining a monotonic sequence.
  Queue: FIFO — great for BFS, sliding window, and order processing.
  Monotonic stack/deque: maintain elements in sorted order for O(n) total.

AMAZON FAVORITES:
  - Valid Parentheses
  - Min Stack
  - Daily Temperatures (monotonic stack)
  - LRU Cache
=============================================================================
"""

from collections import OrderedDict


# ---------------------------------------------------------------------------
# Problem 1: Valid Parentheses (LC 20)
# ---------------------------------------------------------------------------
# Given a string s containing just '(', ')', '{', '}', '[', ']',
# determine if the input string is valid.
#
# Example:
#   Input:  s = "()[]{}"    Output: True
#   Input:  s = "(]"        Output: False
#   Input:  s = "([)]"      Output: False
# ---------------------------------------------------------------------------
def is_valid(s: str) -> bool:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 2: Min Stack (LC 155)
# ---------------------------------------------------------------------------
# Design a stack that supports push, pop, top, and getMin in O(1) time.
#
# Example:
#   minStack = MinStack()
#   minStack.push(-2)
#   minStack.push(0)
#   minStack.push(-3)
#   minStack.getMin()  → -3
#   minStack.pop()
#   minStack.top()     → 0
#   minStack.getMin()  → -2
# ---------------------------------------------------------------------------
class MinStack:
    def __init__(self):
        pass  # YOUR CODE HERE

    def push(self, val: int) -> None:
        pass  # YOUR CODE HERE

    def pop(self) -> None:
        pass  # YOUR CODE HERE

    def top(self) -> int:
        pass  # YOUR CODE HERE

    def getMin(self) -> int:
        pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 3: Daily Temperatures (LC 739)
# ---------------------------------------------------------------------------
# Given an array of daily temperatures, return an array where answer[i]
# is the number of days you have to wait after day i to get a warmer
# temperature. If no future day is warmer, answer[i] = 0.
#
# Example:
#   Input:  temperatures = [73,74,75,71,69,72,76,73]
#   Output: [1,1,4,2,1,1,0,0]
# ---------------------------------------------------------------------------
def daily_temperatures(temperatures: list[int]) -> list[int]:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: LRU Cache (LC 146) — VERY common at Amazon
# ---------------------------------------------------------------------------
# Design a data structure for Least Recently Used (LRU) cache.
#   - get(key): Return value if key exists, else -1. Marks as recently used.
#   - put(key, value): Insert or update. If over capacity, evict LRU item.
# Both operations must be O(1).
#
# Example:
#   cache = LRUCache(2)
#   cache.put(1, 1)
#   cache.put(2, 2)
#   cache.get(1)       → 1
#   cache.put(3, 3)    → evicts key 2
#   cache.get(2)       → -1
# ---------------------------------------------------------------------------
class LRUCache:
    def __init__(self, capacity: int):
        pass  # YOUR CODE HERE

    def get(self, key: int) -> int:
        pass  # YOUR CODE HERE

    def put(self, key: int, value: int) -> None:
        pass  # YOUR CODE HERE


# ========================== TEST YOUR SOLUTIONS ==========================
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING STACK & QUEUE")
    print("=" * 60)

    # Test Problem 1
    print("\n--- Valid Parentheses ---")
    assert is_valid("()[]{}") == True, "Test 1 failed"
    assert is_valid("(]") == False, "Test 2 failed"
    assert is_valid("([)]") == False, "Test 3 failed"
    assert is_valid("{[]}") == True, "Test 4 failed"
    assert is_valid("") == True, "Test 5 failed"
    print("All tests passed!")

    # Test Problem 2
    print("\n--- Min Stack ---")
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.getMin() == -3, "Test 1 failed"
    ms.pop()
    assert ms.top() == 0, "Test 2 failed"
    assert ms.getMin() == -2, "Test 3 failed"
    print("All tests passed!")

    # Test Problem 3
    print("\n--- Daily Temperatures ---")
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0], "Test 1 failed"
    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0], "Test 2 failed"
    assert daily_temperatures([30, 60, 90]) == [1, 1, 0], "Test 3 failed"
    print("All tests passed!")

    # Test Problem 4
    print("\n--- LRU Cache ---")
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1, "Test 1 failed"
    cache.put(3, 3)  # evicts key 2
    assert cache.get(2) == -1, "Test 2 failed"
    cache.put(4, 4)  # evicts key 1
    assert cache.get(1) == -1, "Test 3 failed"
    assert cache.get(3) == 3, "Test 4 failed"
    assert cache.get(4) == 4, "Test 5 failed"
    print("All tests passed!")

    print("\n" + "=" * 60)
    print("ALL STACK & QUEUE PROBLEMS SOLVED!")
    print("=" * 60)
