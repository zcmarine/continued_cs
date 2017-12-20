# A heap can be implemented in Python using a list
import logging

LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'
PERCOLATE_MSG = 'Calculating need to percolate {t} for parent idx {p} and child idx {c}'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class MinHeap(object):
    '''
    Class-based implementation of a MinHeap from scratch. It would be trivial to extend this to be
    a MaxHeap (see the Heap class defined in incremental_median.py to see the changes), but as
    this is just an exercise for self-learning I'm gonna skip that part
    '''
    def __init__(self):
        logger.debug('Initializing heap')
        self.h = []

    def get_children(self, idx):
        '''
        Return any children that exist. If one or both children don't exist, return None instead
        '''
        logger.debug('Getting children for index {}'.format(idx))
        left_child_idx = 1 + 2 * idx

        if self.size <= left_child_idx:
            left_child_idx = None
            right_child_idx = None
        elif self.size <= left_child_idx + 1:
            right_child_idx = None
        else:
            right_child_idx = left_child_idx + 1

        logger.debug('Returning children indexes {} and {} for index {}'.format(left_child_idx,
                                                                                right_child_idx,
                                                                                idx))
        return (left_child_idx, right_child_idx)

    def get_idx_of_smaller_child(self, parent_idx):
        left_child_idx, right_child_idx = self.get_children(parent_idx)

        if right_child_idx is None or self.h[left_child_idx] < self.h[right_child_idx]:
            smaller_child_idx = left_child_idx
        else:
            smaller_child_idx = right_child_idx

        logger.debug('Smaller child idx for parent idx {} is: {}'.format(parent_idx, smaller_child_idx))
        return smaller_child_idx

    @staticmethod
    def get_parent(idx):
        logger.debug('Getting parent for index {}'.format(idx))
        if idx == 0:
            return None

        parent_idx = (idx - 1) // 2
        logger.debug('Returning parent index {} for index {}'.format(parent_idx, idx))
        return parent_idx

    def peek(self):
        if self.size == 0:
            return None

        val = self.h[0]
        logger.debug('Peeking at top item ({}) in heap'.format(val))
        return val

    def percolate_down(self):
        '''
        Starting from the root, look at a node and the smaller of its two children. If that child
        is smaller than the node, swap them. Keep doing this until the heap relation is maintained
        again
        '''
        do_percolate_down = True
        parent_idx = 0

        while do_percolate_down:
            smaller_child_idx = self.get_idx_of_smaller_child(parent_idx)
            logger.debug(PERCOLATE_MSG.format(t='down', p=parent_idx, c=smaller_child_idx))
            if smaller_child_idx is not None and self.h[smaller_child_idx] < self.h[parent_idx]:
                self.swap(smaller_child_idx, parent_idx)
                parent_idx = smaller_child_idx
            else:
                do_percolate_down = False

    def percolate_up(self):
        '''
        Starting from the last element in the heap, swap it with its ancestors until the heap
        relation is maintained again
        '''
        do_percolate_up = True
        child_idx = self.size - 1

        while do_percolate_up:
            parent_idx = self.get_parent(child_idx)
            logger.debug(PERCOLATE_MSG.format(t='up', p=parent_idx, c=child_idx))
            if parent_idx is not None and self.h[child_idx] < self.h[parent_idx]:
                self.swap(child_idx, parent_idx)
                child_idx = parent_idx
            else:
                do_percolate_up = False

    def pop(self):
        if self.size == 0:
            raise Exception('Cannot pop from an empty heap')

        # Swap the last and first element
        self.swap(0, self.size - 1)

        # The last element was our root; pop it to return later
        prev_root = self.h.pop()
        logger.debug('Popping item {} from heap'.format(prev_root))

        # Percolate down to restore the heap relation
        self.percolate_down()
        return prev_root

    def push(self, val):
        '''
        To maintain a compact tree, we will insert the new item into the end of our list, then
        percolate it up by attempting to swap it with its parent, then that parent with its
        grandparent, etc. until a swap doesn't happen
        '''
        logger.debug('Pushing item {} to heap'.format(val))
        self.h.append(val)
        self.percolate_up()

    @property
    def size(self):
        return len(self.h)

    def swap(self, idx1, idx2):
        val1 = self.h[idx1]
        val2 = self.h[idx2]
        logger.debug('Swapping index {} (val: {}) and index {} (val: {})'.format(idx1, val1, idx2,
                                                                                 val2))
        self.h[idx1] = val2
        self.h[idx2] = val1
