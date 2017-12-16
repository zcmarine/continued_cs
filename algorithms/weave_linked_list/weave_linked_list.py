import logging

LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class Node(object):
    def __init__(self, data, next_=None):
        self.data = data
        self.next = next_

    def __repr__(self):
        return '< Node / data: {} >'.format(self.data)


def get_midpoint_pointer(head):
    '''
    Return a pointer for the midpoint of the linked list. Also return a boolean, is_odd_length,
    that tells if the linked list is of odd or even length

    If the linked list is of odd length then the number of nodes from the head to the midpoint
    will be 1 greater than the number of nodes from the midpoint to the end of the linked list
    '''
    ptr1 = head
    ptr2 = head

    # Advanced ptr1 twice as much as ptr2. Once ptr1.next is None, we've reached
    # the end of the linked list and ptr2 must be at the midpoint
    while ptr1.next is not None and ptr1.next.next is not None:
        ptr1 = ptr1.next.next
        ptr2 = ptr2.next

    # Keep track of whether the linked list is odd or not. If it is then when we weave the
    # two halves we'll need to do one extra append of ptr1 after ptr2.next is None
    is_odd_length = (ptr1.next is None)
    logger.debug('is_odd_length: {}'.format(is_odd_length))

    # Move ptr1 back to head now and advance ptr2 one last time to get it to the midpoint
    ptr1 = head
    ptr2 = ptr2.next

    return ptr2, is_odd_length


def append_node(pointer, current_node):
    next_node = Node(data=pointer.data)
    current_node.next = next_node
    current_node = next_node
    pointer = pointer.next
    return pointer, current_node


def create_woven_linked_list(head, midpoint, is_odd_length):
    ''' Create a fully new woven linked list. This does not mutate the original linked list. '''
    new_head = Node(data=head.data)
    ptr1 = head.next
    ptr2, current_node = append_node(midpoint, new_head)

    while ptr2 is not None:
        ptr1, current_node = append_node(ptr1, current_node)
        ptr2, current_node = append_node(ptr2, current_node)

    if is_odd_length:
        # There's one last ptr1 node to append
        logger.debug('doing is_odd_length')
        ptr1, current_node = append_node(ptr1, current_node)

    return new_head


def weave(head):
    # If the linked list is only one element long we can't weave it
    if not head.next:
        return head

    midpoint, is_odd_length = get_midpoint_pointer(head)
    return create_woven_linked_list(head, midpoint, is_odd_length)
