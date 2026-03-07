"""
=============================================================================
PATTERN 10: LINKED LIST
=============================================================================

HOW TO RECOGNIZE:
- Given a ListNode / linked list
- "Reverse", "detect cycle", "merge", "find middle"
- In-place modification of list structure
- "Remove nth node from end"

KEY IDEA:
  Linked list problems use a small set of techniques:
  1. Two pointers (slow/fast) — cycle detection, find middle
  2. Dummy head — simplifies edge cases (empty list, head removal)
  3. Reverse — iterative with prev/curr/next
  4. Merge — similar to merge sort's merge step

AMAZON FAVORITES:
  - Reverse Linked List
  - Linked List Cycle
  - Merge Two Sorted Lists
  - Remove Nth Node From End
=============================================================================
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ---------------------------------------------------------------------------
# Problem 1: Reverse Linked List (LC 206)
# ---------------------------------------------------------------------------
# Given the head of a singly linked list, reverse it and return the new head.
#
# Example:
#   Input:  1 → 2 → 3 → 4 → 5
#   Output: 5 → 4 → 3 → 2 → 1
# ---------------------------------------------------------------------------
def reverse_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while(curr):
        temp = curr.next # we should keep eye on the next elemetn so we 
        # we don't lose it
        curr.next = prev
        prev = curr
        curr = temp 
    return prev


# ---------------------------------------------------------------------------
# Problem 2: Linked List Cycle (LC 141)
# ---------------------------------------------------------------------------
# Given head, determine if the linked list has a cycle.
#
# A cycle exists if some node's next points back to a previous node.
# ---------------------------------------------------------------------------
def has_cycle(head: ListNode) -> bool:
    slow = head
    fast = head
    while(fast and fast.next): # so that mean it's finite
        if(slow == fast):
            return True
        slow = slow.next
        fast = fast.next.next
    return False


# ---------------------------------------------------------------------------
# Problem 3: Merge Two Sorted Lists (LC 21)
# ---------------------------------------------------------------------------
# Merge two sorted linked lists into one sorted list (made by splicing nodes).
#
# Example:
#   Input:  1 → 2 → 4,  1 → 3 → 4
#   Output: 1 → 1 → 2 → 3 → 4 → 4
# ---------------------------------------------------------------------------
def merge_two_lists(list1: ListNode, list2: ListNode) -> ListNode:
    pass  # YOUR CODE HERE


# ---------------------------------------------------------------------------
# Problem 4: Remove Nth Node From End of List (LC 19)
# ---------------------------------------------------------------------------
# Given the head, remove the nth node from the end and return the head.
#
# Example:
#   Input:  1 → 2 → 3 → 4 → 5,  n = 2
#   Output: 1 → 2 → 3 → 5
# ---------------------------------------------------------------------------
def remove_nth_from_end(head: ListNode, n: int) -> ListNode:
    pass  # YOUR CODE HERE


# ========================== TEST YOUR SOLUTIONS ==========================
def to_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


def from_list(arr):
    dummy = ListNode(0)
    curr = dummy
    for val in arr:
        curr.next = ListNode(val)
        curr = curr.next
    return dummy.next


if __name__ == "__main__":
    print("=" * 60)
    print("TESTING LINKED LIST")
    print("=" * 60)

    # Test Problem 1
    print("\n--- Reverse Linked List ---")
    assert to_list(reverse_list(from_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1], "Test 1 failed"
    assert to_list(reverse_list(from_list([1, 2]))) == [2, 1], "Test 2 failed"
    assert reverse_list(None) is None, "Test 3 failed"
    print("All tests passed!")

    # Test Problem 2
    print("\n--- Linked List Cycle ---")
    # Create cycle: 1 → 2 → 3 → 4 → 2
    n1 = ListNode(1)
    n2 = ListNode(2)
    n3 = ListNode(3)
    n4 = ListNode(4)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n2  # cycle
    assert has_cycle(n1) == True, "Test 1 failed"
    assert has_cycle(from_list([1, 2, 3])) == False, "Test 2 failed"
    assert has_cycle(None) == False, "Test 3 failed"
    print("All tests passed!")

    # Test Problem 3
    print("\n--- Merge Two Sorted Lists ---")
    assert to_list(merge_two_lists(from_list([1, 2, 4]), from_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4], "Test 1 failed"
    assert to_list(merge_two_lists(None, from_list([0]))) == [0], "Test 2 failed"
    print("All tests passed!")

    # Test Problem 4
    print("\n--- Remove Nth From End ---")
    assert to_list(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5], "Test 1 failed"
    assert to_list(remove_nth_from_end(from_list([1]), 1)) == [], "Test 2 failed"
    assert to_list(remove_nth_from_end(from_list([1, 2]), 1)) == [1], "Test 3 failed"
    print("All tests passed!")

    print("\n" + "=" * 60)
    print("ALL LINKED LIST PROBLEMS SOLVED!")
    print("=" * 60)
