# A note on heaps:
#     Heaps in Python are implemented via the heapq library
#     Really, Python just uses lists for heaps, hence the operations
#     are implemented by first instantiating a list:
#         h = []
#     then pushing to it:
#         heapq.heappush(h, val)
#     and popping from it:
#         heapq.heappop(h)

import heapq
import logging

LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'

# Note: if you ever want to override a module / library's logger levels
# (e.g. you want to set this to DEBUG, you can find all loggers with:
#     logging.Logger.manager.loggerDict
# Then you can grab that logger and change its level:
#     logging.getLogger('incremental_median').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class Heap(object):
    '''
    Class-based implementation of a Heap since Python's
    functional approach is a bit clunky
    '''
    def __init__(self, is_minheap=True):
        self._h = []
        self.sign = 1 if is_minheap else -1
        self.kind = 'min' if is_minheap else 'max'
        self.len = 0
        logger.debug('Initializing {} heap'.format(self.kind))

    @property
    def h(self):
        ''' Property provided to allow end user to view the heap; not used internally '''
        return [self.sign * val for val in self._h]

    def pop(self):
        item = self.sign * heapq.heappop(self._h)
        self.len -= 1
        logger.debug('Popping item {} from {} heap'.format(item, self.kind))
        return item

    def push(self, val):
        heapq.heappush(self._h, self.sign * val)
        logger.debug('Pushing item {} to {} heap'.format(val, self.kind))
        self.len += 1

    def peek(self):
        val = self.pop()
        self.push(val)
        logger.debug('Peeking at top item ({}) in {} heap'.format(val, self.kind))
        return val


class IncrementalMedian(object):
    def __init__(self):
        # Initialize min heap; used for all values larger than the median
        self.minh = Heap()
        # Initialize max heap; used for all values smaller than the median
        self.maxh = Heap(is_minheap=False)

    def get_median(self):
        if self.minh.len == self.maxh.len:
            logger.debug('Getting median for equally sized min and max heaps')
            smallest_minh = self.minh.peek()
            largest_maxh = self.maxh.peek()
            return 0.5 * (smallest_minh + largest_maxh)
        else:
            logger.debug('Getting median from min heap (heaps are unequal in size)')
            # minh should have the extra element
            return float(self.minh.peek())

    def insert(self, val):
        ''' Insert a new value into the appropriate heap '''
        # For simplicity's sake, just stick things onto minh and rebalance
        self.minh.push(val)
        self.rebalance()

    def rebalance(self):
        '''
        Rebalance the min and max heaps so that their lengths are within 1 of each other
        '''
        # Since all elements go into minh, it will always be at least as large as maxh
        imbalance = self.minh.len - self.maxh.len
        # If there is an imbalance, we will move half the items to maxh, but if there is
        # an extra item (i.e. imbalance is an odd number), then that extra item stays in
        # minh, so here we do floor division
        moves = imbalance // 2

        for _ in range(moves):
            item = self.minh.pop()
            logger.debug('Moving item {} from min heap to max heap'.format(item))
            self.maxh.push(item)

        if self.maxh.len == 0:
            return

        # We moved things around, but make sure it still holds that
        # max of self.minh is less than min of self.maxh; swap items
        # until this is true
        while self.minh.peek() < self.maxh.peek():
            self.swap()

    def swap(self):
        minh_tip = self.minh.pop()
        maxh_tip = self.maxh.pop()
        logger.debug('Swapping minh item {} and maxh item {}'.format(minh_tip, maxh_tip))

        self.maxh.push(minh_tip)
        self.minh.push(maxh_tip)
