"""
=============================================================================
PATTERN 4: STACK & QUEUE — SOLUTIONS
=============================================================================
"""

from collections import OrderedDict


# ---------------------------------------------------------------------------
# Problem 1: Valid Parentheses
# ---------------------------------------------------------------------------
# APPROACH: Stack + matching map.
#   - Push opening brackets onto stack
#   - For closing bracket: pop and check if it matches
#   - End: stack should be empty
#
# TIME: O(n)   SPACE: O(n)
#
# TRICK: Use a dict mapping closing → opening for clean code.
# ---------------------------------------------------------------------------
def is_valid(s: str) -> bool:
    stack = []
    match = {")": "(", "]": "[", "}": "{"}
    for char in s:
        if char in match:  # closing bracket
            if not stack or stack[-1] != match[char]:
                return False
            stack.pop()
        else:  # opening bracket
            stack.append(char)
    return len(stack) == 0


# ---------------------------------------------------------------------------
# Problem 2: Min Stack
# ---------------------------------------------------------------------------
# APPROACH: Two stacks — one for values, one for minimums.
#   - The min_stack always has the current minimum on top
#   - On push: push to min_stack if val <= current min
#   - On pop: pop from min_stack if popped value == current min
#
# CLEANER APPROACH: Store (val, current_min) pairs in a single stack.
#
# TIME: O(1) for all operations   SPACE: O(n)
# ---------------------------------------------------------------------------
class MinStack:
    def __init__(self):
        self.stack = []  # stores (val, min_so_far)

    def push(self, val: int) -> None:
        current_min = min(val, self.stack[-1][1] if self.stack else val)
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


# ---------------------------------------------------------------------------
# Problem 3: Daily Temperatures
# ---------------------------------------------------------------------------
# APPROACH: Monotonic decreasing stack (store indices).
#   - Iterate through temperatures
#   - While stack is not empty and current temp > temp at stack top:
#     - Pop index, compute days difference
#   - Push current index
#
# TIME: O(n)   SPACE: O(n)
#
# TRICK TO REMEMBER: "Monotonic stack for 'next greater/smaller' problems."
# The stack keeps indices of unresolved elements in decreasing temp order.
# When we find a warmer day, we resolve all colder days on the stack.
# ---------------------------------------------------------------------------
def daily_temperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    answer = [0] * n
    stack = []  # indices of days waiting for a warmer day
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev = stack.pop()
            answer[prev] = i - prev
        stack.append(i)
    return answer


# ---------------------------------------------------------------------------
# Problem 4: LRU Cache
# ---------------------------------------------------------------------------
# APPROACH: OrderedDict (Python's built-in doubly-linked-list + hash map).
#   - get: move to end (most recent), return value
#   - put: if exists, move to end and update; if new, insert at end
#          if over capacity, popitem(last=False) removes the LRU (front)
#
# TIME: O(1) for both get and put   SPACE: O(capacity)
#
# IN INTERVIEW: You may be asked to implement with a raw dict + doubly
# linked list. OrderedDict is the Pythonic shortcut.
#
# TRICK TO REMEMBER: "OrderedDict = dict + doubly linked list."
#   move_to_end() = mark as most recently used
#   popitem(last=False) = evict least recently used
# ---------------------------------------------------------------------------
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # mark as recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # evict LRU
