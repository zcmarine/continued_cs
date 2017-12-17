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


def reverse_linked_list(head):
    ''' Move through a linked list, setting each node's `next` to point to the previous node '''
    if head.next is None:
        return head

    base_rev = None
    base_fwd = head

    while base_fwd is not None:
        logger.debug('\n*** Starting next iteration ***')
        next_rev = base_rev
        logger.debug('Setting next reverse node to {}'.format(next_rev))
        base_rev = base_fwd
        logger.debug('Setting reverse base to {}'.format(base_rev))
        base_fwd = base_fwd.next
        logger.debug('Setting forward base to {}'.format(base_fwd))
        base_rev.next = next_rev
        logger.debug('Linking reverse base {} to {}'.format(base_rev, next_rev))

    return base_rev


def reverse_and_clone_linked_list(head):
    '''
    for each node in the original linked list
    (i.e. as long as the current node isn't None)
        make a copy of that node
        set its .next to be the current head
        make it the head
        advance to the next node
    '''
    n = head
    rev_head = None
    while n is not None:
        n_cloned = Node(data=n.data)
        n_cloned.next = rev_head
        rev_head = n_cloned
        n = n.next

    return rev_head

