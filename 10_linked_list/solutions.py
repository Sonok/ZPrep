"""
=============================================================================
PATTERN 10: LINKED LIST — SOLUTIONS
=============================================================================
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ---------------------------------------------------------------------------
# Problem 1: Reverse Linked List
# ---------------------------------------------------------------------------
# APPROACH: Iterative with prev/curr/next.
#   - prev starts at None (new tail)
#   - For each node: save next, point current to prev, advance both
#
# TIME: O(n)   SPACE: O(1)
#
# TRICK TO REMEMBER: "Three pointers: prev, curr, next_node.
# Point backward, step forward."
#
#   None ← 1 ← 2 ← 3    (prev points backward)
#                    ^curr
# ---------------------------------------------------------------------------
def reverse_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        next_node = curr.next  # save
        curr.next = prev  # reverse
        prev = curr  # advance prev
        curr = next_node  # advance curr
    return prev


# ---------------------------------------------------------------------------
# Problem 2: Linked List Cycle
# ---------------------------------------------------------------------------
# APPROACH: Floyd's Tortoise and Hare.
#   - slow moves 1 step, fast moves 2 steps
#   - If cycle exists, they will meet
#   - If no cycle, fast reaches end (None)
#
# TIME: O(n)   SPACE: O(1)
#
# WHY THEY MEET: Once both are in the cycle, the gap between them
# decreases by 1 each step. They must meet.
# ---------------------------------------------------------------------------
def has_cycle(head: ListNode) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


# ---------------------------------------------------------------------------
# Problem 3: Merge Two Sorted Lists
# ---------------------------------------------------------------------------
# APPROACH: Dummy head + compare-and-attach.
#   - Use a dummy node to simplify edge cases
#   - Compare heads of both lists, attach the smaller one
#   - Append remaining nodes
#
# TIME: O(n + m)   SPACE: O(1)
#
# TRICK TO REMEMBER: "Dummy head avoids special-casing the first node."
# This pattern is used in many linked list problems.
# ---------------------------------------------------------------------------
def merge_two_lists(list1: ListNode, list2: ListNode) -> ListNode:
    dummy = ListNode(0)
    curr = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            curr.next = list1
            list1 = list1.next
        else:
            curr.next = list2
            list2 = list2.next
        curr = curr.next
    curr.next = list1 or list2
    return dummy.next


# ---------------------------------------------------------------------------
# Problem 4: Remove Nth Node From End of List
# ---------------------------------------------------------------------------
# APPROACH: Two pointers with n-gap.
#   - Advance fast pointer n steps ahead
#   - Move both pointers until fast reaches end
#   - slow is now at the node BEFORE the one to remove
#   - Use dummy head to handle removing the first node
#
# TIME: O(n)   SPACE: O(1)
#
# TRICK TO REMEMBER: "Advance fast by n, then walk together.
# When fast hits end, slow is at the right spot."
#
# WHY DUMMY HEAD? If we need to remove the first node (head), slow.next
# needs a valid pointer. Dummy head makes this uniform.
# ---------------------------------------------------------------------------
def remove_nth_from_end(head: ListNode, n: int) -> ListNode:
    dummy = ListNode(0, head)
    fast = slow = dummy
    # Advance fast by n + 1 steps
    for _ in range(n + 1):
        fast = fast.next
    # Walk together
    while fast:
        fast = fast.next
        slow = slow.next
    # Remove the nth node
    slow.next = slow.next.next
    return dummy.next
