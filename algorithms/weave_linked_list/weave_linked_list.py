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


def link_node(pointer, current_node):
    next_node = Node(data=pointer.data)
    current_node.next = next_node
    current_node = next_node
    pointer = pointer.next
    return pointer, current_node


def create_woven_linked_list(head, midpoint, is_odd_length):
    ''' Create a fully new woven linked list. This does not mutate the original linked list. '''
    new_head = Node(data=head.data)
    ptr1 = head.next
    ptr2, current_node = link_node(midpoint, new_head)

    while ptr2 is not None:
        ptr1, current_node = link_node(ptr1, current_node)
        ptr2, current_node = link_node(ptr2, current_node)

    if is_odd_length:
        # There's one last ptr1 node to append
        logger.debug('doing is_odd_length')
        ptr1, current_node = link_node(ptr1, current_node)

    return new_head


def mutate_and_weave(head, midpoint, is_odd_length):
    first_half_node = head
    second_half_node = midpoint
    log_msg = "Link: Next node for {} half item {} is now {}"

    terminated = False
    while not terminated:
        # Figure out what would be next
        first_half_next_node = first_half_node.next
        second_half_next_node = second_half_node.next
        if second_half_node.next is None:
            logger.debug('Is None! Thank god! second_half_node: {}'.format(second_half_node))

        # Insert the second half's node between the current first half's node and its next node
        first_half_node.next = second_half_node
        logger.debug(log_msg.format('first', first_half_node.data, second_half_node.data))

        if second_half_next_node:
            # Add the second half's current node and prepare for the next iteration
            second_half_node.next = first_half_next_node
            logger.debug(log_msg.format('second', second_half_node.data, first_half_next_node.data))

            first_half_node = first_half_next_node
            second_half_node = second_half_next_node
        else:
            if is_odd_length:
                # Add the last node from the first half and set its next to None, then we're done
                second_half_node.next = first_half_next_node
                logger.debug(log_msg.format('second', second_half_node.data, first_half_next_node.data))
                first_half_next_node.next = None
                logger.debug(log_msg.format('first', first_half_next_node.data, None))
                terminated = True
            else:
                # We're done!
                terminated = True

    return head


def weave(head, mutate=False):
    # If the linked list is only one element long we can't weave it
    if not head.next:
        return head

    midpoint, is_odd_length = get_midpoint_pointer(head)
    if mutate:
        return mutate_and_weave(head, midpoint, is_odd_length)
    else:
        return create_woven_linked_list(head, midpoint, is_odd_length)

