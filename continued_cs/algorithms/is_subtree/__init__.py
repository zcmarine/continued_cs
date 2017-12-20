import logging

from continued_cs.data_structures.stack import Stack


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def is_same_tree(node1, node2):
    ''' Determine if the trees rooted at node2 and node1 are identical '''
    if node1 is None and node2 is None:
        return True
    elif node1 is None or node2 is None:
        # only one is None
        return False
    elif node1.name != node2.name:
        return False
    elif is_same_tree(node1.left_child, node2.left_child) and \
         is_same_tree(node1.right_child, node2.right_child):
        return True
    else:
        return False


def is_subtree(T1, T2):
    ''' Determine if T2 is a subtree of T1 '''
    stack = Stack()
    stack.push(T1)
    logger.debug('Pushed node {} onto stack'.format(T1.name))
    match = False
    while not match and not stack.is_empty():
        node1 = stack.pop()
        logger.debug('Popped node: {}'.format(node1.name))
        match = is_same_tree(T2, node1)
        if not match:
            logger.debug('No match for node {}'.format(node1.name))

            if node1.left_child:
                stack.push(node1.left_child)
                logger.debug('Pushed left child {} for parent {}'.format(node1.left_child.name, node1.name))

            if node1.right_child:
                stack.push(node1.right_child)
                logger.debug('Pushed right child {} for parent {}'.format(node1.right_child.name, node1.name))

    return match
